import traceback

from datasets import Dataset, load_dataset

from app.db import CACHE_PATH, DB_PATH, DatabaseHandler
from app.insights import data_insights
from app.logging_config import configure_logging

# Configure logging
logger = configure_logging()

# Global constant for dataset
DATASET_NAME = "alpindale/two-million-bluesky-posts"
DATASET_SPLIT = "train"  # Only 'train' split exists as of 2024-12-26


class ETL:
    """Extract, Transform, and Load pipeline."""

    def __init__(self, db_path: str = DB_PATH, cache_path: str = CACHE_PATH) -> None:
        """
        Initialize the ETL pipeline.

        Args:
            db_path (str): Path to the database file.
            cache_path (str): Path to the cache directory for the dataset.
        """
        self.db_handler = DatabaseHandler(db_path)
        self.cache_path = cache_path

    def extract(self) -> Dataset:
        """
        Extract data from Hugging Face dataset.

        Returns:
            Dataset: The loaded dataset.
        """
        try:
            logger.info(f"Fetching data from dataset '{DATASET_NAME}'...")
            ds = load_dataset(
                DATASET_NAME, split=DATASET_SPLIT, cache_dir=self.cache_path
            )
            logger.info("Data extraction completed.")
            return ds
        except Exception as e:
            logger.error(f"Failed to extract data: {e}")
            raise

    def transform(self, ds: Dataset) -> dict:
        """
        Transform data into insights.

        Args:
            ds (Dataset): The dataset to transform.

        Returns:
            dict: The transformed data.
        """
        try:
            logger.info("Transforming data into insights...")
            results = data_insights(ds)
            logger.info("Data transformation completed.")
            return results
        except Exception as e:
            logger.error(f"Failed to transform data: {e}")
            raise

    def load(self, insights: dict) -> None:
        """
        Load transformed insights into the database.

        Args:
            insights (dict): The insights to load.
        """
        try:
            logger.info("Loading insights into the database...")
            self.db_handler.upsert_insights(insights)
            logger.info("Data loading completed.")
        except Exception as e:
            logger.error(f"Failed to load data into the database: {e}")
            raise

    def has_new_version(self, version: str) -> bool:
        """
        Check if a new version of the dataset exists.

        Args:
            version (str): The version of the dataset to check.

        Returns:
            bool: True if a new version exists, False otherwise.
        """
        try:
            latest_version = self.db_handler.get_latest_insights_version()
            if not latest_version:
                logger.info("No previous data version found. Running pipeline.")
                return True
            if version > latest_version:
                logger.info(
                    f"New data version found ({version} > {latest_version}). Running pipeline."
                )
                return True
            logger.info("No new data version found.")
            return False
        except Exception as e:
            logger.error(f"Failed to check dataset version: {e}")
            raise


def main():
    """
    Main entry point for the ETL pipeline.
    """
    try:
        etl = ETL()
        raw_data = etl.extract()

        # Version check before running the pipeline
        if etl.has_new_version(raw_data.version):
            insights = etl.transform(raw_data)
            etl.load(insights)
            logger.info("ETL pipeline completed successfully.")
        else:
            logger.info("ETL pipeline skipped. No new version detected.")
    except Exception as e:
        logger.error(f"ETL pipeline failed: {traceback.format_exc()}")


if __name__ == "__main__":
    main()
