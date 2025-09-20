from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db import db
from src.api.v1 import teams, athletes
from fastapi.middleware.cors import CORSMiddleware
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager."""
    await db.connect()
    await db.create_all()

    yield

    await db.close()

app = FastAPI(lifespan=lifespan)

app.include_router(teams.router)
app.include_router(athletes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


@app.get("/")
def read_root():
    return {"goi": "da"}
