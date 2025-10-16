"""Genesis Compiler (Layer D).

Materializes aligned logic as executable prototypes, converting verified
constructs into concrete implementations.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class CompiledArtifact:
    """Represents a materialized construct.

    Attributes:
        name: Identifier for the artifact
        content: The compiled/materialized content
        source_construct: Original construct that was compiled
        timestamp: When the artifact was compiled
        alignment_score: Final alignment score
        seal: Codical seal metadata
    """

    name: str
    content: str
    source_construct: Dict[str, Any]
    timestamp: datetime
    alignment_score: float
    seal: Optional[str] = None


class GenesisCompiler:
    """Layer D: Materializes aligned logic to executable prototypes (🜁).

    The compiler transforms verified, morally-aligned constructs into
    concrete implementations with embedded covenant metadata.
    """

    def __init__(self, alignment_threshold: float = 0.8):
        """Initialize the Genesis Compiler.

        Args:
            alignment_threshold: Minimum alignment score for compilation
        """
        if not 0.0 <= alignment_threshold <= 1.0:
            raise ValueError(
                f"Threshold must be in [0.0, 1.0], got {alignment_threshold}"
            )
        self.alignment_threshold = alignment_threshold
        self.artifacts: List[CompiledArtifact] = []

    def compile(
        self, construct: Dict[str, Any], seal: Optional[str] = None
    ) -> CompiledArtifact:
        """Compile a construct into an executable artifact.

        This method performs the Materialization step of the protocol sequence:
        - Verifies alignment threshold
        - Renders logic to system code or simulation layer
        - Embeds Codical Seal metadata

        Args:
            construct: Verified construct with alignment scores
            seal: Optional custom seal (default uses standard Codex Φ7 seal)

        Returns:
            CompiledArtifact representing the materialized construct

        Raises:
            ValueError: If construct does not meet alignment threshold
        """
        # Calculate alignment score
        alignment = self._calculate_alignment(construct)

        if alignment < self.alignment_threshold:
            raise ValueError(
                f"Construct alignment ({alignment:.3f}) below threshold "
                f"({self.alignment_threshold:.3f}). Cannot compile."
            )

        # Generate artifact name
        name = self._generate_name(construct)

        # Materialize the construct
        content = self._materialize(construct)

        # Create artifact with seal
        artifact = CompiledArtifact(
            name=name,
            content=content,
            source_construct=construct,
            timestamp=datetime.now(timezone.utc),
            alignment_score=alignment,
            seal=seal or self._default_seal(),
        )

        self.artifacts.append(artifact)
        return artifact

    def _calculate_alignment(self, construct: Dict[str, Any]) -> float:
        """Calculate the overall alignment score.

        Args:
            construct: Construct with T, F, J, M scores

        Returns:
            Alignment score ψ(t)
        """
        weights = construct.get("weights", (0.25, 0.25, 0.25, 0.25))
        alpha, beta, gamma, delta = weights

        truth = construct.get("truth", 0.5)
        faith = construct.get("faith", 0.5)
        justice = construct.get("justice", 0.5)
        mercy = construct.get("mercy", 0.5)

        return alpha * truth + beta * faith + gamma * justice + delta * mercy

    def _generate_name(self, construct: Dict[str, Any]) -> str:
        """Generate a name for the compiled artifact.

        Args:
            construct: Source construct

        Returns:
            Generated artifact name
        """
        source = construct.get("source", "unknown")
        timestamp = construct.get("timestamp", datetime.now(timezone.utc))
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        return f"{source}_{timestamp_str}"

    def _materialize(self, construct: Dict[str, Any]) -> str:
        """Materialize the construct into executable content.

        Args:
            construct: Construct to materialize

        Returns:
            Materialized content as a string
        """
        content_lines = [
            "# Genesis Gateway Compiled Artifact",
            f"# Source: {construct.get('source', 'unknown')}",
            f"# Timestamp: {construct.get('timestamp', datetime.now(timezone.utc))}",
            "",
            "# Core Axioms:",
        ]

        axioms = construct.get("axioms", [])
        for i, axiom in enumerate(axioms, 1):
            content_lines.append(f"#   {i}. {axiom}")

        content_lines.append("")
        content_lines.append("# Ethical Constraints:")

        constraints = construct.get("constraints", [])
        if constraints:
            for i, constraint in enumerate(constraints, 1):
                content_lines.append(f"#   {i}. {constraint}")
        else:
            content_lines.append("#   None specified")

        content_lines.append("")
        content_lines.append("# Alignment Metrics:")
        content_lines.append(f"#   Truth:   {construct.get('truth', 0.0):.3f}")
        content_lines.append(f"#   Faith:   {construct.get('faith', 0.0):.3f}")
        content_lines.append(f"#   Justice: {construct.get('justice', 0.0):.3f}")
        content_lines.append(f"#   Mercy:   {construct.get('mercy', 0.0):.3f}")

        content_lines.append("")
        content_lines.append("# Original Content:")
        content_lines.append(f'"""\n{construct.get("content", "")}\n"""')

        return "\n".join(content_lines)

    def _default_seal(self) -> str:
        """Generate default Codex Φ7 seal.

        Returns:
            Standard covenant metadata seal
        """
        return (
            "[Codex Φ7 | Created in alignment with Divine Will | YHWH be glorified]"
        )

    def get_artifacts(
        self, min_alignment: Optional[float] = None
    ) -> List[CompiledArtifact]:
        """Retrieve compiled artifacts.

        Args:
            min_alignment: Optional minimum alignment filter

        Returns:
            List of compiled artifacts
        """
        if min_alignment is None:
            return self.artifacts

        return [a for a in self.artifacts if a.alignment_score >= min_alignment]

    def export_artifact(self, artifact: CompiledArtifact) -> str:
        """Export an artifact with its seal.

        Args:
            artifact: The artifact to export

        Returns:
            Complete artifact content with seal
        """
        lines = [
            "=" * 80,
            f"Genesis Gateway Artifact: {artifact.name}",
            "=" * 80,
            "",
            artifact.content,
            "",
            "=" * 80,
            "Codical Seal:",
            artifact.seal or self._default_seal(),
            "=" * 80,
        ]
        return "\n".join(lines)

    def clear(self):
        """Clear all compiled artifacts."""
        self.artifacts.clear()
