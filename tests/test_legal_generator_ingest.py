from __future__ import annotations

import json

import numpy as np

from syntechrev_polycodcal.legal_generator import ingest
from syntechrev_polycodcal.legal_generator.ingest import ingest_cases


def test_ingest_runs_with_minimal_case(tmp_path, monkeypatch):
    # Redirect paths in ingest module (not config, since ingest imports them directly)
    monkeypatch.setattr(ingest, "CASE_DIR", tmp_path)
    monkeypatch.setattr(ingest, "VECTOR_DIR", tmp_path)
    monkeypatch.setattr(ingest, "VECTOR_PATH", tmp_path / "vectors.npz")

    # Create a minimal case file
    (tmp_path / "TestCase.json").write_text(
        json.dumps({"case_name": "Test Case", "summary": "Simple text"}),
        encoding="utf-8",
    )

    names, emb = ingest_cases()
    assert names == ["Test Case"]
    assert isinstance(emb, np.ndarray)
    assert emb.shape[0] == 1
