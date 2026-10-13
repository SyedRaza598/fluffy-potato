from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.schemas.category import CreateCategory, CategoryResponse

async def getAll(db: AsyncSession) -> list[Category]:
    result = await db.execute(select(Category))
    return result.scalars().all()

async def create(db: AsyncSession, data: CreateCategory) -> CategoryResponse:
    category = Category(**data.model_dump())

    db.add(category)
    await db.commit()
    await db.refresh(category)

    return CategoryResponse(message="Category created successfully", category=category)


async def delete(db: AsyncSession):
    return {"message": "Category deleted successfully"}