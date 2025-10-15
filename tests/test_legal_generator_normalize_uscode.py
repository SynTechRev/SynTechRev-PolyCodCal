from __future__ import annotations

import json

from syntechrev_polycodcal.legal_generator import ingest, retriever
from syntechrev_polycodcal.legal_generator.embedder import Embedder
from syntechrev_polycodcal.legal_generator.ingest import ingest_cases
from syntechrev_polycodcal.legal_generator.normalize import normalize_uscode


def test_normalize_uscode_and_ingest(tmp_path, monkeypatch):
    # Prepare simple US Code JSON list
    source = tmp_path / "uscode.json"
    data = [
        {
            "title": 42,
            "section": 1983,
            "heading": "Civil action for deprivation of rights",
            "text": "Every person who, under color of ...",
        },
        {
            "title": 15,
            "section": "1",
            "heading": "Trusts, etc., in restraint of trade illegal; penalty",
            "text": "Every contract, combination in the form of trust or otherwise ...",
        },
    ]
    source.write_text(json.dumps(data), encoding="utf-8")

    # Normalize
    out_dir = tmp_path / "cases"
    written = normalize_uscode(source, out_dir=out_dir)
    assert len(written) == 2

    # Redirect paths
    vector_path = tmp_path / "vectors.npz"
    monkeypatch.setattr(ingest, "CASE_DIR", out_dir)
    monkeypatch.setattr(ingest, "VECTOR_DIR", tmp_path)
    monkeypatch.setattr(ingest, "VECTOR_PATH", vector_path)
    monkeypatch.setattr(retriever, "VECTOR_PATH", vector_path)

    # Ingest and query
    names, embs = ingest_cases()
    assert len(names) == 2
    assert embs.shape[0] == 2

    query = "civil rights action"
    q_emb = Embedder().encode_texts([query])[0]
    results = retriever.search(q_emb, top_k=2)
    assert len(results) == 2
    top_names = [n for n, _ in results]
    assert any("USC" in n for n in top_names)
