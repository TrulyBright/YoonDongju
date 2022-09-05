from datetime import datetime, timedelta
import re
from typing import Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
import FastAPIApp.crud as crud
import FastAPIApp.database as database
import FastAPIApp.models as models
from FastAPIApp.settings import get_settings
import requests

SECRET_KEY = get_settings().JWT_SECRET
ALGORITHM = "HS256"

id_pattern = "^.{1,65}$"  # 1자 이상 64자 이하에 어떤 문자든 허용됨
# 10자 이상에 숫자와 영문이 하나씩은 있어야 함.
password_pattern = "^(?=.*[0-9])(?=.*[a-zA-Z]).{10,}$"

sinchon_student_id_pattern = "^[0-9]{4}1[0-9]{5}$"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate(db: Session, username: str, password: str):
    member = crud.get_member_by_username(db, username)
    if not member:
        return False
    if not pwd_context.verify(password, member.password):
        return False
    return member


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
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
    member = models.Member.from_orm(
        crud.get_member_by_username(db, username=token_data.username))
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
    return get_student_information(id, pw)


def is_sinchon_member(student_id: str) -> bool:
    return re.match(sinchon_student_id_pattern, student_id)


def get_student_status(id: str, pw: str):
    return get_student_information(id, pw).status


def get_student_information(id: str, pw: str):
    id = str(id)
    pw = str(pw)
    print(len(id))
    print(len(pw))
    if len(pw) > 1024:
        raise
    if len(id) > 1024:
        raise
    if not is_sinchon_member(id):
        raise HTTPException(401, "신촌캠 학부 학번이 필요합니다.")
    settings = get_settings()
    response = requests.get(settings.YONSEI_AUTH_FUNCTION_ENDPOINT, params={
        "id": id,
        "pw": pw,
        "code": settings.YONSEI_AUTH_FUNCTION_CODE
    })
    if response.status_code != 200:
        raise HTTPException(500, "연세포탈에서 정보를 받아오는 데 실패했습니다.")
    json = response.json()
    return models.ClubMember(status=json["status"], student_id=id, name=json["name"], dept_and_major=json["deptMajor"])
