# app/backend/crud.py
from sqlalchemy.orm import Session, selectinload
import models, schemas
from security import hash_password


def get_student_by_email(db: Session, email: str):
    return db.query(models.Student).filter(models.Student.email == email).first()


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).options(selectinload(models.Student.interests)).offset(skip).limit(limit).all()


def create_student(db: Session, student: schemas.StudentCreate):
    hashed_pwd = hash_password(student.password)
    db_student = models.Student(
        name=student.name,
        email=student.email,
        hashed_password=hashed_pwd,
        course=student.course,
        bio=student.bio,
        profile_picture_url=student.profile_picture_url
    )
    db.add(db_student)

    interest_names = [name.strip().lower() for name in student.interests.split(',')]
    for name in interest_names:
        interest = db.query(models.Interest).filter_by(name=name).first()
        if not interest:
            interest = models.Interest(name=name)
            db.add(interest)
        db_student.interests.append(interest)

    db.commit()
    db.refresh(db_student)
    return db_student