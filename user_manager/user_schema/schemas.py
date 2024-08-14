from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str


class UserUpdate(BaseModel):
    username: str
    email: str
    full_name: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str

    class Config:
        orm_mode = True
