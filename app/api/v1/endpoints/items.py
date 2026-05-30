from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.item import ItemCreate, ItemRead
from app.services import item as item_service

router = APIRouter()


@router.get("/", response_model=list[ItemRead])
async def list_items(db: AsyncSession = Depends(get_db)):
    return await item_service.get_all(db)


@router.get("/{item_id}", response_model=ItemRead)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await item_service.get_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(data: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await item_service.create(db, data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await item_service.delete(db, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
