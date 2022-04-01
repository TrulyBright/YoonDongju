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
    "attached": [],
}
posted_posts = dict()
rules = {
    "title": "rules",
    "content": "not that strict",
    "attached": [],
}

class_data = models.ClassCreate(
    moderator="성춘향",
    schedule="주 52시간",
    description="이몽룡 참석 금지"
).dict()

class_record_data = {
    "conducted": "1920-01-01",
    "topic": "김민규, 「카스테라」",
    "content": "<b>미상불 이보다 난해한 작품도 없습니다.</b>",
    "participants": [
        models.ClassParticipantCreate(
            name="채만식"
        ).dict()
    for _ in range(10)]
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
    for i, post in enumerate(list(posted_posts.values())[::-1][:4]):
        for key, value in response.json()[i].items():
            assert post[key] == value
    response = tested.get("/recent-notices", params={"limit":10})
    for i, post in enumerate(list(posted_posts.values())[::-1][:4]):
        for key, value in response.json()[i].items():
            assert post[key] == value

def test_get_notices():
    for _ in range(10):
        test_create_notice()
    span = {
        "skip": 0,
        "limit": 50
    }
    response = tested.get("/notices", params=span)
    assert response.status_code == 200
    for i, post in enumerate(list(posted_posts.values())[::-1][span["skip"]:span["skip"]+span["limit"]]):
        for key, value in response.json()[i].items():
            assert post[key] == value
    span["skip"] = 17
    response = tested.get("/notices", params=span)
    for i, post in enumerate(list(posted_posts.values())[::-1][span["skip"]:span["skip"]+span["limit"]]):
        for key, value in response.json()[i].items():
            assert post[key] == value

def test_create_notice():
    change_role(models.Role.board)
    attached = [tested.post(
        "/uploaded",
        files={
            "uploaded": (
                "main.py",
                open("main.py", "rb"),
                "text/plain"
            )
        },
        headers=get_jwt_header()
    ).json()["uuid"] for _ in range(3)]
    change_role(models.Role.member)
    global last_post_no
    data = {
        "title": "tested-title",
        "content": "tested=content",
        "attached": attached
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
    assert len(posted["attached"]) == len(attached)
    assert {uploaded["uuid"] for uploaded in posted["attached"]} == set(attached)
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
        assert len(posted["attached"]) == len(data["attached"])
        assert {uploaded["uuid"] for uploaded in posted["attached"]} == {uploaded["uuid"] for uploaded in data["attached"]}

def test_update_notice():
    change_role(models.Role.board)
    attached = [tested.post(
        "/uploaded",
        files={
            "uploaded": (
                "main.py",
                open("main.py", "rb"),
                "text/plain"
            )
        },
        headers=get_jwt_header()
    ).json()["uuid"] for _ in range(10)]
    change_role(models.Role.member)
    modified = {
        "title": "updated-title",
        "content": "updated=content",
        "attached": attached
    }
    assert tested.patch(f"/notices/{last_post_no}", json=modified, headers=get_jwt_header()).status_code == 403

    change_role(models.Role.board)
    today = datetime.today().strftime("%Y-%m-%d")
    response = tested.patch(f"/notices/{last_post_no}", json=modified, headers=get_jwt_header())
    assert response.status_code == 200
    posted: dict = response.json()
    assert posted["title"] == modified["title"]
    assert posted["content"] == modified["content"]
    assert len(posted["attached"]) == len(modified["attached"])
    assert {uploaded["uuid"] for uploaded in posted["attached"]} == set(attached)
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

def test_update_member():
    data = {
        "role": models.Role.member.value # downgrade? LOL
    }
    response = tested.patch(f"/members/{settings.test_portal_id}", json=data)
    assert response.status_code == 401

    change_role(models.Role.member)
    response = tested.patch(f"/members/{settings.test_portal_id}", json=data, headers=get_jwt_header())
    assert response.status_code == 403
    
    change_role(models.Role.board)
    response = tested.patch(f"/members/{settings.test_portal_id}", json=data, headers=get_jwt_header())
    assert response.status_code == 200
    assert response.json()["role"] == data["role"]

def test_get_magazines():
    change_role(models.Role.board)
    LENGTH = 10
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
        ).json() for _ in range(1, LENGTH)
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
    } for i in range(1, LENGTH)]
    change_role(models.Role.board)
    for d in dummies:
        tested.post("/magazines", json=d, headers=get_jwt_header())
    response = tested.get("/magazines")
    assert response.status_code == 200
    assert response.json() == dummies[::-1][:LENGTH]
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

    response = tested.get(f"/magazines/{prev['published']}")
    assert response.status_code == 404

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

    response = tested.get(f"/magazines/{data['published']}")
    assert response.status_code == 404
    
def test_get_uploaded_file():
    generated = uuid.uuid4()
    response = tested.get(f"uploaded/{generated}")
    assert response.status_code == 404
    response = tested.get("uploaded/../requirements.txt")
    assert response.status_code == 404

def test_update_class():
    for name in models.ClassName:
        expected = class_data.copy()
        expected["name"] = name
        response = tested.patch(f"/classes/{name}", json=class_data)
        assert response.status_code == 401

        change_role(models.Role.member)
        response = tested.patch(f"/classes/{name}", json=class_data, headers=get_jwt_header())
        assert response.status_code == 403

        change_role(models.Role.board)
        response = tested.patch(f"/classes/{name}", json=class_data, headers=get_jwt_header())
        assert response.status_code == 200
        assert response.json() == expected

        response = tested.get(f"/classes/{name}")
        assert response.status_code == 200
        assert response.json() == expected
        
        modified = class_data
        modified["moderator"] = expected["moderator"] = "이몽룡"
        modified["description"] = expected["description"] = "성춘향 환영"
        response = tested.patch(f"/classes/{name}", json=modified, headers=get_jwt_header())
        assert response.status_code == 200
        assert response.json() == expected
        response = tested.get(f"/classes/{name}")
        assert response.status_code == 200
        assert response.json() == expected

def test_get_classes():
    every_class = [tested.get(f"/classes/{name}").json() for name in models.ClassName]
    response = tested.get("/classes")
    assert response.status_code == 200
    assert response.json() == every_class

def test_get_class():
    for name in models.ClassName:
        expected = class_data.copy()
        expected["name"] = name
        response = tested.get(f"/classes/{name}")
        assert response.status_code == 200
        assert response.json() == expected

def test_get_class_records():
    for name in models.ClassName:
        change_role(models.Role.board)
        data = {
            "topic": "뒤치닥, 『투명드래곤』",
            "content": "본 회차 독서반에서 우리는 뒤치닥이 톨킨보다 위대한 이유를 명쾌히 논증해냈으나 여백이 부족해 그 내용을 적지 않는다.",
            "participants": [
                models.ClassParticipantCreate(
                    name="페르마"
                ).dict() for _ in range(100)
            ]
        }
        for d in range(1, 10):
            data["conducted"] = f"200{d}-0{d}-0{d}"
            tested.post(f"/classes/{name}/records", headers=get_jwt_header(), json=data)
        response = tested.get(f"/classes/{name}/records")
        assert response.status_code == 200
        for d, row in enumerate(response.json()[::-1]):
            d += 1
            assert row["topic"] == data["topic"]
            assert row["number_of_participants"] == len(data["participants"])
            assert row["moderator"] == settings.test_real_name
            assert row["conducted"] == f"200{d}-0{d}-0{d}"

def test_create_class_record():
    for name in models.ClassName:
        response = tested.post(f"/classes/{name}/records", json=class_record_data)
        assert response.status_code == 401

        change_role(models.Role.member)
        response = tested.post(f"/classes/{name}/records", json=class_record_data, headers=get_jwt_header())
        assert response.status_code == 403

        change_role(models.Role.board)
        response = tested.post(f"/classes/{name}/records", json=class_record_data, headers=get_jwt_header())
        assert response.status_code == 200
        parsed = response.json()
        assert parsed["conducted"] == class_record_data["conducted"]
        assert parsed["participants"] == class_record_data["participants"]
        assert parsed["topic"] == class_record_data["topic"]
        assert parsed["content"] == class_record_data["content"]

        response = tested.get(f"/classes/{name}/records/{class_record_data['conducted']}", headers=get_jwt_header())
        assert response.status_code == 200
        parsed = response.json()
        assert parsed["conducted"] == class_record_data["conducted"]
        assert parsed["participants"] == class_record_data["participants"]
        assert parsed["topic"] == class_record_data["topic"]
        assert parsed["content"] == class_record_data["content"]

