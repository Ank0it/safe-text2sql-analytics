"""
Pydantic models for the Safe Text2SQL Analytics API.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ConfidenceLevel(str, Enum):
    """
    Confidence levels for generated SQL.
    """

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class QueryRequest(BaseModel):
    """
    Incoming natural-language analytics request.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question": "Show the top 5 customers by total spending."
            }
        }
    )

    question: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Natural-language analytics question.",
    )

    @field_validator("question")
    @classmethod
    def strip_question(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Question cannot be empty.")

        return value


class ValidationResult(BaseModel):
    """
    SQL validation outcome.
    """

    safe: bool = Field(
        ...,
        description="Whether the SQL passed safety validation.",
    )

    reason: str = Field(
        ...,
        description="Reason returned by the SQL validator.",
    )


class Confidence(BaseModel):
    """
    Confidence information about the generated response.
    """

    level: ConfidenceLevel = Field(
        ...,
        description="Overall confidence level.",
    )

    notes: list[str] = Field(
        default_factory=list,
        description="Factors affecting confidence.",
    )


class QueryResponse(BaseModel):
    """
    Successful API response.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question": "Show total revenue.",
                "generated_sql": "SELECT SUM(amount) FROM payments;",
                "validation": {
                    "safe": True,
                    "reason": "Validation passed.",
                },
                "result_table": [
                    {
                        "total_revenue": 15432.80
                    }
                ],
                "row_count": 1,
                "execution_time_ms": 18.74,
                "explanation": "Calculated the total revenue from the payments table.",
                "confidence": {
                    "level": "High",
                    "notes": [
                        "Query validated successfully.",
                        "Schema matched exactly."
                    ]
                },
            }
        }
    )

    question: str = Field(
        ...,
        description="Original user question.",
    )

    generated_sql: str = Field(
        ...,
        description="Generated SQL query.",
    )

    validation: ValidationResult

    result_table: list[dict[str, Any]]

    row_count: int = Field(
        ...,
        ge=0,
        description="Number of rows returned.",
    )

    execution_time_ms: float = Field(
        ...,
        ge=0,
        description="End-to-end processing time.",
    )

    explanation: str = Field(
        ...,
        description="Human-readable explanation of the query.",
    )

    confidence: Confidence


class ErrorResponse(BaseModel):
    """
    Standard API error response.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": "ValidationError",
                "detail": "Only SELECT statements are allowed.",
            }
        }
    )

    error: str

    detail: str


class HealthResponse(BaseModel):
    """
    Health check response.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "database": "connected",
                "llm": "available",
            }
        }
    )

    status: str

    database: str

    llm: str