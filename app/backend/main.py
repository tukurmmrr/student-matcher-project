# app/backend/main.py
# (This file now includes the new /courses and /interests endpoints)
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas, matching, security, auth
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CORS Middleware ---
origins = [
    "http://localhost:3000",
    "http://localhost:5173", # Default Vite port
    "https://fancy-bunny-d46e4d.netlify.app",
]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- NEW PUBLIC ENDPOINTS ---
@app.get("/interests", response_model=List[schemas.Interest])
def read_interests(db: Session = Depends(get_db)):
    return crud.get_interests(db)

@app.get("/courses", response_model=List[schemas.Course])
def read_courses(db: Session = Depends(get_db)):
    return crud.get_courses(db)

# --- AUTHENTICATION ENDPOINTS ---
@app.post("/register", response_model=schemas.Student)
def register_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_email(db, email=student.email)
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_student(db=db, student=student)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    student = auth.authenticate_user(db, form_data.username, form_data.password)
    if not student:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": student.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- PROTECTED ENDPOINTS ---
@app.get("/users/me", response_model=schemas.Student)
async def read_users_me(current_user: schemas.Student = Depends(auth.get_current_active_user)):
    return current_user

@app.get("/matches/jaccard")
def get_jaccard_matches(db: Session = Depends(get_db), current_user: schemas.Student = Depends(auth.get_current_active_user)):
    students = crud.get_students(db)
    matches = matching.calculate_jaccard_similarity(students, current_user.id)
    return matches

@app.get("/matches/cosine")
def get_cosine_matches(db: Session = Depends(get_db), current_user: schemas.Student = Depends(auth.get_current_active_user)):
    students = crud.get_students(db)
    matches = matching.calculate_cosine_similarity(students, current_user.id)
    return matches