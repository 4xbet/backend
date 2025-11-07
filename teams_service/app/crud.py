from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas


async def get_team(db: AsyncSession, team_id: int):
    result = await db.execute(select(models.Team).filter(models.Team.id == team_id))
    return result.scalars().first()


async def get_teams(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Team).offset(skip).limit(limit))
    return result.scalars().all()


async def create_team(db: AsyncSession, team: schemas.TeamCreate):
    db_team = models.Team(**team.dict())
    db.add(db_team)
    await db.commit()
    await db.refresh(db_team)
    return db_team


async def update_team(db: AsyncSession, team_id: int, team: schemas.TeamCreate):
    db_team = await get_team(db, team_id)
    if db_team:
        team_data = team.dict(exclude_unset=True)
        for key, value in team_data.items():
            setattr(db_team, key, value)
        await db.commit()
        await db.refresh(db_team)
    return db_team


async def delete_team(db: AsyncSession, team_id: int):
    db_team = await get_team(db, team_id)
    if db_team:
        await db.delete(db_team)
        await db.commit()
    return db_team
