from fastapi import HTTPException


class BaseException(Exception):
    detail = "Ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ObjectNotFoundException(BaseException):
    detail = "Объект не найден"


class WalletNotFoundException(BaseException):
    detail = "Кошелек не найден"


class WalletNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Кошелек не найден"


class WithdrawOperationFailedException(BaseException):
    detail = "Ошибка при снятии средств с кошелька"


class WithdrawOperationFailedHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Недостаточно средств"


class UnknownOperationTypeException(BaseException):
    detail = "Неизвестаня операция"


class UnknownOperationTypeHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Неизвестаня операция"
