from pydantic import BaseModel, EmailStr
from typing import Optional

# 👤 Schema for creating a user (input)
class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    username: str
    password: str  # This is raw and will be hashed

# 📤 Schema for returning a user (output)
class UserOut(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    username: str
    approved: bool

    class Config:
        orm_mode = True  # Enables SQLAlchemy model → Pydantic conversion



class LoginInput(BaseModel):
    username: str
    password: str


class LoginOut(BaseModel):
    access_token: str
    refresh_token: str
    


class UpdateProfile(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: EmailStr| None = None
    password: Optional[str] = None
