# app/backend/main.py

"""
Main FastAPI app - all the endpoints are here
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas, matching, auth
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",  # dev server
    "https://studentmatcher.netlify.app" # production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# public stuff - no login needed

@app.get("/interests", response_model=List[schemas.Interest])
def read_interests(db: Session = Depends(get_db)):
    return crud.get_interests(db)

@app.get("/courses", response_model=List[schemas.Course])
def read_courses(db: Session = Depends(get_db)):
    return crud.get_courses(db)

@app.post("/register", response_model=schemas.StudentInDB)
def register_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    # make sure email isn't already taken
    if crud.get_student_by_email(db, email=student.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_student(db=db, student=student)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # login and get JWT token
    student = auth.authenticate_user(db, form_data.username, form_data.password)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": student.email})
    return {"access_token": access_token, "token_type": "bearer"}

# user endpoints - need to be logged in

@app.get("/users/me", response_model=schemas.StudentInDB)
async def read_users_me(current_user: models.Student = Depends(auth.get_current_user)):
    # get your own profile
    return current_user

@app.put("/users/me", response_model=schemas.StudentInDB)
async def update_user_profile_endpoint(profile_data: schemas.StudentUpdate, db: Session = Depends(get_db), current_user: models.Student = Depends(auth.get_current_active_user)):
    # update your course and interests
    return crud.update_student_profile(db=db, user=current_user, profile_data=profile_data)

@app.get("/matches/user", response_model=List[schemas.UserMatch])
def get_user_matches(db: Session = Depends(get_db), current_user: models.Student = Depends(auth.get_current_active_user)):
    # see who you match with
    students = crud.get_students(db)
    return matching.calculate_matches_for_user(students, current_user.id)

# admin only endpoints

@app.get("/admin/matches/jaccard", response_model=List[schemas.AdminMatch])
def get_admin_jaccard_matches(db: Session = Depends(get_db), admin_user: models.Student = Depends(auth.require_admin)):
    # admin view of all matches using jaccard
    students = crud.get_students(db)
    return matching.calculate_jaccard_for_admin(students)

@app.get("/admin/matches/dice", response_model=List[schemas.AdminMatch])
def get_admin_dice_matches(db: Session = Depends(get_db), admin_user: models.Student = Depends(auth.require_admin)):
    # admin view using dice coefficient instead
    students = crud.get_students(db)
    return matching.calculate_dice_for_admin(students)

@app.get("/admin/users", response_model=List[schemas.StudentInDB])
def get_all_users_as_admin(db: Session = Depends(get_db), admin_user: models.Student = Depends(auth.require_admin)):
    # see all users
    return crud.get_students(db)

@app.delete("/admin/users/{user_id}", response_model=schemas.StudentInDB)
def delete_user_as_admin(user_id: int, db: Session = Depends(get_db), admin_user: models.Student = Depends(auth.require_admin)):
    # delete someone
    user_to_delete = crud.delete_user_by_admin(db=db, user_id=user_id)
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")
    return user_to_delete

@app.get("/_make_admin_")
def make_admin(db: Session = Depends(get_db)):
    """
    Temp endpoint to make myself admin during development.
    TODO: remove this before going live!
    """
    admin_email = "tukurmmr@gmail.com"
    user = crud.get_student_by_email(db, email=admin_email)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {admin_email} not found. Please register first.")
    user.is_admin = True
    db.commit()
    return {"message": f"User {admin_email} has been made an admin."}