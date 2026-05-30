from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Todo(Base):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task: Mapped[str] = mapped_column(String, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)