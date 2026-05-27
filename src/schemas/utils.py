from enum import Enum


class OperationType(str, Enum):
    """
    Используется для выбора операции
    """
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
