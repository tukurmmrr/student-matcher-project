# app/backend/models.py

"""
This module defines the SQLAlchemy ORM models, which represent the
database tables as Python classes. It defines the structure, columns,
and relationships for students, interests, and courses.
"""

from sqlalchemy import Column, Integer, String, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

# This is an association table for the many-to-many relationship
# between Students and Interests. It links them together without
# needing its own separate model class.
student_interests_table = Table('student_interests', Base.metadata,
                                Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
                                Column('interest_id', Integer, ForeignKey('interests.id'), primary_key=True)
                                )


class Student(Base):
    """Represents the 'students' table in the database."""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    # Foreign key to link a student to a course.
    course_id = Column(Integer, ForeignKey('courses.id'))

    # --- Relationships ---
    # Defines the one-to-many relationship: One Course has many Students.
    # The 'back_populates' argument is not used here but would be added
    # to the Course model if we needed to access students from a course object.
    course = relationship("Course")

    # Defines the many-to-many relationship with Interest,
    # using the 'student_interests_table' as the join table.
    interests = relationship("Interest", secondary=student_interests_table)


class Interest(Base):
    """Represents the 'interests' table in the database."""
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class Course(Base):
    """Represents the 'courses' table in the database."""
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)