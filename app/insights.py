import json
from collections import Counter
from datetime import datetime
from typing import Dict

from datasets import Dataset

BATCH_SIZE = 1000
NUM_PROC = 4


# Unique posts
def unique_posts(ds: Dataset) -> Dict:
    """Calculates unique posts."""
    partial_results = ds.map(
        lambda x: {"unique_posts": [set(x["text"])]},
        batched=True,
        batch_size=BATCH_SIZE,
        num_proc=NUM_PROC,
    )
    result = set()
    for s in partial_results["unique_posts"]:
        result.update(s)
    count = len(result)
    return count


# Average post length
def average_post_length(ds: Dataset) -> Dict:
    """Calculates average post length."""
    partial_results = ds.map(
        lambda batch: {
            "partial_sum": [
                sum(len(post) for post in batch["text"])
            ],  # Sum of lengths in the batch
            "partial_count": [len(batch["text"])],  # Number of posts in the batch
        },
        batched=True,
        batch_size=BATCH_SIZE,
        num_proc=NUM_PROC,
    )
    total_sum = sum(partial_results["partial_sum"])
    total_count = sum(partial_results["partial_count"])
    average_post_length = total_sum / total_count if total_count > 0 else 0
    return average_post_length


# Top Authors
def top_authors(ds: Dict) -> Dict:
    """Calculates top authors."""
    unique_authors = set(ds["author"])
    partial_results = ds.map(
        lambda batch: {
            "partial_author_counts": [
                {author: batch["author"].count(author) for author in unique_authors}
            ]
        },
        batched=True,
        batch_size=BATCH_SIZE,
        num_proc=NUM_PROC,
    )
    result = Counter()
    for batch_count in partial_results["partial_author_counts"]:
        result.update(dict(batch_count))
    top_authors = result.most_common(10)
    return top_authors


# Posting times
def hourly_distribution(ds: Dict) -> Dict:
    """Calculates hourly distribution."""
    times = [datetime.fromisoformat(time).hour for time in ds["created_at"]]
    hourly_counts = dict(Counter(times))
    return hourly_counts


# Hashtags
def top_hashtags(batch: Dataset) -> Dict:
    """Calculates top hashtags."""
    hashtags = Counter(
        [tag for post in batch["text"] for tag in post.split() if tag.startswith("#")]
    )
    top_hashtags_list = hashtags.most_common(10)
    return top_hashtags_list


def data_insights(ds: Dataset) -> Dict:
    insights = {}
    insights["version"] = ds.info.version
    insights["top_hashtags"] = top_hashtags(ds)
    insights["hourly_distribution"] = hourly_distribution(ds)
    insights["top_authors"] = top_authors(ds)
    insights["average_post_length"] = average_post_length(ds)
    insights["unique_posts"] = unique_posts(ds)
    return insights


## TODO:
# unique_authors_ct
# total_posts_num
# avg_posting_time
# posts_with_images_ct
# unique_hashtags_ct
# peak_posting
# top_posting_date
