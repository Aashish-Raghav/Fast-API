from fastapi import FastAPI
from .database import engine, Base
from .routers import users


app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(users.router)

@app.get("/")
async def root():
    return {"message" : "FastAPI with SQLAlchemy is running!"}