def test_update_class_record():
    class_record_data["topic"] = "One Day in the Life of Ivan Denisovich"
    class_record_data["content"] = "Death is the solution to all problems; no man, no problem."
    class_record_data["participants"] = [
        models.ClassParticipantCreate(
            name="Joseph Stalin"
        ).dict() for _ in range(17)
    ]
    original_conducted = class_record_data["conducted"]
    class_record_data["conducted"] = "1962-01-01"
    for name in models.ClassName:
        response = tested.patch(f"/classes/{name}/records/{original_conducted}", json=class_record_data)
        assert response.status_code == 401
        
        change_role(models.Role.member)
        response = tested.patch(f"/classes/{name}/records/{original_conducted}", json=class_record_data, headers=get_jwt_header())
        assert response.status_code == 403

        change_role(models.Role.board)
        response = tested.patch(f"/classes/{name}/records/{original_conducted}", json=class_record_data, headers=get_jwt_header())
        assert response.status_code == 200
        parsed = response.json()
        assert parsed["topic"] == class_record_data["topic"]
        assert parsed["conducted"] == class_record_data["conducted"]
        assert parsed["participants"] == class_record_data["participants"]
        assert parsed["content"] == class_record_data["content"]
        
        response = tested.get(f"/classes/{name}/records/{class_record_data['conducted']}", headers=get_jwt_header())
        assert response.json() == parsed
        response = tested.get(f"/classes/{name}/records/{original_conducted}", headers=get_jwt_header())
        assert response.status_code == 404

def test_get_class_record():
    for name in models.ClassName:
        response = tested.get(f"/classes/{name}/records/{class_record_data['conducted']}")
        assert response.status_code == 401

        change_role(models.Role.board)
        response = tested.get(f"/classes/{name}/records/{class_record_data['conducted']}", headers=get_jwt_header())
        assert response.status_code == 200
        parsed = response.json()
        assert parsed["topic"] == class_record_data["topic"]
        assert parsed["conducted"] == class_record_data["conducted"]
        assert parsed["participants"] == class_record_data["participants"]
        assert parsed["content"] == class_record_data["content"]
        
        change_role(models.Role.member)
        response = tested.get(f"/classes/{name}/records/{class_record_data['conducted']}", headers=get_jwt_header())
        assert response.status_code == 200
        parsed = response.json()
        assert parsed["topic"] == class_record_data["topic"]
        assert parsed["conducted"] == class_record_data["conducted"]
        assert parsed.get("participants") == None
        assert parsed["content"] == class_record_data["content"]

def test_delete_class_record():
    for name in models.ClassName:
        response = tested.delete(f"/classes/{name}/records/{class_record_data['conducted']}")
        assert response.status_code == 401

        change_role(models.Role.member)
        response = tested.delete(f"/classes/{name}/records/{class_record_data['conducted']}", headers=get_jwt_header())
        assert response.status_code == 403
        
        change_role(models.Role.board)
        response = tested.delete(f"/classes/{name}/records/{class_record_data['conducted']}", headers=get_jwt_header())
        assert response.status_code == 200
        response = tested.delete(f"/classes/{name}/records/{class_record_data['conducted']}", headers=get_jwt_header())
        assert response.status_code == 404
        for record in tested.get(f"/classes/{name}/records").json():
            response = tested.delete(f"/classes/{name}/records/{record['conducted']}", headers=get_jwt_header())
            assert response.status_code == 200
            response = tested.delete(f"/classes/{name}/records/{record['conducted']}", headers=get_jwt_header())
            assert response.status_code == 404
        response = tested.get(f"/classes/{name}/records")
        assert response.status_code == 200
        assert response.json() == []

