from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field
from src.schemas.utils import OperationType


class WalletOperation(BaseModel):
    """
    Схема для операций над кошельком
    """
    operation_type: OperationType
    amount: Decimal = Field(gt=0, max_digits=16, decimal_places=2)


class Wallet(BaseModel):
    """
    Схема для получения кошелька
    """
    uuid: UUID
    balance: Decimal
