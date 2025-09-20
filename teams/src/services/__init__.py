from .logger import LoggerService
import logging

logger = LoggerService(
        log_level=logging.DEBUG,
        log_to_console=True,
        log_to_file=True,
        log_file_path="app.log"
)