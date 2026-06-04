from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.team import Team, TeamMember
from app.schemas.team import TeamCreate, AddMemberRequest


async def create(db: AsyncSession, data: TeamCreate) -> Team:
    team = Team(
        name=data.name,
        description=data.description,
        created_by=data.created_by,
    )
    db.add(team)
    await db.commit()
    await db.refresh(team)
    return team


async def get_by_id(db: AsyncSession, team_id: int) -> Team | None:
    result = await db.execute(select(Team).where(Team.id == team_id))
    return result.scalar_one_or_none()


async def get_members(db: AsyncSession, team_id: int) -> list[TeamMember]:
    result = await db.execute(select(TeamMember).where(TeamMember.team_id == team_id))
    return result.scalars().all()


async def add_member(db: AsyncSession, team_id: int, data: AddMemberRequest) -> TeamMember | None:
    # Check if already a member
    existing = await db.execute(
        select(TeamMember).where(
            TeamMember.team_id == team_id,
            TeamMember.user_id == data.user_id,
        )
    )
    if existing.scalar_one_or_none():
        return None  # already a member

    member = TeamMember(team_id=team_id, user_id=data.user_id, role=data.role)
    db.add(member)
    await db.commit()
    await db.refresh(member)
    return member


async def remove_member(db: AsyncSession, team_id: int, user_id: int) -> bool:
    result = await db.execute(
        select(TeamMember).where(
            TeamMember.team_id == team_id,
            TeamMember.user_id == user_id,
        )
    )
    member = result.scalar_one_or_none()
    if not member:
        return False
    await db.delete(member)
    await db.commit()
    return True


async def delete(db: AsyncSession, team_id: int) -> bool:
    team = await get_by_id(db, team_id)
    if not team:
        return False
    await db.delete(team)
    await db.commit()
    return True
