from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    role: str


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Wallet(BaseModel):
    id: int
    user_id: int
    balance: float
    currency: str

    class Config:
        orm_mode = True
