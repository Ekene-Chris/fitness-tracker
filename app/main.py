# main.py
from fastapi import FastAPI
from .routes import exercise, goals, records, calories
from .database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Tracking API")

# Include routers
app.include_router(exercise.router, prefix="/api/v1", tags=["exercises"])
app.include_router(goals.router, prefix="/api/v1", tags=["goals"])
app.include_router(records.router, prefix="/api/v1", tags=["records"])
app.include_router(calories.router, prefix="/api/v1", tags=["calories"])