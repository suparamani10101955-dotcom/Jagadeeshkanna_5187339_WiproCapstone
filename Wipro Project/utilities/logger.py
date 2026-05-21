from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from config.settings import settings


def get_logger(name: str = "automation") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    settings.log_dir.mkdir(parents=True, exist_ok=True)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    log_file = Path(settings.log_dir) / f"execution_{datetime.now():%Y%m%d_%H%M%S}.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False
    return logger
