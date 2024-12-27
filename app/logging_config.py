import logging
from typing import Optional


def configure_logging(
    name: Optional[str] = None,
    level: int = logging.INFO,
    format: str = "%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]",
) -> logging.Logger:
    """
    Configures the logging setup with line numbers and returns a logger.

    Args:
        name (Optional[str]): Name of the logger. Defaults to the root logger if None.
        level (int): Logging level. Defaults to logging.INFO.
        format (str): Log message format. Defaults to include timestamp, level, message, file, and line number.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:  # Prevent duplicate handlers
        handler = logging.StreamHandler()
        handler.setLevel(level)

        formatter = logging.Formatter(format)
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    logger.setLevel(level)
    return logger
