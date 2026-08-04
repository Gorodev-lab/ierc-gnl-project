"""
Centralized Logging — IERC-GNL
================================
Single logging setup. Derives log path from PROJECT_ROOT automatically.
"""

import logging
from pathlib import Path
from typing import Optional

# Resolve project root: src/utils/logging.py -> parents[2] = project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOG_DIR = PROJECT_ROOT / "logs"

_loggers_initialized = set()


def setup_logging(
    name: str,
    log_dir: Optional[Path] = None,
    level: int = logging.INFO,
    file_handler: bool = True,
) -> logging.Logger:
    """
    Configure and return a logger with console + file handler.

    Args:
        name: Logger name (use __name__)
        log_dir: Custom log directory (defaults to PROJECT_ROOT/logs)
        level: Logging level
        file_handler: Whether to add file handler

    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)

    if name in _loggers_initialized:
        return logger

    logger.setLevel(level)
    logger.propagate = False

    # Clear existing handlers
    logger.handlers.clear()

    # Console handler
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(console)

    # File handler
    if file_handler:
        log_path = (log_dir or DEFAULT_LOG_DIR) / f"{name.replace('.', '_')}.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_h = logging.FileHandler(log_path)
        file_h.setLevel(level)
        file_h.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(file_h)

    _loggers_initialized.add(name)
    return logger