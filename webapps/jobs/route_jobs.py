from fastapi import APIRouter,Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import  Jinja2Templates
from db.repository.jobs import list_jobs, retrieve_job
from sqlalchemy.orm import Session
from db.session import get_db



templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)

@router.get("/")
def home(request:Request,db:Session=Depends(get_db)):
    jobs = list_jobs(db=db)
    return templates.TemplateResponse("jobs/homepage.html",{"request":request,"jobs":jobs})

@router.get("/detail/{id}")
def job_detail(id:int,request:Request,db:Session=Depends(get_db)):
    job = retrieve_job(id=id,db=db)
    return templates.TemplateResponse("jobs/detail.html",{"request":request,"job":job})
