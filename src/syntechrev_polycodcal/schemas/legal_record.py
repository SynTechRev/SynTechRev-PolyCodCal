"""Legal record schema for case data."""

from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class LegalRecord(BaseModel):
    """Schema for a legal case record.

    Attributes:
        case_name: Official name of the case (e.g., "Brown v. Board of Education")
        year: Year the case was decided
        citation: Legal citation (e.g., "347 U.S. 483")
        court: Court that decided the case (e.g., "U.S. Supreme Court")
        jurisdiction: Legal jurisdiction (e.g., "Federal")
        doctrine: Legal doctrine or area (e.g., "Civil Rights", "Constitutional Law")
        summary: Brief summary of the case
        holding: The court's decision or holding
        significance: Why this case is important
        keywords: Optional list of relevant keywords
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "case_name": "Brown v. Board of Education",
                "year": 1954,
                "citation": "347 U.S. 483",
                "court": "U.S. Supreme Court",
                "jurisdiction": "Federal",
                "doctrine": "Civil Rights",
                "summary": "Challenged racial segregation in public schools",
                "holding": "Separate educational facilities are inherently unequal",
                "significance": "Landmark decision ending legal segregation",
                "keywords": ["segregation", "equal protection", "education"],
            }
        }
    )

    case_name: str = Field(..., description="Official name of the case")
    year: int = Field(..., description="Year the case was decided")
    citation: str = Field(..., description="Legal citation")
    court: str = Field(..., description="Court that decided the case")
    jurisdiction: str = Field(..., description="Legal jurisdiction")
    doctrine: str = Field(..., description="Legal doctrine or area")
    summary: str = Field(..., description="Brief summary of the case")
    holding: str = Field(..., description="The court's decision or holding")
    significance: str = Field(..., description="Why this case is important")
    keywords: Optional[List[str]] = Field(default=None, description="Relevant keywords")
