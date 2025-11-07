from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from . import crud, models, schemas, auth
from .database import get_db, engine
import httpx
import os

app = FastAPI()

MATCHES_SERVICE_URL = os.getenv("MATCHES_SERVICE_URL", "http://matches_service:80")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user_service:80")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.post("/bets/", response_model=schemas.Bet)
async def create_bet(
    bet: schemas.BetCreate,
    db: AsyncSession = Depends(get_db),
    current_user: auth.User = Depends(auth.get_current_user),
):
    # Verify user balance
    if not await crud.verify_user_balance(
        current_user.id, bet.amount_staked, current_user.token
    ):
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Get odds from matches_service
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MATCHES_SERVICE_URL}/matches/{bet.match_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Match not found")
        match = response.json()
        odds_on_bet = match["odds"][bet.outcome]

    # Create bet
    db_bet = await crud.create_bet(
        db=db, bet=bet, user_id=current_user.id, odds_on_bet=odds_on_bet
    )

    # Deduct bet amount from user's wallet
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {current_user.token}"}
        response = await client.patch(
            f"{USER_SERVICE_URL}/users/me/wallet",
            json={"amount": -bet.amount_staked},
            headers=headers,
        )
        if response.status_code != 200:
            # Rollback bet creation if wallet update fails
            await db.delete(db_bet)
            await db.commit()
            raise HTTPException(
                status_code=500, detail="Failed to update wallet balance"
            )

    # Create transaction
    transaction = schemas.TransactionCreate(
        wallet_id=current_user.id,  # Assuming wallet_id is the same as user_id
        amount=-bet.amount_staked,
        type="bet_placed",
        related_bet_id=db_bet.id,
    )
    await crud.create_transaction(db=db, transaction=transaction)

    return db_bet


@app.get("/bets/", response_model=List[schemas.Bet])
async def read_bets(
    db: AsyncSession = Depends(get_db),
    current_user: auth.User = Depends(auth.get_current_user),
):
    return await crud.get_bets_by_user(db=db, user_id=current_user.id)
