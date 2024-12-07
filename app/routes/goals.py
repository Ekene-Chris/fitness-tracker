# routes/goals.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.exercise import Goal
from ..schemas.exercise import Goal as GoalSchema, GoalCreate

router = APIRouter()

@router.post("/goals/", response_model=GoalSchema)
def create_goal(goal: GoalCreate, user_id: int, db: Session = Depends(get_db)):
    db_goal = Goal(**goal.dict(), user_id=user_id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.get("/goals/", response_model=List[GoalSchema])
def list_goals(
    user_id: int,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Goal).filter(Goal.user_id == user_id)
    if status:
        query = query.filter(Goal.status == status)
    return query.all()

@router.put("/goals/{goal_id}/progress", response_model=GoalSchema)
def update_goal_progress(
    goal_id: int,
    current_value: float,
    db: Session = Depends(get_db)
):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    goal.current_value = current_value
    if current_value >= goal.target_value:
        goal.status = "completed"
    
    db.commit()
    db.refresh(goal)
    return goal

@router.put("/goals/{goal_id}", response_model=GoalSchema)
def update_goal(
    goal_id: int,
    goal: GoalCreate,
    db: Session = Depends(get_db)
):
    db_goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    for key, value in goal.dict().items():
        setattr(db_goal, key, value)
    
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.delete("/goals/{goal_id}")
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    db_goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    db.delete(db_goal)
    db.commit()
    return {"message": "Goal deleted successfully"}
