# routes/exercise.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.exercise import Exercise, Workout, WorkoutExercise
from ..schemas.exercise import (
    Exercise as ExerciseSchema,
    ExerciseCreate,
    Workout as WorkoutSchema,
    WorkoutCreate,
    WorkoutExercise as WorkoutExerciseSchema
)

router = APIRouter()

@router.post("/exercises/", response_model=ExerciseSchema)
def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    db_exercise = Exercise(**exercise.dict())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@router.get("/exercises/", response_model=List[ExerciseSchema])
def list_exercises(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    muscle_group: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Exercise)
    if category:
        query = query.filter(Exercise.category == category)
    if muscle_group:
        query = query.filter(Exercise.muscle_group == muscle_group)
    return query.offset(skip).limit(limit).all()

@router.post("/workouts/", response_model=WorkoutSchema)
def log_workout(workout: WorkoutCreate, user_id: int, db: Session = Depends(get_db)):
    db_workout = Workout(**workout.dict(), user_id=user_id)
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

@router.get("/workouts/{workout_id}", response_model=WorkoutSchema)
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

@router.put("/exercises/{exercise_id}", response_model=ExerciseSchema)
def update_exercise(
    exercise_id: int,
    exercise: ExerciseCreate,
    db: Session = Depends(get_db)
):
    db_exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if db_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    for key, value in exercise.dict().items():
        setattr(db_exercise, key, value)
    
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@router.delete("/exercises/{exercise_id}")
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    db_exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if db_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    db.delete(db_exercise)
    db.commit()
    return {"message": "Exercise deleted successfully"}

@router.put("/workouts/{workout_id}", response_model=WorkoutSchema)
def update_workout(
    workout_id: int,
    workout: WorkoutCreate,
    db: Session = Depends(get_db)
):
    db_workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if db_workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    for key, value in workout.dict().items():
        setattr(db_workout, key, value)
    
    db.commit()
    db.refresh(db_workout)
    return db_workout

@router.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    db_workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if db_workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    db.delete(db_workout)
    db.commit()
    return {"message": "Workout deleted successfully"}
