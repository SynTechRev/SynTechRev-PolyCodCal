from __future__ import annotations

import json

import numpy as np

from syntechrev_polycodcal.legal_generator import ingest
from syntechrev_polycodcal.legal_generator.ingest import ingest_cases


def test_ingest_rebuild_and_append(tmp_path, monkeypatch):
    # Prepare two batches
    cases_dir = tmp_path / "cases"
    cases_dir.mkdir()

    (cases_dir / "A.json").write_text(
        json.dumps({"case_name": "A", "summary": "alpha"}), encoding="utf-8"
    )

    monkeypatch.setattr(ingest, "CASE_DIR", cases_dir)
    monkeypatch.setattr(ingest, "VECTOR_DIR", tmp_path)
    monkeypatch.setattr(ingest, "VECTOR_PATH", tmp_path / "vectors.npz")

    names1, emb1 = ingest_cases(rebuild=True)
    assert names1 == ["A"]
    assert isinstance(emb1, np.ndarray)
    assert emb1.shape[0] == 1

    # Add second case and append
    (cases_dir / "B.json").write_text(
        json.dumps({"case_name": "B", "summary": "beta"}), encoding="utf-8"
    )
    names2, emb2 = ingest_cases(rebuild=False)
    assert len(names2) == 2
    assert emb2.shape[0] == 2

    meta = (tmp_path / "vectors.meta.json").read_text(encoding="utf-8")
    assert '"model"' in meta and '"count"' in meta
