from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

router = APIRouter(
    prefix="/schools",
    tags=["schools"]
)
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))

# Create a new school
@router.post("/", response_model=schemas.SchoolBase)
def create_school(school: schemas.SchoolCreate, db: Session = Depends(get_db)):
    db_school = models.School(Schname=school.Schname)
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school

# Get all schools
@router.get("/", response_model=List[schemas.SchoolBase])
async def get_schools(request: Request, db: Session = Depends(get_db)):
    schools = db.query(models.School).all()
    return templates.TemplateResponse("schools.html", {"request": request, "schools": schools})


# Get a specific school by ID
@router.get("/{school_id}", response_model=schemas.SchoolBase)
def get_school(school_id: int, db: Session = Depends(get_db)):
    school = db.query(models.School).filter(models.School.School_id == school_id).first()
    if school is None:
        raise HTTPException(status_code=404, detail="School not found")
    return school

# Update a school by ID
@router.put("/{school_id}", response_model=schemas.SchoolBase)
def update_school(school_id: int, school_update: schemas.SchoolCreate, db: Session = Depends(get_db)):
    school = db.query(models.School).filter(models.School.School_id == school_id).first()
    if school is None:
        raise HTTPException(status_code=404, detail="School not found")
    school.Schname = school_update.Schname
    db.commit()
    db.refresh(school)
    return school

# Delete a school by ID
@router.delete("/{school_id}", response_model=schemas.SchoolBase)
def delete_school(school_id: int, db: Session = Depends(get_db)):
    school = db.query(models.School).filter(models.School.School_id == school_id).first()
    if school is None:
        raise HTTPException(status_code=404, detail="School not found")
    db.delete(school)
    db.commit()
    return school
