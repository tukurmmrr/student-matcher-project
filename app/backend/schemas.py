# app/backend/schemas.py

"""
This module defines the Pydantic models (schemas) used for data validation,
serialization, and documentation in the FastAPI application. They define the
shape of the data for API requests and responses.
"""

from pydantic import BaseModel
from typing import List, Optional


# --- Token Schema ---
class Token(BaseModel):
    """Schema for the JWT access token response."""
    access_token: str
    token_type: str


# --- Data Schemas (Interest, Course) ---
class Interest(BaseModel):
    """Schema for representing an Interest."""
    id: int
    name: str

    class Config:
        # This allows Pydantic to read the data from ORM models (SQLAlchemy).
        from_attributes = True


class Course(BaseModel):
    """Schema for representing a Course."""
    id: int
    name: str

    class Config:
        from_attributes = True


# --- Student Schemas ---
class StudentBase(BaseModel):
    """Base schema for a student's core information."""
    name: str
    email: str
    course_id: int
    interest_ids: List[int]


class StudentCreate(StudentBase):
    """Schema used when creating a new student. Includes the password."""
    password: str


class StudentUpdate(BaseModel):
    """Schema used when a student updates their own profile."""
    course_id: int
    interest_ids: List[int]


class StudentInDB(BaseModel):
    """Schema for representing a student as returned from the API."""
    id: int
    name: str
    email: str
    is_admin: bool
    course: Optional[Course] = None
    interests: List[Interest] = []

    class Config:
        from_attributes = True


# --- Matching Schemas ---
class AdminMatchStudent(BaseModel):
    """A simplified student schema for the admin's match view."""
    name: str
    course: Optional[str] = None


class AdminMatch(BaseModel):
    """Schema for a single pairwise match shown on the admin dashboard."""
    student1: AdminMatchStudent
    student2: AdminMatchStudent
    score: float


class UserMatch(BaseModel):
    """Schema for a single match shown on a regular user's dashboard."""
    student: StudentInDB
    score: float