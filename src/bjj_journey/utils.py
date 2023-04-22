"""bjj_journey.logging_utils - General utilties.

"""
import logging
import os

from dotenv import load_dotenv


LEVELS = [logging.WARNING, logging.INFO, logging.DEBUG]


def set_up_logging(verbosity: int) -> None:
    """
    Set up root logger by:
        - establishing a log format
        - adding a handler
        - setting the log level
    """
    # Add handler with formatter
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "{asctime} [{levelname}] {name} - {message}", style="{"
    )
    handler.setFormatter(formatter)

    # Add handler to root logger
    logger = logging.getLogger()
    logger.addHandler(handler)

    # Determine log level  for root logger
    level = LEVELS[min(verbosity, len(LEVELS) - 1)]
    logger.setLevel(level)


def load_dotenv_file():
    """Load a .env file based on tier."""
    tier = os.environ.get("TIER", "dev")
    load_dotenv(f"secrets.{tier}.env")
