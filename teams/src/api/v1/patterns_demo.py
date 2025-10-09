from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ...db.repositories import (
    TeamRepository, 
    AthleteRepository,
    team_repository_instance,
    athlete_repository_instance,
    team_repository_with_logging,
    athlete_repository_with_logging
)
from ...services.team_service import TeamServiceFacade 
from ...adapters import DataSourceAdapter, DatabaseDataSource, ExternalAPIDataSource
from ..schemas.teams import TeamCreate
from ..schemas.athletes import AthleteCreate

router = APIRouter(prefix="/patterns", tags=["Design Patterns Demo"])


def get_team_service() -> TeamServiceFacade:
    """Dependency для получения TeamServiceFacade (паттерн Facade)"""
    return TeamServiceFacade(team_repository_instance, athlete_repository_instance)


@router.post("/facade/team-with-athletes", status_code=status.HTTP_201_CREATED)
async def create_team_with_athletes_facade(
    team_data: TeamCreate,
    athletes_data: List[AthleteCreate],
    team_service: TeamServiceFacade = Depends(get_team_service)
):
    """
    ДЕМОНСТРАЦИЯ ПАТТЕРНА FACADE (Фасад)
    
    Упрощенное создание команды вместе с несколькими атлетами за одну операцию.
    Фасад скрывает сложность работы с двумя разными репозиториями.
    """
    result = await team_service.create_team_with_athletes(team_data, athletes_data)
    return {
        "message": "ПАТТЕРН FACADE использован успешно",
        "description": "Создана команда вместе с атлетами через упрощенный интерфейс",
        "team": result
    }


@router.get("/facade/team/{team_id}/full-info")
async def get_team_full_info_facade(
    team_id: int,
    team_service: TeamServiceFacade = Depends(get_team_service)
):
    """
    ДЕМОНСТРАЦИЯ ПАТТЕРНА FACADE (Фасад)
    
    Получение полной информации о команде включая статистику атлетов.
    Фасад объединяет данные из разных источников.
    """
    result = await team_service.get_team_full_info(team_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found"
        )
    
    return {
        "message": "ПАТТЕРН FACADE использован успешно",
        "description": "Получена агрегированная информация о команде",
        "data": result
    }


@router.get("/facade/statistics")
async def get_teams_statistics_facade(
    team_service: TeamServiceFacade = Depends(get_team_service)
):
    """
    ДЕМОНСТРАЦИЯ ПАТТЕРНА FACADE (Фасад)
    
    Получение статистики по всем командам.
    Фасад инкапсулирует сложную бизнес-логику.
    """
    stats = await team_service.get_teams_statistics()
    return {
        "message": "ПАТТЕРН FACADE использован успешно",
        "description": "Получена статистика по всем командам",
        "statistics": stats
    }


@router.get("/decorator/teams-with-logging")
async def get_teams_with_logging():
    """
    ДЕМОНСТРАЦИЯ ПАТТЕРНА DECORATOR (Декоратор)
    
    Получение списка команд с автоматическим логированием операций.
    Декоратор добавляет функциональность логирования без изменения оригинального репозитория.
    """
    teams = await team_repository_with_logging.list()
    stats = team_repository_with_logging.get_statistics()
    
    return {
        "message": "ПАТТЕРН DECORATOR использован успешно",
        "description": "Операции с репозиторием логируются автоматически. Проверьте логи!",
        "teams": teams,
        "decorator_stats": stats
    }


@router.get("/decorator/team/{team_id}/with-logging")
async def get_team_with_logging(team_id: int):
    """
    ДЕМОНСТРАЦИЯ ПАТТЕРНА DECORATOR (Декоратор)
    
    Получение команды по ID с логированием.
    """
    team = await team_repository_with_logging.get(team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found"
        )
    
    stats = team_repository_with_logging.get_statistics()
    
    return {
        "message": "ПАТТЕРН DECORATOR использован успешно",
        "description": "Операция get() была залогирована",
        "team": team,
        "decorator_stats": stats
    }


@router.get("/adapter/teams-from-database")
async def get_teams_from_database():
    """
    ДЕМОНСТРАЦИЯ ПАТТЕРНА ADAPTER (Адаптер)
    
    Получение команд из локальной базы данных через адаптер.
    Адаптер предоставляет единый интерфейс для разных источников данных.
    """
    db_source = DatabaseDataSource(team_repository_instance)
    adapter = DataSourceAdapter(db_source)
    
    teams = await adapter.fetch_teams_unified()
    
    return {
        "message": "ПАТТЕРН ADAPTER использован успешно",
        "description": "Данные получены из локальной БД через унифицированный интерфейс",
        "source": "database",
        "teams": teams
    }


@router.get("/adapter/teams-from-external-api")
async def get_teams_from_external_api():
    """
    ДЕМОНСТРАЦИЯ ПАТТЕРНА ADAPTER (Адаптер)
    
    Получение команд из внешнего API через адаптер.
    Адаптер преобразует несовместимый формат внешнего API в наш внутренний формат.
    """
    external_source = ExternalAPIDataSource(api_url="https://api.example.com")
    adapter = DataSourceAdapter(external_source)
    
    teams = await adapter.fetch_teams_unified()
    
    return {
        "message": "ПАТТЕРН ADAPTER использован успешно",
        "description": "Данные из внешнего API адаптированы к нашему формату",
        "source": "external_api",
        "teams": teams
    }


@router.get("/adapter/teams-merged")
async def get_teams_from_multiple_sources():
    """
    ДЕМОНСТРАЦИЯ ПАТТЕРНА ADAPTER (Адаптер)
    
    Объединение данных из нескольких источников через адаптер.
    """
    db_source = DatabaseDataSource(team_repository_instance)
    external_source = ExternalAPIDataSource()
    
    adapter = DataSourceAdapter(db_source)
    merged_teams = await adapter.merge_data_from_multiple_sources([db_source, external_source])
    
    return {
        "message": "ПАТТЕРН ADAPTER использован успешно",
        "description": "Данные объединены из нескольких источников (БД + внешний API)",
        "total_teams": len(merged_teams),
        "teams": merged_teams
    }


@router.get("/all-patterns-summary")
async def get_all_patterns_summary():
    """
    Сводка по всем реализованным структурным паттернам
    """
    return {
        "patterns": {
            "facade": {
                "name": "FACADE (Фасад)",
                "description": "Упрощает работу со сложной подсистемой",
                "location": "teams/src/services/team_service.py",
                "endpoints": [
                    "POST /patterns/facade/team-with-athletes",
                    "GET /patterns/facade/team/{team_id}/full-info",
                    "GET /patterns/facade/statistics"
                ]
            },
            "decorator": {
                "name": "DECORATOR (Декоратор)",
                "description": "Динамически добавляет функциональность (логирование)",
                "location": "teams/src/db/repositories/logging_decorator.py",
                "endpoints": [
                    "GET /patterns/decorator/teams-with-logging",
                    "GET /patterns/decorator/team/{team_id}/with-logging"
                ]
            },
            "adapter": {
                "name": "ADAPTER (Адаптер)",
                "description": "Преобразует несовместимые интерфейсы",
                "location": "teams/src/adapters/data_source_adapter.py",
                "endpoints": [
                    "GET /patterns/adapter/teams-from-database",
                    "GET /patterns/adapter/teams-from-external-api",
                    "GET /patterns/adapter/teams-merged"
                ]
            }
        },
        "total_patterns": 3,
        "type": "Структурные паттерны проектирования"
    }
