# app/backend/security.py

"""
Password hashing utilities using bcrypt
"""

from passlib.context import CryptContext

# bcrypt context for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """Check if password matches hash"""
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)