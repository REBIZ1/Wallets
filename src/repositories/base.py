from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.exceptions.exceptions import ObjectNotFoundException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper

    def __init__(self, session):
        self.session = session

    async def get_one(self, *filter, **filter_by):
        """
        Принимает аргументы для фильтрации и возвращает одно значение
        """
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            obj = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(obj)
