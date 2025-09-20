from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from pydantic import BaseModel
from .athletes import AthleteResponse

class TeamBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=2, max_length=50)
    city: Optional[str] = Field(None, max_length=50)
    founded_year: int = Field(..., ge=1800, le=2024)
    logo_url: Optional[str] = Field(None, max_length=255)

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    country: Optional[str] = Field(None, min_length=2, max_length=50)
    city: Optional[str] = Field(None, max_length=50)
    founded_year: Optional[int] = Field(None, ge=1800, le=2024)
    logo_url: Optional[str] = Field(None, max_length=255)

class TeamResponse(TeamBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class TeamWithAthletesResponse(TeamResponse):
    athletes: list[AthleteResponse] = []