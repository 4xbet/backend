from .base import BaseRepository
from ..models import Athlete
from sqlalchemy.ext.asyncio import AsyncSession

class AthleteRepository(BaseRepository[Athlete]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    def get_model(self):
        return Athlete
