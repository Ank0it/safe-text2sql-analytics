import sqlite3
from pathlib import Path
from typing import Dict, List

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database files
DB_PATH = BASE_DIR / "database" / "business.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"
SEED_PATH = BASE_DIR / "database" / "seed.sql"


def get_connection() -> sqlite3.Connection:
    """
    Returns a SQLite connection with rows accessible as dictionaries.
    """

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


def initialize_database(force_reset: bool = False) -> None:
    """
    Initializes the SQLite database.

    Parameters
    ----------
    force_reset : bool
        If True, recreate the database using schema.sql and seed.sql.
        If False, initialize only when the database does not already exist.
    """

    if DB_PATH.exists() and not force_reset:
        return

    conn = get_connection()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
        conn.executescript(schema_file.read())

    with open(SEED_PATH, "r", encoding="utf-8") as seed_file:
        conn.executescript(seed_file.read())

    conn.commit()
    conn.close()


def execute_query(sql: str):
    """
    Executes a validated SELECT query.

    Returns
    -------
    tuple[list[str], list[dict]]
        columns, rows
    """

    conn = get_connection()

    cursor = conn.execute(sql)

    columns = [column[0] for column in cursor.description]

    rows = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return columns, rows


def get_schema() -> Dict[str, List[str]]:
    """
    Returns all tables and their columns.

    Example
    -------
    {
        "customers": [
            "customer_id",
            "name",
            "email"
        ],
        "orders": [
            ...
        ]
    }
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """)

    schema = {}

    for (table_name,) in cursor.fetchall():

        cursor.execute(f"PRAGMA table_info({table_name})")

        schema[table_name] = [
            row[1]
            for row in cursor.fetchall()
        ]

    conn.close()

    return schema


def get_relationships() -> List[str]:
    """
    Reads all foreign-key relationships from SQLite.

    Example
    -------
    [
        "orders.customer_id -> customers.customer_id",
        "payments.order_id -> orders.order_id"
    ]
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """)

    tables = [row[0] for row in cursor.fetchall()]

    relationships = []

    for table in tables:

        cursor.execute(f"PRAGMA foreign_key_list({table})")

        foreign_keys = cursor.fetchall()

        for fk in foreign_keys:

            parent_table = fk[2]
            child_column = fk[3]
            parent_column = fk[4]

            relationships.append(
                f"{table}.{child_column} -> {parent_table}.{parent_column}"
            )

    conn.close()

    return relationships