from abc import ABC, abstractmethod
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, Any

class ErrorHandler(ABC):
    def __init__(self):
        self.next_handler: Optional['ErrorHandler'] = None

    def set_next(self, handler: 'ErrorHandler') -> 'ErrorHandler':
        self.next_handler = handler
        return handler

    def handle(self, request: Request, exc: Exception) -> Optional[JSONResponse]:
        if self.can_handle(exc):
            return self.process(request, exc)
        elif self.next_handler:
            return self.next_handler.handle(request, exc)
        return None

    @abstractmethod
    def can_handle(self, exc: Exception) -> bool:
        pass

    @abstractmethod
    def process(self, request: Request, exc: Exception) -> JSONResponse:
        pass

class HTTPExceptionHandler(ErrorHandler):
    def can_handle(self, exc: Exception) -> bool:
        return isinstance(exc, HTTPException)

    def process(self, request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )

class ValidationErrorHandler(ErrorHandler):
    def can_handle(self, exc: Exception) -> bool:
        return hasattr(exc, 'status_code') and getattr(exc, 'status_code', None) == 422

    def process(self, request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"error": "Validation error", "details": str(exc)}
        )

class DatabaseErrorHandler(ErrorHandler):
    def can_handle(self, exc: Exception) -> bool:
        db_errors = ('IntegrityError', 'OperationalError', 'ProgrammingError')
        return any(error in type(exc).__name__ for error in db_errors)

    def process(self, request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"error": "Database error"}
        )

class GenericErrorHandler(ErrorHandler):
    def can_handle(self, exc: Exception) -> bool:
        return True  

    def process(self, request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )

class ErrorHandlerChain:
    def __init__(self):
        self.chain = HTTPExceptionHandler()
        self.chain.set_next(ValidationErrorHandler())\
                 .set_next(DatabaseErrorHandler())\
                 .set_next(GenericErrorHandler())

    def handle(self, request: Request, exc: Exception) -> JSONResponse:
        result = self.chain.handle(request, exc)
        if result:
            return result
        
        return JSONResponse(
            status_code=500,
            content={"error": "Unexpected error occurred"}
        )