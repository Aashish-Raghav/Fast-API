from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models
from . import schemas

async def create_user(db: AsyncSession, user : schemas.UserCreate):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user(db: AsyncSession, user_id : int):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalar_one_or_none()