from __future__ import annotations

import json

from syntechrev_polycodcal.legal_generator import ingest, retriever
from syntechrev_polycodcal.legal_generator.embedder import Embedder
from syntechrev_polycodcal.legal_generator.ingest import ingest_cases
from syntechrev_polycodcal.legal_generator.normalize import (
    normalize_amjur,
    normalize_blacks,
)


def test_normalize_blacks_and_ingest(tmp_path, monkeypatch):
    source = tmp_path / "blacks.json"
    data = [
        {
            "term": "Consideration",
            "definition": "A benefit to the promisor or a detriment to the promisee.",
        }
    ]
    source.write_text(json.dumps(data), encoding="utf-8")

    out_dir = tmp_path / "cases"
    written = normalize_blacks(source, out_dir=out_dir)
    assert len(written) == 1

    vector_path = tmp_path / "vectors.npz"
    monkeypatch.setattr(ingest, "CASE_DIR", out_dir)
    monkeypatch.setattr(ingest, "VECTOR_DIR", tmp_path)
    monkeypatch.setattr(ingest, "VECTOR_PATH", vector_path)
    monkeypatch.setattr(retriever, "VECTOR_PATH", vector_path)

    names, embs = ingest_cases(rebuild=True)
    assert len(names) == 1
    assert embs.shape[0] == 1

    q = "consideration detriment"
    emb = Embedder().encode_texts([q])[0]
    results = retriever.search(emb, top_k=1)
    assert len(results) == 1


def test_normalize_amjur_and_ingest(tmp_path, monkeypatch):
    source = tmp_path / "amjur.jsonl"
    lines = [
        json.dumps(
            {
                "title": "Estoppel Basics",
                "abstract": "Representation and reliance.",
                "body": "When a party...",
            }
        )
    ]
    source.write_text("\n".join(lines), encoding="utf-8")

    out_dir = tmp_path / "cases"
    written = normalize_amjur(source, out_dir=out_dir)
    assert len(written) == 1

    vector_path = tmp_path / "vectors.npz"
    monkeypatch.setattr(ingest, "CASE_DIR", out_dir)
    monkeypatch.setattr(ingest, "VECTOR_DIR", tmp_path)
    monkeypatch.setattr(ingest, "VECTOR_PATH", vector_path)
    monkeypatch.setattr(retriever, "VECTOR_PATH", vector_path)

    names, embs = ingest_cases(rebuild=True)
    assert len(names) == 1
    assert embs.shape[0] == 1

    q = "representation reliance estoppel"
    emb = Embedder().encode_texts([q])[0]
    results = retriever.search(emb, top_k=1)
    assert len(results) == 1
