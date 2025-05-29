# main.py (FastAPI app entrypoint)

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import plant_analysis_api

# 🔧 New imports for DB setup
from backend.db.models import Base
from backend.db.session import engine

# Enable debug-level logging
logging.basicConfig(level=logging.DEBUG)

# Initialize app
app = FastAPI(title="Plant Analysis Backend")

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to ["http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔧 Create database tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(plant_analysis_api.router, prefix="/api")
