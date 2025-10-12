from __future__ import annotations

import json
import pathlib
from typing import List, Tuple

import numpy as np

from .config import CASE_DIR, VECTOR_DIR, VECTOR_PATH
from .embedder import Embedder


def _extract_text(record: dict) -> str:
    # Prefer rich fields if available
    for key in ("summary", "facts", "holding", "opinion_text"):
        if val := record.get(key):
            return str(val)
    # Fallbacks
    return str(record.get("case_name", ""))


def ingest_cases(case_dir: pathlib.Path | None = None) -> Tuple[List[str], np.ndarray]:
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
    embeddings = (
        embedder.encode_texts(texts) if texts else np.zeros((0, 256), dtype=np.float32)
    )

    np.save(VECTOR_PATH, {"names": names, "embeddings": embeddings})
    return names, embeddings
