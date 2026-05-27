from decimal import Decimal
from uuid import UUID
from sqlalchemy import update, insert

from src.exceptions.exceptions import WithdrawOperationFailedException
from src.models import WalletOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.wallets import WalletDataMapper


class WalletRepository(BaseRepository):
    model = WalletOrm
    mapper = WalletDataMapper

    async def deposit_wallet(self, wallet_uuid: UUID, amount: Decimal):
        """
        Пополнить баланс кошелька
        """
        stmt = (
            update(self.model)
            .where(self.model.uuid == wallet_uuid)
            .values(balance=self.model.balance + amount)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        obj = result.scalars().one()
        return self.mapper.map_to_domain_entity(obj)

    async def withdraw_wallet(self, wallet_uuid: UUID, amount: Decimal):
        """
        Снять средства с кошелька
        """
        stmt = (
            update(self.model)
            .where(
                self.model.uuid == wallet_uuid,
                self.model.balance >= amount,
            )
            .values(balance=self.model.balance - amount)
            .returning(self.model)
        )

        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        if obj is None:
            raise WithdrawOperationFailedException
        return self.mapper.map_to_domain_entity(obj)

    async def create_wallet(self):
        """
        Создать кошелек
        """
        stmt = insert(self.model).values().returning(self.model)
        result = await self.session.execute(stmt)
        obj = result.scalar_one()
        return self.mapper.map_to_domain_entity(obj)
