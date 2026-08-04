import sqlite3
from pathlib import Path

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


def initialize_database() -> None:
    """
    Creates the database from schema.sql and inserts seed data.
    Safe to run multiple times because schema.sql drops existing tables.
    """
    conn = get_connection()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    with open(SEED_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()


def execute_query(sql: str):
    """
    Executes a validated SELECT query.

    Returns:
        columns (list[str])
        rows (list[dict])
    """
    conn = get_connection()

    cursor = conn.execute(sql)

    columns = [description[0] for description in cursor.description]

    rows = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return columns, rows


def get_schema():
    """
    Returns database schema metadata.

    Used to verify that generated SQL references only
    existing tables and columns.
    """
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
    """)

    tables = {}

    for (table_name,) in cursor.fetchall():

        cursor.execute(f"PRAGMA table_info({table_name})")

        columns = [
            row[1]
            for row in cursor.fetchall()
        ]

        tables[table_name] = columns

    conn.close()

    return tables