from pydantic import BaseModel

class TodoCreate(BaseModel):
    task: str
    completed: bool = False

class TodoUpdate(BaseModel):
    id: int
    task: str | None = None
    completed: bool | None = None

class TodoRead(BaseModel):
    id: int
    task: str
    completed: bool

    model_config = {"from_attributes": True}