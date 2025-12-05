from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
import httpx
import os
import random
from datetime import datetime, timezone
from sqlalchemy.orm import selectinload
 
BETS_SERVICE_URL = os.getenv("BETS_SERVICE_URL", "http://bets_service:80")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user_service:80")
 
 
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
 
 
async def complete_match(db: AsyncSession, match_id: int, token: str):
    db_match = await get_match(db, match_id)
    if not db_match:
        raise httpx.HTTPStatusError(404, "Match not found", request=None, response=None)
    if db_match.status != "active":
        raise httpx.HTTPStatusError(400, "Match is not active", request=None, response=None)
 
    db_match.status = "processing"
    await db.commit()
    await db.refresh(db_match)
 
    try:
        participants = [db_match.home_team_id, db_match.away_team_id]
        winner_id = random.choice(participants)
        
        winning_outcome = "win_home" if winner_id == db_match.home_team_id else "win_away"
 
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            
            settle_response = await client.post(
                f"{BETS_SERVICE_URL}/matches/{match_id}/settle",
                json={"winning_outcome": winning_outcome},
                headers=headers
            )
            settle_response.raise_for_status()

            response = await client.get(
                f"{BETS_SERVICE_URL}/matches/{match_id}/bets/", headers=headers
            )
            response.raise_for_status()
            bets = response.json()
 
            total_pot = sum(bet["amount_staked"] for bet in bets)
            
            winning_bets = [
                bet for bet in bets if bet["outcome"] == winning_outcome
            ]
            total_winning_stake = sum(bet["amount_staked"] for bet in winning_bets)
    
            if total_winning_stake > 0:
                for bet in winning_bets:
                    try:
                        payout = (bet["amount_staked"] / total_winning_stake) * total_pot
                        
                        await client.patch(
                            f"{USER_SERVICE_URL}/users/{bet['user_id']}/wallet",
                            json={"amount": payout},
                            headers=headers,
                        )
                    except Exception as e:
                        print(f"Error paying user {bet['user_id']}: {e}")
 
        db_match.status = "completed"
        db_match.winner_id = winner_id
        db_match.completed_time = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(db_match)
 
        return db_match
 
    except Exception as e:
        db_match.status = "active"
        await db.commit()
        raise e


async def start_match(db: AsyncSession, match_id: int):
    db_match = await get_match(db, match_id)
    if not db_match:
        raise httpx.HTTPStatusError(404, "Match not found", request=None, response=None)
    if db_match.status != "scheduled":
        raise httpx.HTTPStatusError(
            400, "Match is not scheduled", request=None, response=None
        )

    db_match.status = "active"
    await db.commit()
    await db.refresh(db_match)
    return db_match


async def start_match(db: AsyncSession, match_id: int):
    db_match = await get_match(db, match_id)
    if not db_match:
        raise httpx.HTTPStatusError(404, "Match not found", request=None, response=None)
    if db_match.status != "scheduled":
        raise httpx.HTTPStatusError(
            400, "Match is not scheduled", request=None, response=None
        )

    db_match.status = "active"
    await db.commit()
    await db.refresh(db_match)
    return db_match
