from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.team import TeamCreate, TeamRead, TeamMemberRead, AddMemberRequest
from app.services import team as team_service
from app.core.deps import get_current_user, require_admin
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
async def create_team(
    data: TeamCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Only admins can create a team."""
    data.created_by = current_user.id
    return await team_service.create(db, data)


@router.get("/{team_id}/members", response_model=list[TeamMemberRead])
async def get_members(
    team_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Any authenticated user can view team members."""
    team = await team_service.get_by_id(db, team_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return await team_service.get_members(db, team_id)


@router.post("/{team_id}/members", response_model=TeamMemberRead, status_code=status.HTTP_201_CREATED)
async def add_member(
    team_id: int,
    data: AddMemberRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Only the team owner or an admin can add members."""
    team = await team_service.get_by_id(db, team_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    if team.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    member = await team_service.add_member(db, team_id, data)
    if member is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already a member of this team")
    return member


@router.delete("/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    team_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Only the team owner or an admin can remove members."""
    team = await team_service.get_by_id(db, team_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    if team.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    removed = await team_service.remove_member(db, team_id, user_id)
    if not removed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found in this team")


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    team_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Only admins can delete a team."""
    deleted = await team_service.delete(db, team_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
