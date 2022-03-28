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
last_post_no = -1
club_info = {
    "address": "somewhere",
    "email": "someone@some.where",
    "president_name": "john doe",
    "president_tel": "010-0000-0000",
    "join_form_url": "https://example.com"
}
about_data = {
    "title": "about",
    "content": "us",
}
posted_posts = dict()

def change_role(into: models.Role):
    db: Session = TestingSessionLocal()
    crud.update_member(
        db=db,
        student_id=settings.test_portal_id,
        member=models.MemberModify(role=into)
    )
    assert crud.get_member(db=db, student_id=settings.test_portal_id).role == into.value
    db.close()


def test_register():
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

def test_login():
    global my_token
    data = {
        "username": settings.test_username,
        "password": settings.test_password,
    }
    response = tested.post("/login", data=data)
    assert response.status_code == 200
    my_token = response.json()["access_token"]

def test_update_club_information():
    change_role(models.Role.member)
    info = club_info.copy()
    info["token"] = "asdf"
    response = tested.put("/club-information", json=info)
    assert response.status_code == 401
    info["token"] = my_token
    response = tested.put("/club-information", json=info)
    assert response.status_code == 403
    change_role(models.Role.board)
    response = tested.put("/club-information", json=info)
    assert response.status_code == 200
    updated: dict = response.json()
    assert updated == club_info

def test_get_club_information():
    response = tested.get("/club-information")
    assert response.status_code == 200
    assert response.json() == club_info

def test_get_recent_magazines():
    response = tested.get("/recent-magazines")
    assert response.status_code == 200

def test_update_about():
    change_role(models.Role.member)
    
    data = about_data.copy()
    data["token"] = "asdf"
    response = tested.put("/about", json=data)
    assert response.status_code == 401

    data["token"] = my_token
    response = tested.put("/about", json=data)
    assert response.status_code == 403
    
    change_role(models.Role.board)
    response = tested.put("/about", json=data)
    assert response.status_code == 200
    posted = response.json()
    assert posted["title"] == data["title"]
    assert posted["content"] == data["content"]
    assert posted["modified"] == datetime.today().date().strftime("%Y-%m-%d")
    assert posted["modifier"] == settings.test_real_name
    assert posted["type"] == models.PostType.about
    
    response = tested.get("/about")
    assert response.json() == posted

def test_get_about():
    response = tested.get("/about")
    assert response.status_code == 200
    about = response.json()
    assert about["title"] == about_data["title"]
    assert about["content"] == about_data["content"]
    assert about["type"] == models.PostType.about

def test_get_rules():
    response = tested.get("/rules")
    assert response.status_code == 200

def test_update_rules():
    change_role(models.Role.member)
    response = tested.patch("/rules")
    assert response.status_code == 200

def test_get_recent_notices():
    for _ in range(10):
        test_create_notice()
    response = tested.get("/recent-notices")
    assert response.status_code == 200
    assert response.json() == list(posted_posts.values())[::-1][:4]
    response = tested.get("/recent-notices", params={"limit":10})
    assert response.json() == list(posted_posts.values())[::-1]

def test_get_notices():
    for _ in range(100):
        test_create_notice()
    span = {
        "skip": 0,
        "limit": 50
    }
    response = tested.get("/notices", params=span)
    assert response.status_code == 200
    assert response.json() == list(posted_posts.values())[::-1][span["skip"]:span["skip"]+span["limit"]]
    span["skip"] = 17
    response = tested.get("/notices", params=span)
    assert response.json() == list(posted_posts.values())[::-1][span["skip"]:span["skip"]+span["limit"]]

def test_create_notice():
    change_role(models.Role.member)
    global last_post_no
    data = {
        "title": "tested-title",
        "content": "tested=content",
        "token": "asdf"
    }
    response = tested.post("/notices", json=data)
    assert response.status_code == 401

    data["token"] = my_token
    response = tested.post("/notices", json=data)
    assert response.status_code == 403

    change_role(models.Role.board)
    response = tested.post("/notices", json=data)
    assert response.status_code == 200
    posted: dict = response.json()
    assert posted["title"] == data["title"]
    assert posted["content"] == data["content"]
    assert posted["type"] == models.PostType.notice.value
    assert posted["author"] == settings.test_real_name
    assert posted["published"] == datetime.today().strftime("%Y-%m-%d")
    assert posted["modifier"] == None
    assert posted["modified"] == None
    last_post_no = posted["no"]
    test_get_notice(posted)
    posted_posts[posted["no"]] = posted

