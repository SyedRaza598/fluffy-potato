from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.team import TeamCreate, TeamRead, TeamMemberRead, AddMemberRequest
from app.services import team as team_service

router = APIRouter()


@router.post("/", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
async def create_team(data: TeamCreate, db: AsyncSession = Depends(get_db)):
    return await team_service.create(db, data)


@router.get("/{team_id}/members", response_model=list[TeamMemberRead])
async def get_members(team_id: int, db: AsyncSession = Depends(get_db)):
    team = await team_service.get_by_id(db, team_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return await team_service.get_members(db, team_id)


@router.post("/{team_id}/members", response_model=TeamMemberRead, status_code=status.HTTP_201_CREATED)
async def add_member(team_id: int, data: AddMemberRequest, db: AsyncSession = Depends(get_db)):
    team = await team_service.get_by_id(db, team_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    member = await team_service.add_member(db, team_id, data)
    if member is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already a member of this team")
    return member


@router.delete("/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(team_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    removed = await team_service.remove_member(db, team_id, user_id)
    if not removed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found in this team")


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await team_service.delete(db, team_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
