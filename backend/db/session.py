# session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# For local SQLite, or change to your actual DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./plant_analysis.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)