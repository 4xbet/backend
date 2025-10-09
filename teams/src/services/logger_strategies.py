from abc import ABC, abstractmethod
import json
from datetime import datetime
from typing import Dict, Any

class LoggingStrategy(ABC):
    @abstractmethod
    def log(self, level: str, message: str, extra: Dict[str, Any] = None):
        pass

class ConsoleLoggingStrategy(LoggingStrategy):
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