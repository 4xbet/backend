from typing import TypeVar, Generic, List, Optional, Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    def get_model(self) -> Type[T]:
        """Должен вернуть модель SQLAlchemy (например, Team или Athlete)."""
        pass

    async def get(self, id: int) -> Optional[T]:
        result = await self.session.execute(
            select(self.get_model()).filter_by(id=id)
        )
        return result.scalars().first()

    async def list(self, limit: int = 100, offset: int = 0) -> List[T]:
        result = await self.session.execute(
            select(self.get_model()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())
    
    async def list_all(self) -> List[T]:
        """Получить все записи без ограничений по лимиту"""
        result = await self.session.execute(
            select(self.get_model())
        )
        return list(result.scalars().all())

    async def create(self, entity: T) -> T:
        entity_id = getattr(entity, 'id', None)
        if entity_id is not None:
            existing_entity = await self.session.get(self.get_model(), entity_id)
            if existing_entity:
                raise ValueError(f"Entity with id {entity_id} already exists")
                    
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update(self, id: int, entity: T) -> T:
        existing_entity = await self.session.get(self.get_model(), id)
        if not existing_entity:
            raise ValueError(f"Entity with id {id} not found")

        entity_id = getattr(entity, 'id', None)
        if entity_id is not None and entity_id != id:
            raise ValueError("Entity id does not match the requested id")

        setattr(entity, 'id', id)
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def delete(self, entity_id: int):
        entity = await self.session.get(self.get_model(), entity_id)
        if entity:
            await self.session.delete(entity)
            await self.session.commit()
