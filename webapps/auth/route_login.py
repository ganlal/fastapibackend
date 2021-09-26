from webapps.auth.forms import load_data
from fastapi import APIRouter,Request, Depends, responses, status
from fastapi.templating import  Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.users import UserCreate
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)

@router.get("/login/")
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request":request})
    
