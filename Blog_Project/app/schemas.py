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
        orm_mode = True


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None


# Schemas for user
class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    username: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    # posts : list[PostResponse] = []

    class Config:
        orm_mode = True
