from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from . import crud, models, schemas, auth
from .database import get_db, engine

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


def is_admin(user: auth.User = Depends(auth.get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return user


@app.post("/teams/", response_model=schemas.Team, dependencies=[Depends(is_admin)])
async def create_team(team: schemas.TeamCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_team(db=db, team=team)


@app.get("/teams/", response_model=List[schemas.Team])
async def read_teams(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    teams = await crud.get_teams(db, skip=skip, limit=limit)
    return teams


@app.get("/teams/{team_id}", response_model=schemas.Team)
async def read_team(team_id: int, db: AsyncSession = Depends(get_db)):
    db_team = await crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team


@app.put(
    "/teams/{team_id}", response_model=schemas.Team, dependencies=[Depends(is_admin)]
)
async def update_team(
    team_id: int, team: schemas.TeamCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.update_team(db=db, team_id=team_id, team=team)


@app.delete(
    "/teams/{team_id}", response_model=schemas.Team, dependencies=[Depends(is_admin)]
)
async def delete_team(team_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_team(db=db, team_id=team_id)
