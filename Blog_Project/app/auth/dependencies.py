from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.database import get_db
from app.config import settings
from app.auth.jwt import verify_token
from app.logger import logger
from app.schemas import TokenData
from app.models import User
from app.crud import get_user_by_id

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token=Depends(oauth_scheme), db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = await verify_token(token, token_type="access")
        if payload is None:
            logger.warning("Token verification failed")
            raise credentials_exception

        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")

        if username is None or user_id is None:
            logger.warning("Token payload missing required fields")
            raise credentials_exception

        token_data = TokenData(username=username, user_id=user_id)

    except JWTError as e:
        logger.error(f"JWT Error : {str(e)}")
        raise credentials_exception

    # get user from db
    user = await get_user_by_id(db, token_data.user_id)

    if user is None:
        logger.warning(f"User not found: {token_data.username}")
        raise credentials_exception

    logger.info(f"User authenticated successfully: {user.username}")
    return user
