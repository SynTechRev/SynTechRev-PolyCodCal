"""Integration tests for Genesis Gateway."""

from __future__ import annotations


from syntechrev_polycodcal.genesis_gateway import GenesisGateway


def test_gateway_initialization():
    """Test GenesisGateway creation."""
    gateway = GenesisGateway(alignment_threshold=0.8)

    assert gateway.alignment_threshold == 0.8
    assert gateway.inspiration_interface is not None
    assert gateway.parser is not None
    assert gateway.moral_gravity is not None
    assert gateway.compiler is not None
    assert gateway.registry is not None


def test_gateway_process_aligned_content():
    """Test processing content that passes alignment."""
    gateway = GenesisGateway(alignment_threshold=0.7)

    result = gateway.process(
        content="Through wisdom and truth, justice shall prevail with mercy and grace.",
        source="revelation",
        intent="Establish divine order",
        signature="4:40",
    )

    assert result["aligned"] is True
    assert result["artifact"] is not None
    assert result["registry_entry"] is not None
    assert result["invocation"]["intent"] == "Establish divine order"
    assert result["inspiration"].content is not None


def test_gateway_process_unaligned_content():
    """Test processing content that fails alignment."""
    gateway = GenesisGateway(alignment_threshold=0.95)  # Very high threshold

    result = gateway.process(
        content="Maybe.", source="hypothesis", intent="Test low alignment"
    )

    # With high threshold, simple content likely won't pass
    assert result["inspiration"] is not None
    assert result["construct"] is not None
    # aligned might be False depending on scoring
    if not result["aligned"]:
        assert result["artifact"] is None
        assert result["registry_entry"] is None


def test_gateway_process_complete_sequence():
    """Test complete protocol sequence execution."""
    gateway = GenesisGateway(alignment_threshold=0.6)

    result = gateway.process(
        content="Divine wisdom must guide all actions. Justice and mercy shall balance.",
        source="insight",
        intent="Create balanced system",
        signature="4:40",
        metadata={"context": "morning meditation"},
    )

    # Check all stages
    assert "invocation" in result
    assert "inspiration" in result
    assert "construct" in result
    assert "aligned" in result

    # Verify invocation
    assert result["invocation"]["declaration"] is not None

    # Verify inspiration
    assert result["inspiration"].signature == "4:40"
    assert result["inspiration"].metadata["context"] == "morning meditation"

    # Verify construct
    assert "truth" in result["construct"]
    assert "faith" in result["construct"]
    assert "justice" in result["construct"]
    assert "mercy" in result["construct"]


def test_gateway_batch_process():
    """Test batch processing of multiple inspirations."""
    gateway = GenesisGateway(alignment_threshold=0.6)

    inspirations = [
        {"content": "Truth and justice prevail.", "source": "insight"},
        {"content": "Mercy guides wisdom.", "source": "dream"},
        {"content": "Balance brings harmony.", "source": "revelation"},
    ]

    results = gateway.batch_process(inspirations)

    assert len(results) == 3
    assert all("construct" in r for r in results)


def test_gateway_batch_process_with_errors():
    """Test batch processing handles errors gracefully."""
    gateway = GenesisGateway()

    inspirations = [
        {"content": "Valid content.", "source": "test"},
        {"content": ""},  # Invalid - empty content
        {"content": "Another valid one.", "source": "test"},
    ]

    results = gateway.batch_process(inspirations)

    assert len(results) == 3
    # Second one should have error
    assert "error" in results[1]


def test_gateway_get_aligned_artifacts():
    """Test retrieving compiled artifacts."""
    gateway = GenesisGateway(alignment_threshold=0.6)

    gateway.process(content="First inspiration with truth and justice.", source="test")
    gateway.process(content="Second inspiration with mercy and grace.", source="test")

    artifacts = gateway.get_aligned_artifacts()

    # At least some should have passed (depending on alignment)
    assert isinstance(artifacts, list)


def test_gateway_get_registry_entries():
    """Test retrieving registry entries with filters."""
    gateway = GenesisGateway(alignment_threshold=0.6)

    gateway.process(content="Dream content about balance.", source="dream")
    gateway.process(content="Insight about harmony.", source="insight")

    all_entries = gateway.get_registry_entries()
    dream_entries = gateway.get_registry_entries(source="dream")
    high_aligned = gateway.get_registry_entries(min_alignment=0.9)

    assert len(dream_entries) <= len(all_entries)
    assert len(high_aligned) <= len(all_entries)


