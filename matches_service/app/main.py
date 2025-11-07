from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from . import crud, models, schemas, auth
from .database import get_db, engine
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_PATH = os.getenv("ROOT_PATH", "")
app = FastAPI(root_path=ROOT_PATH)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600,
)

router = APIRouter()


@app.on_event("startup")
async def startup():
    logger.info(f"FastAPI app starting with ROOT_PATH: {ROOT_PATH}")
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


def is_admin(user: auth.User = Depends(auth.get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return user


@router.post(
    "/matches/", response_model=schemas.Match, dependencies=[Depends(is_admin)]
)
async def create_match(match: schemas.MatchCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_match(db=db, match=match)


@router.get("/matches/", response_model=List[schemas.Match])
async def read_matches(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    matches = await crud.get_matches(db, skip=skip, limit=limit)
    return matches


@router.get("/matches/{match_id}", response_model=schemas.Match)
async def read_match(match_id: int, db: AsyncSession = Depends(get_db)):
    db_match = await crud.get_match(db, match_id=match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match


@router.post(
    "/matches/{match_id}/odds",
    response_model=schemas.Odds,
    dependencies=[Depends(is_admin)],
)
async def create_odds_for_match(
    match_id: int, odds: schemas.OddsCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_match_odds(db=db, match_id=match_id, odds=odds)


@router.put(
    "/matches/{match_id}/odds",
    response_model=schemas.Odds,
    dependencies=[Depends(is_admin)],
)
async def update_odds_for_match(
    match_id: int, odds: schemas.OddsCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.update_odds(db=db, match_id=match_id, odds=odds)


@app.get("/")
async def health_check():
    return {"status": "ok"}


app.include_router(router)
