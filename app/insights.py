import json
from collections import Counter
from datetime import datetime
from typing import Dict

from datasets import Dataset


# Unique posts
def unique_posts(batch: Dataset) -> Dict:
    """Calculates unique posts."""
    unique_content = len(set(batch["text"]))
    return {"unique_posts": [unique_content] * len(batch["text"])}


# Average post length
def average_post_length(batch: Dataset) -> Dict:
    """Calculates average post length."""
    lengths = [len(post) for post in batch["text"]]
    avg_length = sum(lengths) / len(lengths)
    return {"average_post_length": [avg_length] * len(batch["text"])}


# Top Authors
def top_authors(batch: Dataset) -> Dict:
    """Calculates top authors."""
    authors = Counter(batch["author"])
    top_authors_list = authors.most_common(10)
    return {"top_authors": [json.dumps(top_authors_list)] * len(batch["text"])}


# Posting times
def hourly_distribution(batch: Dataset) -> Dict:
    """Calculates hourly distribution."""
    times = [datetime.fromisoformat(time).hour for time in batch["created_at"]]
    hourly_counts = Counter(times)
    return {
        "hourly_distribution": [json.dumps(dict(hourly_counts))] * len(batch["text"])
    }


# Hashtags
def top_hashtags(batch: Dataset) -> Dict:
    """Calculates top hashtags."""
    hashtags = Counter(
        [tag for post in batch["text"] for tag in post.split() if tag.startswith("#")]
    )
    top_hashtags_list = hashtags.most_common(10)
    return {"top_hashtags": [json.dumps(top_hashtags_list)] * len(batch["text"])}


insight_functions = [
    unique_posts,
    average_post_length,
    top_authors,
    hourly_distribution,
    top_hashtags,
]


def data_insights(ds: Dataset) -> Dict:
    """Parallel calculations."""
    insights = {}
    for func in insight_functions:
        result = ds.map(
            func, batched=True, batch_size=1000, num_proc=4
        )  # Adjust num_proc for parallelism
        # Extract relevant columns added by the function
        for column in result.column_names:
            if (
                column not in ds.column_names
            ):  # Identify new columns added by the function
                insights[column] = result[column][
                    0
                ]  # Extract the first value or summary
    insights["version"] = ds.info.version
    return insights
