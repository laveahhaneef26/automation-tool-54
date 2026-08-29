import logging
from logging.handlers import RotatingFileHandler
import os

def configure_rotating_logger(
    logger_name: str = "automation_tool",
    log_file: str = "logs/automation.log",
    max_bytes: int = 10485760,
    backup_count: int = 5,
    log_level: int = logging.INFO
) -> logging.Logger:
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    )
    console_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    class DebugFilter(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            msg = record.getMessage()
            return not (record.levelno == logging.DEBUG and "internal" in msg.lower())
    logger.addFilter(DebugFilter())
    return logger

default_logger = configure_rotating_logger()