from .base import BaseRepository
from .team_repository import TeamRepository
from .athlete_repository import AthleteRepository
from .logging_decorator import RepositoryLoggingDecorator
from ...db import db

team_repository_instance = TeamRepository(db)
athlete_repository_instance = AthleteRepository(db)

team_repository_with_logging = RepositoryLoggingDecorator(team_repository_instance)
athlete_repository_with_logging = RepositoryLoggingDecorator(athlete_repository_instance)

__all__ = [
    "BaseRepository", 
    "TeamRepository", 
    "AthleteRepository", 
    "RepositoryLoggingDecorator",
    "team_repository_instance", 
    "athlete_repository_instance",
    "team_repository_with_logging",
    "athlete_repository_with_logging"
]
