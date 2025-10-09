# Overview

This is a FastAPI-based microservice for managing sports teams and athletes. The service demonstrates implementation of various structural design patterns (Facade, Decorator, Adapter) while providing CRUD operations for teams and athletes. Built with asynchronous Python using SQLAlchemy ORM and PostgreSQL.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Framework
- **FastAPI** - Modern async web framework for building APIs
- **Python 3.x** - Using async/await patterns throughout

## Database Layer
- **PostgreSQL** - Primary data store
- **SQLAlchemy 2.0** - Async ORM for database operations
- **asyncpg** - Asynchronous PostgreSQL driver
- **Database Singleton Pattern** - Single database connection instance managed via `Database` class

## Data Models
Two main entities with one-to-many relationship:
- **Team** - Stores team information (name, country, city, founded_year, logo_url)
- **Athlete** - Stores athlete information (first_name, last_name, date_of_birth, position) with foreign key to Team

## Repository Pattern
- **BaseRepository** - Generic abstract base providing CRUD operations
- **TeamRepository** - Team-specific repository extending BaseRepository
- **AthleteRepository** - Athlete-specific repository extending BaseRepository
- Repositories are instantiated as singletons and injected via FastAPI dependencies

## Design Patterns Implementation

### Структурные паттерны (самописные)

#### 1. Facade Pattern (`TeamServiceFacade`)
**Расположение:** `teams/src/services/team_service.py`

Simplifies complex operations involving multiple repositories. Provides unified interface for:
- Creating teams with athletes in single operation (`create_team_with_athletes`)
- Retrieving complete team information with all athletes (`get_team_full_info`)
- Managing complex multi-repository transactions (`delete_team_cascade`)
- Getting aggregated statistics (`get_teams_statistics`)

**Endpoints:** `/patterns/facade/*`

#### 2. Decorator Pattern (`RepositoryLoggingDecorator`)
**Расположение:** `teams/src/db/repositories/logging_decorator.py`

Dynamically adds logging and monitoring capabilities to repositories without modifying original code:
- Logs all CRUD operations with execution time
- Tracks operation count and statistics
- Can be toggled on/off dynamically
- Supports both `list()` and `list_all()` methods

**Endpoints:** `/patterns/decorator/*`

#### 3. Adapter Pattern (`DataSourceAdapter`)
**Расположение:** `teams/src/adapters/data_source_adapter.py`

Unifies access to different data sources through common interface:
- **DatabaseDataSource** - Works with local PostgreSQL database
- **ExternalAPIDataSource** - Adapts external API responses to match internal format
- Provides consistent data structure regardless of source
- Supports merging data from multiple sources

**Endpoints:** `/patterns/adapter/*`

**Документация:** См. `teams/DESIGN_PATTERNS.md` для подробного описания

### Поведенческие паттерны

#### Chain of Responsibility (`ErrorHandlerChain`)
Handles different exception types through chain of specialized handlers:
- HTTPExceptionHandler - Handles FastAPI HTTP exceptions
- ValidationErrorHandler - Handles Pydantic validation errors
- DatabaseErrorHandler - Handles database-specific errors

#### Strategy Pattern (`LoggingStrategy`)
Allows runtime selection of logging behavior:
- ConsoleLoggingStrategy - Logs to console
- FileLoggingStrategy - Logs to file with rotation
- JsonLoggingStrategy - Structured JSON logging

## API Structure
REST endpoints organized by version (`/api/v1/`):
- **/teams** - Team CRUD operations
- **/athletes** - Athlete CRUD operations
- **/patterns** - Design pattern demonstrations

## Request/Response Handling
- **Pydantic schemas** - Data validation and serialization
- Separate schemas for Create, Update, and Response operations
- ConfigDict for ORM model conversion

## Configuration Management
- **pydantic-settings** - Type-safe environment variable management
- Settings singleton pattern via `Settings` class
- `.env` file support for local development

## CORS Configuration
Fully configurable CORS middleware with settings for:
- Allowed origins
- Credentials handling  
- HTTP methods
- Headers

# External Dependencies

## Database
- **PostgreSQL** - Relational database (default connection: localhost:5432)
- **asyncpg** - Async PostgreSQL adapter

## Python Packages
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM and database toolkit
- **Pydantic** - Data validation using Python type hints
- **pydantic-settings** - Settings management
- **uvicorn** - ASGI server
- **accessify** - Provides @private decorator for methods

## Development Tools
- **uv** - Package manager for dependency installation
- Rotating file handler for log management

## External Services
The Adapter pattern includes placeholder for external API integration, though no specific external API is currently implemented. The architecture supports adding external sports data APIs or other third-party services.