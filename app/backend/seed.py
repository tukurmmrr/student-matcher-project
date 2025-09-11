# app/backend/seed.py

"""
Script to populate database with initial courses and interests data
"""
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# course list can be modified based on courses a university offers
COURSES = [
    "Computer Science", "Data Science", "Software Engineering", "Business Administration",
    "Mechanical Engineering", "Electrical Engineering", "Civil Engineering", "Biology",
    "Chemistry", "Physics", "Mathematics", "History", "Psychology", "Sociology",
    "Political Science", "Economics", "Fine Arts", "Graphic Design", "Medicine", "Law"
]
# interests list - mix of hobbies, sports, tech stuff
INTERESTS = [
    "Reading", "Movies", "Gaming", "Music", "Cooking", "Baking", "Photography", "Traveling",
    "Hiking", "Running", "Gym", "Yoga", "Dancing", "Painting", "Drawing",
    "Football", "Basketball", "Tennis", "Swimming", "Cycling", "Cricket",
    "Startups", "Investing", "Technology", "Artificial Intelligence", "Web Development",
    "Cybersecurity", "Volunteering", "History", "Politics", "Chess", "Languages"
]

def seed_data():
    """Populate database with courses and interests"""
    models.Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # check if data already exists
        if db.query(models.Interest).first() or db.query(models.Course).first():
            print("Data already exists, skipping seed")
            return

        print("Adding interests...")
        for interest_name in INTERESTS:
            db_interest = models.Interest(name=interest_name)
            db.add(db_interest)

        print("Adding courses...")
        for course_name in COURSES:
            db_course = models.Course(name=course_name)
            db.add(db_course)

        db.commit()
        print("Seeding completed successfully")

    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Running database seed...")
    seed_data()