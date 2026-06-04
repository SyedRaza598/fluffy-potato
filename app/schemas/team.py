from pydantic import BaseModel


class TeamCreate(BaseModel):
    name: str
    description: str | None = None
    created_by: int


class TeamRead(BaseModel):
    id: int
    name: str
    description: str | None = None
    created_by: int

    model_config = {"from_attributes": True}


class TeamMemberRead(BaseModel):
    id: int
    team_id: int
    user_id: int
    role: str

    model_config = {"from_attributes": True}


class AddMemberRequest(BaseModel):
    user_id: int
    role: str = "member"
