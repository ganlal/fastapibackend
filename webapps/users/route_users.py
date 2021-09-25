from db.repository.users import create_new_user
from webapps.users.forms import UserCreateForm
from fastapi import APIRouter,Request, Depends, responses, status
from fastapi.templating import  Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.users import UserCreate
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError




router = APIRouter(include_in_schema=False)
template = Jinja2Templates(directory="templates")

@router.get("/register/")
def register(request:Request):
    return template.TemplateResponse("users/register.html",{"request":request}) 

@router.post("/register/")
async def register(request:Request,db:Session = Depends(get_db)):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            user = UserCreate(username=form.username, email=form.email,password=form.password)
            try:
                user = create_new_user(user=user,db=db)
                return responses.RedirectResponse("/?msg=Successfully registered",status_code=status.HTTP_302_FOUND)
            except IntegrityError:
                form.__dict__.get("errors").append("Duplicate user name or email")
                return template.TemplateResponse("users/register.html",form.__dict__)

            return template.TemplateResponse("users/register.html",form.__dict__)
        except ValidationError:
            print("Pydantic validation error")
            form.__dict__.get("errors").append("Email not valid")
            return template.TemplateResponse("users/register.html",form.__dict__)





