# app/schemas/user.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_organizer: bool = False

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_organizer: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
