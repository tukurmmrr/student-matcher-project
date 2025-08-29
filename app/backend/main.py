# app/backend/main.py

"""
Main application file for the FastAPI backend.
This file defines all the API endpoints, sets up CORS middleware,
and ties together the other modules (crud, auth, matching, etc.).
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas, matching, auth
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

# Create all database tables based on the models defined in models.py
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI()

# Define the list of allowed origins for Cross-Origin Resource Sharing (CORS)
origins = [
    "http://localhost:5173",  # For local development
    "https://studentmatcher.netlify.app" # For the deployed frontend
]

# Add CORS middleware to allow the frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get a new database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Public Endpoints (No Authentication Required) ---

@app.get("/interests", response_model=List[schemas.Interest])
def read_interests(db: Session = Depends(get_db)):
    """Endpoint to fetch the list of all available interests."""
    return crud.get_interests(db)

@app.get("/courses", response_model=List[schemas.Course])
def read_courses(db: Session = Depends(get_db)):
    """Endpoint to fetch the list of all available courses."""
    return crud.get_courses(db)

@app.post("/register", response_model=schemas.StudentInDB)
def register_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Endpoint for new students to register an account."""
    # Check if a user with the same email already exists
    if crud.get_student_by_email(db, email=student.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_student(db=db, student=student)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Endpoint for students to log in and receive a JWT access token."""
    student = auth.authenticate_user(db, form_data.username, form_data.password)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Create a JWT token with the user's email as the subject
    access_token = auth.create_access_token(data={"sub": student.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- User Endpoints (Login Required) ---

@app.get("/users/me", response_model=schemas.StudentInDB)
async def read_users_me(current_user: models.Student = Depends(auth.get_current_user)):
    """Endpoint to get the profile information of the currently logged-in user."""
    return current_user

@app.put("/users/me", response_model=schemas.StudentInDB)
async def update_user_profile_endpoint(profile_data: schemas.StudentUpdate, db: Session = Depends(get_db), current_user: models.Student = Depends(auth.get_current_active_user)):
    """Endpoint for the logged-in user to update their own profile (course and interests)."""
    return crud.update_student_profile(db=db, user=current_user, profile_data=profile_data)

@app.get("/matches/user", response_model=List[schemas.UserMatch])
def get_user_matches(db: Session = Depends(get_db), current_user: models.Student = Depends(auth.get_current_active_user)):
    """Endpoint to get a personalized list of matches for the logged-in user."""
    students = crud.get_students(db)
    return matching.calculate_matches_for_user(students, current_user.id)

# --- ADMIN ENDPOINTS (Admin Login Required) ---

@app.get("/admin/matches/jaccard", response_model=List[schemas.AdminMatch])
def get_admin_jaccard_matches(db: Session = Depends(get_db), admin_user: models.Student = Depends(auth.require_admin)):
    """Endpoint for admins to view all pairwise matches using the Jaccard Index."""
    students = crud.get_students(db)
    return matching.calculate_jaccard_for_admin(students)

@app.get("/admin/matches/dice", response_model=List[schemas.AdminMatch])
def get_admin_dice_matches(db: Session = Depends(get_db), admin_user: models.Student = Depends(auth.require_admin)):
    """Endpoint for admins to view all pairwise matches using the Dice Coefficient."""
    students = crud.get_students(db)
    # This now correctly calls the new Dice function
    return matching.calculate_dice_for_admin(students)

@app.get("/admin/users", response_model=List[schemas.StudentInDB])
def get_all_users_as_admin(db: Session = Depends(get_db), admin_user: models.Student = Depends(auth.require_admin)):
    """Endpoint for admins to get a list of all registered users."""
    return crud.get_students(db)

@app.delete("/admin/users/{user_id}", response_model=schemas.StudentInDB)
def delete_user_as_admin(user_id: int, db: Session = Depends(get_db), admin_user: models.Student = Depends(auth.require_admin)):
    """Endpoint for admins to delete a user by their ID."""
    user_to_delete = crud.delete_user_by_admin(db=db, user_id=user_id)
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")
    return user_to_delete

# (Secret admin endpoint remains)
@app.get("/_make_admin_")
def make_admin(db: Session = Depends(get_db)):
    """
    A secret endpoint to grant admin privileges to a specific user.
    Note: This is for development/setup purposes and would not be used in a real production environment.
    """
    admin_email = "tukurmmr@gmail.com"
    user = crud.get_student_by_email(db, email=admin_email)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {admin_email} not found. Please register first.")
    user.is_admin = True
    db.commit()
    return {"message": f"User {admin_email} has been made an admin."}