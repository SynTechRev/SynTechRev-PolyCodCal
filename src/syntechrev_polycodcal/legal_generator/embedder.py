from __future__ import annotations

import hashlib
from typing import Iterable, List

import numpy as np


class Embedder:
    """Deterministic lightweight text embedder.

    This avoids heavy dependencies by using hashing to produce fixed-size
    numeric representations suitable for simple similarity search. The
    interface mirrors typical embedders: call encode_texts(list[str]) and
    receive an ndarray[float32] of shape (N, D).
    """

    def __init__(self, dim: int = 256) -> None:
        self.dim = dim

    def _hash_to_vec(self, text: str) -> np.ndarray:
        # Hash to bytes, map to floats in [-1, 1]
        h = hashlib.sha256(text.encode("utf-8", errors="ignore")).digest()
        # Repeat hash to reach required dimension, then slice
        raw = (h * ((self.dim // len(h)) + 1))[: self.dim]
        arr = np.frombuffer(bytes(raw), dtype=np.uint8).astype(np.float32)
        # Normalize into [-1, 1]
        arr = (arr / 127.5) - 1.0
        # L2 normalize for cosine stability
        norm = np.linalg.norm(arr) or 1.0
        return arr / norm

    def encode_texts(self, texts: Iterable[str]) -> np.ndarray:
        vecs: List[np.ndarray] = [self._hash_to_vec(t or "") for t in texts]
        return np.vstack(vecs).astype(np.float32)
