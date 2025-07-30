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

# (Public and User endpoints remain the same)
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
@app.get("/matches/user", response_model=List[schemas.UserMatch])
def get_user_matches(db: Session = Depends(get_db), current_user: models.Student = Depends(auth.get_current_active_user)):
    students = crud.get_students(db)
    return matching.calculate_matches_for_user(students, current_user.id)

# --- NEW AND UPDATED ADMIN ENDPOINTS ---
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

# --- Secret endpoint to make an admin ---
@app.get("/_make_admin_")
def make_admin(db: Session = Depends(get_db)):
    admin_email = "tukurmmr@gmail.com"
    user = crud.get_student_by_email(db, email=admin_email)
    if not user: raise HTTPException(status_code=404, detail=f"User {admin_email} not found. Please register first.")
    user.is_admin = True
    db.commit()
    return {"message": f"User {admin_email} has been made an admin."}