from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.database import get_db  # Changed to absolute import
from . import models
from .auth import router as auth_router
from .crud import get_all_students, delete_student, make_admin, get_courses, get_interests
from .matching import compute_jaccard_matches, compute_dice_matches
from .auth import get_current_user, get_current_admin
from .crud import update_student_profile

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://studentmatcher.netlify.app"],  # Allow your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/admin/users")
def read_users(db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    users = get_all_students(db)
    return users

@app.delete("/admin/users/{student_id}")
def delete_user(student_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    success = delete_student(db, student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted successfully"}

@app.post("/admin/make_admin/{student_id}")
def make_user_admin(student_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    student = make_admin(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.get("/admin/matches/jaccard")
def get_jaccard_matches(db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    matches = compute_jaccard_matches(db)
    return matches

@app.get("/admin/matches/dice")
def get_dice_matches(db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    matches = compute_dice_matches(db)
    return matches

@app.get("/courses")
def read_courses(db: Session = Depends(get_db)):
    return get_courses(db)

@app.get("/interests")
def read_interests(db: Session = Depends(get_db)):
    return get_interests(db)

@app.get("/users/me")
def read_current_user(current_user = Depends(get_current_user)):
    return current_user

@app.get("/matches/user")
def get_user_matches(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    matches = compute_jaccard_matches(db, current_user.id)  # Use Jaccard or Dice as default
    return matches[0] if matches else None  # Return top match

@app.patch("/profile")
def update_profile(course_id: int, interest_ids: list[int], db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    student = update_student_profile(db, current_user.id, course_id, interest_ids)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.delete("/profile")
def delete_my_profile(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    success = delete_student(db, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Profile deleted successfully"}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # Run as module to fix import issues
