import logging
from logging.handlers import RotatingFileHandler


def get_logger(name: str, log_file_path="blog_project_logs.log") -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if logger.handlers:
        return logger

    # File Handler
    fh = RotatingFileHandler(log_file_path, maxBytes=2048)

    fh.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh.setFormatter(fh_formatter)

    logger.addHandler(fh)

    return logger


logger = get_logger(__name__)
