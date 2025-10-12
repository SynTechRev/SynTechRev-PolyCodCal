from __future__ import annotations

import pathlib
from typing import Final

# Base dir is repo root (src/../../)
BASE_DIR: Final[pathlib.Path] = pathlib.Path(__file__).resolve().parents[3]
DATA_DIR: Final[pathlib.Path] = BASE_DIR / "data"
CASE_DIR: Final[pathlib.Path] = DATA_DIR / "cases"
VECTOR_DIR: Final[pathlib.Path] = DATA_DIR / "vectors"
VECTOR_PATH: Final[pathlib.Path] = VECTOR_DIR / "case_embeddings.npy"

# Default model label (for future, optional heavy model swaps)
MODEL_NAME: Final[str] = "hash-embedder-256"

# Ensure directories exist at runtime where relevant (not on import)
