from typing import Any, Dict, List

from app.schema import ConfidenceNotes


def generate_explanation(
    question: str,
    sql: str,
    result_table: List[Dict[str, Any]],
    validation_passed: bool,
) -> str:
    """
    Generate a simple plain-English explanation of the query result.
    """

    if not validation_passed:
        return (
            "The generated SQL was blocked because it failed safety validation "
            "and was not executed."
        )

    if not result_table:
        return (
            "The SQL query executed successfully, but no matching records were found."
        )

    row_count = len(result_table)

    return (
        f"The question was translated into a SQL query and executed successfully. "
        f"The query returned {row_count} record(s)."
    )


def generate_confidence(
    sql: str,
    validation_passed: bool,
    validation_reason: str,
    result_table: List[Dict[str, Any]],
) -> ConfidenceNotes:
    """
    Generate confidence notes for the API response.
    """

    notes: List[str] = []

    if validation_passed:
        level = "High"

        notes.append("SQL passed all safety validation checks.")
        notes.append("Only a read-only SELECT query was executed.")

        if result_table:
            notes.append("The query returned data successfully.")
        else:
            notes.append("The query executed successfully but returned no rows.")

    else:
        level = "Low"

        notes.append("SQL failed validation.")
        notes.append(validation_reason)
        notes.append("The query was not executed.")

    return ConfidenceNotes(
        level=level,
        notes=notes,
    )