"""Tests for Moral Gravity Field and Alignment Scoring."""

from __future__ import annotations

import pytest

from syntechrev_polycodcal.genesis_gateway.alignment import (
    AlignmentScore,
    MoralGravityField,
)


def test_alignment_score_initialization():
    """Test AlignmentScore creation with valid values."""
    score = AlignmentScore(
        truth=0.9, faith=0.85, justice=0.8, mercy=0.95, weights=(0.25, 0.25, 0.25, 0.25)
    )

    assert score.truth == 0.9
    assert score.faith == 0.85
    assert score.justice == 0.8
    assert score.mercy == 0.95


def test_alignment_score_compute():
    """Test alignment score computation."""
    score = AlignmentScore(
        truth=0.8, faith=0.8, justice=0.8, mercy=0.8, weights=(0.25, 0.25, 0.25, 0.25)
    )

    result = score.compute()
    assert result == 0.8


def test_alignment_score_weighted_compute():
    """Test alignment score with custom weights."""
    score = AlignmentScore(
        truth=1.0, faith=0.0, justice=0.5, mercy=0.5, weights=(0.5, 0.2, 0.2, 0.1)
    )

    result = score.compute()
    # 0.5*1.0 + 0.2*0.0 + 0.2*0.5 + 0.1*0.5 = 0.5 + 0 + 0.1 + 0.05 = 0.65
    assert abs(result - 0.65) < 1e-9


def test_alignment_score_is_aligned():
    """Test alignment threshold checking."""
    score_high = AlignmentScore(
        truth=0.9, faith=0.9, justice=0.9, mercy=0.9, weights=(0.25, 0.25, 0.25, 0.25)
    )
    assert score_high.is_aligned()

    score_low = AlignmentScore(
        truth=0.5, faith=0.5, justice=0.5, mercy=0.5, weights=(0.25, 0.25, 0.25, 0.25)
    )
    assert not score_low.is_aligned()


def test_alignment_score_custom_threshold():
    """Test alignment with custom threshold."""
    score = AlignmentScore(
        truth=0.7, faith=0.7, justice=0.7, mercy=0.7, weights=(0.25, 0.25, 0.25, 0.25)
    )

    assert not score.is_aligned(threshold=0.8)
    assert score.is_aligned(threshold=0.6)


def test_alignment_score_invalid_values():
    """Test AlignmentScore validation."""
    with pytest.raises(ValueError, match="Truth must be in"):
        AlignmentScore(truth=1.5, faith=0.5, justice=0.5, mercy=0.5)

    with pytest.raises(ValueError, match="Faith must be in"):
        AlignmentScore(truth=0.5, faith=-0.1, justice=0.5, mercy=0.5)

    with pytest.raises(ValueError, match="Justice must be in"):
        AlignmentScore(truth=0.5, faith=0.5, justice=2.0, mercy=0.5)

    with pytest.raises(ValueError, match="Mercy must be in"):
        AlignmentScore(truth=0.5, faith=0.5, justice=0.5, mercy=-1.0)


def test_alignment_score_invalid_weights():
    """Test weight normalization validation."""
    with pytest.raises(ValueError, match="Weights must sum to 1.0"):
        AlignmentScore(
            truth=0.5, faith=0.5, justice=0.5, mercy=0.5, weights=(0.3, 0.3, 0.3, 0.3)
        )


def test_moral_gravity_field_initialization():
    """Test MoralGravityField creation."""
    field = MoralGravityField(threshold=0.8)
    assert field.threshold == 0.8


def test_moral_gravity_field_invalid_threshold():
    """Test MoralGravityField threshold validation."""
    with pytest.raises(ValueError, match="Threshold must be in"):
        MoralGravityField(threshold=1.5)

    with pytest.raises(ValueError, match="Threshold must be in"):
        MoralGravityField(threshold=-0.1)


def test_moral_gravity_field_evaluate():
    """Test construct evaluation."""
    field = MoralGravityField()

    construct = {"truth": 0.9, "faith": 0.85, "justice": 0.8, "mercy": 0.95}

    score = field.evaluate(construct)

    assert score.truth == 0.9
    assert score.faith == 0.85
    assert score.justice == 0.8
    assert score.mercy == 0.95


def test_moral_gravity_field_evaluate_defaults():
    """Test evaluation with missing fields uses defaults."""
    field = MoralGravityField()

    construct = {}  # Empty construct

    score = field.evaluate(construct)

    assert score.truth == 0.5
    assert score.faith == 0.5
    assert score.justice == 0.5
    assert score.mercy == 0.5


def test_moral_gravity_field_filter_pass():
    """Test filtering with construct that passes threshold."""
    field = MoralGravityField(threshold=0.7)

    construct = {"truth": 0.8, "faith": 0.8, "justice": 0.8, "mercy": 0.8}

    assert field.filter(construct) is True


def test_moral_gravity_field_filter_fail():
    """Test filtering with construct that fails threshold."""
    field = MoralGravityField(threshold=0.9)

    construct = {"truth": 0.6, "faith": 0.6, "justice": 0.6, "mercy": 0.6}

    assert field.filter(construct) is False


def test_moral_gravity_field_apply():
    """Test batch filtering of constructs."""
    field = MoralGravityField(threshold=0.7)

    constructs = [
        {"truth": 0.9, "faith": 0.9, "justice": 0.9, "mercy": 0.9},  # Pass
        {"truth": 0.5, "faith": 0.5, "justice": 0.5, "mercy": 0.5},  # Fail
        {"truth": 0.8, "faith": 0.7, "justice": 0.7, "mercy": 0.8},  # Pass
    ]

    filtered = field.apply(constructs)

    assert len(filtered) == 2
    assert filtered[0]["truth"] == 0.9
    assert filtered[1]["truth"] == 0.8


def test_moral_gravity_field_custom_weights():
    """Test evaluation with custom weights."""
    field = MoralGravityField(threshold=0.6)

    construct = {
        "truth": 1.0,
        "faith": 0.0,
        "justice": 0.5,
        "mercy": 0.5,
        "weights": (0.5, 0.2, 0.2, 0.1),
    }

    assert field.filter(construct) is True  # 0.65 > 0.6
