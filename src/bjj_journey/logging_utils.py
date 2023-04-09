"""bjj_journey.logging_utils

Utilities for logging.
"""
import logging


LEVELS = [logging.WARNING, logging.INFO, logging.DEBUG]


def set_up_logging(verbosity: int) -> None:
    """
    Set up root logger by:
        - establishing a log format
        - adding a handler
        - setting the log level
    """
    # add handler with formatter
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "{asctime} [{levelname}] {name} - {message}", style="{"
    )
    handler.setFormatter(formatter)

    # add handler to root logger
    logger = logging.getLogger()
    logger.addHandler(handler)

    # determine log level  for root logger
    level = LEVELS[min(verbosity, len(LEVELS) - 1)]
    logger.setLevel(level)
