from src.models import WalletOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.wallets import Wallet


class WalletDataMapper(DataMapper):
    db_model = WalletOrm
    schema = Wallet
