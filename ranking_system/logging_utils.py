"""Logging utilities used to setup the logger configuration."""
import logging
import logging.handlers
import os


def setup_logging(logger_name=None):
    """Setup the logging format, logger, console handler, and file handler.

    :param logger_name: The name of the logger.
    """

    # If no logger name is provided use the package name.
    if logger_name is None:
        logger_name = __package__

    # Create a logger filename
    logger_filename = logger_name + '.log'

    # Create a logging formatter
    time = '%(asctime)s'
    details = '[%(filename)s:%(lineno)s:%(funcName)s:%(threadName)s]'
    level = '%(levelname)s'
    message = '%(message)s'
    logging_format = time + ' ' + details + ' ' + level + ' - ' + message
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(logging_format, date_format)

    # Create a logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Create a file handler
    file_handler = logging.handlers.RotatingFileHandler(logger_filename,
                                                        mode='w', backupCount=5)

    if os.path.isfile(logger_filename):
        # If the file exists roll the file over.
        # This will start a new log file each run of the program.
        file_handler.doRollover()

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
