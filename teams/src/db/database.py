from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from accessify import private
from config import settings
from src.services import logger

class Database:
    def __init__(self):
        self.POSTGRES = {
            "user": settings.POSTGRES_USER,
            "password": settings.POSTGRES_PASSWORD,
            "host": settings.POSTGRES_HOST,
            "port": settings.POSTGRES_PORT,
            "db": settings.POSTGRES_DB
        }
        self.engine = None

    @private
    def get_url(self):
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(**self.POSTGRES)

    async def connect(self):
        logger.info("Connecting to database...")
        self.engine = create_async_engine(self.get_url())
        self.async_session = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )

    async def close(self):
        if not self.engine:
            return
        await self.engine.dispose()
        logger.info("Database connection closed")

    def get_session(self):
        if not self.async_session:
            raise Exception("Database is not connected")
        return self.async_session()

    async def create_all(self):
            if not self.engine:
                raise Exception("Database is not connected")
            from .models import Base
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
            if not self.engine:
                raise Exception("Database is not connected")
            from .models import Base
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
            logger.info("All tables dropped")