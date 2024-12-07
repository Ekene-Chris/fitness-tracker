# routes/records.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.exercise import PersonalRecord
from ..schemas.exercise import PersonalRecord as PRSchema, PersonalRecordCreate

router = APIRouter()

@router.post("/records/", response_model=PRSchema)
def create_personal_record(
    record: PersonalRecordCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    db_record = PersonalRecord(**record.dict(), user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.get("/records/exercise/{exercise_id}", response_model=List[PRSchema])
def get_exercise_records(
    exercise_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    records = db.query(PersonalRecord).filter(
        PersonalRecord.exercise_id == exercise_id,
        PersonalRecord.user_id == user_id
    ).order_by(PersonalRecord.value.desc()).all()
    return records

@router.put("/records/{record_id}", response_model=PRSchema)
def update_personal_record(
    record_id: int,
    record: PersonalRecordCreate,
    db: Session = Depends(get_db)
):
    db_record = db.query(PersonalRecord).filter(PersonalRecord.id == record_id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Personal record not found")
    
    for key, value in record.dict().items():
        setattr(db_record, key, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record

@router.delete("/records/{record_id}")
def delete_personal_record(record_id: int, db: Session = Depends(get_db)):
    db_record = db.query(PersonalRecord).filter(PersonalRecord.id == record_id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Personal record not found")
    
    db.delete(db_record)
    db.commit()
    return {"message": "Personal record deleted successfully"}
