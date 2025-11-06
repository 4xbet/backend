import pytest
from unittest.mock import Mock, AsyncMock
from datetime import date
from fastapi import HTTPException, status
from src.api.v1.athletes import get_athletes, get_athlete, create_athlete, update_athlete, delete_athlete
from src.api.schemas.athletes import AthleteCreate, AthleteUpdate
from src.db.models import Athlete, Team


@pytest.mark.unit
class TestAthletesAPI:
    """Unit tests for athletes API endpoints."""

    @pytest.fixture
    def mock_athlete_repo(self):
        """Create mock athlete repository."""
        repo = Mock()
        repo.list = AsyncMock()
        repo.get = AsyncMock()
        repo.create = AsyncMock()
        repo.update = AsyncMock()
        repo.delete = AsyncMock()
        return repo

    @pytest.fixture
    def mock_team_repo(self):
        """Create mock team repository."""
        repo = Mock()
        repo.get = AsyncMock()
        return repo

    @pytest.fixture
    def sample_athlete(self):
        """Create sample athlete data."""
        return Athlete(
            id=1,
            first_name="John",
            last_name="Doe",
            date_of_birth=date(2000, 1, 1),
            position="Forward",
            team_id=1
        )

    @pytest.fixture
    def sample_athletes(self, sample_athlete):
        """Create sample list of athletes."""
        athlete2 = Athlete(
            id=2,
            first_name="Jane",
            last_name="Smith",
            date_of_birth=date(2001, 2, 15),
            position="Defender",
            team_id=1
        )
        return [sample_athlete, athlete2]

    @pytest.mark.asyncio
    async def test_get_athletes_success(self, mock_athlete_repo, sample_athletes):
        """Test getting all athletes successfully."""
        # Arrange
        mock_athlete_repo.list.return_value = sample_athletes
        
        # Act
        result = await get_athletes(athlete_repo=mock_athlete_repo)
        
        # Assert
        assert result == sample_athletes
        mock_athlete_repo.list.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_athlete_by_id_success(self, mock_athlete_repo, sample_athlete):
        """Test getting athlete by ID successfully."""
        # Arrange
        mock_athlete_repo.get.return_value = sample_athlete
        
        # Act
        result = await get_athlete(athlete_id=1, athlete_repo=mock_athlete_repo)
        
        # Assert
        assert result == sample_athlete
        mock_athlete_repo.get.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_athlete_by_id_not_found(self, mock_athlete_repo):
        """Test getting non-existent athlete."""
        # Arrange
        mock_athlete_repo.get.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_athlete(athlete_id=999, athlete_repo=mock_athlete_repo)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Athlete with ID 999 not found" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_create_athlete_success(self, mock_athlete_repo, mock_team_repo, sample_athlete):
        """Test creating a new athlete successfully."""
        # Arrange
        athlete_create = AthleteCreate(
            first_name="New",
            last_name="Player",
            date_of_birth=date(2002, 5, 10),
            position="Midfielder",
            team_id=1
        )
        mock_team_repo.get.return_value = Team(id=1, name="Test Team", country="USA", founded_year=2020)
        mock_athlete_repo.create.return_value = sample_athlete
        
        # Act
        result = await create_athlete(
            athlete=athlete_create,
            athlete_repo=mock_athlete_repo,
            team_repo=mock_team_repo
        )
        
        # Assert
        assert result == sample_athlete
        mock_team_repo.get.assert_called_once_with(1)
        mock_athlete_repo.create.assert_called_once()
        created_athlete = mock_athlete_repo.create.call_args[0][0]
        assert created_athlete.first_name == "New"
        assert created_athlete.last_name == "Player"

    @pytest.mark.asyncio
    async def test_create_athlete_team_not_found(self, mock_athlete_repo, mock_team_repo):
        """Test creating athlete with non-existent team."""
        # Arrange
        athlete_create = AthleteCreate(first_name="New", last_name="Player", team_id=999)
        mock_team_repo.get.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await create_athlete(
                athlete=athlete_create,
                athlete_repo=mock_athlete_repo,
                team_repo=mock_team_repo
            )
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Team with ID 999 not found" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_update_athlete_success(self, mock_athlete_repo, mock_team_repo, sample_athlete):
        """Test updating athlete successfully."""
        # Arrange
        athlete_update = AthleteUpdate(first_name="Updated Name")
        existing_athlete = Athlete(id=1, first_name="Old Name", last_name="Doe", team_id=1)
        updated_athlete = Athlete(id=1, first_name="Updated Name", last_name="Doe", team_id=1)
        mock_athlete_repo.get.return_value = existing_athlete
        mock_athlete_repo.update.return_value = updated_athlete
        
        # Act
        result = await update_athlete(
            athlete_id=1,
            athlete_update=athlete_update,
            athlete_repo=mock_athlete_repo,
            team_repo=mock_team_repo
        )
        
        # Assert
        assert result == updated_athlete
        mock_athlete_repo.get.assert_called_once_with(1)
        mock_athlete_repo.update.assert_called_once()
        assert existing_athlete.first_name == "Updated Name"

    @pytest.mark.asyncio
    async def test_update_athlete_not_found(self, mock_athlete_repo, mock_team_repo):
        """Test updating non-existent athlete."""
        # Arrange
        athlete_update = AthleteUpdate(first_name="Updated Name")
        mock_athlete_repo.get.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await update_athlete(
                athlete_id=999,
                athlete_update=athlete_update,
                athlete_repo=mock_athlete_repo,
                team_repo=mock_team_repo
            )
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_update_athlete_team_not_found(self, mock_athlete_repo, mock_team_repo):
        """Test updating athlete with non-existent team."""
        # Arrange
        athlete_update = AthleteUpdate(team_id=999)
        existing_athlete = Athlete(id=1, first_name="Test", last_name="Player", team_id=1)
        mock_athlete_repo.get.return_value = existing_athlete
        mock_team_repo.get.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await update_athlete(
                athlete_id=1,
                athlete_update=athlete_update,
                athlete_repo=mock_athlete_repo,
                team_repo=mock_team_repo
            )
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Team with ID 999 not found" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_delete_athlete_success(self, mock_athlete_repo, sample_athlete):
        """Test deleting athlete successfully."""
        # Arrange
        mock_athlete_repo.get.return_value = sample_athlete
        
        # Act
        result = await delete_athlete(athlete_id=1, athlete_repo=mock_athlete_repo)
        
        # Assert
        assert result is None
        mock_athlete_repo.get.assert_called_once_with(1)
        mock_athlete_repo.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_athlete_not_found(self, mock_athlete_repo):
        """Test deleting non-existent athlete."""
        # Arrange
        mock_athlete_repo.get.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await delete_athlete(athlete_id=999, athlete_repo=mock_athlete_repo)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND