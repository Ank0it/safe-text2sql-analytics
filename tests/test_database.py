from app.database import execute_query


def test_simple_query():

    rows = execute_query("SELECT 1 AS value;")

    assert isinstance(rows, list)