def test_get_notice(data=None):
    response = tested.get(f"/notices/{data['no'] if data else last_post_no}")
    assert response.status_code == 200
    if data:
        posted: dict = response.json()
        assert posted["title"] == data["title"]
        assert posted["content"] == data["content"]
        assert posted["type"] == models.PostType.notice.value
        assert posted["author"] == data["author"]
        assert posted["published"] == data["published"]
        assert posted["modifier"] == data["modifier"]
        assert posted["modified"] == data["modified"]

def test_update_notice():
    change_role(models.Role.member)
    modified = {
        "title": "updated-title",
        "content": "updated=content",
        "token": my_token
    }
    modified["token"] = my_token
    assert tested.patch(f"/notices/{last_post_no}", json=modified).status_code == 403

    change_role(models.Role.board)
    today = datetime.today().strftime("%Y-%m-%d")
    response = tested.patch(f"/notices/{last_post_no}", json=modified)
    assert response.status_code == 200
    posted: dict = response.json()
    assert posted["title"] == modified["title"]
    assert posted["content"] == modified["content"]
    assert posted["type"] == models.PostType.notice.value
    assert posted["author"] == settings.test_real_name
    assert posted["modifier"] == settings.test_real_name
    assert posted["modified"] == today
    assert posted["no"] == last_post_no
    test_get_notice(posted)

    modified["token"] = "asdf"
    assert tested.patch(f"/notices/{last_post_no}", json=modified).status_code == 401

    posted_posts[posted["no"]] = posted

def test_delete_notice():
    change_role(models.Role.member)
    deletion_params = {
        "token": "asdf"
    }
    assert tested.delete(f"/notices/{last_post_no}", params=deletion_params).status_code == 401
    assert tested.get(f"/notices/{last_post_no}").status_code == 200

    deletion_params["token"] = my_token
    assert tested.delete(f"/notices/{last_post_no}", params=deletion_params).status_code == 403
    assert tested.get(f"/notices/{last_post_no}").status_code == 200

    change_role(models.Role.board)
    assert tested.delete(f"/notices/{last_post_no}", params=deletion_params).status_code == 200
    assert tested.get(f"/notices/{last_post_no}").status_code == 404
    assert tested.delete(f"/notices/{last_post_no}", params=deletion_params).status_code == 404
    del posted_posts[last_post_no]

def test_get_members():
    response = tested.get("/members")
    assert response.status_code == 200

def test_get_member():
    response = tested.get(f"/members/{settings.test_portal_id}")
    assert response.status_code == 200

def test_patch_member():
    change_role(models.Role.member)
    response = tested.patch(f"/members/{settings.test_portal_id}")
    assert response.status_code == 200

def test_delete_member():
    change_role(models.Role.member)
    response = tested.delete(f"/members/{settings.test_portal_id}")
    assert response.status_code == 200

def test_get_magazines():
    response = tested.get("/magazines")
    assert response.status_code == 200

def test_create_magazine():
    change_role(models.Role.member)
    response = tested.post("/magazines")
    assert response.status_code == 200

def test_get_magazine():
    response = tested.get(f"/magazines/2022-01-01")
    assert response.status_code == 200

def test_update_magazine():
    change_role(models.Role.member)
    response = tested.patch("/magazines/2022-01-01")
    assert response.status_code == 200

def test_delete_magazine():
    change_role(models.Role.member)
    response = tested.delete("/magazines/2022-01-01")
    assert response.status_code == 200

def test_get_classes():
    response = tested.get("/classes")
    assert response.status_code == 200

def test_get_class():
    response = tested.get("/classes/poetry")
    assert response.status_code == 200

def test_update_class():
    change_role(models.Role.member)
    response = tested.patch("/classes/poetry")
    assert response.status_code == 200

def test_get_class_records():
    response = tested.get("/classes/poetry/records")
    assert response.status_code == 200

def test_create_class_record():
    change_role(models.Role.member)
    response = tested.post("/classes/poetry/records")
    assert response.status_code == 200

def test_get_class_record():
    response = tested.get("/classes/poetry/records/1")
    assert response.status_code == 200

def test_update_class_record():
    change_role(models.Role.member)
    response = tested.patch("/classes/poetry/records/1")
    assert response.status_code == 200

def test_delete_class_record():
    change_role(models.Role.member)
    response = tested.patch("/classes/poetry/records/1")
    assert response.status_code == 200