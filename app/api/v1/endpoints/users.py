from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead
from app.services import user as user_service
from app.core.deps import require_admin
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await user_service.get_all(db)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_service.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    if await user_service.get_by_email(db, data.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    if await user_service.get_by_username(db, data.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")
    return await user_service.create(db, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await user_service.delete(db, user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
