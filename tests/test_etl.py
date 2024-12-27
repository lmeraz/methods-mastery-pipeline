from unittest.mock import MagicMock, patch

import pytest
from datasets import Dataset

from app.db import DatabaseHandler
from app.etl import DATASET_NAME, DATASET_SPLIT, ETL


@pytest.fixture
def mock_db_handler():
    """
    Fixture to provide a mock DatabaseHandler.
    """
    mock_handler = MagicMock(spec=DatabaseHandler)
    mock_handler.get_latest_insights_version.return_value = "1.0"
    return mock_handler


@pytest.fixture
def etl_instance(mock_db_handler):
    """
    Fixture to provide an ETL instance with a mocked DatabaseHandler.
    """
    with patch("app.etl.DatabaseHandler", return_value=mock_db_handler):
        etl = ETL()
        yield etl


@pytest.fixture
def mock_dataset():
    """
    Fixture to provide a mock Hugging Face Dataset.
    """
    data = {
        "text": ["post1", "post2", "post3"],
        "created_at": [
            "2024-12-26T12:00:00",
            "2024-12-26T13:00:00",
            "2024-12-26T14:00:00",
        ],
    }
    return Dataset.from_dict(data)


@patch("app.etl.load_dataset")
def test_extract(mock_load_dataset, etl_instance, mock_dataset):
    """
    Test the extract method.
    """
    mock_load_dataset.return_value = mock_dataset

    dataset = etl_instance.extract()
    mock_load_dataset.assert_called_once_with(
        DATASET_NAME, split=DATASET_SPLIT, cache_dir=etl_instance.cache_path
    )
    assert isinstance(
        dataset, Dataset
    ), "The extracted data should be a Dataset instance."


@patch("app.etl.data_insights")
def test_transform(mock_data_insights, etl_instance, mock_dataset):
    """
    Test the transform method.
    """
    mock_data_insights.return_value = {"unique_posts": 3}

    insights = etl_instance.transform(mock_dataset)
    mock_data_insights.assert_called_once_with(mock_dataset)
    assert insights == {
        "unique_posts": 3
    }, "The transform method should return the expected insights."


def test_load(etl_instance, mock_db_handler):
    """
    Test the load method.
    """
    insights = {"unique_posts": 3}
    etl_instance.load(insights)

    mock_db_handler.upsert_insights.assert_called_once_with(insights)


def test_has_new_version_no_previous(etl_instance, mock_db_handler):
    """
    Test has_new_version when there is no previous version.
    """
    mock_db_handler.get_latest_insights_version.return_value = None

    assert (
        etl_instance.has_new_version("1.0") is True
    ), "Should return True when no previous version exists."


def test_has_new_version_newer_version(etl_instance, mock_db_handler):
    """
    Test has_new_version when a newer version is available.
    """
    mock_db_handler.get_latest_insights_version.return_value = "1.0"

    assert (
        etl_instance.has_new_version("2.0") is True
    ), "Should return True for a newer version."


def test_has_new_version_no_new_version(etl_instance, mock_db_handler):
    """
    Test has_new_version when no new version is available.
    """
    mock_db_handler.get_latest_insights_version.return_value = "2.0"

    assert (
        etl_instance.has_new_version("1.0") is False
    ), "Should return False when no new version is available."
