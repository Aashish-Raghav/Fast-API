from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import datetime

from app.database import get_db
from app.logger import logger
from app.schemas import UserResponse, UserCreate, Token
from app.crud import create_user, get_user_by_username
from app.auth.utils import verify_password
from app.auth.jwt import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):

    try:
        return await create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    # find user
    user = await get_user_by_username(db, form_data.username)

    if not user:
        logger.warning(f"Login attempt with non existent user : {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # verify user
    verified_user = await verify_password(form_data.password, user.hashed_password)
    if not verified_user:
        logger.warning(f"Failed login attempt for user: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login
    user.last_login = datetime.datetime.now(datetime.timezone.utc)
    await db.commit()
    await db.refresh(user)

    access_token = await create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )
    refresh_token = await create_refresh_token(
        data={"sub": user.email, "user_id": user.id}
    )

    logger.info(f"Successful login : {user.username}")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
