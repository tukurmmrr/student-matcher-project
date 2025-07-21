# app/backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class Interest(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    name: str
    email: str
    course: str
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    interests: str

class StudentCreate(StudentBase):
    password: str

class Student(StudentBase):
    id: int
    is_admin: bool
    interests: List[Interest] = []
    class Config:
        from_attributes = True