from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
import httpx
import os

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user_service:80")


async def create_bet(
    db: AsyncSession, bet: schemas.BetCreate, user_id: int, odds_on_bet: float
):
    db_bet = models.Bet(
        **bet.dict(), user_id=user_id, odds_on_bet=odds_on_bet
    )
    db.add(db_bet)
    await db.commit()
    await db.refresh(db_bet)
    return db_bet


async def get_bets_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Bet).filter(models.Bet.user_id == user_id))
    return result.scalars().all()


async def verify_user_balance(user_id: int, amount: float, token: str):
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get(f"{USER_SERVICE_URL}/users/me/wallet", headers=headers)
        if response.status_code == 200:
            wallet = response.json()
            return wallet["balance"] >= amount
        return False


async def create_transaction(db: AsyncSession, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction
