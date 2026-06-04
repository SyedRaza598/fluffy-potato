from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate


async def get_all_for_user(db: AsyncSession, user_id: int) -> list[Todo]:
    result = await db.execute(select(Todo).where(Todo.user_id == user_id))
    return result.scalars().all()


async def get_by_id(db: AsyncSession, todo_id: int, user_id: int) -> Todo | None:
    result = await db.execute(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def create(db: AsyncSession, data: TodoCreate, user_id: int) -> Todo:
    todo = Todo(**data.model_dump(), user_id=user_id)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def update(db: AsyncSession, todo_id: int, data: TodoUpdate, user_id: int) -> Todo | None:
    todo = await get_by_id(db, todo_id, user_id)
    if not todo:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(todo, field, value)
    await db.commit()
    await db.refresh(todo)
    return todo


async def delete(db: AsyncSession, todo_id: int, user_id: int) -> bool:
    todo = await get_by_id(db, todo_id, user_id)
    if not todo:
        return False
    await db.delete(todo)
    await db.commit()
    return True
