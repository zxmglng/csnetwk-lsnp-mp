import logging
from models import logger_config  # We'll create this in handlers

def run(args: list[str]):
    """
    Command to set up logging.
    Usage: setup_logging [level]
    Example: setup_logging DEBUG
    """
    if args:
        level_str = args[0].upper()
        level = getattr(logging, level_str, logging.DEBUG)
    else:
        level = logging.DEBUG

    logger = logger_config.setup_logging(level)
    logger.info(f"Logging initialized at level: {logging.getLevelName(level)}")