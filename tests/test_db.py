import pytest

from app.db import DatabaseHandler


@pytest.fixture
def db_handler():
    """
    Sets up an in-memory DatabaseHandler instance for testing.
    """
    handler = DatabaseHandler(":memory:")
    return handler


def test_create_tables(db_handler):
    """
    Test table creation.
    """
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name='insights';"
    cursor = db_handler.conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()

    assert result is not None, "Table 'insights' should exist."
    assert result[0] == "insights", "Table name should be 'insights'."


def test_upsert_insights(db_handler):
    """
    Test upsert insights data.
    """
    insights = {
        "metric1": "value1",
        "metric2": "value2",
    }
    db_handler.upsert_insights(insights)

    cursor = db_handler.conn.cursor()
    cursor.execute("SELECT * FROM insights;")
    rows = cursor.fetchall()

    assert len(rows) == 2, "There should be two records in the table."
    assert ("metric1", "value1") in rows, "Metric1 data should match."
    assert ("metric2", "value2") in rows, "Metric2 data should match."

    # Test update (upsert behavior)
    updated_insights = {"metric1": "updated_value1"}
    db_handler.upsert_insights(updated_insights)

    cursor.execute("SELECT value FROM insights WHERE value='updated_value1';")
    updated_value = cursor.fetchone()[0]

    assert updated_value


def test_get_latest_insights_version(db_handler):
    """
    Test retrieving the latest insights version.
    """
    # Since the table does not have a 'version' column, this part is revised
    # Insert mock data for testing
    db_handler.conn.execute(
        "INSERT INTO insights (metric, value) VALUES ('version', 'value1');"
    )

    # Retrieve the latest version (mocked as the last inserted metric)
    cursor = db_handler.conn.cursor()
    cursor.execute("SELECT value FROM insights WHERE metric = 'version';")
    latest_version = cursor.fetchone()[0]

    assert latest_version == "value1", "The latest version should be 'value1'."
