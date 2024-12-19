from fastapi import APIRouter, Depends, Form, UploadFile, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from app.database import get_db
from app.models import Competition, Shooter, SportingSSporting
from pathlib import Path
import os

router = APIRouter(
    prefix="/scores",
    tags=["scores"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
BASE_DIR = Path(__file__).resolve().parent.parent


@router.get("/upload", response_class=HTMLResponse)
async def upload_score_page(request: Request, db: Session = Depends(get_db)):
    competitions = db.query(Competition).all()
    shooters = db.query(Shooter).all()
    return templates.TemplateResponse("upload_score.html", {
        "request": request,
        "competitions": competitions,
        "shooters": shooters
    })


@router.post("/upload")
async def upload_score(
    competition_id: int = Form(...),
    shooter_id: int = Form(...),
    score: int = Form(...),
    super: bool = Form(False),  # Default to False if not checked
    photo: UploadFile = Form(...),
    db: Session = Depends(get_db)
):
    # Ensure the "uploads" directory exists
    upload_dir = BASE_DIR / "uploads"
    upload_dir.mkdir(exist_ok=True)

    # Save the uploaded photo to the filesystem
    photo_path = upload_dir / photo.filename
    try:
        with open(photo_path, "wb") as f:
            f.write(await photo.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    # Check if the shooter and competition exist
    shooter = db.query(Shooter).filter(Shooter.Shid == shooter_id).first()
    if not shooter:
        raise HTTPException(status_code=404, detail="Shooter not found")

    competition = db.query(Competition).filter(Competition.Shoot_id == competition_id).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")

    # Dynamically generate a unique Station_id
    max_station_id = db.query(SportingSSporting).filter(SportingSSporting.Shoot_id == competition_id).count()

    # Create a new SportingSSporting entry
    new_entry = SportingSSporting(
        Shoot_id=competition_id,
        Station_id=max_station_id + 1,  # Increment to ensure uniqueness
        super=super,
        #Sqid=0,  # Placeholder; adjust based on your logic
        Shid=shooter_id,
        total=score,
    )

    # Add and commit the new entry to the database
    try:
        db.add(new_entry)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database insertion failed: {str(e)}")

    return {"message": "Score uploaded successfully", "photo_path": str(photo_path)}
