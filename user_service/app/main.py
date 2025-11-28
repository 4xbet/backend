from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from . import crud, models, schemas, auth
from .database import get_db, engine
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_PATH = os.getenv("ROOT_PATH", "")
app = FastAPI(root_path=ROOT_PATH)

router = APIRouter()

class BalanceUpdate(BaseModel):
    amount: float


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@router.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role, "id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(user: auth.User = Depends(auth.get_current_user)):
    return user


@router.get("/users/me", response_model=schemas.User)
async def read_users_me(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user = await crud.get_user_by_email(db, email=current_user.email)
    return user


@router.get("/users/me/wallet", response_model=schemas.Wallet)
async def read_user_wallet(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user = await crud.get_user_by_email(db, email=current_user.email)
    return user.wallet


@router.patch("/users/me/wallet", response_model=schemas.Wallet)
async def update_user_wallet(
    balance_update: BalanceUpdate,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await crud.update_wallet_balance(
        db, user_id=current_user.id, amount=balance_update.amount
    )


@app.get("/")
async def health_check():
    return {"status": "ok"}


app.include_router(router)
