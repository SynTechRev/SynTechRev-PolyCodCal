"""Genesis Gateway - Main orchestration layer.

Coordinates all five layers of the Creative Intelligence system:
A. Inspiration Interface
B. Theo-Syntactic Parser
C. Moral Gravity Field
D. Genesis Compiler
E. Codical Seal Registry
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from syntechrev_polycodcal.genesis_gateway.alignment import MoralGravityField
from syntechrev_polycodcal.genesis_gateway.compiler import (
    CompiledArtifact,
    GenesisCompiler,
)
from syntechrev_polycodcal.genesis_gateway.inspiration import (
    InspirationInterface,
)
from syntechrev_polycodcal.genesis_gateway.parser import TheoSyntacticParser
from syntechrev_polycodcal.genesis_gateway.registry import (
    CodicalSealRegistry,
    RegistryEntry,
)


class GenesisGateway:
    """Main orchestration for the Genesis Gateway system.

    This class coordinates the complete Protocol Sequence:
    1. Invocation - Record intent and timestamp
    2. Ingestion - Parse symbolic input
    3. Transmutation - Encode and filter by moral alignment
    4. Materialization - Compile to executable artifacts
    5. Reflection - Auto-audit and register

    The Gateway ensures that only aligned constructs (ψ(t) ≥ 0.8) are
    materialized, harmonizing faith-based intuition with formal reasoning.
    """

    def __init__(self, alignment_threshold: float = 0.8):
        """Initialize the Genesis Gateway.

        Args:
            alignment_threshold: Minimum alignment score for compilation
        """
        self.alignment_threshold = alignment_threshold

        # Initialize all five layers
        self.inspiration_interface = InspirationInterface()
        self.parser = TheoSyntacticParser()
        self.moral_gravity = MoralGravityField(threshold=alignment_threshold)
        self.compiler = GenesisCompiler(alignment_threshold=alignment_threshold)
        self.registry = CodicalSealRegistry()

    def process(
        self,
        content: str,
        source: str = "unknown",
        intent: Optional[str] = None,
        signature: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Process an inspiration through the complete Protocol Sequence.

        Args:
            content: The intuitive or symbolic content
            source: Origin of the inspiration
            intent: Declared intent for this computation
            signature: Numerological signature (e.g., "4:40")
            metadata: Additional contextual information

        Returns:
            Dictionary containing results from all processing stages:
                - invocation: Invocation record
                - inspiration: Received inspiration
                - construct: Parsed construct
                - aligned: Whether construct passed moral filter
                - artifact: CompiledArtifact (if aligned)
                - registry_entry: RegistryEntry (if compiled)

        Raises:
            ValueError: If content is empty or alignment fails
        """
        # Step 1: Invocation
        invocation = self.inspiration_interface.invoke(
            intent=intent or "Transform inspiration into aligned manifestation",
            signature=signature,
        )

        # Step 2: Ingestion - Receive inspiration
        inspiration = self.inspiration_interface.receive(
            content=content, source=source, metadata=metadata, signature=signature
        )

        # Step 3: Transmutation - Parse and evaluate
        construct = self.parser.parse(inspiration)

        # Apply Moral Gravity Field filter
        aligned = self.moral_gravity.filter(construct)

        result = {
            "invocation": invocation,
            "inspiration": inspiration,
            "construct": construct,
            "aligned": aligned,
            "artifact": None,
            "registry_entry": None,
        }

        if not aligned:
            # Construct did not pass moral alignment - stop here
            return result

        # Step 4: Materialization - Compile the aligned construct
        artifact = self.compiler.compile(construct)
        result["artifact"] = artifact

        # Step 5: Reflection - Register in Codical Ledger
        registry_entry = self.registry.register(
            artifact_name=artifact.name,
            alignment_score=artifact.alignment_score,
            seal=artifact.seal or "",
            source=source,
            purpose=intent or "Aligned manifestation",
        )
        result["registry_entry"] = registry_entry

        return result

    def batch_process(self, inspirations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process multiple inspirations in batch.

        Args:
            inspirations: List of inspiration dictionaries with:
                - content: required
                - source: optional
                - intent: optional
                - signature: optional
                - metadata: optional

        Returns:
            List of processing results for each inspiration
        """
        results = []
        for insp in inspirations:
            try:
                result = self.process(
                    content=insp["content"],
                    source=insp.get("source", "unknown"),
                    intent=insp.get("intent"),
                    signature=insp.get("signature"),
                    metadata=insp.get("metadata"),
                )
                results.append(result)
            except Exception as e:
                results.append({"error": str(e), "inspiration": insp})

        return results

    def get_aligned_artifacts(self) -> List[CompiledArtifact]:
        """Retrieve all compiled artifacts that passed alignment.

        Returns:
            List of CompiledArtifact objects
        """
        return self.compiler.get_artifacts()

    def get_registry_entries(
        self,
        source: Optional[str] = None,
        min_alignment: Optional[float] = None,
        limit: Optional[int] = None,
    ) -> List[RegistryEntry]:
        """Retrieve registry entries with optional filtering.

        Args:
            source: Filter by inspiration source
            min_alignment: Minimum alignment score
            limit: Maximum number of entries to return

        Returns:
            List of RegistryEntry objects
        """
        return self.registry.get_entries(
            source=source, min_alignment=min_alignment, limit=limit
        )

    def generate_report(self) -> str:
        """Generate a comprehensive report of Gateway activity.

        Returns:
            Formatted report string
        """
        lines = [
            "=" * 80,
            "GENESIS GATEWAY REPORT",
            "=" * 80,
            "",
            f"Alignment Threshold: {self.alignment_threshold}",
            "",
            "=" * 80,
            "LAYER STATISTICS",
            "=" * 80,
            "",
            f"Inspirations Received: {len(self.inspiration_interface.inspirations)}",
            f"Constructs Parsed:     {len(self.parser.parsed_constructs)}",
            f"Artifacts Compiled:    {len(self.compiler.artifacts)}",
            f"Registry Entries:      {len(self.registry.entries)}",
            "",
        ]

        # Add introspection data
        introspection = self.registry.introspect()
        if introspection["total_entries"] > 0:
            lines.extend(
                [
                    "=" * 80,
                    "ALIGNMENT ANALYSIS",
                    "=" * 80,
                    "",
                    f"Average Alignment: {introspection['average_alignment']:.3f}",
                    f"High Alignment (≥0.9): {introspection['high_alignment_count']}",
                    "",
                    "Sources:",
                ]
            )
            for source, count in introspection["sources"].items():
                lines.append(f"  {source}: {count}")
            lines.append("")

        # Add Codical Ledger
        lines.extend([self.registry.generate_ledger(), ""])

        return "\n".join(lines)

    def reflect(self) -> Dict[str, Any]:
        """Perform auto-audit of truthfulness and ethical alignment.

        This implements the Reflection step of the Protocol Sequence.

        Returns:
            Dictionary with audit results and alignment verification
        """
        total_processed = len(self.inspiration_interface.inspirations)
        total_compiled = len(self.compiler.artifacts)

        if total_processed == 0:
            alignment_rate = 0.0
        else:
            alignment_rate = total_compiled / total_processed

        introspection = self.registry.introspect()

        return {
            "total_inspirations": total_processed,
            "total_compiled": total_compiled,
            "alignment_pass_rate": alignment_rate,
            "average_alignment_score": introspection.get("average_alignment", 0.0),
            "high_alignment_count": introspection.get("high_alignment_count", 0),
            "mirrors_constants": alignment_rate >= 0.5,  # At least 50% pass
            "audit_timestamp": self.inspiration_interface.invoke(
                "Reflection audit", None
            )["timestamp"],
        }

    def clear_all(self):
        """Clear all data from all layers (use with caution)."""
        self.inspiration_interface.clear()
        self.parser.clear()
        self.compiler.clear()
        self.registry.clear()
