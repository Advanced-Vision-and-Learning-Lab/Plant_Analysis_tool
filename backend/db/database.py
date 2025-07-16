# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Import your Base from models.py
from .models import Base 

# --- Database URL Configuration ---
# For local development, you might use SQLite:
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# For PostgreSQL (local or RDS):
# Replace placeholders with your actual RDS credentials and endpoint
# It's BEST PRACTICE to use environment variables for these sensitive details
SQLALCHEMY_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://user:password@localhost:5432/mydatabase" # Default for local testing
)

# For MySQL (local or RDS):
# SQLALCHEMY_DATABASE_URL = os.environ.get(
#    "DATABASE_URL",
#    "mysql+pymysql://user:password@localhost:3306/mydatabase" # Default for local testing
# )


# Create the SQLAlchemy Engine
# echo=True is useful for debugging as it logs all SQL statements
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create a SessionLocal class
# This class will be an actual database session for a single unit of work (e.g., one request)
# It's an instance of sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session (useful for FastAPI/Flask contexts)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create all tables defined in your models
def create_db_and_tables():
    print("Creating database tables...")
    # This command creates all tables defined in Base.metadata IF THEY DON'T ALREADY EXIST.
    # It does NOT update existing tables (for that, you need migrations).
    Base.metadata.create_all(engine)
    print("Database tables created (if they didn't exist).")