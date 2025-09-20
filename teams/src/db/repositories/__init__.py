from .base import BaseRepository
from .team_repository import TeamRepository
from .athlete_repository import AthleteRepository
from ...db import db

team_repository_instance = TeamRepository(db)
athlete_repository_instance = AthleteRepository(db)


__all__ = ["BaseRepository", "TeamRepository", "AthleteRepository", "team_repository_instance", "athlete_repository_instance"]
