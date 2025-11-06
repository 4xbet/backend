from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .base import BaseRepository
from ..models import Team
from sqlalchemy.ext.asyncio import AsyncSession

class TeamRepository(BaseRepository[Team]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    def get_model(self):
        return Team

    async def get(self, id: int) -> Optional[Team]:
        result = await self.session.execute(
            select(Team).options(selectinload(Team.athletes)).filter_by(id=id)
        )
        return result.scalars().first()

    async def list(self, limit: int = 100, offset: int = 0) -> List[Team]:
        result = await self.session.execute(
            select(Team).options(selectinload(Team.athletes)).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def list_all(self) -> List[Team]:
        result = await self.session.execute(
            select(Team).options(selectinload(Team.athletes))
        )
        return list(result.scalars().all())
