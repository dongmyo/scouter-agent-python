import logging
import os
from logging.handlers import RotatingFileHandler

from scouterx.common.util.os_util import get_scouter_path


def init():
    log_path = os.path.join(get_scouter_path(), 'logs')
    os.makedirs(log_path, exist_ok=True)  # Ensures that the directory exists
    file_name = os.path.join(log_path, 'scouter.log')

    # Set up logging to file
    file_handler = RotatingFileHandler(file_name, mode='a', maxBytes=5 * 1024 * 1024, backupCount=2)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # Set up logging to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # Configure root logger
    logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])

    # Define loggers with different names and levels
    trace_logger = logging.getLogger('trace')
    trace_logger.setLevel(logging.DEBUG)

    info_logger = logging.getLogger('info')
    info_logger.setLevel(logging.INFO)

    warning_logger = logging.getLogger('warning')
    warning_logger.setLevel(logging.WARNING)

    error_logger = logging.getLogger('error')
    error_logger.setLevel(logging.ERROR)

    return trace_logger, info_logger, warning_logger, error_logger
