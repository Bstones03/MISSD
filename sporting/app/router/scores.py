from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app import schemas
from app.database import get_db
from app.models import SportingScore, SportingSSporting, TargetMenu
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

router = APIRouter(
    prefix="/score",
    tags=["score"]
)

# Load Jinja2 templates
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# Fetch scores
@router.get("/", response_class=HTMLResponse)
async def get_scores(request: Request, db: Session = Depends(get_db)):
    scores = (
        db.query(SportingScore)
        .options(
            joinedload(SportingScore.targetmenu),
        )
        .all()
    )
    return templates.TemplateResponse("scores.html", {"request": request, "scores": scores})


# Fetch detailed scores for a competition
@router.get("/competition/{competition_id}", response_class=HTMLResponse)
async def get_competition_scores(competition_id: int, request: Request, db: Session = Depends(get_db)):
    competition_scores = (
        db.query(SportingSSporting)
        .filter(SportingSSporting.Shoot_id == competition_id)
        .all()
    )
    return templates.TemplateResponse(
        "competition_scores.html",
        {"request": request, "competition_scores": competition_scores},
    )
