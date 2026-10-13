from pydantic import BaseModel, ConfigDict

class CreateCategory(BaseModel):
    name: str
    description: str

class ReadCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str
    id: int

class CategoryResponse(BaseModel):
    message: str
    category: ReadCategory