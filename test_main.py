from datetime import datetime, date
import json
import uuid
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import sqlalchemy.event as sqlevent
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
sqlevent.listen(engine, "connect", lambda conn, rec: conn.execute("PRAGMA foreign_keys=ON;"))
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

database.Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

main.app.dependency_overrides[database.get_db] = override_get_db
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
rules = {
    "title": "rules",
    "content": "not that strict"
}

def get_jwt_header(invalid=False):
    return {"Authorization": "Bearer "+("asdf" if invalid else my_token)}

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
    response = tested.post("/token", data=data)
    assert response.status_code == 200
    my_token = response.json()["access_token"]

def test_update_club_information():
    change_role(models.Role.member)
    info = club_info
    response = tested.put("/club-information", json=info, headers=get_jwt_header(True))
    assert response.status_code == 401
    response = tested.put("/club-information", json=info, headers=get_jwt_header())
    assert response.status_code == 403
    change_role(models.Role.board)
    response = tested.put("/club-information", json=info, headers=get_jwt_header())
    assert response.status_code == 200
    updated: dict = response.json()
    assert updated == club_info

def test_get_club_information():
    response = tested.get("/club-information")
    assert response.status_code == 200
    assert response.json() == club_info

def test_update_about():
    change_role(models.Role.member)
    response = tested.put("/about", json=about_data, headers=get_jwt_header(True))
    assert response.status_code == 401

    response = tested.put("/about", json=about_data, headers=get_jwt_header())
    assert response.status_code == 403
    
    change_role(models.Role.board)
    response = tested.put("/about", json=about_data, headers=get_jwt_header())
    assert response.status_code == 200
    posted = response.json()
    assert posted["title"] == about_data["title"]
    assert posted["content"] == about_data["content"]
    assert posted["modified"] == datetime.today().date().strftime("%Y-%m-%d")
    assert posted["modifier"] == settings.test_real_name
    
    response = tested.get("/about")
    assert response.json() == posted

def test_get_about():
    response = tested.get("/about")
    assert response.status_code == 200
    about = response.json()
    assert about["title"] == about_data["title"]
    assert about["content"] == about_data["content"]

def test_update_rules():
    response = tested.put("/rules", json=rules, headers=get_jwt_header(True))
    assert response.status_code == 401
    
    change_role(models.Role.member)
    response = tested.put("/rules", json=rules, headers=get_jwt_header())
    assert response.status_code == 403

    change_role(models.Role.board)
    response = tested.put("/rules", json=rules, headers=get_jwt_header())
    assert response.status_code == 200
    changed = response.json()
    assert changed["title"] == rules["title"]
    assert changed["content"] == rules["content"]
    assert changed["published"] == datetime.today().date().strftime("%Y-%m-%d")
    assert changed["author"] == "연세문학회"
    test_get_rules()

def test_get_rules():
    response = tested.get("/rules")
    assert response.status_code == 200
    posted = response.json()
    assert posted["title"] == rules["title"]
    assert posted["content"] == rules["content"]
    assert posted["published"] == datetime.today().date().strftime("%Y-%m-%d")
    assert posted["author"] == "연세문학회"

def test_get_recent_notices():
    for _ in range(10):
        test_create_notice()
    response = tested.get("/recent-notices")
    assert response.status_code == 200
    assert response.json() == list(posted_posts.values())[::-1][:4]
    response = tested.get("/recent-notices", params={"limit":10})
    assert response.json() == list(posted_posts.values())[::-1]

def test_get_notices():
    for _ in range(10):
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
    }
    response = tested.post("/notices", json=data, headers=get_jwt_header(True))
    assert response.status_code == 401

    response = tested.post("/notices", json=data, headers=get_jwt_header())
    assert response.status_code == 403

    change_role(models.Role.board)
    response = tested.post("/notices", json=data, headers=get_jwt_header())
    assert response.status_code == 200
    posted: dict = response.json()
    assert posted["title"] == data["title"]
    assert posted["content"] == data["content"]
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
        assert posted["author"] == data["author"]
        assert posted["published"] == data["published"]
        assert posted["modifier"] == data["modifier"]
        assert posted["modified"] == data["modified"]

def test_update_notice():
    change_role(models.Role.member)
    modified = {
        "title": "updated-title",
        "content": "updated=content",
    }
    assert tested.patch(f"/notices/{last_post_no}", json=modified, headers=get_jwt_header()).status_code == 403

    change_role(models.Role.board)
    today = datetime.today().strftime("%Y-%m-%d")
    response = tested.patch(f"/notices/{last_post_no}", json=modified, headers=get_jwt_header())
    assert response.status_code == 200
    posted: dict = response.json()
    assert posted["title"] == modified["title"]
    assert posted["content"] == modified["content"]
    assert posted["author"] == settings.test_real_name
    assert posted["modifier"] == settings.test_real_name
    assert posted["modified"] == today
    assert posted["no"] == last_post_no
    test_get_notice(posted)

    assert tested.patch(f"/notices/{last_post_no}", json=modified, headers=get_jwt_header(True)).status_code == 401

    posted_posts[posted["no"]] = posted

def test_delete_notice():
    assert tested.delete(f"/notices/{last_post_no}", headers=get_jwt_header(True)).status_code == 401
    assert tested.get(f"/notices/{last_post_no}").status_code == 200

    change_role(models.Role.member)
    assert tested.delete(f"/notices/{last_post_no}", headers=get_jwt_header()).status_code == 403
    assert tested.get(f"/notices/{last_post_no}").status_code == 200

    change_role(models.Role.board)
    assert tested.delete(f"/notices/{last_post_no}", headers=get_jwt_header()).status_code == 200
    assert tested.get(f"/notices/{last_post_no}").status_code == 404
    assert tested.delete(f"/notices/{last_post_no}", headers=get_jwt_header()).status_code == 404
    del posted_posts[last_post_no]

def test_get_members():
    response = tested.get("/members")
    assert response.status_code == 401
    change_role(models.Role.member)
    response = tested.get("/members", headers=get_jwt_header())
    assert response.status_code == 403
    change_role(models.Role.board)
    response = tested.get("/members", headers=get_jwt_header())
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
    change_role(models.Role.board)
    dummy_upload = [
        tested.post(
            "/uploaded",
            files={
                "uploaded": (
                    "main.py",
                    open("main.py", "rb"),
                    "text/plain"
                )
            },
            headers=get_jwt_header()
        ).json() for _ in range(1, 129)
    ]
    dummies = [{
        "year": i,
        "season": i,
        "cover": dummy_upload[i-1]["uuid"],
        "published": date(year=i, month=1, day=1).strftime("%Y-%m-%d"),
        "contents": [
            models.MagazineContentCreate(
                type="시",
                title="서시",
                author="윤동주",
                language="한국어"
            ).dict() for _ in range(37)]
    } for i in range(1, 129)]
    change_role(models.Role.board)
    for d in dummies:
        tested.post("/magazines", json=d, headers=get_jwt_header())
    response = tested.get("/magazines")
    assert response.status_code == 200
    assert response.json() == dummies[::-1][:100]
    params = {
        "skip": 3,
        "limit": 11
    }
    response = tested.get("/magazines", params=params)
    assert response.status_code == 200
    assert response.json() == dummies[::-1][params["skip"]:params["skip"]+params["limit"]]

def test_get_magazine():
    uploaded = tested.post(
        "/uploaded",
        files={
            "uploaded": (
                "main.py",
                open("main.py", "rb"),
                "text/plain"
            )
        },
        headers=get_jwt_header()
    ).json()["uuid"]
    dummy = {
        "year": 1984,
        "season": 1,
        "cover": uploaded,
        "published": date(year=1984, month=4, day=3).strftime("%Y-%m-%d"),
        "contents": [
            models.MagazineContentCreate(
                type="소설",
                title="1984",
                author="조지 오웰",
                language="영어"
            ).dict()]
    }
    change_role(models.Role.board)
    tested.post("/magazines", json=dummy, headers=get_jwt_header())
    response = tested.get(f"/magazines/{dummy['published']}")
    assert response.status_code == 200
    assert response.json() == dummy

def test_create_magazine():
    uploaded = tested.post(
        "/uploaded",
        files={
            "uploaded": (
                "main.py",
                open("main.py", "rb"),
                "text/plain"
            )
        },
        headers=get_jwt_header()
    ).json()["uuid"]
    data = {
        "year": 2022,
        "season": 1,
        "cover": uploaded,
        "published": "2022-01-01",
        "contents": [
            models.MagazineContentCreate(
                type="시",
                title="「형」",
                author="심보선",
                language="한국어"
            ).dict() for _ in range(100)],
    }
    response = tested.post("/magazines", json=data)
    assert response.status_code == 401

    change_role(models.Role.member)
    response = tested.post("/magazines", headers=get_jwt_header())
    assert response.status_code == 403

    change_role(models.Role.board)
    response = tested.post("/magazines", headers=get_jwt_header(), json=data)
    assert response.status_code == 200
    assert response.json() == data

