import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.adapters.data_source_adapter import DatabaseDataSource, ExternalAPIDataSource, IDataSource, DataSourceAdapter
from src.db.models import Team


@pytest.mark.unit
class TestDatabaseDataSource:
    """Unit tests for DatabaseDataSource."""

    @pytest.fixture
    def mock_team_repo(self):
        """Create mock team repository."""
        repo = Mock()
        repo.list_all = AsyncMock()
        repo.get = AsyncMock()
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
        mock_team_repo.list_all.return_value = sample_teams
        data_source = DatabaseDataSource(team_repo=mock_team_repo)
        
        # Act
        result = await data_source.get_teams()
        
        # Assert
        assert len(result) == 2
        assert result[0]["name"] == "Test Team"
        assert result[1]["name"] == "Another Team"
        mock_team_repo.list_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_team_by_id_success(self, mock_team_repo, sample_team):
        """Test getting team by ID successfully."""
        # Arrange
        mock_team_repo.get.return_value = sample_team
        data_source = DatabaseDataSource(team_repo=mock_team_repo)
        
        # Act
        result = await data_source.get_team_by_id(1)
        
        # Assert
        assert result is not None
        assert result["name"] == "Test Team"
        mock_team_repo.get.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_team_by_id_not_found(self, mock_team_repo):
        """Test getting non-existent team."""
        # Arrange
        mock_team_repo.get.return_value = None
        data_source = DatabaseDataSource(team_repo=mock_team_repo)
        
        # Act
        result = await data_source.get_team_by_id(999)
        
        # Assert
        assert result is None
        mock_team_repo.get.assert_called_once_with(999)


@pytest.mark.unit
class TestExternalAPIDataSource:
    """Unit tests for ExternalApiAdapter."""

    @pytest.fixture
    def mock_external_api_source(self):
        """Create mock external API data source."""
        source = Mock(spec=ExternalAPIDataSource)
        source.get_teams = AsyncMock()
        source.get_team_by_id = AsyncMock()
        return source

    @pytest.fixture
    def sample_external_teams(self):
        """
        Create sample external teams data that matches the adapter's expected input format.
        Note the use of 'teamId', 'teamName', and the nested 'location' dictionary.
        """
        return [
            {
                "teamId": 101,
                "teamName": "External Team 1",
                "location": {"city": "External City 1", "country": "External Country 1"},
                "yearFounded": 1999,
                "logoImage": "https://example.com/ext_logo1.png",
            },
            {
                "teamId": 102,
                "teamName": "External Team 2",
                "location": {"city": "External City 2", "country": "External Country 2"},
                "yearFounded": 2005,
                "logoImage": "https://example.com/ext_logo2.png",
            }
        ]

    @pytest.fixture
    def sample_external_team_details(self):
        """
        Create sample external team details data that matches the adapter's expected input format.
        """
        return {
            "teamId": 101,
            "teamName": "External Team 1",
            "location": {"city": "External City", "country": "External Country"},
            "yearFounded": 1999,
            "logoImage": "https://example.com/ext_logo.png"
        }

    @pytest.mark.asyncio
    async def test_get_teams_adapter_success(self, mock_external_api_source, sample_external_teams):
        """Test getting teams via adapter successfully."""
        # Arrange
        mock_external_api_source.get_teams.return_value = sample_external_teams
        adapter = DataSourceAdapter(mock_external_api_source)
        
        # Act
        result = await adapter.fetch_teams_unified()
        
        # Assert
        assert len(result) == 2
        # Check that the data was correctly mapped to the unified format
        assert result[0]["name"] == "External Team 1"
        assert result[1]["name"] == "External Team 2"
        assert result[0]["country"] == "External Country 1"
        assert result[1]["city"] == "External City 2"
        mock_external_api_source.get_teams.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_get_team_by_id_adapter_success(self, mock_external_api_source, sample_external_team_details):
        """Test getting team by ID via adapter successfully."""
        # Arrange
        mock_external_api_source.get_team_by_id.return_value = sample_external_team_details
        adapter = DataSourceAdapter(mock_external_api_source)
        
        # Act
        result = await adapter.fetch_team_by_id_unified(101)
        
        # Assert
        assert result is not None
        # Check that the data was correctly mapped to the unified format
        assert result["name"] == "External Team 1"
        assert result["city"] == "External City"
        assert result["country"] == "External Country"
        assert result["founded_year"] == 1999
        assert result["logo_url"] == "https://example.com/ext_logo.png"
        mock_external_api_source.get_team_by_id.assert_awaited_once_with(101)

    @pytest.mark.asyncio
    async def test_adapter_interface_implementation(self):
        """Test that adapters implement the IDataSource interface."""
        # Assert
        assert issubclass(DatabaseDataSource, IDataSource)
        assert issubclass(ExternalAPIDataSource, IDataSource)