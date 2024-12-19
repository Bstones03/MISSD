from fastapi import APIRouter, Depends, HTTPException, Request
from app import models, schemas
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import os

# Import your database models and database session
from app.models import Shooter, School
from app.database import get_db

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))

router = APIRouter(
    prefix="/shooters",
    tags=["shooters"]
)



# Create a new shooter
@router.post("/", response_model=schemas.ShooterBase)
def create_shooter(shooter: schemas.ShooterCreate, db: Session = Depends(get_db)):
    db_shooter = models.Shooter(
        S_Fname=shooter.S_Fname,
        S_Lname=shooter.S_Lname,
        school_id=shooter.school_id,
        Schname=shooter.Schname,
        #shooting_level=shooter.shooting_level,
        handed=shooter.handed,
        gender=shooter.gender,
        #ata_num=shooter.ata_num,
        #nssa_num=shooter.nssa_num,
        #nsca_num=shooter.nsca_num,
        #sctp_num=shooter.sctp_num,
        Still_shooting=shooter.Still_shooting,
        sqid=shooter.sqid
    )
    db.add(db_shooter)
    db.commit()
    db.refresh(db_shooter)
    return db_shooter

@router.post("/", response_model=schemas.ShooterBase)
def create_shooter(shooter: schemas.ShooterCreate, db: Session = Depends(get_db)):
    db_shooter = models.Shooter(**shooter.dict())
    db.add(db_shooter)
    db.commit()
    db.refresh(db_shooter)
    return db_shooter

@router.get("/",response_model=schemas.ShooterBase)
async def get_shooters(request: Request, db: Session = Depends(get_db)):
    shooters = db.query(Shooter).join(School, Shooter.school_id == School.school_id).all()
    return templates.TemplateResponse("shooters.html", {"request": request, "shooters": shooters})

@router.get("/{shid}", response_model=schemas.ShooterBase)
async def read_shooter(shid: int, request: Request, db: Session = Depends(get_db)):
    shooter = db.query(Shooter).filter(Shooter.Shid == shid).first()
    if shooter is None:
        raise HTTPException(status_code=404, detail="Shooter not found")
    return templates.TemplateResponse("shooters.html", {"request": request, "shooters": shooter})

@router.delete("/{shid}", response_model=schemas.ShooterBase)
def delete_shooter(shid: int, db: Session = Depends(get_db)):
    shooter = db.query(models.Shooter).filter(models.Shooter.Shid == shid).first()
    if shooter is None:
        raise HTTPException(status_code=404, detail="Shooter not found")
    db.delete(shooter)
    db.commit()
    return shooter

@router.get("/search_shooters")
async def search_shooters(request: Request, query: str = "", db: Session = Depends(get_db)):
    shooters = db.query(Shooter).join(School).filter(
        (Shooter.S_Fname.contains(query)) |
        (Shooter.S_Lname.contains(query)) |
        (Shooter.Shid.contains(query)) |
        (School.Schname.contains(query))
    ).all()
    return templates.TemplateResponse("shooters.html", {"request": request, "shooters": shooters})