import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.db.repositories.team_repository import TeamRepository
from src.db.repositories.athlete_repository import AthleteRepository
from src.db.models import Team, Athlete


@pytest.mark.unit
class TestTeamRepository:
    """Unit tests for TeamRepository."""

    @pytest.fixture
    def mock_database(self):
        """Create mock database."""
        database = Mock()
        database.get_session = Mock()
        return database

    @pytest.fixture
    def team_repository(self, mock_database):
        """Create TeamRepository instance."""
        return TeamRepository(mock_database)

    def test_team_repository_initialization(self, team_repository, mock_database):
        """Test TeamRepository initialization."""
        # Assert
        assert team_repository.database == mock_database
        assert team_repository.get_model() == Team

    def test_team_repository_inherits_base_repository(self, team_repository):
        """Test that TeamRepository inherits from BaseRepository."""
        # Assert
        from src.db.repositories.base import BaseRepository
        assert isinstance(team_repository, BaseRepository)

    @pytest.mark.asyncio
    async def test_team_repository_methods_exist(self, team_repository):
        """Test that TeamRepository has all expected methods."""
        # Assert
        assert hasattr(team_repository, 'get')
        assert hasattr(team_repository, 'list')
        assert hasattr(team_repository, 'list_all')
        assert hasattr(team_repository, 'create')
        assert hasattr(team_repository, 'update')
        assert hasattr(team_repository, 'delete')


@pytest.mark.unit
class TestAthleteRepository:
    """Unit tests for AthleteRepository."""

    @pytest.fixture
    def mock_database(self):
        """Create mock database."""
        database = Mock()
        database.get_session = Mock()
        return database

    @pytest.fixture
    def athlete_repository(self, mock_database):
        """Create AthleteRepository instance."""
        return AthleteRepository(mock_database)

    def test_athlete_repository_initialization(self, athlete_repository, mock_database):
        """Test AthleteRepository initialization."""
        # Assert
        assert athlete_repository.database == mock_database
        assert athlete_repository.get_model() == Athlete

    def test_athlete_repository_inherits_base_repository(self, athlete_repository):
        """Test that AthleteRepository inherits from BaseRepository."""
        # Assert
        from src.db.repositories.base import BaseRepository
        assert isinstance(athlete_repository, BaseRepository)

    @pytest.mark.asyncio
    async def test_athlete_repository_methods_exist(self, athlete_repository):
        """Test that AthleteRepository has all expected methods."""
        # Assert
        assert hasattr(athlete_repository, 'get')
        assert hasattr(athlete_repository, 'list')
        assert hasattr(athlete_repository, 'list_all')
        assert hasattr(athlete_repository, 'create')
        assert hasattr(athlete_repository, 'update')
        assert hasattr(athlete_repository, 'delete')


@pytest.mark.unit
class TestRepositoryIntegration:
    """Integration tests for repositories."""

    @pytest.fixture
    def mock_database(self):
        """Create mock database."""
        database = Mock()
        database.get_session = Mock()
        return database

    def test_repository_model_consistency(self, mock_database):
        """Test that repositories return correct models."""
        # Arrange
        team_repo = TeamRepository(mock_database)
        athlete_repo = AthleteRepository(mock_database)
        
        # Act & Assert
        assert team_repo.get_model() == Team
        assert athlete_repo.get_model() == Athlete
        assert team_repo.get_model() != athlete_repo.get_model()

    def test_repository_polymorphism(self, mock_database):
        """Test repository polymorphism."""
        # Arrange
        team_repo = TeamRepository(mock_database)
        athlete_repo = AthleteRepository(mock_database)
        
        # Act
        models = [repo.get_model() for repo in [team_repo, athlete_repo]]
        
        # Assert
        assert models[0] == Team
        assert models[1] == Athlete
        assert len(set(models)) == 2  # Different models