from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..db.models import Team, Athlete
from ..db.repositories import TeamRepository, AthleteRepository
from ...services import logger


class IDataSource(ABC):
    """
    Интерфейс источника данных.
    Определяет общий контракт для всех источников данных.
    """
    
    @abstractmethod
    async def get_teams(self) -> List[Dict[str, Any]]:
        """Получить список команд из источника"""
        pass
    
    @abstractmethod
    async def get_team_by_id(self, team_id: int) -> Optional[Dict[str, Any]]:
        """Получить команду по ID"""
        pass


class DatabaseDataSource(IDataSource):
    """
    Реализация источника данных для работы с локальной БД.
    Это существующая система (Adaptee).
    """
    
    def __init__(self, team_repo: TeamRepository):
        self._team_repo = team_repo
    
    async def get_teams(self) -> List[Dict[str, Any]]:
        """Получить команды из базы данных"""
        teams = await self._team_repo.list()
        return [self._team_to_dict(team) for team in teams]
    
    async def get_team_by_id(self, team_id: int) -> Optional[Dict[str, Any]]:
        """Получить команду по ID из базы данных"""
        team = await self._team_repo.get(team_id)
        return self._team_to_dict(team) if team else None
    
    def _team_to_dict(self, team: Team) -> Dict[str, Any]:
        """Конвертация ORM модели в словарь"""
        return {
            "id": team.id,
            "name": team.name,
            "country": team.country,
            "city": team.city,
            "founded_year": team.founded_year,
            "logo_url": team.logo_url
        }


class ExternalAPIDataSource(IDataSource):
    """
    Реализация источника данных для работы с внешним API.
    Это несовместимая система, которую нужно адаптировать.
    """
    
    def __init__(self, api_url: str = "https://api.example.com"):
        self._api_url = api_url
        self._cache: Dict[int, Dict[str, Any]] = {}
    
    async def get_teams(self) -> List[Dict[str, Any]]:
        """
        Эмуляция получения данных из внешнего API.
        В реальности здесь был бы HTTP запрос.
        """
        mock_api_response = [
            {
                "teamId": 1,
                "teamName": "External Team 1",
                "location": {"country": "USA", "city": "New York"},
                "yearFounded": 2000,
                "logoImage": "http://example.com/logo1.png"
            },
            {
                "teamId": 2,
                "teamName": "External Team 2",
                "location": {"country": "UK", "city": "London"},
                "yearFounded": 1995,
                "logoImage": "http://example.com/logo2.png"
            }
        ]
        
        logger.info(f"[EXTERNAL API] Fetching teams from {self._api_url}")
        return mock_api_response
    
    async def get_team_by_id(self, team_id: int) -> Optional[Dict[str, Any]]:
        """Получить команду по ID из внешнего API"""
        teams = await self.get_teams()
        for team in teams:
            if team.get("teamId") == team_id:
                return team
        return None


class DataSourceAdapter:
    """
    ПАТТЕРН: ADAPTER (Адаптер)
    
    Преобразует интерфейс несовместимого внешнего API в интерфейс,
    который ожидает наше приложение.
    
    Адаптер позволяет работать с разными источниками данных
    (локальная БД, внешний API, файлы и т.д.) через единый интерфейс.
    
    Преимущества:
    - Позволяет интегрировать несовместимые интерфейсы
    - Переиспользование существующего кода
    - Соблюдение принципа единственной ответственности (SRP)
    - Легко добавлять новые источники данных
    """
    
    def __init__(self, data_source: IDataSource):
        """
        Args:
            data_source: Источник данных (локальная БД или внешний API)
        """
        self._data_source = data_source
    
    async def fetch_teams_unified(self) -> List[Dict[str, Any]]:
        """
        Унифицированный метод получения команд из любого источника.
        Адаптирует данные к единому формату.
        """
        raw_data = await self._data_source.get_teams()
        
        if isinstance(self._data_source, ExternalAPIDataSource):
            return self._adapt_external_api_format(raw_data)
        
        return raw_data
    
    async def fetch_team_by_id_unified(self, team_id: int) -> Optional[Dict[str, Any]]:
        """
        Унифицированный метод получения команды по ID из любого источника.
        """
        raw_data = await self._data_source.get_team_by_id(team_id)
        
        if raw_data is None:
            return None
        
        if isinstance(self._data_source, ExternalAPIDataSource):
            return self._adapt_external_api_team(raw_data)
        
        return raw_data
    
    def _adapt_external_api_format(self, api_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Адаптация формата внешнего API к нашему внутреннему формату.
        
        Внешний API возвращает:
        {
            "teamId": 1,
            "teamName": "Name",
            "location": {"country": "USA", "city": "NYC"},
            "yearFounded": 2000,
            "logoImage": "url"
        }
        
        Наш формат:
        {
            "id": 1,
            "name": "Name",
            "country": "USA",
            "city": "NYC",
            "founded_year": 2000,
            "logo_url": "url"
        }
        """
        adapted_teams = []
        
        for team in api_data:
            adapted_team = {
                "id": team.get("teamId"),
                "name": team.get("teamName"),
                "country": team.get("location", {}).get("country"),
                "city": team.get("location", {}).get("city"),
                "founded_year": team.get("yearFounded"),
                "logo_url": team.get("logoImage"),
                "source": "external_api"
            }
            adapted_teams.append(adapted_team)
        
        logger.info(f"[ADAPTER] Adapted {len(adapted_teams)} teams from external API format")
        return adapted_teams
    
    def _adapt_external_api_team(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Адаптация одной команды из внешнего API"""
        return {
            "id": team_data.get("teamId"),
            "name": team_data.get("teamName"),
            "country": team_data.get("location", {}).get("country"),
            "city": team_data.get("location", {}).get("city"),
            "founded_year": team_data.get("yearFounded"),
            "logo_url": team_data.get("logoImage"),
            "source": "external_api"
        }
    
    async def merge_data_from_multiple_sources(
        self, 
        sources: List[IDataSource]
    ) -> List[Dict[str, Any]]:
        """
        Дополнительная функциональность: объединение данных из нескольких источников.
        """
        all_teams = []
        
        for source in sources:
            adapter = DataSourceAdapter(source)
            teams = await adapter.fetch_teams_unified()
            all_teams.extend(teams)
        
        logger.info(f"[ADAPTER] Merged data from {len(sources)} sources: {len(all_teams)} total teams")
        return all_teams
