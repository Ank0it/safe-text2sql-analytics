from app.validator import validate_sql


def test_select():
    safe, _ = validate_sql("SELECT * FROM customers;")
    assert safe


def test_delete():
    safe, _ = validate_sql("DELETE FROM customers;")
    assert not safe


def test_drop():
    safe, _ = validate_sql("DROP TABLE customers;")
    assert not safe


def test_update():
    safe, _ = validate_sql("UPDATE customers SET name='abc';")
    assert not safe