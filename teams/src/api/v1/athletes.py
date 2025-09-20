from fastapi import APIRouter, Depends, HTTPException, status
from ...db.repositories import AthleteRepository, TeamRepository
from ..schemas.athletes import AthleteCreate, AthleteResponse, AthleteUpdate
from ...db.models import Athlete
from ..dependencies import get_athlete_repository, get_team_repository 

router = APIRouter(prefix="/athletes", tags=["athletes"])

@router.get("/", response_model=list[AthleteResponse])
async def get_athletes(
    athlete_repo: AthleteRepository = Depends(get_athlete_repository)
):
    """Get all athletes."""
    return await athlete_repo.list()

@router.get("/{athlete_id}", response_model=AthleteResponse)
async def get_athlete(
    athlete_id: int,
    athlete_repo: AthleteRepository = Depends(get_athlete_repository) 
):
    """Get an athlete by ID."""
    athlete = await athlete_repo.get(athlete_id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Athlete with ID {athlete_id} not found"
        )
    return athlete

@router.post("/", response_model=AthleteResponse, status_code=status.HTTP_201_CREATED)
async def create_athlete(
    athlete: AthleteCreate,
    athlete_repo: AthleteRepository = Depends(get_athlete_repository),
    team_repo: TeamRepository = Depends(get_team_repository)
):
    """Create a new athlete."""
    team = await team_repo.get(athlete.team_id)
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
    return await athlete_repo.create(athlete_data)

@router.put("/{athlete_id}", response_model=AthleteResponse)
async def update_athlete(
    athlete_id: int,
    athlete_update: AthleteUpdate, # Используем AthleteUpdate для частичного обновления
    athlete_repo: AthleteRepository = Depends(get_athlete_repository), # Внедрение зависимости
    team_repo: TeamRepository = Depends(get_team_repository) # Внедрение зависимости для проверки команды
):
    """Update an athlete by ID."""
    existing_athlete = await athlete_repo.get(athlete_id)
    if not existing_athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Athlete with ID {athlete_id} not found"
        )
    
    update_data = athlete_update.model_dump(exclude_unset=True)
    
    # Проверка существования команды, если team_id обновляется
    if "team_id" in update_data:
        team_id_to_check = update_data["team_id"]
        team = await team_repo.get(team_id_to_check)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Team with ID {team_id_to_check} not found"
            )
    
    # Обновляем атрибуты существующего объекта напрямую
    for key, value in update_data.items():
        setattr(existing_athlete, key, value)
    
    return await athlete_repo.update(athlete_id, existing_athlete) # Передаем обновленный объект

@router.delete("/{athlete_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_athlete(
    athlete_id: int,
    athlete_repo: AthleteRepository = Depends(get_athlete_repository) # Внедрение зависимости
):
    """Delete an athlete by ID."""
    existing_athlete = await athlete_repo.get(athlete_id)
    if not existing_athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Athlete with ID {athlete_id} not found"
        )
    
    await athlete_repo.delete(athlete_id)
    return None