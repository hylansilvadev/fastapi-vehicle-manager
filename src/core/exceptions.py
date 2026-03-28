from typing import Any, Dict, Optional

from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    """
    Classe base para exceptions customizadas da aplicação.
    """

    def __init__(
        self, status_code: int, message: str, details: Optional[Dict[str, Any]] = None
    ):
        self.status_code = status_code
        self.message = message
        self.details = details


class NotFoundException(AppException):
    def __init__(
        self,
        message: str = 'Recurso não encontrado',
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, message=message, details=details
        )


class BadRequestException(AppException):
    def __init__(
        self,
        message: str = 'Requisição inválida',
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, message=message, details=details
        )


class ConflictException(AppException):
    def __init__(
        self,
        message: str = 'Conflito de dados. Recurso já existe.',
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, message=message, details=details
        )


def setup_exception_handlers(app):
    """
    Registra os handlers de exceptions no ciclo de vida do FastAPI.
    """

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        content = {
            'error': True,
            'message': exc.message,
        }
        if exc.details:
            content['details'] = exc.details

        return JSONResponse(
            status_code=exc.status_code,
            content=content,
        )
