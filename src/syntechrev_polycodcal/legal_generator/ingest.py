from __future__ import annotations

import hashlib
import json
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
    case_dir: pathlib.Path | None = None, rebuild: bool = False
) -> Tuple[List[str], np.ndarray]:
    """Ingest legal cases from JSON files and persist embeddings.

    Args:
        case_dir: Optional override for cases directory (defaults to CASE_DIR)
        rebuild: If True, rebuild from scratch; if False (default), append mode

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
    embeddings = (
        embedder.encode_texts(texts) if texts else np.zeros((0, 256), dtype=np.float32)
    )

    # Persist as compressed NPZ for portability and smaller size
    names_arr = np.array(names, dtype=str)
    np.savez_compressed(VECTOR_PATH, names=names_arr, embeddings=embeddings)

    # Write metadata file
    meta_path = VECTOR_DIR / "vectors.meta.json"
    names_hash = hashlib.sha256(names_arr.tobytes()).hexdigest()[:16]
    metadata = {
        "model": MODEL_NAME,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "count": len(names),
        "dim": embeddings.shape[1] if embeddings.shape[0] > 0 else 256,
        "file_version": "1.0",
        "names_hash": names_hash,
    }
    meta_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return names, embeddings
