from fastapi import APIRouter, Depends, HTTPException, status
from ...db.repositories import AthleteRepository, TeamRepository # Добавлено TeamRepository
from ..schemas.athletes import AthleteCreate, AthleteResponse, AthleteUpdate
from ...db.models import Athlete

router = APIRouter(prefix="/athletes", tags=["athletes"])

@router.get("/", response_model=list[AthleteResponse])
async def get_athletes():
    """Get all athletes."""
    return await AthleteRepository.list()

@router.get("/{athlete_id}", response_model=AthleteResponse)
async def get_athlete(athlete_id: int):
    """Get an athlete by ID."""
    athlete = await AthleteRepository.get(athlete_id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Athlete with ID {athlete_id} not found"
        )
    return athlete

@router.post("/", response_model=AthleteResponse, status_code=status.HTTP_201_CREATED)
async def create_athlete(athlete: AthleteCreate):
    """Create a new athlete."""
    team = await TeamRepository.get(athlete.team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {athlete.team_id} not found"
        )

    athlete_data = Athlete(
        first_name=athlete.first_name,
        last_name=athlete.last_name,
        date_of_birth=athlete.date_of_birth,
        position=athlete.position,
        team_id=athlete.team_id
    )
    return await AthleteRepository.create(athlete_data)

@router.put("/{athlete_id}", response_model=AthleteResponse)
async def update_athlete(athlete_id: int, athlete: AthleteUpdate):
    """Update an athlete by ID."""
    existing_athlete = await AthleteRepository.get(athlete_id)
    if not existing_athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Athlete with ID {athlete_id} not found"
        )
    
    update_data = athlete.model_dump(exclude_unset=True)
    if "team_id" in update_data:
        team_id_to_check = update_data["team_id"]
        team = await TeamRepository.get(team_id_to_check)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Team with ID {team_id_to_check} not found"
            )
    
    updated_athlete = Athlete(
        id=athlete_id,
        first_name=update_data.get('first_name', existing_athlete.first_name),
        last_name=update_data.get('last_name', existing_athlete.last_name),
        date_of_birth=update_data.get('date_of_birth', existing_athlete.date_of_birth),
        position=update_data.get('position', existing_athlete.position),
        team_id=update_data.get('team_id', existing_athlete.team_id)
    )
    
    return await AthleteRepository.update(athlete_id, updated_athlete)

@router.delete("/{athlete_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_athlete(athlete_id: int):
    """Delete an athlete by ID."""
    existing_athlete = await AthleteRepository.get(athlete_id)
    if not existing_athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Athlete with ID {athlete_id} not found"
        )
    
    await AthleteRepository.delete(athlete_id)
    return None