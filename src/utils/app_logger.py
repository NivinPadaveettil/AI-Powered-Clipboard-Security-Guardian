import logging
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[2]
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOGS_DIR / "app.log"

_logger = logging.getLogger("ClipboardGuardian")
_logger.setLevel(logging.INFO)

if not _logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    _logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(file_formatter)
    _logger.addHandler(console_handler)


class AppLogger:

    @staticmethod
    def info(message):
        _logger.info(message)

    @staticmethod
    def warning(message):
        _logger.warning(message)

    @staticmethod
    def error(message, exc_info=False):
        _logger.error(message, exc_info=exc_info)

    @staticmethod
    def log_event(event_type, details=""):
        _logger.info(f"EVENT: {event_type} | {details}")

    @staticmethod
    def get_log_file_path():
        return str(LOG_FILE)


app_logger = AppLogger()
