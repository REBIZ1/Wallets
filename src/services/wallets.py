from uuid import UUID

from src.exceptions.exceptions import (
    ObjectNotFoundException,
    WalletNotFoundException,
    UnknownOperationTypeException,
)
from src.schemas.utils import OperationType
from src.schemas.wallets import WalletOperation
from src.services.base import BaseService


class WalletService(BaseService):
    OPERATION_MAP = {
        OperationType.DEPOSIT: "deposit_wallet",
        OperationType.WITHDRAW: "withdraw_wallet",
    }

    async def get_wallet_balance(self, wallet_uuid: UUID):
        """
        Возвращает баланс кошелька
        """
        try:
            return await self.db.wallets.get_one(uuid=wallet_uuid)
        except ObjectNotFoundException:
            raise WalletNotFoundException

    async def change_wallet_balance(self, wallet_uuid: UUID, data: WalletOperation):
        """
        Изменить баланс кошелька
        """
        await self.get_wallet_balance(wallet_uuid)
        method_name = self.OPERATION_MAP.get(data.operation_type)
        if not method_name:
            raise UnknownOperationTypeException
        method = getattr(self.db.wallets, method_name)
        wallet = await method(wallet_uuid, data.amount)
        await self.db.commit()
        return wallet

    async def create_wallet(self):
        """
        Создать кошелек
        """
        wallet = await self.db.wallets.create_wallet()
        await self.db.commit()
        return wallet
