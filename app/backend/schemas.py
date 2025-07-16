from pydantic import BaseModel
from typing import List

class InterestBase(BaseModel):
    name: str

class InterestCreate(InterestBase):
    pass

class Interest(InterestBase):
    id: int

    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    name: str
    email: str
    course: str

class StudentCreate(StudentBase):
    interests: str # e.g., "coding, hiking, movies"

class Student(StudentBase):
    id: int
    interests: List[Interest] = []

    class Config:
        orm_mode = True