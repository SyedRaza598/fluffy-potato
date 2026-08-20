from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=False, index=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, default="member")

    todos: Mapped[list["Todo"]] = relationship("Todo", back_populates="owner", cascade="all, delete-orphan")  # noqa: F821
    teams: Mapped[list["Team"]] = relationship("Team", back_populates="owner", cascade="all, delete-orphan")  # noqa: F821
    team_memberships: Mapped[list["TeamMember"]] = relationship("TeamMember", back_populates="user", cascade="all, delete-orphan")  # noqa: F821
