import os
from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.auth.sso import router as sso_router
from dotenv import load_dotenv
from app.router import shooter, school, scores, competition, upload

# Load environment variables from .env file
load_dotenv()

# Fetch values from the environment
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.include_router(shooter.router)
app.include_router(school.router)
app.include_router(scores.router)
app.include_router(competition.router)
app.include_router(upload.router)
app.include_router(sso_router, prefix="/auth")

@app.get("/")
async def index(request: Request):
    user = request.session.get("user")
    if user:
        return RedirectResponse("/auth/welcome")
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/login")
async def index(request: Request):

    return templates.TemplateResponse("login.html", {"request": request})