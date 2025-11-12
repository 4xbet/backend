from pydantic import BaseModel, field_validator
from datetime import datetime, timezone
from typing import Optional


class MatchBase(BaseModel):
    home_team_id: int
    away_team_id: int
    start_time: datetime

    @field_validator("start_time", mode="before")
    def ensure_tz_aware(cls, v):
        if isinstance(v, str):
            if v.endswith("Z"):
                return datetime.fromisoformat(v[:-1] + "+00:00")
            return datetime.fromisoformat(v)
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


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
