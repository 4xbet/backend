from typing import TypeVar, Generic, List, Optional, Type
from sqlalchemy import select
from ..database import Database
from abc import ABC, abstractmethod

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    def __init__(self, database: Database):
        self.database = database

    @abstractmethod
    def get_model(self) -> Type[T]:
        """Должен вернуть модель SQLAlchemy (например, Team или Athlete)."""
        pass

    async def get(self, id: int) -> Optional[T]:
        async with self.database.get_session() as session:
            result = await session.execute(
                select(self.get_model()).filter_by(id=id)
            )
            return result.scalars().first()

    async def list(self, limit: int = 100, offset: int = 0) -> List[T]:
        async with self.database.get_session() as session:
            result = await session.execute(
                select(self.get_model()).limit(limit).offset(offset)
            )
            return list(result.scalars().all())

    async def create(self, entity: T) -> T:
        async with self.database.get_session() as session:
            session.add(entity)
            await session.commit()
            await session.refresh(entity)
            return entity

    async def update(self, id: int, entity: T) -> T:
        async with self.database.get_session() as session:
            existing_entity = await session.get(self.get_model(), id)
            if not existing_entity:
                raise ValueError(f"Entity with id {id} not found")

            entity_id = getattr(entity, 'id', None)
            if entity_id is not None and entity_id != id:
                raise ValueError("Entity id does not match the requested id")

            setattr(entity, 'id', id)
            session.add(entity)
            await session.commit()
            await session.refresh(entity)
            return entity

    async def delete(self, entity_id: int):
        async with self.database.get_session() as session:
            entity = await session.get(self.get_model(), entity_id)
            if entity:
                await session.delete(entity)
                await session.commit()
