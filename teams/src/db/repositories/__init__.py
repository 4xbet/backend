from .team_repository import TeamRepository
from .athlete_repository import AthleteRepository
from ...db import db

TeamRepository = TeamRepository(db)
AthleteRepository = AthleteRepository(db)
