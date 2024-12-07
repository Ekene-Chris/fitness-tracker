# models/exercise.py
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database import Base

class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    category = Column(String)  # e.g., "strength", "cardio", "flexibility"
    muscle_group = Column(String)
    difficulty_level = Column(String)

class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)
    duration_minutes = Column(Integer)
    notes = Column(Text)
    
    exercise = relationship("Exercise")
    workout = relationship("Workout", back_populates="exercises")

class Workout(Base):
    __tablename__ = "workouts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    date = Column(DateTime)
    duration_minutes = Column(Integer)
    calories_burned = Column(Integer)
    notes = Column(Text)
    
    exercises = relationship("WorkoutExercise", back_populates="workout")

class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    name = Column(String)
    description = Column(Text)
    target_value = Column(Float)
    current_value = Column(Float)
    deadline = Column(DateTime)
    status = Column(String)  # "in_progress", "completed", "failed"
    category = Column(String)  # "weight", "strength", "endurance", etc.

class PersonalRecord(Base):
    __tablename__ = "personal_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    value = Column(Float)
    date_achieved = Column(DateTime)
    notes = Column(Text)
    
    exercise = relationship("Exercise")

class CalorieLog(Base):
    __tablename__ = "calorie_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    date = Column(DateTime)
    calories_consumed = Column(Integer)
    protein_grams = Column(Float)
    carbs_grams = Column(Float)
    fat_grams = Column(Float)
    notes = Column(Text)
