from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    roles: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
