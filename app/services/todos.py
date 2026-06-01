from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.todo import Todo
from app.schemas.todos import TodoCreate, TodoUpdate

async def get_all_todos(db: AsyncSession) -> list[Todo]:
    result = await db.execute(select(Todo))
    return result.scalars().all()

async def get_todo_by_id(db: AsyncSession, todo_id: int) -> Todo | None:
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    return result.scalar_one_or_none()

async def create(db: AsyncSession, data: TodoCreate) -> Todo:
    todo = Todo(**data.model_dump())
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo

async def update(db: AsyncSession, todo_id: int, data: TodoUpdate) -> Todo:
    todo = await get_todo_by_id(db, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    for field in data.model_fields_set:
        setattr(todo, field, getattr(data, field))

    await db.commit()
    await db.refresh(todo)
    return todo

async def delete_todo(db: AsyncSession, todo_id: int) -> dict:
    todo = await get_todo_by_id(db, todo_id)

    if not todo:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Todo not found!")
    
    await db.delete(todo)
    await db.commit()

    return {"message": "Todo has been deleted successfully!"}

