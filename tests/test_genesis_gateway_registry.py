"""Tests for Codical Seal Registry."""

from __future__ import annotations

import pytest

from syntechrev_polycodcal.genesis_gateway.registry import CodicalSealRegistry


def test_registry_initialization():
    """Test CodicalSealRegistry creation."""
    registry = CodicalSealRegistry()

    assert registry.entries == []


def test_registry_register():
    """Test registering an artifact."""
    registry = CodicalSealRegistry()

    entry = registry.register(
        artifact_name="test_artifact",
        alignment_score=0.85,
        seal="[Test Seal]",
        source="test",
        purpose="Testing registration",
    )

    assert entry.artifact_name == "test_artifact"
    assert entry.alignment_score == 0.85
    assert entry.seal == "[Test Seal]"
    assert entry.source == "test"
    assert entry.purpose == "Testing registration"
    assert entry.outcomes == []
    assert len(registry.entries) == 1


def test_registry_register_invalid_alignment():
    """Test registration with invalid alignment score."""
    registry = CodicalSealRegistry()

    with pytest.raises(ValueError, match="Alignment score must be in"):
        registry.register(
            artifact_name="test",
            alignment_score=1.5,
            seal="seal",
            source="test",
            purpose="test",
        )

    with pytest.raises(ValueError, match="Alignment score must be in"):
        registry.register(
            artifact_name="test",
            alignment_score=-0.1,
            seal="seal",
            source="test",
            purpose="test",
        )


def test_registry_record_outcome():
    """Test recording an outcome for an artifact."""
    registry = CodicalSealRegistry()

    registry.register(
        artifact_name="test_artifact",
        alignment_score=0.85,
        seal="seal",
        source="test",
        purpose="test",
    )

    success = registry.record_outcome(
        artifact_name="test_artifact", outcome="Successfully deployed"
    )

    assert success is True

    entry = registry.get_entry("test_artifact")
    assert len(entry.outcomes) == 1
    assert entry.outcomes[0] == "Successfully deployed"


def test_registry_record_outcome_multiple():
    """Test recording multiple outcomes."""
    registry = CodicalSealRegistry()

    registry.register(
        artifact_name="test_artifact",
        alignment_score=0.85,
        seal="seal",
        source="test",
        purpose="test",
    )

    registry.record_outcome("test_artifact", "Outcome 1")
    registry.record_outcome("test_artifact", "Outcome 2")
    registry.record_outcome("test_artifact", "Outcome 3")

    entry = registry.get_entry("test_artifact")
    assert len(entry.outcomes) == 3


def test_registry_record_outcome_not_found():
    """Test recording outcome for non-existent artifact."""
    registry = CodicalSealRegistry()

    success = registry.record_outcome(
        artifact_name="nonexistent", outcome="Test outcome"
    )

    assert success is False


def test_registry_get_entry():
    """Test retrieving a specific entry."""
    registry = CodicalSealRegistry()

    registry.register(
        artifact_name="artifact1",
        alignment_score=0.85,
        seal="seal1",
        source="test",
        purpose="test1",
    )
    registry.register(
        artifact_name="artifact2",
        alignment_score=0.90,
        seal="seal2",
        source="test",
        purpose="test2",
    )

    entry = registry.get_entry("artifact2")

    assert entry is not None
    assert entry.artifact_name == "artifact2"
    assert entry.alignment_score == 0.90


def test_registry_get_entry_not_found():
    """Test retrieving non-existent entry returns None."""
    registry = CodicalSealRegistry()

    entry = registry.get_entry("nonexistent")

    assert entry is None


def test_registry_get_entries_all():
    """Test retrieving all entries."""
    registry = CodicalSealRegistry()

    for i in range(3):
        registry.register(
            artifact_name=f"artifact{i}",
            alignment_score=0.8,
            seal="seal",
            source="test",
            purpose="test",
        )

    entries = registry.get_entries()

    assert len(entries) == 3


def test_registry_get_entries_by_source():
    """Test filtering entries by source."""
    registry = CodicalSealRegistry()

    registry.register(
        artifact_name="dream1",
        alignment_score=0.85,
        seal="seal",
        source="dream",
        purpose="test",
    )
    registry.register(
        artifact_name="insight1",
        alignment_score=0.90,
        seal="seal",
        source="insight",
        purpose="test",
    )
    registry.register(
        artifact_name="dream2",
        alignment_score=0.88,
        seal="seal",
        source="dream",
        purpose="test",
    )

    dreams = registry.get_entries(source="dream")

    assert len(dreams) == 2
    assert all(e.source == "dream" for e in dreams)


