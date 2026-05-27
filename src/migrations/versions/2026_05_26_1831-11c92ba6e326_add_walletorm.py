"""add WalletOrm

Revision ID: 11c92ba6e326
Revises:
Create Date: 2026-05-26 18:31:17.853482

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "11c92ba6e326"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "wallets",
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column(
            "balance",
            sa.Numeric(precision=16, scale=2),
            nullable=False,
            server_default="0.00",
        ),
        sa.CheckConstraint("balance >= 0", name="balance_non_negative"),
        sa.PrimaryKeyConstraint("uuid"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("wallets")
