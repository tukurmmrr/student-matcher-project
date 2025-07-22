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

class Course(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    name: str
    email: str
    course_id: int
    interest_ids: List[int]

class StudentCreate(StudentBase):
    password: str

class Student(StudentBase):
    id: int
    is_admin: bool
    interests: List[Interest] = []
    class Config:
        from_attributes = True