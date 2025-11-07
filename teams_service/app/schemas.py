from pydantic import BaseModel
from typing import Optional


class TeamBase(BaseModel):
    name: str
    country: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True
