from datetime import datetime
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from pydantic import BaseSettings
import database
import models
import crud
import schemas
import main

SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

database.Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

main.app.dependency_overrides[main.get_db] = override_get_db
tested = TestClient(main.app)

class Settings(BaseSettings):
    test_portal_id: str
    test_portal_pw: str
    test_real_name: str
    test_username: str
    test_password: str
    class Config:
        env_file = "test.env"
        env_file_encoding = "utf-8"

settings = Settings()

my_token = str()

def change_role(into: models.Role):
    db: Session = TestingSessionLocal()
    crud.update_member(
        db=db,
        student_id=settings.test_portal_id,
        member=models.MemberModify(role=into)
    )
    assert crud.get_member(db=db, student_id=settings.test_portal_id).role == into.value
    db.close()

def test_auth():
    global my_token
    data = {
        "portal_id": settings.test_portal_id,
        "portal_pw": settings.test_portal_pw,
        "real_name": settings.test_real_name,
        "username": settings.test_username,
        "password": settings.test_password
    }
    response = tested.post("/register", json=data)
    assert response.status_code == 200
    created: dict = response.json()
    assert created["student_id"] == int(settings.test_portal_id)
    assert created["real_name"] == settings.test_real_name
    assert created["username"] == settings.test_username
    assert created["role"] == models.Role.member.value
    data = {
        "username": settings.test_username,
        "password": settings.test_password,
    }
    response = tested.post("/login", data=data)
    assert response.status_code == 200
    my_token = response.json()["access_token"]

def test_posting():
    # a list with no post
    response = tested.get("/notices")
    assert response.status_code == 200
    assert response.json() == []
    # no such post 404
    response = tested.get("/notices/1")
    assert response.status_code == 404
    # creation: unauthorized
    initial = {
        "title": "tested-title",
        "content": "tested=content",
        "token": "asdf"
    }
    response = tested.post("/notices", json=initial)
    assert response.status_code == 401
    # creation: forbidden
    initial["token"] = my_token
    response = tested.post("/notices", json=initial)
    assert response.status_code == 403
    # creation: authorized
    change_role(models.Role.board)
    response = tested.post("/notices", json=initial)
    assert response.status_code == 200
    posted: dict = response.json()
    assert posted["title"] == initial["title"]
    assert posted["content"] == initial["content"]
    assert posted["type"] == models.PostType.notice.value
    assert posted["author"] == settings.test_real_name
    assert posted["published"] == datetime.today().strftime("%Y-%m-%d")
    assert posted["modifier"] == None
    assert posted["modified"] == None
    no = posted["no"]
    # confirm creation
    response = tested.get(f"/notices/{no}")
    assert response.status_code == 200
    # patch
    modified = {
        "title": "updated-title",
        "content": "updated=content",
        "token": my_token
    }
    response = tested.patch(f"/notices/{no}", json=modified)
    today = datetime.today().strftime("%Y-%m-%d")
    assert response.status_code == 200
    posted: dict = response.json()
    assert posted["title"] == modified["title"]
    assert posted["content"] == modified["content"]
    assert posted["type"] == models.PostType.notice.value
    assert posted["author"] == settings.test_real_name
    assert posted["modifier"] == settings.test_real_name
    assert posted["modified"] == today
    assert posted["no"] == no
    # confirm patched
    response = tested.get(f"/notices/{no}")
    assert response.status_code == 200
    posted: dict = response.json()
    assert posted["title"] == modified["title"]
    assert posted["content"] == modified["content"]
    assert posted["type"] == models.PostType.notice.value
    assert posted["author"] == settings.test_real_name
    assert posted["modifier"] == settings.test_real_name
    assert posted["modified"] == today
    assert posted["no"] == no
    # unauthorized patch
    modified["token"] = "asdf"
    assert tested.patch(f"/notices/{no}", json=modified).status_code == 401
    # forbidden patch
    change_role(models.Role.member)
    modified["token"] = my_token
    assert tested.patch(f"/notices/{no}", json=modified).status_code == 403
    # delete
    response = tested.delete(f"/notices/{no}")
    assert response.status_code == 200
    # confirm deletion
    response = tested.get(f"/notices/{no}")
    assert response.status_code == 404