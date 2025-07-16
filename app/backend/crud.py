from sqlalchemy.orm import Session
import models, schemas


def get_student_by_email(db: Session, email: str):
    return db.query(models.Student).filter(models.Student.email == email).first()


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(name=student.name, email=student.email, course=student.course)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    # Process interests
    interest_names = [name.strip().lower() for name in student.interests.split(',')]
    for name in interest_names:
        interest = db.query(models.Interest).filter_by(name=name).first()
        if not interest:
            interest = models.Interest(name=name)
            db.add(interest)
            db.commit()
            db.refresh(interest)
        db_student.interests.append(interest)

    db.commit()
    db.refresh(db_student)
    return db_student
# Add this function to app/backend/crud.py

def delete_student(db: Session, student_id: int):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
        return db_student
    return None