import pytest
from src.services.team_service import TeamServiceFacade
from src.db.models import Team, Athlete
from src.db.repositories import TeamRepository, AthleteRepository
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date


@pytest.mark.integration
class TestTeamServiceFacadeIntegration:
    """Integration tests for TeamServiceFacade with a real database session."""

    @pytest.mark.asyncio
    async def test_create_team_with_athletes_integration(self, test_db: AsyncSession):
        """Test creating a team with athletes and persisting to the database."""
        # Arrange
        team_repo = TeamRepository(database=test_db)
        athlete_repo = AthleteRepository(database=test_db)
        service = TeamServiceFacade(team_repo=team_repo, athlete_repo=athlete_repo)
        team_data = {
            "name": "Integration Service Team",
            "country": "Serviceland",
            "founded_year": 2024
        }
        athletes_data = [
            {"first_name": "Service", "last_name": "Player1", "date_of_birth": date(2001, 1, 1), "position": "Forward"},
            {"first_name": "Service", "last_name": "Player2", "date_of_birth": date(2002, 2, 2), "position": "Defender"}
        ]

        # Act
        created_team = await service.create_team_with_athletes(team_data, athletes_data)

        # Assert
        assert created_team.id is not None
        retrieved_team = await team_repo.get(created_team.id)
        assert retrieved_team is not None
        assert len(retrieved_team.athletes) == 2
        assert retrieved_team.athletes[0].first_name == "Service"

    @pytest.mark.asyncio
    async def test_get_team_full_info_integration(self, test_db: AsyncSession, sample_team_in_db: Team):
        """Test getting full team info, including athletes, from the database."""
        # Arrange
        team_repo = TeamRepository(database=test_db)
        athlete_repo = AthleteRepository(database=test_db)
        service = TeamServiceFacade(team_repo=team_repo, athlete_repo=athlete_repo)

        # Act
        full_info = await service.get_team_full_info(sample_team_in_db.id)

        # Assert
        assert full_info is not None
        assert full_info["team"].name == sample_team_in_db.name
        assert len(full_info["athletes"]) > 0

    @pytest.mark.asyncio
    async def test_transfer_athlete_integration(self, test_db: AsyncSession, sample_team_in_db: Team, sample_athlete_in_db: Athlete):
        """Test transferring an athlete between teams in the database."""
        # Arrange
        team_repo = TeamRepository(database=test_db)
        athlete_repo = AthleteRepository(database=test_db)
        service = TeamServiceFacade(team_repo=team_repo, athlete_repo=athlete_repo)
        new_team_data = Team(name="New Transfer Team", country="Transferland", founded_year=2025)
        new_team = await team_repo.create(new_team_data)

        # Act
        transferred_athlete = await service.transfer_athlete(sample_athlete_in_db.id, new_team.id)

        # Assert
        assert transferred_athlete.team_id == new_team.id
        retrieved_athlete = await athlete_repo.get(sample_athlete_in_db.id)
        assert retrieved_athlete.team_id == new_team.id

    @pytest.mark.asyncio
    async def test_delete_team_cascade_integration(self, test_db: AsyncSession):
        """Test that deleting a team also deletes its athletes from the database."""
        # Arrange
        team_repo = TeamRepository(database=test_db)
        athlete_repo = AthleteRepository(database=test_db)
        service = TeamServiceFacade(team_repo=team_repo, athlete_repo=athlete_repo)
        team_to_delete = await service.create_team_with_athletes(
            {"name": "Team to Delete", "country": "Deleteland", "founded_year": 2021},
            [{"first_name": "Delete", "last_name": "Me", "date_of_birth": date(2000, 1, 1), "position": "Forward"}]
        )
        athlete_id = team_to_delete.athletes[0].id

        # Act
        await service.delete_team_cascade(team_to_delete.id)

        # Assert
        assert await team_repo.get(team_to_delete.id) is None
        assert await athlete_repo.get(athlete_id) is None