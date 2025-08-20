from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Course, Interest

DATABASE_URL = "postgresql://user:password@localhost/student_matcher"  # Update with your Supabase URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_data():
    db = SessionLocal()
    Base.metadata.create_all(bind=engine)  # Ensure tables exist

    # Curated courses
    courses = [
        "Computer Science", "Business Administration", "Psychology", "Engineering", "Biology",
        "English Literature", "History", "Mathematics", "Physics", "Chemistry"
    ]
    for course in courses:
        db_course = db.query(Course).filter(Course.name == course).first()
        if not db_course:
            db.add(Course(name=course))
    db.commit()

    # Curated interests (sensible list: hobbies, academics, sports)
    interests = [
        "sports", "music", "reading", "coding", "travel", "art", "gaming", "cooking", "fitness", "photography",
        "writing", "dancing", "singing", "programming", "nature", "football", "basketball", "cycling", "Working out" "volunteering", "movies", "hiking", "yoga", "technology", "science", "history", "languages"
    ]
    for interest in interests:
        db_interest = db.query(Interest).filter(Interest.name == interest).first()
        if not db_interest:
            db.add(Interest(name=interest))
    db.commit()

if __name__ == "__main__":
    seed_data()
