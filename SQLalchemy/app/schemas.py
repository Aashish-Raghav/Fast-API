from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class UserResponse(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

    class Config:
        orm_mode = True
