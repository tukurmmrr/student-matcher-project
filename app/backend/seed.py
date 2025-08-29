# app/backend/seed.py

"""
This is a utility script to "seed" the database with initial data.
It populates the 'interests' and 'courses' tables with predefined values,
which is useful for development and setting up a new environment.
"""

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# --- Predefined lists of data to be added to the database ---
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

def seed_data():
    """
    Main function to populate the database with courses and interests.
    """
    # Create all tables defined in models.py if they don't already exist.
    models.Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # Check if data already exists to prevent adding duplicates on subsequent runs.
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

        # Commit the session to save all the new data to the database.
        db.commit()
        print("Seeding complete.")
    finally:
        # Always close the database session.
        db.close()

# This block allows the script to be run directly from the command line
# using `python seed.py`.
if __name__ == "__main__":
    print("Running seed script...")
    seed_data()