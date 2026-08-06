from fastapi import APIRouter

from app.executor import run_query
from app.explanation import generate_confidence, generate_explanation
from app.llm import generate_sql
from app.schema import (
    AskDataRequest,
    AskDataResponse,
    ValidationStatus,
)
from app.validator import validate_sql

router = APIRouter()


@router.post(
    "/ask-data",
    response_model=AskDataResponse,
    tags=["Analytics"],
)
def ask_data(request: AskDataRequest):
    """
    Convert a natural-language analytics question into SQL,
    validate it, execute it safely, and return the results.
    """

    question = request.question.strip()

    generated_sql = generate_sql(question)

    is_safe, validation_reason = validate_sql(generated_sql)

    result_table = []

    if is_safe:
        result_table, execution_error = run_query(generated_sql)

        if execution_error:
            is_safe = False
            validation_reason = f"Execution failed: {execution_error}"

    explanation = generate_explanation(
        question=question,
        sql=generated_sql,
        result_table=result_table,
        validation_passed=is_safe,
    )

    confidence = generate_confidence(
        sql=generated_sql,
        validation_passed=is_safe,
        validation_reason=validation_reason,
        result_table=result_table,
    )

    return AskDataResponse(
        question=question,
        generated_sql=generated_sql,
        validation=ValidationStatus(
            safe=is_safe,
            reason=validation_reason,
        ),
        result_table=result_table,
        explanation=explanation,
        confidence=confidence,
    )