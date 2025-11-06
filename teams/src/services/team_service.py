from typing import List, Optional, Dict, Any
from datetime import date
from ..db.repositories import TeamRepository, AthleteRepository
from ..db.models import Team, Athlete
from ..api.schemas.teams import TeamCreate
from ..api.schemas.athletes import AthleteCreate


class TeamServiceFacade:
    def __init__(self, team_repo: TeamRepository, athlete_repo: AthleteRepository):
        self._team_repo = team_repo
        self._athlete_repo = athlete_repo
    
    async def create_team_with_athletes(
        self, 
        team_data: Dict[str, Any],
        athletes_data: List[Dict[str, Any]]
    ) -> Team:
        team_create = TeamCreate(**team_data)
        team = Team(
            name=team_create.name,
            country=team_create.country,
            city=team_create.city,
            founded_year=team_create.founded_year,
            logo_url=team_create.logo_url
        )
        created_team = await self._team_repo.create(team)
        
        for athlete_data in athletes_data:
            athlete_create = AthleteCreate(**athlete_data)
            athlete = Athlete(
                first_name=athlete_create.first_name,
                last_name=athlete_create.last_name,
                date_of_birth=athlete_create.date_of_birth,
                position=athlete_create.position,
                team_id=created_team.id
            )
            await self._athlete_repo.create(athlete)
        
        return await self._team_repo.get(created_team.id)
    
    async def get_team_full_info(self, team_id: int) -> Optional[dict]:
        team = await self._team_repo.get(team_id)
        if not team:
            return None
        
        all_athletes = await self._athlete_repo.list_all()
        team_athletes = [a for a in all_athletes if a.team_id == team_id]
        
        return {
            "team": team,
            "athletes": team_athletes,
            "athletes_count": len(team_athletes),
            "average_age": self._calculate_average_age(team_athletes)
        }
    
    async def transfer_athlete(
        self, 
        athlete_id: int, 
        new_team_id: int
    ) -> Optional[Athlete]:
        athlete = await self._athlete_repo.get(athlete_id)
        if not athlete:
            return None
        
        new_team = await self._team_repo.get(new_team_id)
        if not new_team:
            return None
        
        athlete.team_id = new_team_id
        return await self._athlete_repo.update(athlete_id, athlete)
    
    async def delete_team_cascade(self, team_id: int) -> bool:
        team = await self._team_repo.get(team_id)
        if not team:
            return False
        
        all_athletes = await self._athlete_repo.list_all()
        team_athletes = [a for a in all_athletes if a.team_id == team_id]
        
        for athlete in team_athletes:
            await self._athlete_repo.delete(athlete.id)
        
        await self._team_repo.delete(team_id)
        return True
    
    async def get_teams_statistics(self) -> dict:
        teams = await self._team_repo.list_all()
        all_athletes = await self._athlete_repo.list_all()
        
        stats = {
            "total_teams": len(teams),
            "total_athletes": len(all_athletes),
            "teams_by_country": {},
            "largest_team": None,
            "smallest_team": None
        }
        
        for team in teams:
            country = team.country
            stats["teams_by_country"][country] = stats["teams_by_country"].get(country, 0) + 1
        
        if teams:
            team_sizes = []
            for team in teams:
                team_athletes = [a for a in all_athletes if a.team_id == team.id]
                team_sizes.append((team.name, len(team_athletes)))
            
            if team_sizes:
                stats["largest_team"] = max(team_sizes, key=lambda x: x[1])
                stats["smallest_team"] = min(team_sizes, key=lambda x: x[1])
        
        return stats
    
    def _calculate_average_age(self, athletes: List[Athlete]) -> Optional[float]:
        if not athletes:
            return None
        
        today = date.today()
        ages = []
        for athlete in athletes:
            age = today.year - athlete.date_of_birth.year
            if today.month < athlete.date_of_birth.month or (
                today.month == athlete.date_of_birth.month and today.day < athlete.date_of_birth.day
            ):
                age -= 1
            ages.append(age)
        
        return sum(ages) / len(ages) if ages else None
