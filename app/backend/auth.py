# app/backend/auth.py

"""
This module handles authentication-related functions, including creating
and verifying JWT tokens, checking user credentials, and dependency
injection for protected endpoints.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import crud, models, security
from database import SessionLocal

# --- Configuration ---
# IMPORTANT: In a real production app, this key should be loaded from a secure environment variable.
SECRET_KEY = "your-super-secret-key-that-you-should-change"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# This tells FastAPI how to find the token. It looks for a "Bearer" token
# in the Authorization header of incoming requests.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# --- Database Dependency ---
def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- JWT Token Functions ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a new JSON Web Token (JWT) for authentication.
    The token includes the user's identifier and an expiration time.
    """
    to_encode = data.copy()
    # Set the expiration time for the token.
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Encode the data into a JWT string.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# --- User Authentication ---
def authenticate_user(db: Session, email: str, password: str):
    """
    Verifies a user's email and password against the database.
    Returns the user object if successful, otherwise returns None.
    """
    user = crud.get_student_by_email(db, email=email)
    # Check if the user exists and if the provided password matches the stored hash.
    if not user or not security.verify_password(password, user.hashed_password):
        return None
    return user


# --- Dependencies for Protected Endpoints ---
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    FastAPI dependency that decodes the JWT token from the request,
    validates it, and fetches the corresponding user from the database.
    This is used to protect endpoints and identify the current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT to get the payload.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # The 'sub' (subject) claim should contain the user's email.
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        # If decoding fails (e.g., invalid signature, expired token), raise an error.
        raise credentials_exception

    # Fetch the user from the database using the email from the token.
    user = crud.get_student_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: models.Student = Depends(get_current_user)):
    """
    A simple dependency that builds on `get_current_user`.
    In the future, this could be expanded to check if a user is active/not banned.
    """
    return current_user


def require_admin(current_user: models.Student = Depends(get_current_user)):
    """
    Dependency for admin-only endpoints. It checks if the current user
    has the 'is_admin' flag set to True. If not, it raises a 403 Forbidden error.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return current_user