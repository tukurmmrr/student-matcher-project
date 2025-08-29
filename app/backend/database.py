# app/backend/database.py

"""
This module handles the database connection setup using SQLAlchemy.
It creates the database engine and a session maker for interacting
with the database.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from a .env file (e.g., the database URL).
load_dotenv()

# Get the database connection string from environment variables.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine. This is the core interface to the database.
# For PostgreSQL, we don't need the 'connect_args' used for SQLite.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class. Each instance of SessionLocal will be a
# new database session. This is the primary way we will interact with the DB.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class. Our ORM models (in models.py) will inherit from this
# class so that SQLAlchemy knows about them.
Base = declarative_base()