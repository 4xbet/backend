from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email, hashed_password=hashed_password, role=user.role
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # Create a wallet for the new user
    wallet = models.Wallet(user_id=db_user.id)
    db.add(wallet)
    await db.commit()
    await db.refresh(wallet)

    return db_user


async def update_wallet_balance(db: AsyncSession, user_id: int, amount: float):
    result = await db.execute(select(models.Wallet).filter(models.Wallet.user_id == user_id))
    wallet = result.scalars().first()
    if wallet:
        wallet.balance += amount
        await db.commit()
        await db.refresh(wallet)
    return wallet
