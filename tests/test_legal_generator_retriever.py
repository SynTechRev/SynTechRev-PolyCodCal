from __future__ import annotations

import json

from syntechrev_polycodcal.legal_generator import config
from syntechrev_polycodcal.legal_generator.embedder import Embedder
from syntechrev_polycodcal.legal_generator.ingest import ingest_cases
from syntechrev_polycodcal.legal_generator.retriever import search


def test_retriever_returns_top_results(tmp_path, monkeypatch):
    # Redirect config paths
    monkeypatch.setattr(config, "CASE_DIR", tmp_path)
    monkeypatch.setattr(config, "VECTOR_PATH", tmp_path / "vectors.npz")

    # Create a couple of simple cases
    (tmp_path / "CaseA.json").write_text(
        json.dumps(
            {"case_name": "Case A", "summary": "due process and equal protection"}
        ),
        encoding="utf-8",
    )
    (tmp_path / "CaseB.json").write_text(
        json.dumps({"case_name": "Case B", "summary": "contract breach and remedies"}),
        encoding="utf-8",
    )

    ingest_cases()

    # Query
    q = "equal protection"
    emb = Embedder().encode_texts([q])[0]
    results = search(emb, top_k=2)

    assert len(results) == 2
    # Highest similarity should be Case A given overlapping words
    names = [n for n, _ in results]
    assert "Case A" in names
