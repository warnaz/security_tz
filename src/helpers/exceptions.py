from enum import Enum


class StatusCode(Enum):
    HTTP_404_NOT_FOUND = 404
    HTTP_500_INTERNAL_SERVER_ERROR = 500


status = StatusCode


class BaseException(Exception):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Internal server error"

    def __str__(self) -> str:
        return f"{self.STATUS_CODE.value}: {self.DETAIL}"


class ContentNotFound(BaseException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Feed not found"
