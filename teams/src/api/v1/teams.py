from fastapi import APIRouter, HTTPException, status, Depends
from ...db.repositories import TeamRepository
from ..schemas.teams import TeamCreate, TeamResponse, TeamUpdate
from ...db.models import Team
from ..dependencies import get_team_repository

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/", response_model=list[TeamResponse])
async def get_teams(
    team_repo: TeamRepository = Depends(get_team_repository)
):
    """Get all teams."""
    return await team_repo.list()

@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: int,
    team_repo: TeamRepository = Depends(get_team_repository)
):
    """Get a team by ID."""
    team = await team_repo.get(team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found"
        )
    return team
    

@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(
    team: TeamCreate,
    team_repo: TeamRepository = Depends(get_team_repository)
):
    """Create a new team."""
    team_data = Team(
        name=team.name,
        country=team.country,
        city=team.city,
        founded_year=team.founded_year,
        logo_url=team.logo_url
    )
    return await team_repo.create(team_data)
    
@router.put("/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: int,
    team_update: TeamUpdate,
    team_repo: TeamRepository = Depends(get_team_repository)
):
    """Update a team by ID."""
    existing_team = await team_repo.get(team_id)
    if not existing_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found"
        )

    update_data = team_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(existing_team, key, value)
    
    return await team_repo.update(team_id, existing_team)

@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    team_id: int,
    team_repo: TeamRepository = Depends(get_team_repository)
):
    """Delete a team by ID."""
    existing_team = await team_repo.get(team_id)
    if not existing_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found"
        )
    await team_repo.delete(team_id)
    return None