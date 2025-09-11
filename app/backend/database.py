# app/backend/database.py

"""
Database setup and configuration
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()  # load .env file

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for models
Base = declarative_base()