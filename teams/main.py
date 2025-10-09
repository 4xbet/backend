from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from src.db import db
from src.api.v1 import teams, athletes
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from services.error_handlers import ErrorHandlerChain

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager."""
    await db.connect()
    await db.create_all()
    yield
    await db.close()

app = FastAPI(lifespan=lifespan)

error_handler = ErrorHandlerChain()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return error_handler.handle(request, exc)

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