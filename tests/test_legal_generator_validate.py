from __future__ import annotations

import json
from pathlib import Path  # noqa: F401

from syntechrev_polycodcal.legal_generator.validate import validate_cases


def test_validate_pass_and_fail(tmp_path):
    good = tmp_path / "cases"
    bad = tmp_path / "bad"
    good.mkdir()
    bad.mkdir()

    (good / "ok.json").write_text(
        json.dumps({"case_name": "X", "summary": "Y"}), encoding="utf-8"
    )
    (bad / "missing.json").write_text(json.dumps({"case_name": "X"}), encoding="utf-8")

    errs_good = validate_cases(good)
    errs_bad = validate_cases(bad)

    assert errs_good == []
    assert any("missing/invalid field: summary" in msg for _, msg in errs_bad)
