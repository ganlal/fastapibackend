from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from fastapi import APIRouter

from datetime import datetime, timedelta
from jose import jwt,JWTError

from starlette.status import HTTP_401_UNAUTHORIZED
from core.config import settings
from sqlalchemy.orm import Session

from db.repository.login import get_user
from core.hashing import  Hasher
from db.session import get_db


from core.security import create_access_token

router = APIRouter()

def authenticate_user(username:str,password:str,db:Session):
    user = get_user(username=username,db=db)
    print(user)
    if not user:
        return False
    if not Hasher.verify_password(password,user.hashed_password):
        return False
    return user


@router.post("/token")
def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends(),
    db:Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username / password")
    access_token_expire = timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES)    
    access_token = create_access_token(data={"sub":user.email},expires_delta=access_token_expire)
    return {"access_token":access_token,"token_type":"bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

def get_current_user_from_token(token:str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credential_exception = HTTPException(status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials")
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        username:str = payload.get("sub")
        print(f"email is: {username}")
        if username is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    user = get_user(username=username,db=db)
    if user is None:
        raise credential_exception
    return user