def test_get_recent_magazines():
    params = {"limit": 8}
    response = tested.get("/recent-magazines", params=params)
    assert response.status_code == 200
    assert len(response.json()) == params["limit"]

def test_create_uploaded_file():
    with open("main.py", "rb") as f:
        response = tested.post("/uploaded", headers=get_jwt_header(True), files={"uploaded": ("asdf.asdf", b"wer", "text/plain")})
        assert response.status_code == 401
        change_role(models.Role.member)
        response = tested.post("/uploaded", headers=get_jwt_header(), files={"uploaded": ("asdf.asdf", b"awe", "text/plain")})
        assert response.status_code == 403
        change_role(models.Role.board)
        response = tested.post("/uploaded", headers=get_jwt_header(), files={"uploaded":("main.py", f, "text/plain")})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "main.py"
        uuid = data["uuid"]
    with open("main.py", "rb") as f:
        response = tested.get(f"/uploaded/{uuid}")
        assert response.status_code == 200
        assert response.headers["content-disposition"].endswith(f'"{data["name"]}"')
        assert response.content == f.read()

def test_update_magazine():
    change_role(models.Role.board)
    uploaded = tested.post(
        "/uploaded",
        files={
            "uploaded": (
                "main.py",
                open("main.py", "rb"),
                "text/plain"
            )
        },
        headers=get_jwt_header()
    ).json()["uuid"]
    prev = {
        "year": 2016,
        "season": 5,
        "cover": uploaded,
        "published": "2016-05-13",
        "contents": [
            models.MagazineContentCreate(
                type="시나리오",
                title="『나, 다니엘 블레이크』",
                author="폴 레이버티",
                language="영어"
            ).dict()]
    }
    data = {
        "year": 2019,
        "season": 1,
        "cover": uploaded,
        "published": "2019-05-30",
        "contents": [
            models.MagazineContentCreate(
                type="시나리오",
                title="『기생충』",
                author="봉준호, 한진원",
                language="한국어"
            ).dict()]
    }
    change_role(models.Role.board)
    response = tested.post("/magazines", headers=get_jwt_header(), json=prev)

    response = tested.patch(f"/magazines/{prev['published']}", json=data)
    assert response.status_code == 401

    change_role(models.Role.member)
    response = tested.patch(f"/magazines/{prev['published']}", headers=get_jwt_header(), json=data)
    assert response.status_code == 403
    
    change_role(models.Role.board)
    response = tested.patch(f"/magazines/{prev['published']}", headers=get_jwt_header(), json=data)
    assert response.status_code == 200
    assert response.json() == data
    
    response = tested.get(f"/magazines/{data['published']}")
    assert response.status_code == 200
    assert response.json() == data

def test_delete_magazine():
    uploaded = tested.post(
        "/uploaded",
        files={
            "uploaded": (
                "main.py",
                open("main.py", "rb"),
                "text/plain"
            )
        },
        headers=get_jwt_header()
    ).json()["uuid"]
    data = {
        "year": 2002,
        "season": 1,
        "cover": uploaded,
        "published": "2002-06-25",
        "contents": [
            models.MagazineContentCreate(
                type="소설",
                title="「황만근은 이렇게 말했다」",
                author="성석제",
                language="한국어"
            ).dict()]
    }
    change_role(models.Role.board)
    tested.post("/magazines", json=data, headers=get_jwt_header())

    response = tested.delete(f"/magazines/{data['published']}")
    assert response.status_code == 401
    
    change_role(models.Role.member)
    response = tested.delete(f"/magazines/{data['published']}", headers=get_jwt_header())
    assert response.status_code == 403

    change_role(models.Role.board)
    response = tested.delete(f"/magazines/{data['published']}", headers=get_jwt_header())
    assert response.status_code == 200
    
def test_get_uploaded_file():
    generated = uuid.uuid4()
    response = tested.get(f"uploaded/{generated}")
    assert response.status_code == 404
    response = tested.get("uploaded/../requirements.txt")
    assert response.status_code == 404

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