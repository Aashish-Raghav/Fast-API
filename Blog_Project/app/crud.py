from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
from . import models
from . import schemas


# --------------- User CRUD -----------------


async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    result = await db.execute(
        select(models.User).where(models.User.email == user.email)
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise ValueError("User Already Exists")

    new_user = models.User(**user.model_dump())
    print(f" New User : {new_user}")
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_id(db: AsyncSession, user_id: int) -> models.User | None:
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalars().first()


async def get_all_user(db: AsyncSession) -> list[models.User]:
    result = await db.execute(select(models.User))
    return result.scalars().all()


# --------------- Post CRUD -----------------


async def create_post(
    db: AsyncSession, post: schemas.PostCreate, owner_id: int
) -> models.Post:
    user = await get_user_by_id(db, owner_id)
    if not user:
        raise ValueError("User does not exist")

    new_post = models.Post(**post.model_dump(), owner_id=owner_id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post


async def update_post(
    db: AsyncSession, post_id: int, post_update: schemas.PostUpdate
) -> models.Post | None:
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if not post:
        return None

    update_data = post_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post, key, value)

    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def get_post_by_id(db: AsyncSession, post_id: int) -> models.Post | None:
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    return result.scalars().first()


async def get_all_posts(db: AsyncSession) -> list[models.Post]:
    result = await db.execute(select(models.Post))
    return result.scalars().all()


async def get_post_by_user(db: AsyncSession, user_id: int) -> list[models.Post]:
    user = await get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User does not exist")
    result = await db.execute(
        select(models.Post).where(models.Post.owner_id == user_id)
    )
    return result.scalars().all()
