#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logging configuration for Synology environment with rotating logs
"""
from logging import (
    basicConfig,
    StreamHandler,
    getLevelName,
    INFO,
    DEBUG,
)
from logging.handlers import RotatingFileHandler
from pathlib import Path
from sys import stdout


def setup_logging(app):
    """Setup logging with rotation for both local and Synology environments"""
    # Create log directory in project root
    log_dir = Path(__file__).parent.parent / "log"
    log_dir.mkdir(exist_ok=True)

    # Determine log level based on environment
    log_level = DEBUG if app.debug else INFO

    # Create rotating file handler
    # Max file size: 10MB, keep 5 backup files
    rotating_handler = RotatingFileHandler(
        log_dir / "ddns.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    rotating_handler.setLevel(log_level)

    # Create console handler for Synology compatibility
    console_handler = StreamHandler(stdout)
    console_handler.setLevel(log_level)

    # Create formatter
    formatter = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configure basic logging
    basicConfig(
        level=log_level,
        format=formatter,
        handlers=[rotating_handler, console_handler],
    )

    # Configure Flask app logger
    app.logger.setLevel(log_level)
    app.logger.info(f"Logging initialized - Level: {getLevelName(log_level)}")
    app.logger.info(f"Log rotation: 10MB max, 5 backups in {log_dir}")
