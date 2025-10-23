from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
print("Current Directory:", os.getcwd())
print("DATABASE_URL:", os.getenv("DATABASE_URL"))
print("Loaded .env from:", os.path.abspath("."))

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL="sqlite+aiosqlite:///./test.db"


engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        yield session
