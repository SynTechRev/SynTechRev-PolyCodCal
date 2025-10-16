"""Theo-Syntactic Parser (Layer B).

Translates inspiration into formal logic or algorithmic schema, identifying
core axioms and ethical constraints.
"""

from __future__ import annotations

from typing import Any, Dict, List

from syntechrev_polycodcal.genesis_gateway.inspiration import Inspiration


class TheoSyntacticParser:
    """Layer B: Translates inspiration to formal logic (🜃).

    The parser identifies core axioms, ethical constraints, and structural
    patterns from intuitive input, preparing it for moral evaluation.
    """

    def __init__(self):
        """Initialize the Theo-Syntactic Parser."""
        self.parsed_constructs: List[Dict[str, Any]] = []

    def parse(self, inspiration: Inspiration) -> Dict[str, Any]:
        """Parse an inspiration into structured logic.

        This method performs the Ingestion step of the protocol sequence:
        - Identifies core axioms
        - Extracts ethical constraints
        - Structures the content for formal processing

        Args:
            inspiration: The inspiration to parse

        Returns:
            Structured construct with axioms and constraints

        Raises:
            ValueError: If inspiration content cannot be parsed
        """
        if not inspiration.content:
            raise ValueError("Cannot parse empty inspiration")

        # Extract core axioms (simplified pattern matching)
        axioms = self._extract_axioms(inspiration.content)

        # Identify ethical constraints
        constraints = self._identify_constraints(inspiration.content)

        # Calculate initial alignment metrics
        truth = self._calculate_truth(inspiration.content, axioms)
        faith = self._calculate_faith(inspiration)
        justice = self._calculate_justice(constraints)
        mercy = self._calculate_mercy(inspiration.content)

        construct = {
            "content": inspiration.content,
            "source": inspiration.source,
            "timestamp": inspiration.timestamp,
            "signature": inspiration.signature,
            "axioms": axioms,
            "constraints": constraints,
            "truth": truth,
            "faith": faith,
            "justice": justice,
            "mercy": mercy,
            "metadata": inspiration.metadata,
        }

        self.parsed_constructs.append(construct)
        return construct

    def _extract_axioms(self, content: str) -> List[str]:
        """Extract core axioms from content.

        Args:
            content: The inspiration content

        Returns:
            List of identified axioms
        """
        axioms = []

        # Look for declarative statements (simplified)
        sentences = content.split(".")
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and any(
                word in sentence.lower()
                for word in ["must", "shall", "always", "never", "is", "are"]
            ):
                axioms.append(sentence)

        return axioms if axioms else ["No explicit axioms identified"]

    def _identify_constraints(self, content: str) -> List[str]:
        """Identify ethical constraints from content.

        Args:
            content: The inspiration content

        Returns:
            List of identified constraints
        """
        constraints = []

        # Look for constraint keywords
        constraint_keywords = [
            "should not",
            "must not",
            "cannot",
            "forbidden",
            "prohibited",
            "constraint",
            "limit",
            "boundary",
        ]

        sentences = content.split(".")
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in constraint_keywords):
                constraints.append(sentence)

        return constraints if constraints else []

    def _calculate_truth(self, content: str, axioms: List[str]) -> float:
        """Calculate logical coherence index.

        Args:
            content: The inspiration content
            axioms: Extracted axioms

        Returns:
            Truth score (0.0-1.0)
        """
        # Simple heuristic: more axioms and longer content suggest higher coherence
        base_score = 0.5
        axiom_bonus = min(len(axioms) * 0.1, 0.3)
        length_bonus = min(len(content) / 1000, 0.2)
        return min(base_score + axiom_bonus + length_bonus, 1.0)

    def _calculate_faith(self, inspiration: Inspiration) -> float:
        """Calculate intuitive confidence score.

        Args:
            inspiration: The inspiration object

        Returns:
            Faith score (0.0-1.0)
        """
        # Higher faith for dreams and insights vs hypotheses
        source_scores = {
            "dream": 0.9,
            "insight": 0.85,
            "revelation": 0.95,
            "hypothesis": 0.6,
            "observation": 0.7,
        }
        base = source_scores.get(inspiration.source.lower(), 0.5)

        # Bonus for having a signature
        signature_bonus = 0.1 if inspiration.signature else 0.0

        return min(base + signature_bonus, 1.0)

    def _calculate_justice(self, constraints: List[str]) -> float:
        """Calculate lawful alignment measure.

        Args:
            constraints: Identified ethical constraints

        Returns:
            Justice score (0.0-1.0)
        """
        # More constraints indicate higher attention to lawful alignment
        base_score = 0.6
        constraint_bonus = min(len(constraints) * 0.1, 0.4)
        return min(base_score + constraint_bonus, 1.0)

    def _calculate_mercy(self, content: str) -> float:
        """Calculate ethical moderation factor.

        Args:
            content: The inspiration content

        Returns:
            Mercy score (0.0-1.0)
        """
        # Look for merciful or compassionate language
        mercy_keywords = [
            "mercy",
            "compassion",
            "grace",
            "forgiveness",
            "kindness",
            "gentle",
            "caring",
            "understanding",
        ]

        content_lower = content.lower()
        mercy_count = sum(1 for keyword in mercy_keywords if keyword in content_lower)

        base_score = 0.7
        mercy_bonus = min(mercy_count * 0.1, 0.3)
        return min(base_score + mercy_bonus, 1.0)

    def get_constructs(
        self, aligned_only: bool = False, threshold: float = 0.8
    ) -> List[Dict[str, Any]]:
        """Retrieve parsed constructs.

        Args:
            aligned_only: Return only aligned constructs
            threshold: Alignment threshold for filtering

        Returns:
            List of parsed constructs
        """
        if not aligned_only:
            return self.parsed_constructs

        # Filter by alignment score
        aligned = []
        for construct in self.parsed_constructs:
            score = (
                construct["truth"]
                + construct["faith"]
                + construct["justice"]
                + construct["mercy"]
            ) / 4.0
            if score >= threshold:
                aligned.append(construct)

        return aligned

    def clear(self):
        """Clear all parsed constructs."""
        self.parsed_constructs.clear()
