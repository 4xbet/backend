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


@app.post(
    "/matches/", response_model=schemas.Match, dependencies=[Depends(is_admin)]
)
async def create_match(match: schemas.MatchCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_match(db=db, match=match)


@app.get("/matches/", response_model=List[schemas.Match])
async def read_matches(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    matches = await crud.get_matches(db, skip=skip, limit=limit)
    return matches


@app.get("/matches/{match_id}", response_model=schemas.Match)
async def read_match(match_id: int, db: AsyncSession = Depends(get_db)):
    db_match = await crud.get_match(db, match_id=match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match


@app.post(
    "/matches/{match_id}/odds",
    response_model=schemas.Odds,
    dependencies=[Depends(is_admin)],
)
async def create_odds_for_match(
    match_id: int, odds: schemas.OddsCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_match_odds(db=db, match_id=match_id, odds=odds)


@app.put(
    "/matches/{match_id}/odds",
    response_model=schemas.Odds,
    dependencies=[Depends(is_admin)],
)
async def update_odds_for_match(
    match_id: int, odds: schemas.OddsCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.update_odds(db=db, match_id=match_id, odds=odds)
