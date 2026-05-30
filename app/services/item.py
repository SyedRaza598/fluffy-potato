from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.item import Item
from app.schemas.item import ItemCreate


async def get_all(db: AsyncSession) -> list[Item]:
    result = await db.execute(select(Item))
    return result.scalars().all()


async def get_by_id(db: AsyncSession, item_id: int) -> Item | None:
    result = await db.execute(select(Item).where(Item.id == item_id))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, data: ItemCreate) -> Item:
    item = Item(**data.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def delete(db: AsyncSession, item_id: int) -> bool:
    item = await get_by_id(db, item_id)
    if not item:
        return False
    await db.delete(item)
    await db.commit()
    return True
