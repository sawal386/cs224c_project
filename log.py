import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file, level=logging.DEBUG):
    """
    Function to setup a logger; if handlers exist, clear them first.
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)


    if logger.hasHandlers():
        logger.handlers.clear()


    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler(log_file, maxBytes=20000000000, backupCount=10)


    console_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)  # Ensure file logs all levels

    console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
