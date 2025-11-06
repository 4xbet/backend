import pytest
from unittest.mock import Mock, AsyncMock, patch
from fastapi import HTTPException, status
from src.api.v1.teams import get_teams, get_team, create_team, update_team, delete_team
from src.api.schemas.teams import TeamCreate, TeamUpdate
from src.db.models import Team


@pytest.mark.unit
class TestTeamsAPI:
    """Unit tests for teams API endpoints."""

    @pytest.fixture
    def mock_team_repo(self):
        """Create mock team repository."""
        repo = Mock()
        repo.list = AsyncMock()
        repo.get = AsyncMock()
        repo.create = AsyncMock()
        repo.update = AsyncMock()
        repo.delete = AsyncMock()
        return repo

    @pytest.fixture
    def sample_team(self):
        """Create sample team data."""
        return Team(
            id=1,
            name="Test Team",
            country="USA",
            city="New York",
            founded_year=2020,
            logo_url="https://example.com/logo.png"
        )

    @pytest.fixture
    def sample_teams(self, sample_team):
        """Create sample list of teams."""
        team2 = Team(
            id=2,
            name="Another Team",
            country="Canada",
            city="Toronto",
            founded_year=2021,
            logo_url="https://example.com/logo2.png"
        )
        return [sample_team, team2]

    @pytest.mark.asyncio
    async def test_get_teams_success(self, mock_team_repo, sample_teams):
        """Test getting all teams successfully."""
        # Arrange
        mock_team_repo.list.return_value = sample_teams
        
        # Act
        result = await get_teams(team_repo=mock_team_repo)
        
        # Assert
        assert result == sample_teams
        mock_team_repo.list.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_teams_empty_list(self, mock_team_repo):
        """Test getting teams when no teams exist."""
        # Arrange
        mock_team_repo.list.return_value = []
        
        # Act
        result = await get_teams(team_repo=mock_team_repo)
        
        # Assert
        assert result == []
        mock_team_repo.list.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_team_by_id_success(self, mock_team_repo, sample_team):
        """Test getting team by ID successfully."""
        # Arrange
        mock_team_repo.get.return_value = sample_team
        
        # Act
        result = await get_team(team_id=1, team_repo=mock_team_repo)
        
        # Assert
        assert result == sample_team
        mock_team_repo.get.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_team_by_id_not_found(self, mock_team_repo):
        """Test getting non-existent team."""
        # Arrange
        mock_team_repo.get.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_team(team_id=999, team_repo=mock_team_repo)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Team with ID 999 not found" in str(exc_info.value.detail)
        mock_team_repo.get.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_create_team_success(self, mock_team_repo, sample_team):
        """Test creating a new team successfully."""
        # Arrange
        team_create = TeamCreate(
            name="New Team",
            country="UK",
            city="London",
            founded_year=2022,
            logo_url="https://example.com/new-logo.png"
        )
        mock_team_repo.create.return_value = sample_team
        
        # Act
        result = await create_team(team=team_create, team_repo=mock_team_repo)
        
        # Assert
        assert result == sample_team
        mock_team_repo.create.assert_called_once()
        created_team = mock_team_repo.create.call_args[0][0]
        assert created_team.name == "New Team"
        assert created_team.country == "UK"
        assert created_team.city == "London"
        assert created_team.founded_year == 2022
        assert created_team.logo_url == "https://example.com/new-logo.png"

    @pytest.mark.asyncio
    async def test_create_team_minimal_data(self, mock_team_repo, sample_team):
        """Test creating team with minimal required data."""
        # Arrange
        team_create = TeamCreate(
            name="Minimal Team",
            country="USA",
            founded_year=2023
        )
        mock_team_repo.create.return_value = sample_team
        
        # Act
        result = await create_team(team=team_create, team_repo=mock_team_repo)
        
        # Assert
        assert result == sample_team
        mock_team_repo.create.assert_called_once()
        created_team = mock_team_repo.create.call_args[0][0]
        assert created_team.name == "Minimal Team"
        assert created_team.country == "USA"
        assert created_team.founded_year == 2023
        assert created_team.city is None
        assert created_team.logo_url is None

    @pytest.mark.asyncio
    async def test_update_team_success(self, mock_team_repo, sample_team):
        """Test updating team successfully."""
        # Arrange
        team_update = TeamUpdate(
            name="Updated Team Name",
            country="Canada"
        )
        existing_team = Team(
            id=1,
            name="Original Name",
            country="USA",
            founded_year=2020
        )
        updated_team = Team(
            id=1,
            name="Updated Team Name",
            country="Canada",
            founded_year=2020
        )
        mock_team_repo.get.return_value = existing_team
        mock_team_repo.update.return_value = updated_team
        
        # Act
        result = await update_team(
            team_id=1,
            team_update=team_update,
            team_repo=mock_team_repo
        )
        
        # Assert
        assert result == updated_team
        mock_team_repo.get.assert_called_once_with(1)
        mock_team_repo.update.assert_called_once()
        assert existing_team.name == "Updated Team Name"
        assert existing_team.country == "Canada"

    @pytest.mark.asyncio
    async def test_update_team_not_found(self, mock_team_repo):
        """Test updating non-existent team."""
        # Arrange
        team_update = TeamUpdate(name="Updated Name")
        mock_team_repo.get.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await update_team(
                team_id=999,
                team_update=team_update,
                team_repo=mock_team_repo
            )
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Team with ID 999 not found" in str(exc_info.value.detail)
        mock_team_repo.get.assert_called_once_with(999)
        mock_team_repo.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_team_partial_data(self, mock_team_repo, sample_team):
        """Test updating team with partial data."""
        # Arrange
        team_update = TeamUpdate(city="New City")
        existing_team = Team(
            id=1,
            name="Test Team",
            country="USA",
            city="Old City",
            founded_year=2020
        )
        updated_team = Team(
            id=1,
            name="Test Team",
            country="USA",
            city="New City",
            founded_year=2020
        )
        mock_team_repo.get.return_value = existing_team
        mock_team_repo.update.return_value = updated_team
        
        # Act
        result = await update_team(
            team_id=1,
            team_update=team_update,
            team_repo=mock_team_repo
        )
        
        # Assert
        assert result == updated_team
        assert existing_team.city == "New City"
        assert existing_team.name == "Test Team"  # Unchanged
        assert existing_team.country == "USA"  # Unchanged

    @pytest.mark.asyncio
    async def test_delete_team_success(self, mock_team_repo, sample_team):
        """Test deleting team successfully."""
        # Arrange
        mock_team_repo.get.return_value = sample_team
        
        # Act
        result = await delete_team(team_id=1, team_repo=mock_team_repo)
        
        # Assert
        assert result is None
        mock_team_repo.get.assert_called_once_with(1)
        mock_team_repo.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_team_not_found(self, mock_team_repo):
        """Test deleting non-existent team."""
        # Arrange
        mock_team_repo.get.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await delete_team(team_id=999, team_repo=mock_team_repo)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Team with ID 999 not found" in str(exc_info.value.detail)
        mock_team_repo.get.assert_called_once_with(999)
        mock_team_repo.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_team_data_validation(self):
        """Test team data validation in schemas."""
        # Test valid team create data
        valid_data = TeamCreate(
            name="Valid Team",
            country="USA",
            founded_year=2020
        )
        assert valid_data.name == "Valid Team"
        assert valid_data.country == "USA"
        assert valid_data.founded_year == 2020

        # Test invalid team create data
        with pytest.raises(ValueError):
            TeamCreate(name="", country="USA", founded_year=2020)
        
        with pytest.raises(ValueError):
            TeamCreate(name="Team", country="U", founded_year=2020)
        
        with pytest.raises(ValueError):
            TeamCreate(name="Team", country="USA", founded_year=1700)

    @pytest.mark.asyncio
    async def test_team_update_validation(self):
        """Test team update data validation."""
        # Test valid team update data
        valid_update = TeamUpdate(name="Updated Name")
        assert valid_update.name == "Updated Name"
        assert valid_update.country is None

        # Test invalid team update data
        with pytest.raises(ValueError):
            TeamUpdate(name="")
        
        with pytest.raises(ValueError):
            TeamUpdate(country="U")
        
        with pytest.raises(ValueError):
            TeamUpdate(founded_year=1700)