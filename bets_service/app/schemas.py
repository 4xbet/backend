from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BetBase(BaseModel):
    match_id: int
    outcome: str
    amount_staked: float


class BetCreate(BetBase):
    pass


class Bet(BetBase):
    id: int
    user_id: int
    odds_on_bet: float
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    wallet_id: int
    amount: float
    type: str
    related_bet_id: Optional[int] = None


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
