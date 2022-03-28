from datetime import datetime, timedelta
import requests
from fastapi import Depends, FastAPI, HTTPException, status
import fastapi
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

import crud

SECRET_KEY = "test"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def authenticate(db: Session, username: str, password: str):
    member = crud.get_member_by_username(db, username)
    if not member:
        return False
    if not pwd_context.verify(password, member.password):
        return False
    return member

def create_access_token(data: dict, expires_delta: timedelta | None=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_member(db, token: str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    member = crud.get_member_by_username(db, username=token_data.username)
    if member is None:
        raise credentials_exception
    return member

def is_yonsei_member(id: int, pw: str):
    if len(pw) > 1024: raise
    data = {
        "loginType": "SSO",
        "retUrl": "/relation/otherSiteSSO",
        "type": "pmg",
        "id": id,
        "password": pw
    }
    return data["retUrl"] in requests.post(
        "https://library.yonsei.ac.kr/login",
        data=data,
        allow_redirects=True
    ).url