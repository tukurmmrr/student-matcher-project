# app/backend/security.py

"""
This module contains security-related utility functions, specifically
for password hashing and verification using the passlib library.
"""

from passlib.context import CryptContext

# Create a CryptContext instance, specifying bcrypt as the hashing scheme.
# 'bcrypt' is a strong, widely-used hashing algorithm.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    Verifies a plain-text password against a stored hash.
    Returns True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    """
    Hashes a plain-text password using the configured scheme (bcrypt).
    Returns the generated hash.
    """
    return pwd_context.hash(password)