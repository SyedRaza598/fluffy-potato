from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    name: Mapped[str] = mapped_column(String, nullable = False)
    description: Mapped[str] = mapped_column(String, nullable = True)