from sqlalchemy.orm import Session, selectinload
import models, schemas
from security import hash_password


def get_student_by_email(db: Session, email: str):
    # This is the crucial fix: we must load relationships here too.
    return db.query(models.Student).options(
        selectinload(models.Student.interests),
        selectinload(models.Student.course)
    ).filter(models.Student.email == email).first()


def get_students(db: Session):
    return db.query(models.Student).options(
        selectinload(models.Student.interests),
        selectinload(models.Student.course)
    ).all()


def get_interests(db: Session):
    return db.query(models.Interest).all()


def get_courses(db: Session):
    return db.query(models.Course).all()


def create_student(db: Session, student: schemas.StudentCreate):
    hashed_pwd = hash_password(student.password)
    db_student = models.Student(
        name=student.name,
        email=student.email,
        hashed_password=hashed_pwd,
        course_id=student.course_id
    )
    db.add(db_student)

    interests = db.query(models.Interest).filter(models.Interest.id.in_(student.interest_ids)).all()
    db_student.interests.extend(interests)

    db.commit()
    db.refresh(db_student)
    return db_student