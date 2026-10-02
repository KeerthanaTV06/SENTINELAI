"""Logging configuration for SENTINEL-AI."""
from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

def configure_logging(level: str = "INFO") -> None:
    """Configure root logger with console and rotating file handlers.

    Parameters
    ----------
    level: str
        Logging level name (e.g., 'INFO').
    """
    lvl = getattr(logging, level.upper(), logging.INFO)

    root = logging.getLogger()
    root.setLevel(lvl)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(lvl)
    ch_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(ch_formatter)

    # Rotating file handler
    fh = RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5)
    fh.setLevel(lvl)
    fh.setFormatter(ch_formatter)

    # Avoid duplicate handlers in case called multiple times
    if not any(isinstance(h, RotatingFileHandler) for h in root.handlers):
        root.addHandler(fh)

    if not any(isinstance(h, logging.StreamHandler) for h in root.handlers):
        root.addHandler(ch)

# Initialize default logging configuration at import time
configure_logging()
