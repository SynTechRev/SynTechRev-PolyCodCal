"""Codical Seal Registry (Layer E).

Maintains a ledger of all compiled artifacts with their covenant metadata,
ensuring traceability and integrity.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class RegistryEntry:
    """A single entry in the Codical Seal Registry.

    Attributes:
        artifact_name: Name of the compiled artifact
        timestamp: When the artifact was registered
        alignment_score: Final alignment score
        seal: Covenant metadata seal
        source: Origin of the inspiration
        purpose: Declared purpose/intent
        outcomes: Observed outcomes (populated over time)
    """

    artifact_name: str
    timestamp: datetime
    alignment_score: float
    seal: str
    source: str
    purpose: str
    outcomes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to dictionary.

        Returns:
            Dictionary representation of the entry
        """
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data


class CodicalSealRegistry:
    """Layer E: Embeds and maintains covenant metadata (✶).

    The registry provides a complete audit trail of all acts of creation,
    their purpose, alignment scores, and observed outcomes.
    """

    def __init__(self):
        """Initialize the Codical Seal Registry."""
        self.entries: List[RegistryEntry] = []

    def register(
        self,
        artifact_name: str,
        alignment_score: float,
        seal: str,
        source: str,
        purpose: str,
    ) -> RegistryEntry:
        """Register a compiled artifact in the ledger.

        Args:
            artifact_name: Name of the artifact
            alignment_score: Final alignment score
            seal: Covenant metadata seal
            source: Origin of the inspiration
            purpose: Declared purpose/intent

        Returns:
            RegistryEntry for the registered artifact

        Raises:
            ValueError: If alignment_score is not in [0.0, 1.0]
        """
        if not 0.0 <= alignment_score <= 1.0:
            raise ValueError(
                f"Alignment score must be in [0.0, 1.0], got {alignment_score}"
            )

        entry = RegistryEntry(
            artifact_name=artifact_name,
            timestamp=datetime.now(),
            alignment_score=alignment_score,
            seal=seal,
            source=source,
            purpose=purpose,
            outcomes=[],
        )

        self.entries.append(entry)
        return entry

    def record_outcome(self, artifact_name: str, outcome: str) -> bool:
        """Record an observed outcome for a registered artifact.

        Args:
            artifact_name: Name of the artifact
            outcome: Description of the observed outcome

        Returns:
            True if outcome was recorded, False if artifact not found
        """
        for entry in self.entries:
            if entry.artifact_name == artifact_name:
                entry.outcomes.append(outcome)
                return True
        return False

    def get_entry(self, artifact_name: str) -> Optional[RegistryEntry]:
        """Retrieve a specific registry entry.

        Args:
            artifact_name: Name of the artifact to retrieve

        Returns:
            RegistryEntry if found, None otherwise
        """
        for entry in self.entries:
            if entry.artifact_name == artifact_name:
                return entry
        return None

    def get_entries(
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
            List of registry entries matching the filters
        """
        entries = self.entries

        if source:
            entries = [e for e in entries if e.source == source]

        if min_alignment is not None:
            entries = [e for e in entries if e.alignment_score >= min_alignment]

        if limit:
            entries = entries[-limit:]

        return entries

    def generate_ledger(self) -> str:
        """Generate a complete Codical Ledger report.

        Returns:
            Formatted ledger report as a string
        """
        lines = [
            "=" * 80,
            "CODICAL LEDGER",
            "Genesis Gateway Registry",
            "=" * 80,
            "",
            f"Total Entries: {len(self.entries)}",
            "",
        ]

        if not self.entries:
            lines.append("No artifacts registered.")
        else:
            for i, entry in enumerate(self.entries, 1):
                lines.extend(
                    [
                        f"Entry {i}: {entry.artifact_name}",
                        f"  Timestamp:  {entry.timestamp.isoformat()}",
                        f"  Source:     {entry.source}",
                        f"  Purpose:    {entry.purpose}",
                        f"  Alignment:  {entry.alignment_score:.3f}",
                        f"  Seal:       {entry.seal}",
                    ]
                )

                if entry.outcomes:
                    lines.append("  Outcomes:")
                    for outcome in entry.outcomes:
                        lines.append(f"    - {outcome}")
                else:
                    lines.append("  Outcomes:   None recorded")

                lines.append("")

        lines.extend(["=" * 80, "End of Codical Ledger", "=" * 80])

        return "\n".join(lines)

    def introspect(self) -> Dict[str, Any]:
        """Perform phase-based introspection on the registry.

        Returns:
            Dictionary with summary statistics and alignment analysis
        """
        if not self.entries:
            return {
                "total_entries": 0,
                "average_alignment": 0.0,
                "sources": {},
                "high_alignment_count": 0,
            }

        total = len(self.entries)
        avg_alignment = sum(e.alignment_score for e in self.entries) / total

        # Count by source
        sources: Dict[str, int] = {}
        for entry in self.entries:
            sources[entry.source] = sources.get(entry.source, 0) + 1

        # Count high alignment (>= 0.9)
        high_alignment = sum(1 for e in self.entries if e.alignment_score >= 0.9)

        return {
            "total_entries": total,
            "average_alignment": avg_alignment,
            "sources": sources,
            "high_alignment_count": high_alignment,
        }

    def clear(self):
        """Clear all registry entries."""
        self.entries.clear()
