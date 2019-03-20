"""Logging utilities to setup the logger configuration."""
import logging


def setup_logging():
    # Create a logging formatter
    time = '%(asctime)s'
    details = '[%(filename)s:%(lineno)s:%(funcName)s:%(threadName)s]'
    level = '%(levelname)s'
    message = '%(message)s'
    logging_format = time + ' ' + details + ' ' + level + ' - ' + message
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(logging_format, date_format)

    # Create a logger
    logger = logging.getLogger('ranking_system')
    logger.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Create a file handler
    file_handler = logging.FileHandler('python.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
