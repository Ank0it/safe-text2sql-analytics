"""
API routes for Safe Text2SQL Analytics.
"""

from fastapi import APIRouter, HTTPException

from app.database import execute_query
from app.explainer import build_confidence, build_explanation
from app.llm import generate_sql
from app.models import (
    ErrorResponse,
    QueryRequest,
    QueryResponse,
    ValidationResult,
)
from app.validator import validate_sql

router = APIRouter(
    prefix="",
    tags=["Analytics"],
)


@router.post(
    "/query",
    response_model=QueryResponse,
    responses={
        500: {
            "model": ErrorResponse,
            "description": "Internal server error",
        }
    },
)
def query_database(request: QueryRequest):
    """
    Converts a natural-language question into SQL,
    validates it, executes it safely,
    and returns structured results.
    """

    question = request.question.strip()

    generated_sql = generate_sql(question)

    is_safe, reason = validate_sql(generated_sql)

    validation = ValidationResult(
        safe=is_safe,
        reason=reason,
    )

    # SQL blocked
    if not is_safe:

        explanation = build_explanation(
            executed=False,
            validation_reason=reason,
        )

        confidence = build_confidence(
            executed=False,
            validation_passed=False,
        )

        return QueryResponse(
            question=question,
            generated_sql=generated_sql,
            validation=validation,
            result_table=[],
            explanation=explanation,
            confidence=confidence,
        )

    try:

        columns, rows = execute_query(generated_sql)

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Database execution failed: {exc}",
        )

    explanation = build_explanation(
        executed=True,
        validation_reason=reason,
        row_count=len(rows),
    )

    confidence = build_confidence(
        executed=True,
        validation_passed=True,
        row_count=len(rows),
    )

    return QueryResponse(
        question=question,
        generated_sql=generated_sql,
        validation=validation,
        result_table=rows,
        explanation=explanation,
        confidence=confidence,
    )