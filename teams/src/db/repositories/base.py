from typing import TypeVar, Generic, List, Optional, Type
from sqlalchemy import select
from ..database import Database 

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, database: Database, model: Type[T]):
        """Initialize the repository with the database and model.

        Args:
            database: The database instance
            model: The model class
        """
        self.database = database
        self.model = model

    async def get(self, id: int) -> Optional[T]:
        """Get an entity by ID.

        Args:
            id: The ID of the entity to get

        Returns:
            The entity if found, None otherwise
        """
        async with self.database.get_session() as session:
            result = await session.execute(
                select(self.model).filter_by(id=id)
            )
            return result.scalars().first()

    async def list(self, limit: int = 100, offset: int = 0) -> List[T]:
        """List all entities.

        Args:
            limit: The maximum number of entities to return
            offset: The offset to start from

        Returns:
            List of entities
        """
        async with self.database.get_session() as session:
            result = await session.execute(
                select(self.model).limit(limit).offset(offset)
            )
            return list(result.scalars().all())

    async def create(self, entity: T) -> T:
        """Create a new entity.

        Args:
            entity: The entity to create

        Returns:
            The created entity
        """
        async with self.database.get_session() as session:
            session.add(entity)
            await session.commit()
            await session.refresh(entity)
            return entity

    async def update(self, id: int, entity: T) -> T:
        """Update an existing entity in the database.
        
        Args:
            id: The ID of the entity to update.
            entity: The entity object to update. It can be a detached instance.
            
        Returns:
            The updated and re-attached entity.
        """
        async with self.database.get_session() as session:
            existing_entity = await session.get(self.model, id)
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
        """Delete an entity by ID.

        Args:
            id: The ID of the entity to delete
        """
        async with self.database.get_session() as session:
            entity = await session.get(self.model, entity_id) 
            if entity:
                await session.delete(entity)
                await session.commit()