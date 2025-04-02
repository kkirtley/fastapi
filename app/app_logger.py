"""Application logger module.

This module provides a custom logging setup for the FastAPI application. It uses
a JSON formatter for structured logging and ensures that logs include timestamps,
log levels, and other relevant information. This logger can be used throughout
the application to maintain consistent and informative logs.
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pythonjsonlogger.json import JsonFormatter
import pytz


class AppLogger:
    """Application logger class.

    This class sets up a logger instance with a JSON formatter and writes logs
    to a specified file. It supports log rotation to prevent excessive disk usage
    and ensures that the log directory exists.
    """

    def __init__(self, log_file: str = "/var/log/app/fastapi.log", log_level: int = logging.INFO):
        """
        Initialize the logger.

        Args:
            log_file (str): The file path where logs will be written. Defaults to
                "/var/log/app/fastapi.log".
            log_level (int): The logging level (e.g., logging.INFO, logging.DEBUG).
                Defaults to logging.INFO.
        """
        self.logger = logging.getLogger("app_logger")
        self.logger.setLevel(log_level)

        # Ensure the log directory exists
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir, exist_ok=True)
            except OSError as e:
                raise RuntimeError(
                    f"Failed to create log directory: {log_dir}") from e

        # Set up a rotating file handler to manage log file size
        try:
            log_handler = RotatingFileHandler(
                filename=log_file, maxBytes=5 * 1024 * 1024, backupCount=3  # 5 MB per file, 3 backups
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to set up log file handler: {e}") from e

        # Customize the JSON formatter to include date and time
        formatter = CustomJsonFormatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        log_handler.setFormatter(formatter)
        self.logger.addHandler(log_handler)

    def get_logger(self) -> logging.Logger:
        """
        Get the logger instance.

        Returns:
            logging.Logger: The configured logger instance.
        """
        return self.logger


class CustomJsonFormatter(JsonFormatter):
    """Custom JSON formatter to handle UTC timezone for asctime.

    This formatter customizes the log format based on the log level and ensures
    that timestamps are in UTC.
    """

    def format(self, record):
        """
        Customize the log format based on the log level.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message.
        """
        # Use a detailed format for ERROR logs
        if record.levelno == logging.ERROR:
            self._fmt = "%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)d %(module)s %(funcName)s %(message)s"
        else:
            # Use a simpler format for other log levels
            self._fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
        return super().format(record)

    def formatTime(self, record, datefmt=None):
        """
        Format the time for log records.

        Args:
            record (logging.LogRecord): The log record containing the timestamp.
            datefmt (str, optional): The date format string. Defaults to None.

        Returns:
            str: The formatted timestamp in ISO 8601 format or the specified format.
        """
        # Convert the timestamp to UTC
        dt = datetime.fromtimestamp(record.created, tz=pytz.UTC)
        if datefmt:
            # Format the timestamp using the provided date format
            return dt.strftime(datefmt)
        # Return the timestamp in ISO 8601 format by default
        return dt.isoformat()


logger = AppLogger().get_logger()
