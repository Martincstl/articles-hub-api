from typing import Any


class AppException(Exception):

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 400,
        code: str = "app_error",
        details: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details


class NotFoundException(AppException):
    def __init__(
        self,
        message: str = "Resource not found",
        *,
        code: str = "not_found",
        details: Any | None = None,
    ) -> None:
        super().__init__(message, status_code=404, code=code, details=details)


class ConflictException(AppException):
    def __init__(
        self,
        message: str = "Resource already exists or conflicts with current state",
        *,
        code: str = "conflict",
        details: Any | None = None,
    ) -> None:
        super().__init__(message, status_code=409, code=code, details=details)


class UnauthorizedException(AppException):
    def __init__(
        self,
        message: str = "Authentication required or credentials invalid",
        *,
        code: str = "unauthorized",
        details: Any | None = None,
    ) -> None:
        super().__init__(message, status_code=401, code=code, details=details)


class ForbiddenException(AppException):
    def __init__(
        self,
        message: str = "You do not have permission to perform this action",
        *,
        code: str = "forbidden",
        details: Any | None = None,
    ) -> None:
        super().__init__(message, status_code=403, code=code, details=details)


class BadRequestException(AppException):
    def __init__(
        self,
        message: str = "Invalid request",
        *,
        code: str = "bad_request",
        details: Any | None = None,
    ) -> None:
        super().__init__(message, status_code=400, code=code, details=details)