"""Tests for Genesis Compiler."""

from __future__ import annotations

from datetime import datetime

import pytest

from syntechrev_polycodcal.genesis_gateway.compiler import GenesisCompiler


def test_compiler_initialization():
    """Test GenesisCompiler creation."""
    compiler = GenesisCompiler(alignment_threshold=0.8)

    assert compiler.alignment_threshold == 0.8
    assert compiler.artifacts == []


def test_compiler_invalid_threshold():
    """Test invalid threshold raises ValueError."""
    with pytest.raises(ValueError, match="Threshold must be in"):
        GenesisCompiler(alignment_threshold=1.5)


def test_compiler_compile_aligned_construct():
    """Test compiling a construct that meets threshold."""
    compiler = GenesisCompiler(alignment_threshold=0.7)

    construct = {
        "content": "Test content",
        "source": "test",
        "timestamp": datetime.now(),
        "truth": 0.8,
        "faith": 0.8,
        "justice": 0.8,
        "mercy": 0.8,
        "axioms": ["Axiom 1"],
        "constraints": ["Constraint 1"],
    }

    artifact = compiler.compile(construct)

    assert artifact.name.startswith("test_")
    assert "Test content" in artifact.content
    assert artifact.alignment_score == 0.8
    assert artifact.seal is not None
    assert len(compiler.artifacts) == 1


def test_compiler_compile_below_threshold_raises():
    """Test compiling construct below threshold raises ValueError."""
    compiler = GenesisCompiler(alignment_threshold=0.9)

    construct = {
        "content": "Low alignment",
        "source": "test",
        "timestamp": datetime.now(),
        "truth": 0.5,
        "faith": 0.5,
        "justice": 0.5,
        "mercy": 0.5,
        "axioms": [],
        "constraints": [],
    }

    with pytest.raises(ValueError, match="alignment.*below threshold"):
        compiler.compile(construct)


def test_compiler_compile_custom_seal():
    """Test compiling with custom seal."""
    compiler = GenesisCompiler()

    construct = {
        "content": "Test",
        "source": "test",
        "timestamp": datetime.now(),
        "truth": 0.9,
        "faith": 0.9,
        "justice": 0.9,
        "mercy": 0.9,
        "axioms": [],
        "constraints": [],
    }

    custom_seal = "[Custom Seal | Test]"
    artifact = compiler.compile(construct, seal=custom_seal)

    assert artifact.seal == custom_seal


def test_compiler_compile_weighted_alignment():
    """Test compilation with custom weights."""
    compiler = GenesisCompiler(alignment_threshold=0.6)

    construct = {
        "content": "Weighted test",
        "source": "test",
        "timestamp": datetime.now(),
        "truth": 1.0,
        "faith": 0.0,
        "justice": 0.5,
        "mercy": 0.5,
        "weights": (0.5, 0.2, 0.2, 0.1),  # Truth-heavy
        "axioms": [],
        "constraints": [],
    }

    artifact = compiler.compile(construct)

    # 0.5*1.0 + 0.2*0.0 + 0.2*0.5 + 0.1*0.5 = 0.65
    assert abs(artifact.alignment_score - 0.65) < 1e-9


def test_compiler_get_artifacts_all():
    """Test retrieving all artifacts."""
    compiler = GenesisCompiler(alignment_threshold=0.5)

    for i in range(3):
        construct = {
            "content": f"Content {i}",
            "source": "test",
            "timestamp": datetime.now(),
            "truth": 0.8,
            "faith": 0.8,
            "justice": 0.8,
            "mercy": 0.8,
            "axioms": [],
            "constraints": [],
        }
        compiler.compile(construct)

    artifacts = compiler.get_artifacts()

    assert len(artifacts) == 3


def test_compiler_get_artifacts_filtered():
    """Test filtering artifacts by minimum alignment."""
    compiler = GenesisCompiler(alignment_threshold=0.5)

    # Create artifacts with different alignments
    high_construct = {
        "content": "High",
        "source": "test",
        "timestamp": datetime.now(),
        "truth": 0.95,
        "faith": 0.95,
        "justice": 0.95,
        "mercy": 0.95,
        "axioms": [],
        "constraints": [],
    }

    low_construct = {
        "content": "Low",
        "source": "test",
        "timestamp": datetime.now(),
        "truth": 0.6,
        "faith": 0.6,
        "justice": 0.6,
        "mercy": 0.6,
        "axioms": [],
        "constraints": [],
    }

    compiler.compile(high_construct)
    compiler.compile(low_construct)

    high_artifacts = compiler.get_artifacts(min_alignment=0.9)

    assert len(high_artifacts) == 1
    assert high_artifacts[0].alignment_score >= 0.9


def test_compiler_export_artifact():
    """Test exporting an artifact with seal."""
    compiler = GenesisCompiler()

    construct = {
        "content": "Export test",
        "source": "test",
        "timestamp": datetime.now(),
        "truth": 0.9,
        "faith": 0.9,
        "justice": 0.9,
        "mercy": 0.9,
        "axioms": ["Test axiom"],
        "constraints": [],
    }

    artifact = compiler.compile(construct)
    exported = compiler.export_artifact(artifact)

    assert "Genesis Gateway Artifact" in exported
    assert artifact.name in exported
    assert "Codical Seal" in exported
    assert "[Codex Φ7" in exported


def test_compiler_materialize_includes_metrics():
    """Test that materialized content includes alignment metrics."""
    compiler = GenesisCompiler()

    construct = {
        "content": "Test content",
        "source": "test",
        "timestamp": datetime.now(),
        "truth": 0.85,
        "faith": 0.90,
        "justice": 0.80,
        "mercy": 0.95,
        "axioms": ["Axiom 1", "Axiom 2"],
        "constraints": ["Constraint 1"],
    }

    artifact = compiler.compile(construct)

    assert "Truth:   0.850" in artifact.content
    assert "Faith:   0.900" in artifact.content
    assert "Justice: 0.800" in artifact.content
    assert "Mercy:   0.950" in artifact.content
    assert "Axiom 1" in artifact.content
    assert "Constraint 1" in artifact.content


def test_compiler_clear():
    """Test clearing all artifacts."""
    compiler = GenesisCompiler(alignment_threshold=0.5)

    construct = {
        "content": "Test",
        "source": "test",
        "timestamp": datetime.now(),
        "truth": 0.8,
        "faith": 0.8,
        "justice": 0.8,
        "mercy": 0.8,
        "axioms": [],
        "constraints": [],
    }

    compiler.compile(construct)
    assert len(compiler.artifacts) == 1

    compiler.clear()
    assert len(compiler.artifacts) == 0
