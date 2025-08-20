from sqlalchemy.orm import Session
from .models import Student, Course, Interest, StudentInterest
from .security import get_password_hash

def create_student(db: Session, name: str, email: str, password: str, course_id: int, interest_ids: list):
    hashed_password = get_password_hash(password)
    db_student = Student(name=name, email=email, password_hash=hashed_password, course_id=course_id, is_admin=False)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    for interest_id in interest_ids:
        db_interest_association = StudentInterest(student_id=db_student.id, interest_id=interest_id)
        db.add(db_interest_association)
    db.commit()
    return db_student

def get_student_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email).first()

def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def update_student_profile(db: Session, student_id: int, course_id: int, interest_ids: list):
    db_student = get_student_by_id(db, student_id)
    if not db_student:
        return None
    db_student.course_id = course_id
    # Clear existing interests
    db.query(StudentInterest).filter(StudentInterest.student_id == student_id).delete()
    db.commit()
    # Add new interests
    for interest_id in interest_ids:
        db_interest_association = StudentInterest(student_id=student_id, interest_id=interest_id)
        db.add(db_interest_association)
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = get_student_by_id(db, student_id)
    if not db_student:
        return None
    # Delete associated interests
    db.query(StudentInterest).filter(StudentInterest.student_id == student_id).delete()
    db.delete(db_student)
    db.commit()
    return True

def get_all_students(db: Session):
    return db.query(Student).all()

def get_courses(db: Session):
    return db.query(Course).all()

def get_interests(db: Session):
    return db.query(Interest).all()

def make_admin(db: Session, student_id: int):
    db_student = get_student_by_id(db, student_id)
    if not db_student:
        return None
    db_student.is_admin = True
    db.commit()
    db.refresh(db_student)
    return db_student
