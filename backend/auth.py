from datetime import datetime, timedelta
import json
import requests
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

import crud
import database
import models
from settings import get_settings

SECRET_KEY = get_settings().jwt_secret
ALGORITHM = "HS256"

id_pattern = "^.{1,65}$"  # 1자 이상 64자 이하에 어떤 문자든 허용됨
# 10자 이상에 숫자와 영문이 하나씩은 있어야 함.
password_pattern = "^(?=.*[0-9])(?=.*[a-zA-Z]).{10,}$"


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


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM), expire.timestamp()


async def get_current_member(
    db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
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


async def get_current_member_board_only(
    member: models.Member = Depends(get_current_member),
):
    if member.role in {models.Role.board, models.Role.president}:
        return member
    raise HTTPException(403, "권한이 없습니다.")


def is_yonsei_member(id: str, pw: str) -> bool:
    try:
        return get_student_information(id, pw).usertypename == "학부학생"
    except:
        return False


def get_student_information(id: str, pw: str):
    if len(pw) > 1024:
        raise
    if len(id) > 1024:
        raise
    if id[4] == "2":
        raise HTTPException(status_code=403, detail="신촌캠이 아닙니다.")
    settings = get_settings()
    response = requests.post(
        url=settings.yonsei_fetch_api_endpoint,
        data={"id": settings.yonsei_fetch_api_yonsei_id},
    )
    token: str = json.loads(response.content.decode())["data"][0]["wstoken"]
    response = requests.post(
        url=settings.yonsei_login_api_endpoint,
        data={
            "userid": id,
            "password": pw,
            "wstoken": token,
            "wsfunction": settings.yonsei_login_api_function,
            "lang": "ko",
            "moodlewsrestformat": "json",
        },
    )
    try:
        return models.ClubMember(**json.loads(response.content.decode())["data"])
    except:
        return False
