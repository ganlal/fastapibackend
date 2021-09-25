from fastapi import APIRouter,Request
from fastapi.templating import  Jinja2Templates


router = APIRouter(include_in_schema=False)
template = Jinja2Templates(directory="templates")

@router.get("/register/")
def register(request:Request):
    return template.TemplateResponse("users/register.html",{"request":request}) 

