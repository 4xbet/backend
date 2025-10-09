from .logger_strategies import LoggingStrategy, ConsoleLoggingStrategy

class LoggerService:
    def __init__(self, log_to_file: bool = False, log_file_path: str = 'app.log'):
        self.log_to_file = log_to_file
        self.log_file_path = log_file_path
        self.console_strategy = ConsoleLoggingStrategy()

    def info(self, message: str):
        self.console_strategy.log_info(message)
        if self.log_to_file:
            with open(self.log_file_path, 'a') as f:
                f.write(f"INFO: {message}\n")

    def warning(self, message: str):
        self.console_strategy.log_warning(message)
        if self.log_to_file:
            with open(self.log_file_path, 'a') as f:
                f.write(f"WARNING: {message}\n")

    def error(self, message: str):
        self.console_strategy.log_error(message)
        if self.log_to_file:
            with open(self.log_file_path, 'a') as f:
                f.write(f"ERROR: {message}\n")

logger = LoggerService(log_to_file=True, log_file_path='app.log')