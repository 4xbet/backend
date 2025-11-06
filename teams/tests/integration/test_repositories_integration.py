import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.repositories import TeamRepository, AthleteRepository
from src.db.models import Team, Athlete
from datetime import date


@pytest.mark.integration
class TestRepositoryIntegration:
    """Integration tests for repositories with a real database session."""

    @pytest.mark.asyncio
    async def test_team_repository_operations(self, test_db: AsyncSession):
        """Test CRUD operations for TeamRepository."""
        team_repo = TeamRepository(test_db)
        new_team = Team(
            name="Integration Test Team",
            country="Testland",
            founded_year=2023
        )

        created_team = await team_repo.create(new_team)
        assert created_team.id is not None
        assert created_team.name == "Integration Test Team"

        retrieved_team = await team_repo.get(created_team.id)
        assert retrieved_team is not None
        assert retrieved_team.name == "Integration Test Team"

        all_teams = await team_repo.list()
        assert len(all_teams) >= 1

        retrieved_team.name = "Updated Team Name"
        updated_team = await team_repo.update(retrieved_team.id, retrieved_team)
        assert updated_team.name == "Updated Team Name"

        await team_repo.delete(created_team.id)
        deleted_team = await team_repo.get(created_team.id)
        assert deleted_team is None

    @pytest.mark.asyncio
    async def test_athlete_repository_operations(self, test_db: AsyncSession, sample_team_in_db: Team):
        """Test CRUD operations for AthleteRepository."""
        athlete_repo = AthleteRepository(test_db)
        new_athlete = Athlete(
            first_name="Integration",
            last_name="Tester",
            date_of_birth=date(2000, 1, 1),
            position="QA",
            team_id=sample_team_in_db.id
        )

        created_athlete = await athlete_repo.create(new_athlete)
        assert created_athlete.id is not None
        assert created_athlete.first_name == "Integration"

        retrieved_athlete = await athlete_repo.get(created_athlete.id)
        assert retrieved_athlete is not None
        assert retrieved_athlete.last_name == "Tester"

        all_athletes = await athlete_repo.list()
        assert len(all_athletes) >= 1

        retrieved_athlete.position = "Senior QA"
        updated_athlete = await athlete_repo.update(retrieved_athlete.id, retrieved_athlete)
        assert updated_athlete.position == "Senior QA"

        await athlete_repo.delete(created_athlete.id)
        deleted_athlete = await athlete_repo.get(created_athlete.id)
        assert deleted_athlete is None
