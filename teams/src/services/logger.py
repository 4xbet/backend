import logging
import logging.handlers
from typing import Optional, Dict, Any
from .logger_strategies import LoggingStrategy, ConsoleLoggingStrategy

class LoggerService:
    def __init__(
        self,
        strategy: LoggingStrategy = None,
        log_level: int = logging.INFO,
        log_to_console: bool = True,
        log_to_file: bool = False,
        log_file_path: Optional[str] = None,
        max_file_size: int = 10 * 1024 * 1024,
        backup_count: int = 5
    ):
        self.strategy = strategy or ConsoleLoggingStrategy()
        
        self.logger = logging.getLogger()
        self.logger.setLevel(log_level)
        self.logger.handlers.clear()

        formatter = logging.Formatter(
            '%(levelname)s:     %(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        if log_to_file and log_file_path:
            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_file_path,
                maxBytes=max_file_size,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def set_strategy(self, strategy: LoggingStrategy):
        """Смена стратегии логирования"""
        self.strategy = strategy

    def debug(self, message: str, extra: Dict[str, Any] = None):
        self.strategy.log('debug', message, extra)
        self.logger.debug(message)

    def info(self, message: str, extra: Dict[str, Any] = None):
        self.strategy.log('info', message, extra)
        self.logger.info(message)

    def warning(self, message: str, extra: Dict[str, Any] = None):
        self.strategy.log('warning', message, extra)
        self.logger.warning(message)

    def error(self, message: str, extra: Dict[str, Any] = None):
        self.strategy.log('error', message, extra)
        self.logger.error(message)

    def critical(self, message: str, extra: Dict[str, Any] = None):
        self.strategy.log('critical', message, extra)
        self.logger.critical(message)

    def exception(self, message: str, extra: Dict[str, Any] = None):
        self.strategy.log('error', message, extra)
        self.logger.exception(message)