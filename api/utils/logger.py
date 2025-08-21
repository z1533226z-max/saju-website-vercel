"""
Centralized logging configuration for Saju Backend
Replace print statements with proper logging
"""

import logging
import logging.config
import os
from pathlib import Path

def setup_logging(app=None):
    """
    Setup logging configuration for the application
    
    Args:
        app: Flask application instance (optional)
    """
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'detailed': {
                'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'detailed',
                'filename': str(log_dir / 'saju_app.log'),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            },
            'error_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'ERROR',
                'formatter': 'detailed',
                'filename': str(log_dir / 'saju_errors.log'),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            }
        },
        'loggers': {
            'saju': {
                'level': log_level,
                'handlers': ['console', 'file', 'error_file'],
                'propagate': False
            },
            'werkzeug': {
                'level': 'WARNING',
                'handlers': ['console'],
                'propagate': False
            }
        },
        'root': {
            'level': log_level,
            'handlers': ['console', 'file']
        }
    }
    
    logging.config.dictConfig(logging_config)
    
    if app:
        app.logger.info('Logging configuration initialized')
    
    return logging.getLogger('saju')

# Create default logger instance
logger = setup_logging()

# Convenience functions
def debug(msg, *args, **kwargs):
    """Debug level logging"""
    logger.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    """Info level logging"""
    logger.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    """Warning level logging"""
    logger.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    """Error level logging"""
    logger.error(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    """Critical level logging"""
    logger.critical(msg, *args, **kwargs)