from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True


class UserContext(BaseModel):
    """User context for internal service use."""
    id: int
    username: str
    email: str
    
    class Config:
        from_attributes = True
