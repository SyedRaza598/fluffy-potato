from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.todo import Todo
from app.schemas.todos import TodoCreate

async def get_all_todos(db: AsyncSession) -> list[Todo]:
    result = await db.execute(select(Todo))
    return result.scalars().all()

async def create(db: AsyncSession, data: TodoCreate) -> Todo:
    todo = Todo(**data.model_dump())
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo
