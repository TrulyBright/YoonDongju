from datetime import datetime, timedelta
import requests
from fastapi import Depends, FastAPI, HTTPException, status
import fastapi
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import InvalidHeaderError

import crud
import database
import models
from settings import get_settings

SECRET_KEY = get_settings().authjwt_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

id_pattern = "^.{1,65}$"  # 1자 이상 64자 이하에 어떤 문자든 허용됨
# 10자 이상에 숫자와 영문이 하나씩은 있어야 함.
password_pattern = "^(?=.*[0-9])(?=.*[a-zA-Z]).{10,}$"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


@AuthJWT.load_config
def get_config():
    return get_settings()


def authenticate(db: Session, username: str, password: str):
    member = crud.get_member_by_username(db, username)
    if not member:
        return False
    if not pwd_context.verify(password, member.password):
        return False
    return member

async def get_current_member(db: Session = Depends(database.get_db), Authorize: AuthJWT = Depends()):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        username: str = Authorize.get_jwt_subject()
        if username is None:
            raise credentials_exception
    except InvalidHeaderError:
        raise credentials_exception
    member = crud.get_member_by_username(db, username=username)
    if member is None:
        raise credentials_exception
    return member


async def get_current_member_board_only(member: models.Member = Depends(get_current_member)):
    if member.role in {
        models.Role.board,
        models.Role.president
    }:
        return member
    raise HTTPException(403, "권한이 없습니다.")


def is_yonsei_member(id: int, pw: str):
    if len(pw) > 1024:
        raise
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
