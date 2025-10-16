from __future__ import annotations

import hashlib
import json
import json as _json
import pathlib
from datetime import datetime, timezone
from typing import List, Tuple

import numpy as np

from .config import CASE_DIR, MODEL_NAME, VECTOR_DIR, VECTOR_PATH
from .embedder import Embedder


def _extract_text(record: dict) -> str:
    # Prefer rich fields if available
    for key in ("summary", "facts", "holding", "opinion_text"):
        if val := record.get(key):
            return str(val)
    # Fallbacks
    return str(record.get("case_name", ""))


def ingest_cases(
    case_dir: pathlib.Path | None = None,
    *,
    rebuild: bool = False,
) -> Tuple[List[str], np.ndarray]:
    """Ingest legal cases from JSON files and persist embeddings.

    Args:
        case_dir: Optional override for cases directory (defaults to CASE_DIR)

    Returns:
        Tuple of (names, embeddings ndarray)
    """
    cdir = case_dir or CASE_DIR
    cdir.mkdir(parents=True, exist_ok=True)
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)

    texts: List[str] = []
    names: List[str] = []

    for file in sorted(cdir.glob("*.json")):
        with file.open("r", encoding="utf-8") as f:
            record = json.load(f)
        text = _extract_text(record)
        name = str(record.get("case_name", file.stem))
        texts.append(text)
        names.append(name)

    embedder = Embedder()
    new_embeddings = (
        embedder.encode_texts(texts) if texts else np.zeros((0, 256), dtype=np.float32)
    )

    # Append vs rebuild
    if not rebuild and VECTOR_PATH.exists():
        with np.load(VECTOR_PATH) as data:
            files = set(getattr(data, "files", []))
            old_names = data["names"] if "names" in files else np.array([], dtype=str)
            old_embs = (
                data["embeddings"]
                if "embeddings" in files
                else np.zeros(
                    (0, new_embeddings.shape[1] if new_embeddings.size else 256),
                    dtype=np.float32,
                )
            )
        names_arr = np.concatenate([old_names, np.array(names, dtype=str)])
        embeddings = (
            np.vstack([old_embs, new_embeddings])
            if old_embs.size and new_embeddings.size
            else (new_embeddings if new_embeddings.size else old_embs)
        )
    else:
        names_arr = np.array(names, dtype=str)
        embeddings = new_embeddings

    # Ensure unique names and corresponding embeddings, preserving first occurrence
    _, unique_indices = np.unique(names_arr, return_index=True)
    unique_indices = np.sort(unique_indices)  # Sort to preserve original order
    # Filter names and embeddings to keep only first occurrence of each unique name
    names_arr = names_arr[unique_indices]
    embeddings = embeddings[unique_indices]

    # Persist as compressed NPZ for portability and smaller size
    np.savez_compressed(VECTOR_PATH, names=names_arr, embeddings=embeddings)

    # Write vectors meta sidecar
    dim = int(embeddings.shape[1]) if embeddings.size else 256
    names_concat = (
        "\n".join([str(x) for x in names_arr.tolist()]) if names_arr.size else ""
    )
    names_hash = hashlib.sha1(names_concat.encode("utf-8")).hexdigest()
    meta = {
        "model": MODEL_NAME,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "count": int(embeddings.shape[0]),
        "dim": dim,
        "file": VECTOR_PATH.name,
        "version": 1,
        "names_hash": names_hash,
    }
    (VECTOR_DIR / "vectors.meta.json").write_text(
        _json.dumps(meta, indent=2), encoding="utf-8"
    )
    return names_arr.tolist(), embeddings
