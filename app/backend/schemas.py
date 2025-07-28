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

class StudentInDB(BaseModel):
    id: int
    name: str
    email: str
    is_admin: bool
    course: Optional[Course] = None
    interests: List[Interest] = []
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    name: str
    email: str
    course_id: int
    interest_ids: List[int]

class StudentCreate(StudentBase):
    password: str

# --- THIS CLASS WAS MISSING ---
class StudentUpdate(BaseModel):
    course_id: int
    interest_ids: List[int]
# --------------------------------

class AdminMatchStudent(BaseModel):
    name: str
    course: Optional[str] = None

class AdminMatch(BaseModel):
    student1: AdminMatchStudent
    student2: AdminMatchStudent
    score: float

class UserMatch(BaseModel):
    student: StudentInDB
    score: float