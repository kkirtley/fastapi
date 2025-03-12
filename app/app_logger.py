"""Application logger module."""

import logging
from datetime import datetime
from pythonjsonlogger import jsonlogger
import pytz


class AppLogger:
    """Application logger class."""

    def __init__(self, log_file: str = "app.log"):
        self.logger = logging.getLogger("app_logger")
        self.logger.setLevel(logging.INFO)
        log_handler = logging.FileHandler(filename=log_file)

        # Customize the JSON formatter to include date and time
        formatter = CustomJsonFormatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        log_handler.setFormatter(formatter)
        self.logger.addHandler(log_handler)

    def get_logger(self) -> logging.Logger:
        """Get the logger instance."""
        return self.logger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter to handle UTC timezone for asctime."""

    def format(self, record):
        """Customize the log format based on the log level."""
        if record.levelno == logging.ERROR:
            self._fmt = "%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)d %(module)s %(funcName)s %(message)s"
        else:
            self._fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
        return super().format(record)

    def formatTime(self, record, datefmt=None):
        """Format the time for log records."""
        dt = datetime.fromtimestamp(record.created, tz=pytz.UTC)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()
