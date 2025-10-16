"""Tests for Inspiration Interface."""

from __future__ import annotations

from datetime import datetime

import pytest

from syntechrev_polycodcal.genesis_gateway.inspiration import (
    Inspiration,
    InspirationInterface,
)


def test_inspiration_creation():
    """Test Inspiration dataclass creation."""
    timestamp = datetime.now()
    inspiration = Inspiration(
        content="A vision of harmony",
        timestamp=timestamp,
        source="dream",
        metadata={"intensity": "high"},
        signature="4:40",
    )

    assert inspiration.content == "A vision of harmony"
    assert inspiration.timestamp == timestamp
    assert inspiration.source == "dream"
    assert inspiration.metadata == {"intensity": "high"}
    assert inspiration.signature == "4:40"


def test_inspiration_empty_content_raises():
    """Test that empty content raises ValueError."""
    with pytest.raises(ValueError, match="content cannot be empty"):
        Inspiration(content="", timestamp=datetime.now(), source="test")


def test_inspiration_default_metadata():
    """Test that metadata defaults to empty dict."""
    inspiration = Inspiration(content="Test", timestamp=datetime.now())

    assert inspiration.metadata == {}


def test_inspiration_interface_initialization():
    """Test InspirationInterface creation."""
    interface = InspirationInterface()

    assert interface.inspirations == []


def test_inspiration_interface_receive():
    """Test receiving an inspiration."""
    interface = InspirationInterface()

    inspiration = interface.receive(
        content="Insight about balance", source="insight", signature="4:40"
    )

    assert inspiration.content == "Insight about balance"
    assert inspiration.source == "insight"
    assert inspiration.signature == "4:40"
    assert len(interface.inspirations) == 1


def test_inspiration_interface_receive_multiple():
    """Test receiving multiple inspirations."""
    interface = InspirationInterface()

    interface.receive(content="First", source="dream")
    interface.receive(content="Second", source="insight")
    interface.receive(content="Third", source="hypothesis")

    assert len(interface.inspirations) == 3


def test_inspiration_interface_receive_with_metadata():
    """Test receiving inspiration with metadata."""
    interface = InspirationInterface()

    metadata = {"context": "morning meditation", "intensity": 8}
    inspiration = interface.receive(
        content="Divine guidance", source="revelation", metadata=metadata
    )

    assert inspiration.metadata == metadata


def test_inspiration_interface_receive_empty_content_raises():
    """Test that receiving empty content raises ValueError."""
    interface = InspirationInterface()

    with pytest.raises(ValueError, match="content cannot be empty"):
        interface.receive(content="")


def test_inspiration_interface_invoke():
    """Test invoking the interface with intent."""
    interface = InspirationInterface()

    invocation = interface.invoke(
        intent="Transform insight into manifestation", signature="4:40"
    )

    assert invocation["intent"] == "Transform insight into manifestation"
    assert invocation["signature"] == "4:40"
    assert "timestamp" in invocation
    assert isinstance(invocation["timestamp"], datetime)
    assert (
        invocation["declaration"]
        == "Let this computation manifest only in alignment with Divine Order."
    )


def test_inspiration_interface_invoke_without_signature():
    """Test invocation without signature."""
    interface = InspirationInterface()

    invocation = interface.invoke(intent="Test intent")

    assert invocation["signature"] is None
    assert invocation["intent"] == "Test intent"


def test_inspiration_interface_get_inspirations_all():
    """Test retrieving all inspirations."""
    interface = InspirationInterface()

    interface.receive(content="First", source="dream")
    interface.receive(content="Second", source="insight")

    inspirations = interface.get_inspirations()

    assert len(inspirations) == 2


def test_inspiration_interface_get_inspirations_by_source():
    """Test filtering inspirations by source."""
    interface = InspirationInterface()

    interface.receive(content="Dream 1", source="dream")
    interface.receive(content="Insight 1", source="insight")
    interface.receive(content="Dream 2", source="dream")

    dreams = interface.get_inspirations(source="dream")

    assert len(dreams) == 2
    assert all(i.source == "dream" for i in dreams)


def test_inspiration_interface_get_inspirations_with_limit():
    """Test limiting number of returned inspirations."""
    interface = InspirationInterface()

    for i in range(10):
        interface.receive(content=f"Inspiration {i}", source="test")

    limited = interface.get_inspirations(limit=3)

    assert len(limited) == 3
    # Should return the last 3
    assert limited[0].content == "Inspiration 7"
    assert limited[1].content == "Inspiration 8"
    assert limited[2].content == "Inspiration 9"


def test_inspiration_interface_get_inspirations_source_and_limit():
    """Test filtering by source and limiting results."""
    interface = InspirationInterface()

    for i in range(5):
        interface.receive(content=f"Dream {i}", source="dream")
        interface.receive(content=f"Insight {i}", source="insight")

    dreams = interface.get_inspirations(source="dream", limit=2)

    assert len(dreams) == 2
    assert all(i.source == "dream" for i in dreams)


def test_inspiration_interface_clear():
    """Test clearing all inspirations."""
    interface = InspirationInterface()

    interface.receive(content="First", source="test")
    interface.receive(content="Second", source="test")

    assert len(interface.inspirations) == 2

    interface.clear()

    assert len(interface.inspirations) == 0
