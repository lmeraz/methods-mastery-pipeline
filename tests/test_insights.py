from collections import Counter
from datetime import datetime

import pytest
from datasets import Dataset

from app.insights import (
    average_post_length,
    data_insights,
    hourly_distribution,
    top_authors,
    top_hashtags,
    unique_posts,
)


@pytest.fixture
def mock_dataset():
    """Create a mock dataset."""
    data = {
        "text": [
            "Hello world! #test",
            "Another post without hashtags",
            "Hello world! #test",
            "Unique post here #unique",
        ],
        "created_at": [
            "2024-12-26T10:00:00",
            "2024-12-26T11:00:00",
            "2024-12-26T10:30:00",
            "2024-12-26T12:00:00",
        ],
        "author": ["Alice", "Bob", "Alice", "Charlie"],
        "uri": [
            "uri1",
            "uri2",
            "uri3",
            "uri4",
        ],
        "has_images": [True, True, False, False],
        "reply_to": [
            "uri5",
            "uri5",
            "uri5",
            "uri5",
        ],
    }
    return Dataset.from_dict(data)


def test_unique_posts(mock_dataset):
    """Test unique_posts function."""
    result = unique_posts(mock_dataset)
    expected_result = 3
    assert result == expected_result  # "Hello world!" appears twice


def test_average_post_length(mock_dataset):
    """Test average_post_length function."""
    result = average_post_length(mock_dataset)
    expected_avg = sum(len(post) for post in mock_dataset["text"]) / len(
        mock_dataset["text"]
    )
    assert result == expected_avg


def test_top_authors(mock_dataset):
    """Test top_authors function."""
    result = top_authors(mock_dataset)
    expected_authors = Counter(mock_dataset["author"]).most_common(10)
    assert result == expected_authors


def test_hourly_distribution(mock_dataset):
    """Test hourly_distribution function."""
    # Apply the function using Dataset.map
    result = hourly_distribution(mock_dataset)
    hours = [datetime.fromisoformat(time).hour for time in mock_dataset["created_at"]]
    expected_counts = dict(Counter(hours))
    assert result == expected_counts


def test_top_hashtags(mock_dataset):
    """Test top_hashtags function."""
    # Run the top_hashtags function
    result = top_hashtags(mock_dataset)
    hashtags = Counter(
        [
            tag
            for post in mock_dataset["text"]
            for tag in post.split()
            if tag.startswith("#")
        ]
    ).most_common(10)
    assert result == hashtags


def test_data_insights(mock_dataset):
    """Test data_insights function."""
    result = data_insights(mock_dataset)
    assert "version" in result  # Ensure version metadata is included
    assert "unique_posts" in result
    assert "average_post_length" in result
    assert "top_authors" in result
    assert "hourly_distribution" in result
    assert "top_hashtags" in result
