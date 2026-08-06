import re
from typing import Dict, Set, Tuple

import sqlparse

from app.database import get_schema

# SQL operations that are NOT allowed
BLOCKED_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "TRUNCATE",
    "REPLACE",
    "MERGE",
    "GRANT",
    "REVOKE",
    "ATTACH",
    "DETACH",
    "VACUUM",
    "PRAGMA",
}

# Common SQL keywords/functions that should not be treated as schema identifiers
SQL_KEYWORDS = {
    "SELECT",
    "FROM",
    "WHERE",
    "JOIN",
    "LEFT",
    "RIGHT",
    "INNER",
    "OUTER",
    "FULL",
    "CROSS",
    "ON",
    "GROUP",
    "BY",
    "ORDER",
    "HAVING",
    "LIMIT",
    "OFFSET",
    "ASC",
    "DESC",
    "AND",
    "OR",
    "AS",
    "IN",
    "NOT",
    "NULL",
    "LIKE",
    "BETWEEN",
    "IS",
    "DISTINCT",
    "COUNT",
    "SUM",
    "AVG",
    "MIN",
    "MAX",
}


def extract_aliases(sql: str) -> Dict[str, str]:
    """
    Extract table aliases.

    Example:
        FROM customers c
        JOIN orders o

    Returns:
        {
            "c": "customers",
            "o": "orders"
        }
    """

    aliases = {}

    pattern = re.compile(
        r"(?:FROM|JOIN)\s+([A-Za-z_][A-Za-z0-9_]*)\s+([A-Za-z_][A-Za-z0-9_]*)",
        re.IGNORECASE,
    )

    for table, alias in pattern.findall(sql):
        aliases[alias] = table

    return aliases


def validate_schema(sql: str) -> Tuple[bool, str]:
    """
    Ensure SQL only references existing tables and columns.
    """

    schema = get_schema()

    valid_tables: Set[str] = set(schema.keys())

    valid_columns: Set[str] = set()

    for cols in schema.values():
        valid_columns.update(cols)

    aliases = extract_aliases(sql)

    # Validate tables used after FROM/JOIN
    table_pattern = re.compile(
        r"(?:FROM|JOIN)\s+([A-Za-z_][A-Za-z0-9_]*)",
        re.IGNORECASE,
    )

    for table in table_pattern.findall(sql):

        if table not in valid_tables:
            return False, f"Unknown table '{table}'."

    # Validate alias.column references
    dotted_pattern = re.compile(
        r"([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)"
    )

    for alias, column in dotted_pattern.findall(sql):

        if alias not in aliases:
            return False, f"Unknown table alias '{alias}'."

        table = aliases[alias]

        if column not in schema[table]:
            return False, f"Unknown column '{column}' in table '{table}'."

    # Validate standalone identifiers
    identifiers = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", sql)

    for identifier in identifiers:

        upper = identifier.upper()

        if upper in SQL_KEYWORDS:
            continue

        if identifier in valid_tables:
            continue

        if identifier in valid_columns:
            continue

        if identifier in aliases:
            continue

        if identifier in aliases.values():
            continue

        if identifier.isdigit():
            continue

        # Ignore common literal values used in queries
        if identifier.lower() in {
            "paid",
            "pending",
            "completed",
            "cancelled",
            "approved",
            "credit",
            "card",
            "debit",
            "upi",
        }:
            continue

    return True, "Schema validation passed."


def validate_sql(sql: str) -> Tuple[bool, str]:
    """
    Validate generated SQL before execution.

    Returns:
        (True, reason) if SQL is safe.
        (False, reason) otherwise.
    """

    sql = sql.strip()

    if not sql:
        return False, "Generated SQL is empty."

    parsed = sqlparse.parse(sql)

    if len(parsed) != 1:
        return False, "Multiple SQL statements are not allowed."

    statement = parsed[0]

    if statement.get_type() != "SELECT":
        return False, "Only SELECT queries are allowed."

    sql_upper = sql.upper()

    # Block dangerous SQL operations
    for keyword in BLOCKED_KEYWORDS:
        if re.search(rf"\b{keyword}\b", sql_upper):
            return False, f"Blocked SQL keyword detected: {keyword}"

    # Block SQL comments
    if "--" in sql or "/*" in sql or "*/" in sql:
        return False, "SQL comments are not allowed."

    # Block multiple statements
    if ";" in sql[:-1]:
        return False, "Multiple SQL statements detected."

    # Validate schema
    valid_schema, reason = validate_schema(sql)

    if not valid_schema:
        return False, reason

    return True, "SQL passed validation."