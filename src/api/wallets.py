from uuid import UUID
from fastapi import APIRouter

from src.api.dependencies.dependencies import DBDep
from src.exceptions.exceptions import (
    WalletNotFoundException,
    WalletNotFoundHTTPException,
    WithdrawOperationFailedHTTPException,
    WithdrawOperationFailedException,
    UnknownOperationTypeHTTPException,
    UnknownOperationTypeException,
)
from src.schemas.wallets import WalletOperation
from src.services.wallets import WalletService

router = APIRouter(prefix="/api/v1/wallets", tags=["Кошельки"])


@router.get("/{wallet_uuid}", summary="Получить баланс кошелька")
async def get_wallet_balance(db: DBDep, wallet_uuid: UUID):
    """
    Возвращает баланс кошелька
    """
    try:
        wallet = await WalletService(db).get_wallet_balance(wallet_uuid)
    except WalletNotFoundException:
        raise WalletNotFoundHTTPException
    return wallet


@router.post("", summary="Создать кошелек")
async def create_wallet(db: DBDep):
    """
    Создать кошелек
    """
    return await WalletService(db).create_wallet()


@router.put("/{wallet_uuid}/operation", summary="Изменить баланс кошелька")
async def change_wallet_balance(db: DBDep, wallet_uuid: UUID, data: WalletOperation):
    """
    Изменить баланс кошелька
    """
    try:
        wallet = await WalletService(db).change_wallet_balance(wallet_uuid, data)
    except WithdrawOperationFailedException:
        raise WithdrawOperationFailedHTTPException
    except WalletNotFoundException:
        raise WalletNotFoundHTTPException
    except UnknownOperationTypeException:
        raise UnknownOperationTypeHTTPException
    return wallet
