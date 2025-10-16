"""Tests for Theo-Syntactic Parser."""

from __future__ import annotations

from datetime import datetime

import pytest

from syntechrev_polycodcal.genesis_gateway.inspiration import Inspiration
from syntechrev_polycodcal.genesis_gateway.parser import TheoSyntacticParser


def test_parser_initialization():
    """Test TheoSyntacticParser creation."""
    parser = TheoSyntacticParser()

    assert parser.parsed_constructs == []


def test_parser_parse_basic():
    """Test parsing a basic inspiration."""
    parser = TheoSyntacticParser()

    inspiration = Inspiration(
        content="Justice must prevail. Truth is eternal.",
        timestamp=datetime.now(),
        source="insight",
    )

    construct = parser.parse(inspiration)

    assert construct["content"] == inspiration.content
    assert construct["source"] == "insight"
    assert "axioms" in construct
    assert "constraints" in construct
    assert "truth" in construct
    assert "faith" in construct
    assert "justice" in construct
    assert "mercy" in construct


def test_parser_parse_empty_content_raises():
    """Test that parsing empty content raises ValueError."""
    parser = TheoSyntacticParser()

    # Create inspiration with valid content, then modify it
    inspiration = Inspiration(content="Valid", timestamp=datetime.now(), source="test")
    # Directly modify the content field to bypass validation
    object.__setattr__(inspiration, "content", "")

    with pytest.raises(ValueError, match="Cannot parse empty inspiration"):
        parser.parse(inspiration)


def test_parser_extract_axioms():
    """Test axiom extraction."""
    parser = TheoSyntacticParser()

    inspiration = Inspiration(
        content="Truth must guide all actions. Justice shall be served. Balance is key.",
        timestamp=datetime.now(),
        source="revelation",
    )

    construct = parser.parse(inspiration)
    axioms = construct["axioms"]

    assert len(axioms) > 0
    # Should find statements with "must", "shall", "is"
    assert any("must" in axiom.lower() for axiom in axioms)


def test_parser_identify_constraints():
    """Test constraint identification."""
    parser = TheoSyntacticParser()

    inspiration = Inspiration(
        content="We must not harm. Deception is forbidden. There is a boundary.",
        timestamp=datetime.now(),
        source="insight",
    )

    construct = parser.parse(inspiration)
    constraints = construct["constraints"]

    assert len(constraints) > 0


def test_parser_calculate_truth():
    """Test truth calculation."""
    parser = TheoSyntacticParser()

    # More content and axioms should increase truth
    inspiration_high = Inspiration(
        content="Truth must guide. Justice shall prevail. Wisdom is eternal. "
        * 10,  # Long content
        timestamp=datetime.now(),
        source="insight",
    )

    construct_high = parser.parse(inspiration_high)

    # Short content with few axioms
    inspiration_low = Inspiration(
        content="Maybe.", timestamp=datetime.now(), source="hypothesis"
    )

    construct_low = parser.parse(inspiration_low)

    assert construct_high["truth"] > construct_low["truth"]


def test_parser_calculate_faith_by_source():
    """Test faith calculation varies by source."""
    parser = TheoSyntacticParser()

    # Dreams and revelations should have higher faith
    dream = Inspiration(
        content="A vision appeared", timestamp=datetime.now(), source="dream"
    )

    hypothesis = Inspiration(
        content="A theory emerged", timestamp=datetime.now(), source="hypothesis"
    )

    construct_dream = parser.parse(dream)
    construct_hypothesis = parser.parse(hypothesis)

    assert construct_dream["faith"] > construct_hypothesis["faith"]


def test_parser_calculate_faith_with_signature():
    """Test faith bonus for having signature."""
    parser = TheoSyntacticParser()

    with_sig = Inspiration(
        content="Divine timing",
        timestamp=datetime.now(),
        source="insight",
        signature="4:40",
    )

    without_sig = Inspiration(
        content="Divine timing", timestamp=datetime.now(), source="insight"
    )

    construct_with = parser.parse(with_sig)
    construct_without = parser.parse(without_sig)

    assert construct_with["faith"] > construct_without["faith"]


def test_parser_calculate_justice():
    """Test justice calculation with constraints."""
    parser = TheoSyntacticParser()

    # More constraints indicate higher justice
    with_constraints = Inspiration(
        content="Must not harm. Cannot deceive. Forbidden to steal.",
        timestamp=datetime.now(),
        source="insight",
    )

    without_constraints = Inspiration(
        content="Be good.", timestamp=datetime.now(), source="insight"
    )

    construct_with = parser.parse(with_constraints)
    construct_without = parser.parse(without_constraints)

    assert construct_with["justice"] > construct_without["justice"]


def test_parser_calculate_mercy():
    """Test mercy calculation with merciful language."""
    parser = TheoSyntacticParser()

    merciful = Inspiration(
        content="With compassion and grace, show mercy and forgiveness.",
        timestamp=datetime.now(),
        source="insight",
    )

    harsh = Inspiration(
        content="Punishment and retribution.", timestamp=datetime.now(), source="insight"
    )

    construct_merciful = parser.parse(merciful)
    construct_harsh = parser.parse(harsh)

    assert construct_merciful["mercy"] > construct_harsh["mercy"]


def test_parser_get_constructs_all():
    """Test retrieving all constructs."""
    parser = TheoSyntacticParser()

    for i in range(3):
        inspiration = Inspiration(
            content=f"Content {i}", timestamp=datetime.now(), source="test"
        )
        parser.parse(inspiration)

    constructs = parser.get_constructs()

    assert len(constructs) == 3


def test_parser_get_constructs_aligned_only():
    """Test retrieving only aligned constructs."""
    parser = TheoSyntacticParser()

    # Create high-scoring inspiration
    high = Inspiration(
        content="Truth must guide. Justice shall prevail with mercy and compassion.",
        timestamp=datetime.now(),
        source="revelation",
        signature="4:40",
    )

    # Create low-scoring inspiration
    low = Inspiration(content="Maybe.", timestamp=datetime.now(), source="hypothesis")

    parser.parse(high)
    parser.parse(low)

    aligned = parser.get_constructs(aligned_only=True, threshold=0.7)

    assert len(aligned) >= 1  # At least the high-scoring one should pass


def test_parser_clear():
    """Test clearing parsed constructs."""
    parser = TheoSyntacticParser()

    inspiration = Inspiration(
        content="Test", timestamp=datetime.now(), source="test"
    )
    parser.parse(inspiration)

    assert len(parser.parsed_constructs) == 1

    parser.clear()

    assert len(parser.parsed_constructs) == 0
