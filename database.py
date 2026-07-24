from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Engine
engine = create_engine(
    DATABASE_URL
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def create_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Base class για όλα τα models
Base = declarative_base()