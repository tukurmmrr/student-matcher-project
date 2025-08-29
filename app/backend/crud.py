# app/backend/crud.py

"""
This module contains CRUD (Create, Read, Update, Delete) operations
for interacting with the database. These functions separate the database
logic from the API endpoint logic.
"""

from sqlalchemy.orm import Session, selectinload
import models, schemas
from security import hash_password


def get_student_by_email(db: Session, email: str):
    """Fetches a single student from the database by their email address."""
    # `selectinload` is used to eagerly load related data (interests, course)
    # to prevent additional database queries later (N+1 problem).
    return db.query(models.Student).options(
        selectinload(models.Student.interests),
        selectinload(models.Student.course)
    ).filter(models.Student.email == email).first()


def get_students(db: Session):
    """Fetches all students from the database."""
    return db.query(models.Student).options(
        selectinload(models.Student.interests),
        selectinload(models.Student.course)
    ).all()


def get_interests(db: Session):
    """Fetches all available interests from the database."""
    return db.query(models.Interest).all()


def get_courses(db: Session):
    """Fetches all available courses from the database."""
    return db.query(models.Course).all()


def create_student(db: Session, student: schemas.StudentCreate):
    """Creates a new student record in the database."""
    # Hash the plain-text password before storing it.
    hashed_pwd = hash_password(student.password)
    db_student = models.Student(
        name=student.name,
        email=student.email,
        hashed_password=hashed_pwd,
        course_id=student.course_id
    )
    db.add(db_student)

    # Fetch the interest objects from the DB based on the provided IDs.
    interests = db.query(models.Interest).filter(models.Interest.id.in_(student.interest_ids)).all()
    # Associate the fetched interests with the new student.
    db_student.interests = interests

    db.commit()
    db.refresh(db_student)  # Refresh the object to get the new ID and loaded relationships.
    return db_student


def update_student_profile(db: Session, user: models.Student, profile_data: schemas.StudentUpdate):
    """Updates an existing student's profile (course and interests)."""
    # Update the course ID directly.
    user.course_id = profile_data.course_id
    # Fetch the new set of interests from the database.
    interests = db.query(models.Interest).filter(models.Interest.id.in_(profile_data.interest_ids)).all()
    # Replace the old list of interests with the new one.
    user.interests = interests

    db.commit()
    db.refresh(user)
    return user


def delete_user_by_admin(db: Session, user_id: int):
    """Deletes a user from the database by their ID. (Admin only)"""
    user_to_delete = db.query(models.Student).filter(models.Student.id == user_id).first()
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
    return user_to_delete