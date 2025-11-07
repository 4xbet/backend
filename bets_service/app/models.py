from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    ForeignKey,
    func,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    match_id = Column(Integer, nullable=False, index=True)
    outcome = Column(String, nullable=False)
    amount_staked = Column(Numeric(10, 2), nullable=False)
    odds_on_bet = Column(Numeric(5, 2), nullable=False)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, server_default=func.now())


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(String, nullable=False)
    related_bet_id = Column(Integer, ForeignKey("bets.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
