# auth/sso.py
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# OAuth Configuration
oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    client_kwargs={'scope': 'openid email profile'},
)

@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth")      #not implemented yet
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": e.error})
    user = token.get("userinfo")
    if user:
        request.session["user"] = dict(user)
    return RedirectResponse("/welcome")

@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse("/")

@router.get("/welcome")
async def welcome(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/")
    return templates.TemplateResponse("welcome.html", {"request": request, "user": user})
