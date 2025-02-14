import logging
import os
from logging import Logger
from dotenv import load_dotenv, find_dotenv
from pkg.logger.formater import CustomJsonFormatter

_nameToLevel = {
    'CRITICAL': logging.CRITICAL,
    'FATAL': logging.FATAL,
    'ERROR': logging.ERROR,
    'WARN': logging.WARNING,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET,
}

_log = None


def instance() -> None:
    _get_logger()


def _get_logger():
    if _log is None:
        return _init()
    return _log


def _init():
    try:
        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)
    except Exception as e:
        print("Error load env on log.py : ", e)
        exit(0)

    _logger = logging.getLogger(os.environ.get('APP_NAME', 'flask-service'))

    # Setup log level
    log_level_env = os.environ.get("LOG_LEVEL", "ERROR")
    log_level = _nameToLevel.get(log_level_env)

    if log_level is None:
        log_level = logging.ERROR

    # Set the log level
    _logger.setLevel(log_level)

    # Create handlers
    console_handler = logging.StreamHandler()

    # Set the log level for handlers
    console_handler.setLevel(log_level)

    # Create formatters and add them to handlers
    json_format = CustomJsonFormatter()

    console_handler.setFormatter(json_format)

    # Add handlers to the _logger
    _logger.addHandler(console_handler)

    return _logger


# Create a custom logger
logger: Logger = _get_logger()
