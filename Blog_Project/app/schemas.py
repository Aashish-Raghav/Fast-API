from pydantic import BaseModel, Field, EmailStr
import datetime
from typing import Optional


# Schemas for post
class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str


class PostResponse(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=200)
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None


# Schemas for user
class UserBase(BaseModel):
    fullname: str = Field(..., min_length=3, max_length=100)
    username: str = Field(
        ...,
        min_length=1,
        max_length=50,
        pattern=r"^[a-zA-z0-9Z]+$",
        description="Username must contain only letters, numbers, and underscores.",
    )
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=4, max_length=100)


class UserResponse(UserBase):
    id: int
    created_at: datetime.datetime
    last_login: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True


# Token Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None


# Login Schemas
class UserLogin(BaseModel):
    username: str
    password: str


# Refresh Schemas
class RefreshTokenRequest(BaseModel):
    refresh_token: str
