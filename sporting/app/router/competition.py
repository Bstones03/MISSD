from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from sqlalchemy import func, desc
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import os
from app.models import Competition, Shooter, SportingSSporting, SportingScore, TargetMenu  # Corrected model name

router = APIRouter(
    prefix="/competition",
    tags=["competition"]
)

# Define the directory for templates
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))

@router.get("/", response_class=HTMLResponse)
async def get_competitions(request: Request, db: Session = Depends(get_db)):
    competitions = db.query(Competition).all()
    return templates.TemplateResponse("competition.html", {"request": request, "competitions": competitions})

# Edit competition is_over
@router.get("/{id}/edit", response_class=HTMLResponse)
async def edit_competition(request: Request, id: int, db: Session = Depends(get_db)):
    competition = db.query(Competition).filter(Competition.Shoot_id == id).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    return templates.TemplateResponse("edit_competition.html", {"request": request, "competition": competition})

# Update competition is_over
@router.post("/{id}/edit")
async def update_competition(id: int, is_over: bool = Form(...), db: Session = Depends(get_db)):
    competition = db.query(Competition).filter(Competition.Shoot_id == id).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    competition.is_over = is_over
    db.commit()
    return RedirectResponse("/competition", status_code=303)

# Route for displaying the form to add a new competition
@router.get("/add", response_class=HTMLResponse)
async def get_add_competition_form(request: Request):
    return templates.TemplateResponse("add_competition.html", {"request": request})

# Route for handling the form submission to add a new competition
@router.post("/add")
async def add_competition(
    Shoot_name: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    is_over: bool = Form(...),
    db: Session = Depends(get_db)
):
    new_competition = Competition(
        Shoot_name=Shoot_name,
        city=city,
        state=state,
        is_over=is_over
    )
    db.add(new_competition)
    db.commit()
    return {"message": "Competition added successfully"}


@router.get("/{id}/shooters", response_class=HTMLResponse)
async def get_competition_shooters(request: Request, id: int, db: Session = Depends(get_db)):
    # Fetch competition based on ID
    competition = db.query(Competition).filter(Competition.Shoot_id == id).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    
    # Fetch shooters and their scores, ordered by total score in descending order
    shooters_scores = (
        db.query(Shooter, SportingSSporting)
        .join(SportingSSporting, Shooter.Shid == SportingSSporting.Shid)
        .filter(SportingSSporting.Shoot_id == id)
        .order_by(desc(SportingSSporting.total))
        .all()
    )

    if not shooters_scores:
        raise HTTPException(status_code=404, detail="No shooters found for this competition.")

    # Prepare data for the template
    shooters = [
        {
            "S_Fname": shooter.S_Fname,
            "S_Lname": shooter.S_Lname,
            "total": sportingSSporting.total,
        }
        for shooter, sportingSSporting in shooters_scores
    ]

    return templates.TemplateResponse("shooters_scores.html", {
        "request": request,
        "competition": competition,
        "shooters": shooters,  # Pass flattened data
    })
