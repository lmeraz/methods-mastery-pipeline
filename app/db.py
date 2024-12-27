import logging
from pathlib import Path
from typing import Union, Dict
import sqlite3
from app.logging_config import configure_logging

# Configure logging
logger = configure_logging()

# Constants
BASE_DIR = Path(__file__).resolve().parent
DATA_FOLDER = BASE_DIR.parent / "data"
DB_NAME = "pipeline.db"
DB_PATH = DATA_FOLDER / DB_NAME
CACHE_PATH = DATA_FOLDER

# Ensure the data folder exists
DATA_FOLDER.mkdir(parents=True, exist_ok=True)


class DatabaseHandler:
    """Handles database operations."""

    def __init__(self, db_path: Union[str, Path] = DB_PATH):
        """
        Initialize the DatabaseHandler.

        Args:
            db_path (Union[str, Path]): Path to the SQLite database file.
        """
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        logger.info(f"Connected to database at {self.db_path}.")
        self._create_tables()

    def _create_tables(self):
        """Create required tables if they don't exist."""
        create_table_queries = [
            """
            CREATE TABLE IF NOT EXISTS insights (
                metric TEXT PRIMARY KEY,
                value TEXT
            );
            """
        ]
        try:
            with self.conn:
                for query in create_table_queries:
                    self.conn.execute(query)
            logger.info("Database tables initialized.")
        except sqlite3.DatabaseError as e:
            logger.error(f"Error initializing tables: {e}")
            raise

    def upsert_insights(self, insights: Dict[str, str]) -> None:
        """
        Insert or update insights data in the database.

        Args:
            insights (Dict[str, str]): Dictionary containing insights to insert or update.
        """
        query = """
        INSERT INTO insights (metric, value)
        VALUES (?, ?)
        ON CONFLICT(metric) DO UPDATE SET value = excluded.value;
        """
        try:
            with self.conn:
                for metric, value in insights.items():
                    logger.debug(f"Upserting metric '{metric}' with value '{value}'.")
                    self.conn.execute(query, (metric, str(value)))
            logger.info(f"{len(insights)} insights upserted successfully.")
        except sqlite3.DatabaseError as e:
            logger.error(f"Failed to upsert insights: {e}")
            raise

    def get_latest_insights_version(self) -> Union[str, None]:
        """
        Retrieve the latest insights version from the database.

        Returns:
            Union[str, None]: The latest version string, or None if not found.
        """
        query = "SELECT value FROM insights WHERE metric = 'version';"
        try:
            with self.conn:
                result = self.conn.execute(query).fetchone()
                if result:
                    logger.info(f"Latest version retrieved: {result[0]}")
                    return result[0]
                logger.info("No version found in database.")
                return None
        except sqlite3.DatabaseError as e:
            logger.error(f"Failed to retrieve the latest insights version: {e}")
            raise


# Example usage
if __name__ == "__main__":
    try:
        with DatabaseHandler(DB_PATH) as db_handler:
            version = db_handler.get_latest_insights_version()
            logger.info(f"Database version: {version}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")