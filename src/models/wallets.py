from uuid import UUID, uuid4
from decimal import Decimal
from sqlalchemy import CheckConstraint, Numeric
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class WalletOrm(Base):
    __tablename__ = "wallets"

    __table_args__ = (CheckConstraint("balance >= 0", name="balance_non_negative"),)

    uuid: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(16, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
