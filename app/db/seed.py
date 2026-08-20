from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.core.security import hash_password
from app.core.config import settings


async def seed_first_admin(db: AsyncSession) -> None:
    """Creates the first admin user if no admin exists yet."""
    result = await db.execute(select(User).where(User.role == "admin"))
    if result.scalar_one_or_none():
        return  # an admin already exists, nothing to do

    admin = User(
        username=settings.FIRST_ADMIN_USERNAME,
        email=settings.FIRST_ADMIN_EMAIL,
        hashed_password=hash_password(settings.FIRST_ADMIN_PASSWORD),
        role="admin",
    )
    db.add(admin)
    await db.commit()
    print(f"[seed] First admin created: {settings.FIRST_ADMIN_EMAIL}")
