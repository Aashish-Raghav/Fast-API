import datetime
from jose import jwt, JWTError
from typing import Optional, Any
from app.logger import logger
from app.config import settings


async def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    now = datetime.datetime.now(datetime.timezone.utc)
    expire = now + datetime.timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update(
        {"expire": expire.timestamp(), "type": "access", "iat": now.timestamp()}
    )

    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


async def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    now = datetime.datetime.now(datetime.timezone.utc)
    expire = now + datetime.timedelta(days=settings.refresh_token_expire_days)

    to_encode.update(
        {"expire": expire.timestamp(), "type": "refresh", "iat": now.timestamp()}
    )

    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


async def verify_token(
    token: str, token_type: str = "access"
) -> Optional[dict[str, Any]]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        if payload.get("type") != token_type:
            logger.warning(
                f"Invalid token type. Expected {token_type}, got {payload.get('type')}"
            )
            raise None

        exp = payload.get("expire")
        exp_dt = datetime.datetime.fromtimestamp(exp, tz=datetime.timezone.utc)
        now = datetime.datetime.now(datetime.timezone.utc)
        if exp is None or exp_dt < now:
            logger.warning(f"Token expired for subject : {payload.get('sub')}")
            return None

        logger.info(f"Token verified for subject : {payload.get('sub')}")

        return payload
    except JWTError as e:
        return None
