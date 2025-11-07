from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MatchBase(BaseModel):
    home_team_id: int
    away_team_id: int
    start_time: datetime


class MatchCreate(MatchBase):
    pass


class OddsBase(BaseModel):
    win_home: float
    draw: float
    win_away: float


class OddsCreate(OddsBase):
    pass


class Odds(OddsBase):
    id: int
    match_id: int
    updated_at: datetime

    class Config:
        from_attributes = True


class Match(MatchBase):
    id: int
    status: str
    result: Optional[str]
    odds: Optional[Odds]

    class Config:
        from_attributes = True