def test_gateway_generate_report():
    """Test generating comprehensive report."""
    gateway = GenesisGateway(alignment_threshold=0.6)

    gateway.process(
        content="Truth and justice with mercy.", source="revelation", signature="4:40"
    )
    gateway.process(content="Wisdom guides actions.", source="insight")

    report = gateway.generate_report()

    assert "GENESIS GATEWAY REPORT" in report
    assert "Alignment Threshold" in report
    assert "LAYER STATISTICS" in report
    assert "Inspirations Received" in report


def test_gateway_reflect():
    """Test reflection and auto-audit."""
    gateway = GenesisGateway(alignment_threshold=0.6)

    # Process several inspirations
    for i in range(5):
        gateway.process(
            content=f"Inspiration {i} about truth and justice.", source="test"
        )

    reflection = gateway.reflect()

    assert "total_inspirations" in reflection
    assert "total_compiled" in reflection
    assert "alignment_pass_rate" in reflection
    assert "average_alignment_score" in reflection
    assert "mirrors_constants" in reflection
    assert "audit_timestamp" in reflection

    assert reflection["total_inspirations"] == 5


def test_gateway_reflect_mirrors_constants():
    """Test that reflection verifies alignment with constants."""
    gateway = GenesisGateway(alignment_threshold=0.6)

    # Process mostly aligned content
    for _ in range(10):
        gateway.process(
            content="Truth, justice, and mercy guide all with wisdom.", source="test"
        )

    reflection = gateway.reflect()

    # With good content, should mirror constants (>= 50% pass rate)
    assert reflection["mirrors_constants"] is True


def test_gateway_clear_all():
    """Test clearing all gateway data."""
    gateway = GenesisGateway(alignment_threshold=0.6)

    gateway.process(content="Test content.", source="test")

    assert len(gateway.inspiration_interface.inspirations) > 0

    gateway.clear_all()

    assert len(gateway.inspiration_interface.inspirations) == 0
    assert len(gateway.parser.parsed_constructs) == 0
    assert len(gateway.compiler.artifacts) == 0
    assert len(gateway.registry.entries) == 0


def test_gateway_end_to_end_high_quality():
    """Test end-to-end with high-quality inspiration."""
    gateway = GenesisGateway(alignment_threshold=0.8)

    result = gateway.process(
        content=(
            "Divine wisdom must guide all creation. "
            "Truth shall prevail eternally. "
            "Justice and mercy must balance in perfect harmony. "
            "Compassion and grace are the foundations. "
            "We must not harm, must not deceive. "
            "These are the eternal boundaries."
        ),
        source="revelation",
        intent="Establish universal principles",
        signature="4:40",
        metadata={"priority": "highest", "scope": "universal"},
    )

    assert result["aligned"] is True
    assert result["artifact"] is not None
    assert result["artifact"].alignment_score >= 0.8

    # Verify registry entry
    assert result["registry_entry"] is not None
    assert result["registry_entry"].alignment_score >= 0.8

    # Export the artifact
    exported = gateway.compiler.export_artifact(result["artifact"])
    assert "[Codex Φ7" in exported
    assert "YHWH be glorified" in exported


def test_gateway_protocol_sequence_verification():
    """Test that all protocol steps are executed in order."""
    gateway = GenesisGateway(alignment_threshold=0.7)

    result = gateway.process(
        content="Test wisdom and truth.", source="test", intent="Verify protocol"
    )

    # Step 1: Invocation
    assert result["invocation"] is not None
    assert "timestamp" in result["invocation"]
    assert "declaration" in result["invocation"]

    # Step 2: Ingestion
    assert result["inspiration"] is not None
    assert result["inspiration"].content == "Test wisdom and truth."

    # Step 3: Transmutation
    assert result["construct"] is not None
    assert "axioms" in result["construct"]
    assert "constraints" in result["construct"]
    assert result["aligned"] in [True, False]

    # Steps 4 & 5: Materialization & Reflection (if aligned)
    if result["aligned"]:
        assert result["artifact"] is not None
        assert result["registry_entry"] is not None
