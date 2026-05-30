from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.todos import TodoCreate, TodoRead, TodoUpdate
from app.services import todos as todo_service

router = APIRouter()

@router.get("/", response_model=list[TodoRead])
async def todo_list(db: AsyncSession = Depends(get_db)):
    return await todo_service.get_all_todos(db)

@router.post("/", response_model = TodoRead, status_code = status.HTTP_201_CREATED)
async def create_todo(data: TodoCreate, db: AsyncSession = Depends(get_db)):
    return await todo_service.create(db, data)