from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import  Session
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND


from db.session import get_db
from db.models.jobs import Job
from db.models.users import User
from schemas.jobs import JobCreate, ShowJob
from db.repository.jobs import create_new_job, retrieve_job, list_jobs,update_job_by_id,delete_job_by_id

from apis.version1.route_login import  get_current_user_from_token

from typing import List


router = APIRouter()


@router.post("/create-job",response_model=ShowJob)
def create_job(job: JobCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user_from_token)):
    owner_id = current_user.id
# def create_job(job: JobCreate,db:Session=Depends(get_db)):
#     owner_id = 1
    job = create_new_job(job=job, db=db, owner_id=owner_id)
    return job

@router.get("/get/{id}",response_model=ShowJob)
def retrieve_job_by_id(id:int,db:Session = Depends(get_db)):
    job = retrieve_job(id=id,db=db)
    if not job :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Job with id {id} does not exist")
    return job    

@router.get("/all",response_model=List[ShowJob])
def retrieve_all_jobs(db:Session = Depends(get_db)):
    jobs = list_jobs(db=db)
    return jobs

# @router.put("/update/{id}")
# def update_job(id:int,job:JobCreate,db:Session=Depends(get_db)):
#     owner_id = 1
#     message = update_job_by_id(id=id,job=job,db=db,owner_id=owner_id)
#     if not message:
#         raise HTTPException(status_code=HTTP_404_NOT_FOUND,
#         detail=f"Job with {id} does not exist") 
#     return{"detail:Successfully updated the data"}

@router.put("/update/{id}")
def update_job(id:int,job:JobCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user_from_token)):
    owner_id = current_user.id
    # print("I reached here .. update")
    job_chk = retrieve_job(id=id,db=db)
    if not job_chk:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
        detail=f"Job with {id} does not exist")     
    if job_chk.owner_id == current_user.id or current_user.is_superuser:
        update_job_by_id(id=id,job=job,db=db,owner_id=owner_id)
        return{"detail":"Job successfully updated"}
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
    detail=f"You are not authorised") 


@router.delete("/delete/{id}")
def delete_job(id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user_from_token)):
    owner_id = current_user.id
    job = retrieve_job(id=id,db=db)
    if not job:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
        detail=f"Job with {id} does not exist")        

    if job.owner_id == current_user.id or current_user.is_superuser:
        delete_job_by_id(id=id,db=db,owner_id=current_user.id)
        return{"detail":"Job successfully deleted"}

    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
    detail=f"You are not authorised") 
