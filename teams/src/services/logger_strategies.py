import logging
from abc import ABC, abstractmethod
import json
from datetime import datetime
from typing import Dict, Any

class LoggingStrategy(ABC):
    @abstractmethod
    def log(self, level: str, message: str, extra: Dict[str, Any] = None):
        pass

class ConsoleLoggingStrategy(LoggingStrategy):
    def __init__(self):
        self.logger = logging.getLogger("console_logger")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_info(self, message: str):
        self.logger.info(message)

    def log_warning(self, message: str):
        self.logger.warning(message)

    def log_error(self, message: str):
        self.logger.error(message)

    def log(self, level: str, message: str, extra: Dict[str, Any] = None):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        extra_info = f" - {json.dumps(extra)}" if extra else ""
        print(f"{level.upper()}:     {timestamp} - {message}{extra_info}")

class FileLoggingStrategy(LoggingStrategy):
    def __init__(self, filename: str = "app.log"):
        self.filename = filename
    
    def log(self, level: str, message: str, extra: Dict[str, Any] = None):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        extra_info = f" - {json.dumps(extra)}" if extra else ""
        log_entry = f"{level.upper()}:     {timestamp} - {message}{extra_info}\n"
        
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(log_entry)

class JsonLoggingStrategy(LoggingStrategy):
    def log(self, level: str, message: str, extra: Dict[str, Any] = None):
        log_data = {
            "level": level,
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "extra": extra or {}
        }
        print(json.dumps(log_data))