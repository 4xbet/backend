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


@router.post("/teams/", response_model=schemas.Team, dependencies=[Depends(is_admin)])
async def create_team(team: schemas.TeamCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_team(db=db, team=team)


@router.get("/teams/", response_model=List[schemas.Team])
async def read_teams(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    teams = await crud.get_teams(db, skip=skip, limit=limit)
    return teams


@router.get("/teams/{team_id}", response_model=schemas.Team)
async def read_team(team_id: int, db: AsyncSession = Depends(get_db)):
    db_team = await crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team


@router.put(
    "/teams/{team_id}", response_model=schemas.Team, dependencies=[Depends(is_admin)]
)
async def update_team(
    team_id: int, team: schemas.TeamCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.update_team(db=db, team_id=team_id, team=team)


@router.delete(
    "/teams/{team_id}", response_model=schemas.Team, dependencies=[Depends(is_admin)]
)
async def delete_team(team_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_team(db=db, team_id=team_id)


@app.get("/")
async def health_check():
    return {"status": "ok"}


app.include_router(router)
