from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "member"


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    role: str

    model_config = {"from_attributes": True}