def test_registry_get_entries_by_min_alignment():
    """Test filtering entries by minimum alignment."""
    registry = CodicalSealRegistry()

    registry.register(
        artifact_name="low",
        alignment_score=0.70,
        seal="seal",
        source="test",
        purpose="test",
    )
    registry.register(
        artifact_name="high",
        alignment_score=0.95,
        seal="seal",
        source="test",
        purpose="test",
    )
    registry.register(
        artifact_name="medium",
        alignment_score=0.85,
        seal="seal",
        source="test",
        purpose="test",
    )

    high_aligned = registry.get_entries(min_alignment=0.9)

    assert len(high_aligned) == 1
    assert high_aligned[0].artifact_name == "high"


def test_registry_get_entries_with_limit():
    """Test limiting number of returned entries."""
    registry = CodicalSealRegistry()

    for i in range(10):
        registry.register(
            artifact_name=f"artifact{i}",
            alignment_score=0.8,
            seal="seal",
            source="test",
            purpose="test",
        )

    limited = registry.get_entries(limit=3)

    assert len(limited) == 3
    # Should return the last 3
    assert limited[0].artifact_name == "artifact7"
    assert limited[1].artifact_name == "artifact8"
    assert limited[2].artifact_name == "artifact9"


def test_registry_generate_ledger():
    """Test generating ledger report."""
    registry = CodicalSealRegistry()

    registry.register(
        artifact_name="test_artifact",
        alignment_score=0.85,
        seal="[Test Seal]",
        source="dream",
        purpose="Test purpose",
    )
    registry.record_outcome("test_artifact", "Outcome 1")

    ledger = registry.generate_ledger()

    assert "CODICAL LEDGER" in ledger
    assert "test_artifact" in ledger
    assert "0.850" in ledger
    assert "[Test Seal]" in ledger
    assert "Outcome 1" in ledger


def test_registry_generate_ledger_empty():
    """Test generating ledger with no entries."""
    registry = CodicalSealRegistry()

    ledger = registry.generate_ledger()

    assert "CODICAL LEDGER" in ledger
    assert "No artifacts registered" in ledger


def test_registry_introspect():
    """Test introspection of registry."""
    registry = CodicalSealRegistry()

    registry.register(
        artifact_name="art1",
        alignment_score=0.85,
        seal="seal",
        source="dream",
        purpose="test",
    )
    registry.register(
        artifact_name="art2",
        alignment_score=0.95,
        seal="seal",
        source="insight",
        purpose="test",
    )
    registry.register(
        artifact_name="art3",
        alignment_score=0.75,
        seal="seal",
        source="dream",
        purpose="test",
    )

    stats = registry.introspect()

    assert stats["total_entries"] == 3
    assert abs(stats["average_alignment"] - 0.85) < 0.01
    assert stats["sources"]["dream"] == 2
    assert stats["sources"]["insight"] == 1
    assert stats["high_alignment_count"] == 1  # Only art2 >= 0.9


def test_registry_introspect_empty():
    """Test introspection with empty registry."""
    registry = CodicalSealRegistry()

    stats = registry.introspect()

    assert stats["total_entries"] == 0
    assert stats["average_alignment"] == 0.0
    assert stats["sources"] == {}
    assert stats["high_alignment_count"] == 0


def test_registry_clear():
    """Test clearing all registry entries."""
    registry = CodicalSealRegistry()

    registry.register(
        artifact_name="test",
        alignment_score=0.85,
        seal="seal",
        source="test",
        purpose="test",
    )

    assert len(registry.entries) == 1

    registry.clear()

    assert len(registry.entries) == 0


def test_registry_entry_to_dict():
    """Test converting registry entry to dictionary."""
    registry = CodicalSealRegistry()

    entry = registry.register(
        artifact_name="test",
        alignment_score=0.85,
        seal="seal",
        source="test",
        purpose="test",
    )

    entry_dict = entry.to_dict()

    assert entry_dict["artifact_name"] == "test"
    assert entry_dict["alignment_score"] == 0.85
    assert isinstance(entry_dict["timestamp"], str)  # ISO format
    assert entry_dict["outcomes"] == []
