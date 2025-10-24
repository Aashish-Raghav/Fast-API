from fastapi import FastAPI
from app.routers import users, posts
from app.database import Base, engine

app = FastAPI(title="Blog API")


app.include_router(users.router)
app.include_router(posts.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
