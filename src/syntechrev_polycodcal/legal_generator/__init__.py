"""AI Legal Data Intelligence Scaffold (Phase 6).

Provides ingestion, embedding, and retrieval utilities for legal case data.

Lightweight by default: uses a deterministic hashing embedder to avoid
heavy dependencies. Can be upgraded to sentence-transformers by swapping
Embedder implementation.
"""

from __future__ import annotations

__all__ = [
    "config",
    "ingest",
    "embedder",
    "retriever",
]
