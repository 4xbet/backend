from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.repositories import TeamRepository, AthleteRepository
from ..db.database import Database

db = Database()

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get a database session."""
    async with db.get_session() as session:
        yield session

def get_team_repository(session: AsyncSession = Depends(get_db_session)) -> TeamRepository:
    """Dependency to get the TeamRepository instance."""
    return TeamRepository(session)

def get_athlete_repository(session: AsyncSession = Depends(get_db_session)) -> AthleteRepository:
    """Dependency to get the AthleteRepository instance."""
    return AthleteRepository(session)
