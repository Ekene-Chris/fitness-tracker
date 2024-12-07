# schemas/exercise.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ExerciseBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    muscle_group: str
    difficulty_level: str

class ExerciseCreate(ExerciseBase):
    pass

class Exercise(ExerciseBase):
    id: int
    
    class Config:
        orm_mode = True

class WorkoutExerciseBase(BaseModel):
    exercise_id: int
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None

class WorkoutExerciseCreate(WorkoutExerciseBase):
    pass

class WorkoutExercise(WorkoutExerciseBase):
    id: int
    exercise: Exercise
    
    class Config:
        orm_mode = True

class WorkoutBase(BaseModel):
    date: datetime
    duration_minutes: int
    calories_burned: Optional[int] = None
    notes: Optional[str] = None

class WorkoutCreate(WorkoutBase):
    pass

class Workout(WorkoutBase):
    id: int
    exercises: List[WorkoutExercise] = []
    
    class Config:
        orm_mode = True

class GoalBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_value: float
    current_value: float = 0.0
    deadline: datetime
    category: str
    status: str = "in_progress"

class GoalCreate(GoalBase):
    pass

class Goal(GoalBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

class PersonalRecordBase(BaseModel):
    exercise_id: int
    value: float
    date_achieved: datetime
    notes: Optional[str] = None

class PersonalRecordCreate(PersonalRecordBase):
    pass

class PersonalRecord(PersonalRecordBase):
    id: int
    user_id: int
    exercise: Exercise
    
    class Config:
        orm_mode = True

class CalorieLogBase(BaseModel):
    date: datetime
    calories_consumed: int
    protein_grams: Optional[float] = None
    carbs_grams: Optional[float] = None
    fat_grams: Optional[float] = None
    notes: Optional[str] = None

class CalorieLogCreate(CalorieLogBase):
    pass

class CalorieLog(CalorieLogBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True