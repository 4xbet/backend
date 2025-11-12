from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas


from sqlalchemy.orm import selectinload


async def get_match(db: AsyncSession, match_id: int):
    result = await db.execute(
        select(models.Match)
        .options(selectinload(models.Match.odds))
        .filter(models.Match.id == match_id)
    )
    return result.scalars().first()


async def get_matches(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Match).options(selectinload(models.Match.odds)).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_match(db: AsyncSession, match: schemas.MatchCreate):
    db_match = models.Match(**match.dict())
    db.add(db_match)
    await db.commit()
    await db.refresh(db_match)
    return await get_match(db, db_match.id)


async def create_match_odds(db: AsyncSession, match_id: int, odds: schemas.OddsCreate):
    db_odds = models.Odds(**odds.dict(), match_id=match_id)
    db.add(db_odds)
    await db.commit()
    await db.refresh(db_odds)
    return db_odds


async def update_odds(db: AsyncSession, match_id: int, odds: schemas.OddsCreate):
    result = await db.execute(select(models.Odds).filter(models.Odds.match_id == match_id))
    db_odds = result.scalars().first()
    if db_odds:
        odds_data = odds.dict(exclude_unset=True)
        for key, value in odds_data.items():
            setattr(db_odds, key, value)
        await db.commit()
        await db.refresh(db_odds)
    return db_odds
