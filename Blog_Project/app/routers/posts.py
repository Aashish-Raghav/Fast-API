from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import PostCreate, PostResponse, PostUpdate
from app.database import get_db
from app.crud import create_post, get_all_posts, get_post_by_id, get_post_by_user, update_post

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostResponse)
async def create_new_post(post: PostCreate, owner_id : int ,db: AsyncSession = Depends(get_db)):
    try:
        return await create_post(db, post, owner_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=list[PostResponse])
async def read_posts(db: AsyncSession = Depends(get_db)):
    return await get_all_posts(db)


@router.get("/{post_id}",response_model=PostResponse)
async def read_post_by_id(post_id : int, db: AsyncSession = Depends(get_db)):
    post = await get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found!")
    return post

@router.get("/user/{user_id}", response_model=list[PostResponse])
async def read_post_by_user(user_id : int, db: AsyncSession = Depends(get_db)):
    try : 
        return await get_post_by_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.patch("/{post_id}", response_model=PostResponse)
async def patch_post(
    post_id: int,
    post_update: PostUpdate,
    db: AsyncSession = Depends(get_db)
):
    post = await update_post(db, post_id, post_update)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post