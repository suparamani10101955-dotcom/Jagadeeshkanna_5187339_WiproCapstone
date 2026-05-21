import logging
from pathlib import Path


LOG_DIR = Path("reports") / "logs"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(filename)s | %(message)s"


def get_logger(name="framework"):
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(LOG_FORMAT)
    file_handler = logging.FileHandler(LOG_DIR / "automation.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False
    return logger
