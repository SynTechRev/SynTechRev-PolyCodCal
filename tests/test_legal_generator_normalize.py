from __future__ import annotations

import json

from syntechrev_polycodcal.legal_generator import ingest, retriever
from syntechrev_polycodcal.legal_generator.embedder import Embedder
from syntechrev_polycodcal.legal_generator.ingest import ingest_cases
from syntechrev_polycodcal.legal_generator.normalize import normalize_scotus


def test_normalize_scotus_and_ingest(tmp_path, monkeypatch):
    # Prepare source JSONL with two cases (flexible fields)
    source = tmp_path / "scotus.jsonl"
    lines = [
        json.dumps(
            {
                "title": "Brown v. Board of Education",
                "syllabus": "Equal protection in public education.",
                "opinion": "Segregation in public education is inherently unequal.",
            }
        ),
        json.dumps(
            {
                "case_name": "Hadley v. Baxendale",
                "summary": "Contract damages limited to foreseeable losses.",
            }
        ),
    ]
    source.write_text("\n".join(lines), encoding="utf-8")

    # Normalize into a dedicated out dir
    out_dir = tmp_path / "cases"
    written = normalize_scotus(source, out_dir=out_dir)
    assert len(written) == 2
    assert all(p.suffix == ".json" for p in written)

    # Redirect ingest/retriever paths
    vector_path = tmp_path / "vectors.npz"
    monkeypatch.setattr(ingest, "CASE_DIR", out_dir)
    monkeypatch.setattr(ingest, "VECTOR_DIR", tmp_path)
    monkeypatch.setattr(ingest, "VECTOR_PATH", vector_path)
    monkeypatch.setattr(retriever, "VECTOR_PATH", vector_path)

    # Ingest and query
    names, embs = ingest_cases()
    assert len(names) == 2
    assert embs.shape[0] == 2

    query = "equal protection in education"
    q_emb = Embedder().encode_texts([query])[0]
    results = retriever.search(q_emb, top_k=2)
    assert len(results) == 2
    # Brown should be among top results given overlapping terms
    top_names = [n for n, _ in results]
    assert any("Brown" in n for n in top_names)
