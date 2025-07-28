from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas, matching, security, auth
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://studentmatcher.netlify.app",
]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.get("/interests", response_model=List[schemas.Interest])
def read_interests(db: Session = Depends(get_db)):
    return crud.get_interests(db)

@app.get("/courses", response_model=List[schemas.Course])
def read_courses(db: Session = Depends(get_db)):
    return crud.get_courses(db)

@app.post("/register", response_model=schemas.StudentInDB)
def register_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    if crud.get_student_by_email(db, email=student.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_student(db=db, student=student)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    student = auth.authenticate_user(db, form_data.username, form_data.password)
    if not student:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": student.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.StudentInDB)
async def read_users_me(current_user: models.Student = Depends(auth.get_current_user)):
    return current_user

# --- ADMIN ENDPOINT ---
@app.get("/matches/admin", response_model=List[schemas.AdminMatch])
def get_admin_matches(db: Session = Depends(get_db), current_user: models.Student = Depends(auth.require_admin)):
    students = crud.get_students(db)
    # The Jaccard function is now for the admin view
    return matching.calculate_jaccard_similarity(students)

# --- USER ENDPOINT ---
@app.get("/matches/user", response_model=List[schemas.UserMatch])
def get_user_matches(db: Session = Depends(get_db), current_user: models.Student = Depends(auth.get_current_active_user)):
    students = crud.get_students(db)
    # The Cosine function is for the user view
    return matching.calculate_cosine_similarity(students, current_user.id)

# --- Secret endpoint to make an admin ---
@app.get("/_make_admin_")
def make_admin(db: Session = Depends(get_db)):
    admin_email = "tukurmmr@gmail.com"
    user = crud.get_student_by_email(db, email=admin_email)
    if not user: raise HTTPException(status_code=404, detail=f"User {admin_email} not found. Please register first.")
    user.is_admin = True
    db.commit()
    return {"message": f"User {admin_email} has been made an admin."}