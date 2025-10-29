from fastapi import FastAPI
from app.routers import users, posts, auth
from app.database import Base, engine
from app.config import settings
from app.logger import logger

# Initialize FastAPI app
logger.info("Starting FastAPI app....")
app = FastAPI(
    title=settings.app_name,
    description="JWT Authentication API with FastAPI",
    version="1.0.0",
)

logger.info("FastAPI App started at localhost")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
