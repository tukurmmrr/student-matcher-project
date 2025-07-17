# app/backend/schemas.py

from pydantic import BaseModel
from typing import List, Optional

class InterestBase(BaseModel):
    name: str

class InterestCreate(InterestBase):
    pass

class Interest(InterestBase):
    id: int

    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    name: str
    email: str
    course: str
    # --- THESE FIELDS WERE MISSING FROM YOUR 'StudentCreate' LOGIC ---
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    # ----------------------------------------------------------------

class StudentCreate(StudentBase):
    interests: str

class Student(StudentBase):
    id: int
    interests: List[Interest] = []

    class Config:
        from_attributes = True