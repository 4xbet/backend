from ..db.repositories import TeamRepository, AthleteRepository
from ..db.repositories import team_repository_instance, athlete_repository_instance

def get_team_repository() -> TeamRepository:
    """Dependency to get the TeamRepository instance."""
    return team_repository_instance

def get_athlete_repository() -> AthleteRepository:
    """Dependency to get the AthleteRepository instance."""
    return athlete_repository_instance