from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserResponse,UserCreate
from app.database import get_db
from app.crud import create_user, get_all_user, get_user_by_id

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model = UserResponse, status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate, db:AsyncSession = Depends(get_db)):
    try:
        return await create_user(db,user)  
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[UserResponse])
async def read_users(db: AsyncSession = Depends(get_db)):
    users = await get_all_user(db)
    if not users:
        raise HTTPException(status_code=404, detail="Users not found!")
    return users
    

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id : int, db : AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail = "User not found!")
    return user


