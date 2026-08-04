from typing import Any, Dict, List

from pydantic import BaseModel, Field


class AskDataRequest(BaseModel):
    """
    Request model for the /ask-data endpoint.
    """
    question: str = Field(
        ...,
        min_length=1,
        description="Natural language analytics question."
    )


class ValidationStatus(BaseModel):
    """
    SQL validation result.
    """
    safe: bool
    reason: str


class ConfidenceNotes(BaseModel):
    """
    Confidence assessment for the generated SQL.
    """
    level: str
    notes: List[str]


class AskDataResponse(BaseModel):
    """
    Response returned by the /ask-data endpoint.
    """
    question: str

    generated_sql: str

    validation: ValidationStatus

    result_table: List[Dict[str, Any]]

    explanation: str

    confidence: ConfidenceNotes