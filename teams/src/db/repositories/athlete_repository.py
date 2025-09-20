from .base import BaseRepository
from ..models import Athlete
from ..database import Database

class AthleteRepository(BaseRepository[Athlete]):
    def __init__(self, database: Database):
        super().__init__(database, Athlete)
