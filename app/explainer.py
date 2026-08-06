"""
Generates human-readable explanations and confidence scores
for Text2SQL responses.
"""

from app.models import Confidence


def build_explanation(
    *,
    executed: bool,
    validation_reason: str,
    row_count: int = 0,
) -> str:
    """
    Generate a user-friendly explanation describing
    what happened with the request.
    """

    if not executed:
        return (
            "The generated SQL was blocked because it failed "
            "safety validation and was not executed."
        )

    if row_count == 0:
        return (
            "The SQL query passed validation and executed "
            "successfully, but no matching records were found."
        )

    if row_count == 1:
        return (
            "The SQL query passed validation and executed "
            "successfully. One record was returned."
        )

    return (
        f"The SQL query passed validation and executed "
        f"successfully. {row_count} records were returned."
    )


def build_confidence(
    *,
    executed: bool,
    validation_passed: bool,
    row_count: int = 0,
) -> Confidence:
    """
    Build a confidence object for the API response.
    """

    notes = []

    if validation_passed:
        notes.append("SQL passed validation.")
    else:
        notes.append("SQL failed validation.")

    if executed:
        notes.append("The query executed successfully.")
    else:
        notes.append("The query was not executed.")

    if executed:
        if row_count == 0:
            notes.append("No matching rows were found.")
        else:
            notes.append(f"{row_count} row(s) returned.")

    if not validation_passed:
        return Confidence(
            level="Low",
            notes=notes,
        )

    if row_count == 0:
        return Confidence(
            level="Medium",
            notes=notes,
        )

    return Confidence(
        level="High",
        notes=notes,
    )