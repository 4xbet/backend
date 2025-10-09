from .logger import LoggerService
from .logger_strategies import LoggingStrategy, ConsoleLoggingStrategy
from .error_handlers import ErrorHandlerChain
from .team_service import TeamServiceFacade

logger = LoggerService(log_to_file=True, log_file_path='app.log')

__all__ = [
    "logger",
    "LoggerService", 
    "LoggingStrategy", 
    "ConsoleLoggingStrategy",
    "ErrorHandlerChain",
    "TeamServiceFacade"
]
