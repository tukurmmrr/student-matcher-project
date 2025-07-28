from sqlalchemy import Column, Integer, String, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

# --- THIS TABLE DEFINITION MUST BE BEFORE THE STUDENT CLASS ---
student_interests_table = Table('student_interests', Base.metadata,
                                Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
                                Column('interest_id', Integer, ForeignKey('interests.id'), primary_key=True)
                                )


# -----------------------------------------------------------

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship("Course")
    interests = relationship("Interest", secondary=student_interests_table)


class Interest(Base):
    __tablename__ = "interests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
