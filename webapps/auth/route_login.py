from webapps.auth.forms import LoginForm
from fastapi import APIRouter,Request, Depends, responses, status, HTTPException
from fastapi.templating import  Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.users import UserCreate
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from apis.version1.route_login import login_for_access_token

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)

@router.get("/login/")
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request":request})
    

@router.post("/login/")
async def login(request: Request, db : Session = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login successful")
            response = templates.TemplateResponse("auth/login.html",form.__dict__)
            login_for_access_token(response=response,form_data=form,db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect email / passowrd")
            return templates.TemplateResponse("auth/login.html",form.__dict__)
    return templates.TemplateResponse("auth/login.html",form.__dict__)




    
