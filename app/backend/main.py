from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas, matching, security, auth
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [ "http://localhost:5173", "https://studentmatcher.netlify.app" ]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# --- Public Endpoints ---
# (Courses, Interests, Register, Token - no changes needed)

# --- User Endpoints (Require Login) ---
@app.get("/users/me", response_model=schemas.StudentInDB)
async def read_users_me(current_user: models.Student = Depends(auth.get_current_user)):
    return current_user

# --- THIS ENDPOINT WAS MISSING ---
@app.put("/users/me", response_model=schemas.StudentInDB)
async def update_user_profile_endpoint(profile_data: schemas.StudentUpdate, db: Session = Depends(get_db), current_user: models.Student = Depends(auth.get_current_active_user)):
    return crud.update_student_profile(db=db, user=current_user, profile_data=profile_data)

@app.get("/matches/user", response_model=List[schemas.UserMatch])
def get_user_matches(db: Session = Depends(get_db), current_user: models.Student = Depends(auth.get_current_active_user)):
    students = crud.get_students(db)
    return matching.calculate_matches_for_user(students, current_user.id)

# --- ADMIN ENDPOINTS (Require Admin Login) ---
@app.get("/admin/matches/jaccard", response_model=List[schemas.AdminMatch])
def get_admin_jaccard_matches(db: Session = Depends(get_db), admin_user: models.Student = Depends(auth.require_admin)):
    students = crud.get_students(db)
    return matching.calculate_jaccard_for_admin(students)

@app.get("/admin/matches/dice", response_model=List[schemas.AdminMatch])
def get_admin_dice_matches(db: Session = Depends(get_db), admin_user: models.Student = Depends(auth.require_admin)):
    students = crud.get_students(db)
    return matching.calculate_dice_for_admin(students)

@app.get("/admin/users", response_model=List[schemas.StudentInDB])
def get_all_users_as_admin(db: Session = Depends(get_db), admin_user: models.Student = Depends(auth.require_admin)):
    return crud.get_students(db)

@app.delete("/admin/users/{user_id}", response_model=schemas.StudentInDB)
def delete_user_as_admin(user_id: int, db: Session = Depends(get_db), admin_user: models.Student = Depends(auth.require_admin)):
    user_to_delete = crud.delete_user_by_admin(db=db, user_id=user_id)
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")
    return user_to_delete
