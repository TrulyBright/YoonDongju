from datetime import datetime, timedelta
import re
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

import crud
import database
import models
from settings import get_settings

SECRET_KEY = get_settings().jwt_secret
ALGORITHM = "HS256"

id_pattern = "^.{1,65}$"  # 1자 이상 64자 이하에 어떤 문자든 허용됨
# 10자 이상에 숫자와 영문이 하나씩은 있어야 함.
password_pattern = "^(?=.*[0-9])(?=.*[a-zA-Z]).{10,}$"

sinchon_student_id_pattern = "^[0-9]{4}1[0-9]{5}$"


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
    return get_student_information(id, pw)


def is_sinchon_member(student_id: str) -> bool:
    return re.match(sinchon_student_id_pattern, student_id)


def get_student_status(id: str, pw: str):
    return get_student_information(id, pw).status


def get_student_information(id: str, pw: str):
    if len(pw) > 1024:
        raise
    if len(id) > 1024:
        raise
    if id[4] != "1":
        raise HTTPException(status_code=403, detail="신촌캠 학부 학번이 필요합니다.")
    options = FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1280,720")
    driver = Firefox(options=options)
    # NOTE: Ubuntu on OCI for some reason doesn't work with geckodriver.
    # Use Fedora or something as an alternative.
    driver.get("https://portal.yonsei.ac.kr")
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "jooyohaksalink1"))
    ).click()
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "loginId"))
    ).send_keys(id)
    driver.find_element(By.ID, "loginPasswd").send_keys(pw)
    driver.find_element(By.ID, "loginBtn").click()
    unauthorized = False
    try:
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "btn_open_icon"))
        ).click()
    except TimeoutException:
        unauthorized = True
    else:
        name = driver.find_element(By.ID, "wq_uuid_63").get_attribute("textContent")
        dept_and_major = driver.find_element(By.ID, "wq_uuid_77").get_attribute(
            "textContent"
        )
        status = driver.find_element(By.ID, "wq_uuid_90").get_attribute("textContent")
    finally:
        driver.quit()
    if unauthorized:
        raise HTTPException(401, "연세포탈에 로그인하는 데 실패했습니다.")
    return models.ClubMember(
        status=status, student_id=id, name=name, dept_and_major=dept_and_major
    )
