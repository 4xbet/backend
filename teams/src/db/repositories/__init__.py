from .base import BaseRepository
from ...db import db
from ..models import Athlete, Team

AthleteRepository = BaseRepository(db, Athlete)
TeamRepository = BaseRepository(db, Team)