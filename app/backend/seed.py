# app/backend/seed.py
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# --- NEW, MORE GENERIC LISTS ---
COURSES = [
    "Computer Science", "Data Science", "Software Engineering", "Business Administration",
    "Mechanical Engineering", "Electrical Engineering", "Civil Engineering", "Biology",
    "Chemistry", "Physics", "Mathematics", "History", "Psychology", "Sociology",
    "Political Science", "Economics", "Fine Arts", "Graphic Design", "Medicine", "Law"
]

INTERESTS = [
    # Hobbies & Leisure
    "Reading", "Movies", "Gaming", "Music", "Cooking", "Baking", "Photography", "Traveling",
    "Hiking", "Running", "Gym", "Yoga", "Dancing", "Painting", "Drawing",

    # Sports
    "Football", "Basketball", "Tennis", "Swimming", "Cycling", "Cricket",

    # Academic & Tech
    "Startups", "Investing", "Technology", "Artificial Intelligence", "Web Development",
    "Cybersecurity",

    # Social & Other
    "Volunteering", "History", "Politics", "Chess", "Languages"
]


# -------------------------

def seed_data():
    # This creates all the tables first
    models.Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # Check if data already exists to prevent duplication
        if db.query(models.Interest).first() or db.query(models.Course).first():
            print("Data already exists. Skipping seed.")
            return

        print("Seeding interests...")
        for interest_name in INTERESTS:
            db_interest = models.Interest(name=interest_name)
            db.add(db_interest)

        print("Seeding courses...")
        for course_name in COURSES:
            db_course = models.Course(name=course_name)
            db.add(db_course)

        db.commit()
        print("Seeding complete.")
    finally:
        db.close()


if __name__ == "__main__":
    print("Running seed script...")
    seed_data()