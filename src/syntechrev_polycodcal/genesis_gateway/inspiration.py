"""Inspiration Interface (Layer A).

Receives intuitive or symbolic data including dreams, insights, and hypotheses,
and prepares them for formal processing.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass
class Inspiration:
    """Represents an intuitive or symbolic input.

    Attributes:
        content: The raw intuitive/symbolic content
        timestamp: When the inspiration was received
        source: Origin of the inspiration (e.g., "dream", "insight", "hypothesis")
        metadata: Additional contextual information
        signature: Numerological or temporal signature (e.g., "4:40")
    """

    content: str
    timestamp: datetime
    source: str = "unknown"
    metadata: Optional[Dict[str, Any]] = None
    signature: Optional[str] = None

    def __post_init__(self):
        """Validate inspiration data."""
        if not self.content:
            raise ValueError("Inspiration content cannot be empty")
        if self.metadata is None:
            self.metadata = {}


class InspirationInterface:
    """Layer A: Receives and processes intuitive or symbolic data (🜂).

    The Inspiration Interface is the entry point for creative and symbolic
    input into the Genesis Gateway system.
    """

    def __init__(self):
        """Initialize the Inspiration Interface."""
        self.inspirations: list[Inspiration] = []

    def receive(
        self,
        content: str,
        source: str = "unknown",
        metadata: Optional[Dict[str, Any]] = None,
        signature: Optional[str] = None,
    ) -> Inspiration:
        """Receive and record an inspiration.

        Args:
            content: The intuitive or symbolic content
            source: Origin of the inspiration
            metadata: Additional contextual information
            signature: Numerological or temporal signature

        Returns:
            Inspiration object containing the recorded data

        Raises:
            ValueError: If content is empty
        """
        inspiration = Inspiration(
            content=content,
            timestamp=datetime.now(timezone.utc),
            source=source,
            metadata=metadata or {},
            signature=signature,
        )
        self.inspirations.append(inspiration)
        return inspiration

    def invoke(self, intent: str, signature: Optional[str] = None) -> Dict[str, Any]:
        """Invoke the interface with a declared intent.

        This method performs the Invocation step of the protocol sequence:
        - Records timestamp & numerological signature
        - Declares intent for alignment verification

        Args:
            intent: The declared intent of the computation
            signature: Numerological signature (e.g., "4:40")

        Returns:
            Invocation record with timestamp and alignment declaration
        """
        timestamp = datetime.now(timezone.utc)
        return {
            "intent": intent,
            "timestamp": timestamp,
            "signature": signature,
            "declaration": (
                "Let this computation manifest only in alignment with Divine Order."
            ),
        }

    def get_inspirations(
        self, source: Optional[str] = None, limit: Optional[int] = None
    ) -> list[Inspiration]:
        """Retrieve recorded inspirations.

        Args:
            source: Filter by source type (optional)
            limit: Maximum number of inspirations to return (optional)

        Returns:
            List of recorded inspirations, filtered and limited as specified
        """
        inspirations = self.inspirations
        if source:
            inspirations = [i for i in inspirations if i.source == source]
        if limit:
            inspirations = inspirations[-limit:]
        return inspirations

    def clear(self):
        """Clear all recorded inspirations."""
        self.inspirations.clear()
