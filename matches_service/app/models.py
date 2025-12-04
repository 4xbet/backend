from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    home_team_id = Column(Integer, nullable=False, index=True)
    away_team_id = Column(Integer, nullable=False, index=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, nullable=False, default="scheduled")
    result = Column(String, nullable=True)
    winner_id = Column(Integer, nullable=True)
    completed_time = Column(DateTime(timezone=True), nullable=True)
    odds = relationship("Odds", back_populates="match", uselist=False)


class Odds(Base):
    __tablename__ = "odds"

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"), unique=True)
    win_home = Column(Numeric(5, 2), nullable=False)
    draw = Column(Numeric(5, 2), nullable=False)
    win_away = Column(Numeric(5, 2), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    match = relationship("Match", back_populates="odds")
