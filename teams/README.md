# Teams Microservice

Микросервис для управления командами и атлетами с реализацией структурных паттернов проектирования.

## 🏗️ Архитектура

Микросервис построен на FastAPI с использованием:
- **PostgreSQL** - база данных
- **SQLAlchemy** - ORM для работы с БД
- **asyncpg** - асинхронный драйвер PostgreSQL
- **Pydantic** - валидация данных

## 🎯 Реализованные паттерны проектирования

### Структурные паттерны (самописные)

1. **FACADE (Фасад)** - `src/services/team_service.py`
   - Упрощает работу с командами и атлетами через единый интерфейс
   - Скрывает сложность взаимодействия нескольких репозиториев

2. **DECORATOR (Декоратор)** - `src/db/repositories/logging_decorator.py`
   - Добавляет логирование и мониторинг к репозиториям
   - Измеряет время выполнения операций

3. **ADAPTER (Адаптер)** - `src/adapters/data_source_adapter.py`
   - Унифицирует работу с разными источниками данных (БД, внешний API)
   - Преобразует несовместимые форматы данных

### Другие паттерны

- **Singleton** - Database класс
- **Chain of Responsibility** - Обработка ошибок
- **Strategy** - Стратегия логирования
- **Repository** - Работа с данными

📚 **Подробная документация:** [DESIGN_PATTERNS.md](DESIGN_PATTERNS.md)

## 🚀 Запуск

### Установка зависимостей
```bash
uv sync
```

### Запуск сервера
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### Переменные окружения
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123456
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=test
```

## 📋 API Endpoints

### Основные endpoints

#### Teams
- `GET /teams/` - Получить все команды
- `GET /teams/{team_id}` - Получить команду по ID
- `POST /teams/` - Создать команду
- `PUT /teams/{team_id}` - Обновить команду
- `DELETE /teams/{team_id}` - Удалить команду

#### Athletes
- `GET /athletes/` - Получить всех атлетов
- `GET /athletes/{athlete_id}` - Получить атлета по ID
- `POST /athletes/` - Создать атлета
- `PUT /athletes/{athlete_id}` - Обновить атлета
- `DELETE /athletes/{athlete_id}` - Удалить атлета

### Демонстрация паттернов

#### FACADE Pattern
- `POST /patterns/facade/team-with-athletes` - Создание команды с атлетами
- `GET /patterns/facade/team/{team_id}/full-info` - Полная информация о команде
- `GET /patterns/facade/statistics` - Статистика по командам

#### DECORATOR Pattern
- `GET /patterns/decorator/teams-with-logging` - Команды с логированием
- `GET /patterns/decorator/team/{team_id}/with-logging` - Команда с логированием

#### ADAPTER Pattern
- `GET /patterns/adapter/teams-from-database` - Данные из БД через адаптер
- `GET /patterns/adapter/teams-from-external-api` - Данные из API через адаптер
- `GET /patterns/adapter/teams-merged` - Объединённые данные

#### Сводка
- `GET /patterns/all-patterns-summary` - Информация обо всех паттернах

## 📖 Документация API

После запуска сервера доступна по адресу:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## 🏛️ Структура проекта

```
teams/
├── src/
│   ├── adapters/              # ПАТТЕРН: Adapter
│   │   ├── __init__.py
│   │   └── data_source_adapter.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── teams.py
│   │   │   ├── athletes.py
│   │   │   └── patterns_demo.py
│   │   ├── schemas/
│   │   └── dependencies.py
│   ├── db/
│   │   ├── repositories/
│   │   │   ├── base.py
│   │   │   ├── team_repository.py
│   │   │   ├── athlete_repository.py
│   │   │   └── logging_decorator.py  # ПАТТЕРН: Decorator
│   │   ├── database.py        # ПАТТЕРН: Singleton
│   │   └── models.py
│   └── services/
│       ├── team_service.py    # ПАТТЕРН: Facade
│       ├── error_handlers.py  # ПАТТЕРН: Chain of Responsibility
│       ├── logger.py
│       └── logger_strategies.py  # ПАТТЕРН: Strategy
├── config.py
├── main.py
├── pyproject.toml
├── README.md
└── DESIGN_PATTERNS.md
```

## 🧪 Тестирование паттернов

1. Запустите сервер
2. Откройте Swagger UI: `http://localhost:8080/docs`
3. Перейдите в раздел "Design Patterns Demo"
4. Протестируйте каждый endpoint

## 📝 Примеры использования

### Facade Pattern
```python
from src.services import TeamServiceFacade

team_service = TeamServiceFacade(team_repo, athlete_repo)

# Создать команду с атлетами за одну операцию
team = await team_service.create_team_with_athletes(
    team_data=team_data,
    athletes_data=[athlete1, athlete2, athlete3]
)

# Получить полную статистику
stats = await team_service.get_teams_statistics()
```

### Decorator Pattern
```python
from src.db.repositories import RepositoryLoggingDecorator

# Обернуть репозиторий декоратором
decorated_repo = RepositoryLoggingDecorator(team_repo)

# Все операции автоматически логируются
teams = await decorated_repo.list()
```

### Adapter Pattern
```python
from src.adapters import DataSourceAdapter, DatabaseDataSource, ExternalAPIDataSource

# Работа с БД
db_source = DatabaseDataSource(team_repo)
adapter = DataSourceAdapter(db_source)
teams = await adapter.fetch_teams_unified()

# Работа с внешним API (формат автоматически адаптируется)
api_source = ExternalAPIDataSource()
adapter = DataSourceAdapter(api_source)
teams = await adapter.fetch_teams_unified()
```

## 🔧 Разработка

### Установка Python 3.12
```bash
# Уже установлен в Replit окружении
```

### Линтинг и форматирование
```bash
# TODO: добавить pre-commit hooks
```

## 📄 Лицензия

MIT
