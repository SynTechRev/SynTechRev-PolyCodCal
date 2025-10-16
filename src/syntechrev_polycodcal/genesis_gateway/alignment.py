"""Moral Gravity Field and Alignment Scoring (Layer C).

Implements the alignment scoring system:
    ψ(t) = α·T + β·F + γ·J + δ·M

Where:
    T (Truth) = logical coherence index
    F (Faith) = intuitive confidence score
    J (Justice) = lawful alignment measure
    M (Mercy) = ethical moderation factor

Normalization: α + β + γ + δ = 1
Output ψ(t) ≥ 0.8 indicates "Aligned" status.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class AlignmentScore:
    """Represents the alignment score of a construct.

    Attributes:
        truth: Logical coherence index (0.0-1.0)
        faith: Intuitive confidence score (0.0-1.0)
        justice: Lawful alignment measure (0.0-1.0)
        mercy: Ethical moderation factor (0.0-1.0)
        weights: Weight coefficients (α, β, γ, δ) that sum to 1.0
    """

    truth: float
    faith: float
    justice: float
    mercy: float
    weights: tuple[float, float, float, float] = (0.25, 0.25, 0.25, 0.25)

    def __post_init__(self):
        """Validate alignment score components."""
        if not (0.0 <= self.truth <= 1.0):
            raise ValueError(f"Truth must be in [0.0, 1.0], got {self.truth}")
        if not (0.0 <= self.faith <= 1.0):
            raise ValueError(f"Faith must be in [0.0, 1.0], got {self.faith}")
        if not (0.0 <= self.justice <= 1.0):
            raise ValueError(f"Justice must be in [0.0, 1.0], got {self.justice}")
        if not (0.0 <= self.mercy <= 1.0):
            raise ValueError(f"Mercy must be in [0.0, 1.0], got {self.mercy}")

        alpha, beta, gamma, delta = self.weights
        weight_sum = alpha + beta + gamma + delta
        if not abs(weight_sum - 1.0) < 1e-9:
            raise ValueError(
                f"Weights must sum to 1.0, got {weight_sum} "
                f"(α={alpha}, β={beta}, γ={gamma}, δ={delta})"
            )

    def compute(self) -> float:
        """Compute the resonant stability score ψ(t).

        Returns:
            Alignment score between 0.0 and 1.0
        """
        alpha, beta, gamma, delta = self.weights
        return (
            alpha * self.truth
            + beta * self.faith
            + gamma * self.justice
            + delta * self.mercy
        )

    def is_aligned(self, threshold: float = 0.8) -> bool:
        """Check if the construct meets alignment threshold.

        Args:
            threshold: Minimum score for alignment (default: 0.8)

        Returns:
            True if ψ(t) ≥ threshold
        """
        return self.compute() >= threshold


class MoralGravityField:
    """Applies constant pull toward Truth, Justice, and Mercy (Layer C).

    The Moral Gravity Field filters constructs based on their alignment with
    divine principles, ensuring only morally aligned logic proceeds to
    materialization.
    """

    def __init__(self, threshold: float = 0.8):
        """Initialize the Moral Gravity Field.

        Args:
            threshold: Minimum alignment score for acceptance (default: 0.8)
        """
        if not 0.0 <= threshold <= 1.0:
            raise ValueError(f"Threshold must be in [0.0, 1.0], got {threshold}")
        self.threshold = threshold

    def evaluate(self, construct: Dict) -> AlignmentScore:
        """Evaluate a construct's moral alignment.

        Args:
            construct: Structured logic construct to evaluate

        Returns:
            AlignmentScore with computed values for T, F, J, M

        Raises:
            KeyError: If required fields are missing
        """
        # Extract alignment metrics from construct
        truth = construct.get("truth", 0.5)
        faith = construct.get("faith", 0.5)
        justice = construct.get("justice", 0.5)
        mercy = construct.get("mercy", 0.5)

        # Allow custom weights if specified
        weights = construct.get("weights", (0.25, 0.25, 0.25, 0.25))

        return AlignmentScore(
            truth=truth, faith=faith, justice=justice, mercy=mercy, weights=weights
        )

    def filter(self, construct: Dict) -> bool:
        """Apply moral gravity filter to a construct.

        Args:
            construct: Structured logic to filter

        Returns:
            True if construct passes alignment threshold, False otherwise
        """
        score = self.evaluate(construct)
        return score.is_aligned(self.threshold)

    def apply(self, constructs: list[Dict]) -> list[Dict]:
        """Filter a list of constructs by moral alignment.

        Args:
            constructs: List of structured logic constructs

        Returns:
            List of constructs that pass the moral gravity filter
        """
        return [c for c in constructs if self.filter(c)]
