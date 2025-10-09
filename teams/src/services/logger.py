from .logger_strategies import LoggingStrategy, ConsoleLoggingStrategy

class LoggerService:
    def __init__(self, log_to_file: bool = False, log_file_path: str = 'app.log'):
        self.log_to_file = log_to_file
        self.log_file_path = log_file_path
        self.console_strategy = ConsoleLoggingStrategy()
        # You might want to add a file logging strategy here too
        # For simplicity, I'll just use the console strategy and a basic file write for now.

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

# Instantiate the logger here, making it a singleton-like instance
logger = LoggerService(log_to_file=True, log_file_path='app.log')