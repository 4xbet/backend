from fastapi import APIRouter, HTTPException, status
from ...db.repositories import TeamRepository
from ..schemas.teams import TeamCreate, TeamResponse
from ...db.models import Team

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/", response_model=list[TeamResponse])
async def get_teams():
    """Get all teams."""
    return await TeamRepository.list()

@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(team_id: int):
    """Get a team by ID."""
    team = await TeamRepository.get(team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found"
        )
    return team
    

@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(team: TeamCreate):
    """Create a new team."""
    team_data = Team(
        name=team.name,
        country=team.country,
        city=team.city,
        founded_year=team.founded_year,
        logo_url=team.logo_url
    )
    return await TeamRepository.create(team_data)
    
@router.put("/{team_id}", response_model=TeamResponse)
async def update_team(team_id: int, team: TeamCreate):
    """Update a team by ID."""
    existing_team = await TeamRepository.get(team_id)
    if not existing_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found"
        )

    update_data = team.model_dump(exclude_unset=True)
    
    team_data = Team(
        id=team_id,
        name=update_data.get("name", existing_team.name),
        country=update_data.get("country", existing_team.country),
        city=update_data.get("city", existing_team.city),
        founded_year=update_data.get("founded_year", existing_team.founded_year),
        logo_url=update_data.get("logo_url", existing_team.logo_url)
    )
    

    return await TeamRepository.update(team_id, team_data)

@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: int):
    """Delete a team by ID."""
    existing_team = await TeamRepository.get(team_id)
    if not existing_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found"
        )
    await TeamRepository.delete(team_id)
    return None