def test_create_book():
    data = {
        "title": "『눈먼 자들의 도시』",
        "author": "주제 사라마구",
        "translator": "정영목",
        "published": "2008-11-30",
        "publisher": "해냄",
        "isbn13": 9788973374939
    }
    response = tested.post("/books", json=data)
    assert response.status_code == 401
    change_role(models.Role.member)
    response = tested.post("/books", json=data, headers=get_jwt_header())
    assert response.status_code == 403

    change_role(models.Role.board)
    response = tested.post("/books", json=data, headers=get_jwt_header())
    assert response.status_code == 200
    for key, value in response.json().items():
        assert data[key] == value

def test_get_book():
    data = {
        "title": "『허삼관 매혈기』",
        "author": "위화",
        "translator": "최용만",
        "published": "2014-09-29",
        "publisher": "푸른숲",
        "isbn13": 9788971847244
    }
    change_role(models.Role.board)
    response = tested.post("/books", json=data, headers=get_jwt_header())
    no = response.json()["no"]
    response = tested.get(f"/books/{no}")
    for key, value in response.json():
        assert data[key] == value

def test_update_book():
    data = {
        "title": "『표준국어문법론』",
        "author": "남기심, 고영근",
        "published": "1985-09-30",
        "publisher": "탑",
        "isbn13": 9788968177231
    }
    change_role(models.Role.board)
    response = tested.post("/books", json=data, headers=get_jwt_header())
    no = response.json()["no"]
    data["title"] = "『표준국어문법론』 (전면개정판)"
    data["published"] = "2019-02-25"
    data["author"] = "남기심, 고영근, 유현경, 최형용"
    data["publisher"] = "한국문화사"
    response = tested.patch(f"/books/{no}", json=data, headers=get_jwt_header())
    for key, value in response.json().items():
        assert data[key] == value

def test_delete_book():
    data = {
        "title": "『미적분학 1+』",
        "author": "김홍종",
        "published": "2018-01-22",
        "publihser": "서울대학교출판문화원",
        "isbn13": 9788952117878
    }
    change_role(models.Role.board)
    response = tested.post("/books", json=data, headers=get_jwt_header())
    no = response.json()["no"]
    
    response = tested.delete(f"/books/{no}")
    assert response.status_code == 401
    
    change_role(models.Role.member)
    response = tested.delete(f"/books/{no}")
    assert response.status_code == 403

    change_role(models.Role.board)
    response = tested.delete(f"/books/{no}")
    assert response.status_code == 200
    response = tested.delete(f"/books/{no}")
    assert response.status_code == 404

    response = tested.get(f"/books/{no}")
    assert response.status_code == 404

def test_borrow_book():
    data = {
        "title": "왜 나는 너를 사랑하는가",
        "author": "알랭 드 보통",
        "published": "2012-08-20"
    }
    change_role(models.Role.board)
    response = tested.post(f"/books", json=data, headers=get_jwt_header())
    no = response.json()["no"]
    response = tested.post(f"/books/{no}/borrow")
    assert response.status_code == 401

    change_role(models.Role.member)
    response = tested.post(f"/books/{no}/borrow", headers=get_jwt_header())
    assert response.status_code == 200

    response = tested.post(f"/books/{no}/borrow", headers=get_jwt_header())
    assert response.status_code == 423 # Locked

    response = tested.post(f"/books/{no}/return")
    assert response.status_code == 401
    # TODO: another member
    response = tested.post(f"/books/{no}/return", headers=get_jwt_header())
    assert response.status_code == 200

    response = tested.post(f"/books/{no}/return")
    assert response.status_code == 401
    # TODO: another member
    response = tested.post(f"/books/{no}/return", headers=get_jwt_header())
    assert response.status_code == 409 # Conflict

def test_delete_member():
    response = tested.delete(f"/members/{settings.test_portal_id}")
    assert response.status_code == 401

    change_role(models.Role.member)
    response = tested.delete(f"/members/{settings.test_portal_id}", headers=get_jwt_header())
    assert response.status_code == 403

    change_role(models.Role.board)
    response = tested.delete("/members/58826974", headers=get_jwt_header())
    assert response.status_code == 404
    
    response = tested.delete(f"/members/{settings.test_portal_id}", headers=get_jwt_header())
    assert response.status_code == 200