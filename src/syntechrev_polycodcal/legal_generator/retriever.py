from __future__ import annotations

from typing import List, Tuple

import numpy as np

from .config import VECTOR_PATH


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    # a: (D,), b: (N, D)
    a_norm = a / (np.linalg.norm(a) or 1.0)
    b_norm = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-12)
    return b_norm @ a_norm


def search(query_embedding: np.ndarray, top_k: int = 3) -> List[Tuple[str, float]]:
    data = np.load(VECTOR_PATH)
    # names saved as object array to preserve strings of varying length
    names_arr = data.get("names")
    emb_arr = data.get("embeddings")
    names: List[str] = [
        str(x) for x in (names_arr.tolist() if names_arr is not None else [])
    ]
    embeddings: np.ndarray = (
        emb_arr if emb_arr is not None else np.zeros((0, 256), dtype=np.float32)
    )
    if embeddings.size == 0 or len(names) == 0:
        return []
    sims = _cosine_similarity(
        query_embedding.astype(np.float32), embeddings.astype(np.float32)
    )
    top_idx = np.argsort(sims)[::-1][: max(0, top_k)]
    return [(names[i], float(sims[i])) for i in top_idx]
