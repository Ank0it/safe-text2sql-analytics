from typing import Any

from app.database import execute_query


def run_query(sql: str) -> tuple[list[dict[str, Any]], str]:
    """
    Executes a validated SQL query.

    Returns:
        result_table: Query results as a list of dictionaries.
        error: Empty string if successful, otherwise the error message.
    """

    try:
        _, rows = execute_query(sql)
        return rows, ""

    except Exception as e:
        return [], str(e)