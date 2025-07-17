from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# CHANGE 1: Import 'database' directly, just like the other files.
import crud, models, schemas, matching, database
from fastapi.middleware.cors import CORSMiddleware

# CHANGE 2: Use the 'database' prefix to get the engine variable.
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# --- CORS Middleware (This part was already correct) ---
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://fancy-bunny-d46e4d.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------

# Dependency to get a DB session
def get_db():
    # CHANGE 3: Use the 'database' prefix to get the SessionLocal class.
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_email(db, email=student.email)
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_student(db=db, student=student)

@app.get("/students/", response_model=List[schemas.Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@app.get("/matches/jaccard")
def get_jaccard_matches(db: Session = Depends(get_db)):
    students = crud.get_students(db, limit=1000)
    matches = matching.calculate_jaccard_similarity(students)
    return matches

@app.get("/matches/cosine")
def get_cosine_matches(db: Session = Depends(get_db)):
    students = crud.get_students(db, limit=1000)
    matches = matching.calculate_cosine_similarity(students)
    return matches
# Add this endpoint to app/backend/main.py

@app.delete("/students/{student_id}", response_model=schemas.Student)
def delete_single_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.delete_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student