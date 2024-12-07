# routes/calories.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ..database import get_db
from ..models.exercise import CalorieLog
from ..schemas.exercise import CalorieLog as CalorieLogSchema, CalorieLogCreate

router = APIRouter()

@router.post("/calories/", response_model=CalorieLogSchema)
def log_calories(
    log: CalorieLogCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    db_log = CalorieLog(**log.dict(), user_id=user_id)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/calories/summary")
def get_calorie_summary(
    user_id: int,
    start_date: datetime,
    end_date: datetime = None,
    db: Session = Depends(get_db)
):
    if end_date is None:
        end_date = start_date + timedelta(days=7)
    
    logs = db.query(CalorieLog).filter(
        CalorieLog.user_id == user_id,
        CalorieLog.date >= start_date,
        CalorieLog.date <= end_date
    ).all()
    
    return {
        "total_calories": sum(log.calories_consumed for log in logs),
        "avg_daily_calories": sum(log.calories_consumed for log in logs) / (end_date - start_date).days,
        "total_protein": sum(log.protein_grams or 0 for log in logs),
        "total_carbs": sum(log.carbs_grams or 0 for log in logs),
        "total_fat": sum(log.fat_grams or 0 for log in logs)
    }

@router.put("/calories/{log_id}", response_model=CalorieLogSchema)
def update_calorie_log(
    log_id: int,
    log: CalorieLogCreate,
    db: Session = Depends(get_db)
):
    db_log = db.query(CalorieLog).filter(CalorieLog.id == log_id).first()
    if db_log is None:
        raise HTTPException(status_code=404, detail="Calorie log not found")
    
    for key, value in log.dict().items():
        setattr(db_log, key, value)
    
    db.commit()
    db.refresh(db_log)
    return db_log

@router.delete("/calories/{log_id}")
def delete_calorie_log(log_id: int, db: Session = Depends(get_db)):
    db_log = db.query(CalorieLog).filter(CalorieLog.id == log_id).first()
    if db_log is None:
        raise HTTPException(status_code=404, detail="Calorie log not found")
    
    db.delete(db_log)
    db.commit()
    return {"message": "Calorie log deleted successfully"}