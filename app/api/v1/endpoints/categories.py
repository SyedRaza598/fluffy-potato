from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.category import CreateCategory, ReadCategory, CategoryResponse
from app.services import category as category_service 

router = APIRouter()


@router.get("/", response_model = list[ReadCategory])
async def getCategories(db: AsyncSession = Depends(get_db)):
    return await category_service.getAll(db)

@router.post("/", response_model = CategoryResponse, status_code=status.HTTP_201_CREATED)
async def createCategory(data: CreateCategory, db: AsyncSession = Depends(get_db)):
    return await category_service.create(db, data)
