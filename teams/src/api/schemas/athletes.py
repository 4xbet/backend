from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import Optional

class AthleteBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    date_of_birth: Optional[date] = None
    position: Optional[str] = None

class AthleteCreate(AthleteBase):
    team_id: Optional[int] = None

class AthleteUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    date_of_birth: Optional[date] = None
    position: Optional[str] = None
    team_id: Optional[int] = None

class AthleteResponse(AthleteBase):
    id: int
    team_id: int
    
    model_config = ConfigDict(from_attributes=True)