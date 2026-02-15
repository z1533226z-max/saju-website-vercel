"""
Serverless-compatible logging for Saju Backend
Uses StreamHandler only (Vercel has no persistent filesystem)
"""

import logging
import os
import sys


def setup_logging():
    """Setup serverless-compatible logging (stdout only)"""
    log_level = os.getenv('LOG_LEVEL', 'INFO')

    logger = logging.getLogger('saju')
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Only add handler if none exist (prevent duplicates on warm starts)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, log_level, logging.INFO))
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s %(module)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# Create default logger instance
logger = setup_logging()


def debug(msg, *args, **kwargs):
    logger.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    logger.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    logger.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    logger.error(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    logger.critical(msg, *args, **kwargs)
