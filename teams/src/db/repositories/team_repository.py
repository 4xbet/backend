from .base import BaseRepository
from ..models import Team
from ..database import Database

class TeamRepository(BaseRepository[Team]):
    def __init__(self, database: Database):
        super().__init__(database)

    def get_model(self):
        return Team
