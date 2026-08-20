from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import verify_password, create_access_token
from app.services import user as user_service
from app.schemas.user import UserCreate, UserRead
from pydantic import BaseModel

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Public self-signup. Role is always forced to 'member'."""
    data.role = "member"
    if await user_service.get_by_email(db, data.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    if await user_service.get_by_username(db, data.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")
    return await user_service.create(db, data)


@router.post("/login", response_model=Token)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await user_service.get_by_email(db, form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token(user.id))


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout():
    # JWT is stateless — logout is handled client-side by discarding the token.
    # To enforce server-side logout, add a token blacklist (e.g. Redis).
    return {"message": "Successfully logged out"}
