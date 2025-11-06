import pytest
from datetime import date
from unittest.mock import AsyncMock, MagicMock
from src.services.team_service import TeamServiceFacade
from src.db.models import Team, Athlete
from src.api.schemas.teams import TeamCreate, TeamUpdate
from src.api.schemas.athletes import AthleteCreate


@pytest.mark.unit
class TestTeamServiceFacade:
    """Unit tests for TeamServiceFacade."""

    @pytest.fixture
    def mock_team_repo(self):
        """Create a mock team repository."""
        return AsyncMock()

    @pytest.fixture
    def mock_athlete_repo(self):
        """Create a mock athlete repository."""
        return AsyncMock()

    @pytest.fixture
    def team_service(self, mock_team_repo, mock_athlete_repo):
        """Create a team service with mocked repositories."""
        return TeamServiceFacade(mock_team_repo, mock_athlete_repo)

    @pytest.fixture
    def team_create_data(self):
        """Sample team creation data."""
        return TeamCreate(
            name="Test Team",
            country="USA",
            city="New York",
            founded_year=2020,
            logo_url="https://example.com/logo.png"
        )

    @pytest.fixture
    def athlete_create_data(self):
        """Sample athlete creation data."""
        return [
            AthleteCreate(
                first_name="John",
                last_name="Doe",
                date_of_birth=date(2000, 1, 1),
                position="Forward"
            ),
            AthleteCreate(
                first_name="Jane",
                last_name="Smith",
                date_of_birth=date(2001, 2, 15),
                position="Defender"
            )
        ]

    async def test_create_team_with_athletes_success(
        self, team_service, mock_team_repo, mock_athlete_repo,
        team_create_data, athlete_create_data
    ):
        """Test successful creation of team with athletes."""
        # Arrange
        created_team = Team(
            id=1,
            name=team_create_data.name,
            country=team_create_data.country,
            city=team_create_data.city,
            founded_year=team_create_data.founded_year,
            logo_url=team_create_data.logo_url
        )
        mock_team_repo.create.return_value = created_team
        mock_team_repo.get.return_value = created_team

        # Act
        result = await team_service.create_team_with_athletes(
            team_create_data, athlete_create_data
        )

        # Assert
        assert result == created_team
        mock_team_repo.create.assert_called_once()
        assert mock_athlete_repo.create.call_count == len(athlete_create_data)
        mock_team_repo.get.assert_called_once_with(1)

    async def test_get_team_full_info_success(
        self, team_service, mock_team_repo, mock_athlete_repo
    ):
        """Test successful retrieval of team full info."""
        # Arrange
        sample_team = Team(id=1, name="Test Team", country="USA", founded_year=2020)
        athletes = [
            Athlete(
                id=1, first_name="John", last_name="Doe",
                date_of_birth=date(2000, 1, 1), position="Forward", team_id=sample_team.id
            ),
            Athlete(
                id=2, first_name="Jane", last_name="Smith",
                date_of_birth=date(2001, 2, 15), position="Defender", team_id=sample_team.id
            )
        ]
        mock_team_repo.get.return_value = sample_team
        mock_athlete_repo.list_all.return_value = athletes

        # Act
        result = await team_service.get_team_full_info(sample_team.id)

        # Assert
        assert result is not None
        assert result["team"] == sample_team
        assert len(result["athletes"]) == 2
        assert result["athletes_count"] == 2
        assert result["average_age"] is not None

    async def test_get_team_full_info_team_not_found(
        self, team_service, mock_team_repo
    ):
        """Test get_team_full_info when team doesn't exist."""
        # Arrange
        mock_team_repo.get.return_value = None

        # Act
        result = await team_service.get_team_full_info(999)

        # Assert
        assert result is None
        mock_team_repo.get.assert_called_once_with(999)

    async def test_transfer_athlete_success(
        self, team_service, mock_team_repo, mock_athlete_repo
    ):
        """Test successful athlete transfer."""
        # Arrange
        athlete = Athlete(
            id=1, first_name="John", last_name="Doe",
            date_of_birth=date(2000, 1, 1), position="Forward", team_id=1
        )
        new_team = Team(id=2, name="New Team", country="USA", founded_year=2021)
        
        mock_athlete_repo.get.return_value = athlete
        mock_team_repo.get.return_value = new_team
        mock_athlete_repo.update.return_value = athlete

        # Act
        result = await team_service.transfer_athlete(1, 2)

        # Assert
        assert result == athlete
        assert result.team_id == 2
        mock_athlete_repo.get.assert_called_once_with(1)
        mock_team_repo.get.assert_called_once_with(2)
        mock_athlete_repo.update.assert_called_once()

    async def test_transfer_athlete_athlete_not_found(
        self, team_service, mock_athlete_repo
    ):
        """Test transfer athlete when athlete doesn't exist."""
        # Arrange
        mock_athlete_repo.get.return_value = None

        # Act
        result = await team_service.transfer_athlete(999, 1)

        # Assert
        assert result is None
        mock_athlete_repo.get.assert_called_once_with(999)

    async def test_transfer_athlete_team_not_found(
        self, team_service, mock_athlete_repo, mock_team_repo
    ):
        """Test transfer athlete when new team doesn't exist."""
        # Arrange
        athlete = Athlete(
            id=1, first_name="John", last_name="Doe",
            date_of_birth=date(2000, 1, 1), position="Forward", team_id=1
        )
        mock_athlete_repo.get.return_value = athlete
        mock_team_repo.get.return_value = None

        # Act
        result = await team_service.transfer_athlete(1, 999)

        # Assert
        assert result is None
        mock_athlete_repo.get.assert_called_once_with(1)
        mock_team_repo.get.assert_called_once_with(999)

    async def test_delete_team_cascade_success(
        self, team_service, mock_team_repo, mock_athlete_repo
    ):
        """Test successful cascade deletion of team."""
        # Arrange
        sample_team = Team(id=1, name="Test Team", country="USA", founded_year=2020)
        athletes = [
            Athlete(id=1, first_name="John", last_name="Doe",
                   date_of_birth=date(2000, 1, 1), position="Forward", team_id=sample_team.id),
            Athlete(id=2, first_name="Jane", last_name="Smith",
                   date_of_birth=date(2001, 2, 15), position="Defender", team_id=sample_team.id)
        ]
        mock_team_repo.get.return_value = sample_team
        mock_athlete_repo.list_all.return_value = athletes

        # Act
        result = await team_service.delete_team_cascade(sample_team.id)

        # Assert
        assert result is True
        mock_team_repo.get.assert_called_once_with(sample_team.id)
        mock_athlete_repo.list_all.assert_called_once()
        assert mock_athlete_repo.delete.call_count == 2
        mock_team_repo.delete.assert_called_once_with(sample_team.id)

    async def test_delete_team_cascade_team_not_found(
        self, team_service, mock_team_repo
    ):
        """Test cascade deletion when team doesn't exist."""
        # Arrange
        mock_team_repo.get.return_value = None

        # Act
        result = await team_service.delete_team_cascade(999)

        # Assert
        assert result is False
        mock_team_repo.get.assert_called_once_with(999)

    async def test_get_teams_statistics_success(
        self, team_service, mock_team_repo, mock_athlete_repo
    ):
        """Test successful retrieval of teams statistics."""
        # Arrange
        teams = [
            Team(id=1, name="Team USA", country="USA", founded_year=2020),
            Team(id=2, name="Team Canada", country="Canada", founded_year=2021),
            Team(id=3, name="Team USA 2", country="USA", founded_year=2022)
        ]
        athletes = [
            Athlete(id=1, first_name="John", last_name="Doe",
                   date_of_birth=date(2000, 1, 1), position="Forward", team_id=1),
            Athlete(id=2, first_name="Jane", last_name="Smith",
                   date_of_birth=date(2001, 2, 15), position="Defender", team_id=1),
            Athlete(id=3, first_name="Bob", last_name="Johnson",
                   date_of_birth=date(1999, 3, 20), position="Goalkeeper", team_id=2)
        ]
        mock_team_repo.list_all.return_value = teams
        mock_athlete_repo.list_all.return_value = athletes

        # Act
        result = await team_service.get_teams_statistics()

        # Assert
        assert result["total_teams"] == 3
        assert result["total_athletes"] == 3
        assert result["teams_by_country"]["USA"] == 2
        assert result["teams_by_country"]["Canada"] == 1
        assert result["largest_team"] == ("Team USA", 2)
        assert result["smallest_team"] == ("Team USA 2", 0)

    async def test_get_teams_statistics_empty(
        self, team_service, mock_team_repo, mock_athlete_repo
    ):
        """Test teams statistics with empty database."""
        # Arrange
        mock_team_repo.list_all.return_value = []
        mock_athlete_repo.list_all.return_value = []

        # Act
        result = await team_service.get_teams_statistics()

        # Assert
        assert result["total_teams"] == 0
        assert result["total_athletes"] == 0
        assert result["teams_by_country"] == {}
        assert result["largest_team"] is None
        assert result["smallest_team"] is None

    def test_calculate_average_age_empty_list(self, team_service):
        """Test average age calculation with empty athlete list."""
        # Act
        result = team_service._calculate_average_age([])

        # Assert
        assert result is None

    def test_calculate_average_age_single_athlete(self, team_service):
        """Test average age calculation with single athlete."""
        # Arrange
        athlete = Athlete(
            id=1, first_name="John", last_name="Doe",
            date_of_birth=date(2000, 1, 1), position="Forward", team_id=1
        )

        # Act
        result = team_service._calculate_average_age([athlete])

        # Assert
        assert result is not None
        assert isinstance(result, float)