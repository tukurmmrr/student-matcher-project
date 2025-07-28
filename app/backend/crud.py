from sqlalchemy.orm import Session, selectinload
import models, schemas
from security import hash_password


def get_student_by_email(db: Session, email: str):
    return db.query(models.Student).options(
        selectinload(models.Student.interests),
        selectinload(models.Student.course)
    ).filter(models.Student.email == email).first()


def get_student_by_id(db: Session, user_id: int):
    return db.query(models.Student).options(
        selectinload(models.Student.interests),
        selectinload(models.Student.course)
    ).filter(models.Student.id == user_id).first()


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
    db_student.interests = interests

    db.commit()
    db.refresh(db_student)
    return db_student


def update_student_profile(db: Session, user: models.Student, profile_data: schemas.StudentUpdate):
    user.course_id = profile_data.course_id
    interests = db.query(models.Interest).filter(models.Interest.id.in_(profile_data.interest_ids)).all()
    user.interests = interests
    db.commit()
    db.refresh(user)
    return user


def delete_user_by_admin(db: Session, user_id: int):
    user_to_delete = db.query(models.Student).filter(models.Student.id == user_id).first()
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
    return user_to_delete