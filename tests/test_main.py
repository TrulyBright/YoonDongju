from __future__ import annotations
import itertools
import re
import uuid
import pytest
from datetime import date
from pydantic import BaseSettings
from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import sqlalchemy.event as sqlevent
from fastapi.testclient import TestClient
from FastAPIApp import auth, app, schemas
import FastAPIApp.database as database
import FastAPIApp.models as models
import FastAPIApp.crud as crud
from WrapperFunction import RegisterForm, FindIDForm, FindPWForm


class Settings(BaseSettings):
    PORTAL_ID: str
    PORTAL_PW: str
    REAL_NAME: str
    USERNAME: str
    PASSWORD: str
    NEW_PW: str
    HR_MANAGER_TEL: str


settings = Settings()


SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
sqlevent.listen(
    engine, "connect", lambda conn, rec: conn.execute(
        "PRAGMA foreign_keys=ON;")
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

database.Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[database.get_db] = override_get_db
tested = TestClient(app)


def with_table_cleared(schema: Table):
    def decorator(function):
        def wrapper(*args, **kwargs):
            db = TestingSessionLocal()
            db.query(schema).delete()
            db.commit()
            db.close()
            return function(*args, **kwargs)
        return wrapper
    return decorator


def jwt(fakemember: FakeMember):
    response = tested.post("/token", data={
        "username": fakemember.username,
        "password": fakemember.password
    })
    assert response.status_code == 200
    parsed = response.json()
    return {
        "Authorization": f"{parsed['token_type']} {parsed['access_token']}"
    }


class FakeMember(dict):
    def __init__(self, role: models.Role):
        self.student_id = str(uuid.uuid4())
        self.username = self.student_id + "_username"
        self.real_name = self.student_id + "_real_name"
        self.password = self.student_id + "_password"
        DB = TestingSessionLocal()
        created = crud.create_member(
            db=DB,
            student_id=self.student_id,
            member=models.MemberCreate(
                username=self.username,
                real_name=self.real_name,
                password=self.password
            ))
        self.model = models.Member.from_orm(crud.update_member(db=DB, student_id=created.student_id, member=models.MemberModify(
            role=role
        )))
        DB.close()


def member():
    return FakeMember(models.Role.member)


def board():
    return FakeMember(models.Role.board)


def president():
    return FakeMember(models.Role.president)


class TestClubInformation:
    info = models.ClubInformationCreate(
        address="어딘가",
        email="someone@some.where",
        president_name="홍길동",
        president_tel="010-0000-0000",
        HR_manager_tel=settings.HR_MANAGER_TEL
    )

    @with_table_cleared(schemas.ClubInformation)
    def test_update_club_information(self):
        response = tested.put("/club-information", json=self.info.dict())
        assert response.status_code == 401
        response = tested.put("/club-information", json=self.info.dict(),
                              headers=jwt(member()))
        assert response.status_code == 403
        response = tested.put("/club-information", json=self.info.dict(),
                              headers=jwt(board()))
        assert response.status_code == 200
        updated = models.ClubInformation(**response.json())
        assert updated == self.info

    @with_table_cleared(schemas.ClubInformation)
    def test_get_club_information(self):
        self.test_update_club_information()
        response = tested.get("/club-information")
        assert response.status_code == 200
        assert models.ClubInformation(**response.json()) == self.info


class TestUploadedFile:
    file_binary = b"foo"

    def create_uploaded_file():
        return models.UploadedFile(**tested.post("/uploaded", headers=jwt(FakeMember(models.Role.board)), files={
            "uploaded": ("test.jpg", TestUploadedFile.file_binary, "image/jpeg")
        }).json())

    @with_table_cleared(schemas.UploadedFile)
    def test_create_uploaded_file(self):
        file_info = ("test.jpg", self.file_binary, "image/jpeg")
        response = tested.post("/uploaded", files={
            "uploaded": file_info
        })
        assert response.status_code == 401
        response = tested.post("/uploaded", headers=jwt(member()), files={
            "uploaded": file_info
        })
        assert response.status_code == 403
        response = tested.post("/uploaded", headers=jwt(board()), files={
            "uploaded": file_info
        })
        assert response.status_code == 200
        assert models.UploadedFileCreate(**response.json()) == models.UploadedFileCreate(
            name=file_info[0],
            content_type=file_info[2]
        )

    @with_table_cleared(schemas.UploadedFile)
    def test_get_uploaded_file(self):
        response = tested.get(f"/uploaded/{0}")
        assert response.status_code == 404
        file = TestUploadedFile.create_uploaded_file()
        response = tested.get(f"/uploaded/{file.id}")
        assert response.status_code == 200
        assert response.content == self.file_binary

    @with_table_cleared(schemas.UploadedFile)
    def test_delete_uploaded_file(self):
        file = TestUploadedFile.create_uploaded_file()
        response = tested.delete(f"/uploaded/{file.id}")
        assert response.status_code == 401
        response = tested.delete(f"/uploaded/{file.id}", headers=jwt(member()))
        assert response.status_code == 403
        response = tested.delete(f"/uploaded/{file.id}", headers=jwt(board()))
        assert response.status_code == 200
        response = tested.get(f"/uploaded/{file.id}")
        assert response.status_code == 404

    @with_table_cleared(schemas.UploadedFile)
    def test_get_uploaded_file_info(self):
        file = TestUploadedFile.create_uploaded_file()
        response = tested.get(f"/uploaded/{file.id}/info")
        assert response.status_code == 200
        assert models.UploadedFile(**response.json()) == file


class TestPost:
    about_data = models.PostCreate(
        title="연세문학회는",
        content="이러저러한 동아리입니다.",
        attached=[]
    )
    rules_data = models.PostCreate(
        title="규칙은",
        content="이러합니다.",
        attached=[]
    )

    def create_post(self, type: models.PostType, post: models.PostCreate):
        """`about`과 `rules`는 이 함수로 만들지 않습니다. `PUT`을 써야 하기 때문입니다."""
        return models.Post(**tested.post({
            models.PostType.notice: "/notices"
        }[type], json=post.dict(), headers=jwt(FakeMember(models.Role.board))).json())

    @with_table_cleared(schemas.Post)
    def test_update_about(self):
        writer = board()
        response = tested.put("/about", json=self.about_data.dict())
        assert response.status_code == 401

        response = tested.put("/about", json=self.about_data.dict(),
                              headers=jwt(member()))
        assert response.status_code == 403

        response = tested.put("/about", json=self.about_data.dict(),
                              headers=jwt(writer))
        assert response.status_code == 200
        posted = models.Post(**response.json())
        assert models.PostCreate(**posted.dict()) == self.about_data
        assert posted.author == writer.real_name

    @with_table_cleared(schemas.Post)
    def test_get_about(self):
        self.test_update_about()
        response = tested.get("/about")
        assert response.status_code == 200
        fetched = models.Post(**response.json())
        assert models.PostCreate(**fetched.dict()) == self.about_data

    @with_table_cleared(schemas.Post)
    def test_update_rules(self):
        writer = board()
        response = tested.put("/rules", json=self.rules_data.dict())
        assert response.status_code == 401
        response = tested.put("/rules", json=self.rules_data.dict(),
                              headers=jwt(member()))
        assert response.status_code == 403
        response = tested.put("/rules", json=self.rules_data.dict(),
                              headers=jwt(writer))
        assert response.status_code == 200
        updated = models.Post(**response.json())
        assert models.PostCreate(**updated.dict()) == self.rules_data
        assert updated.author == writer.real_name

    @with_table_cleared(schemas.Post)
    def test_get_rules(self):
        self.test_update_rules()
        response = tested.get("/rules")
        assert response.status_code == 200
        fetched = models.Post(**response.json())
        assert models.PostCreate(**fetched.dict()) == self.rules_data

    @with_table_cleared(schemas.Post)
    def test_get_notice_count(self):
        count = 17
        for _ in range(count):
            self.create_post(models.PostType.notice, models.PostCreate(
                title="asdf",
                content="qwer",
                attached=[]
            ))
        response = tested.get("/notices/count")
        assert response.status_code == 200
        assert response.json() == count

    @with_table_cleared(schemas.Post)
    def test_get_recent_notices(self):
        limit = 4
        created = [self.create_post(models.PostType.notice, models.PostCreate(
            title=str(i), content=str(i), attached=[])) for i in range(limit*2)]
        response = tested.get("/notices/recent", params={"limit": limit})
        assert response.status_code == 200
        fetched = [models.PostOutline(**data) for data in response.json()]
        assert len(fetched) == limit
        for fetched, standard in zip(fetched, created[::-1][:limit]):
            assert fetched == models.PostOutline(**standard.dict())

    @with_table_cleared(schemas.Post)
    def test_get_notices(self):
        limit = 30
        created = [self.create_post(models.PostType.notice, models.PostCreate(
            title=str(i), content=str(i), attached=[]
        )) for i in range(limit * 2)]
        for skip in range(30):
            params = {"skip": skip, "limit": limit}
            response = tested.get("/notices", params=params)
            assert response.status_code == 200
            fetched = [models.PostOutline(**data) for data in response.json()]
            assert len(fetched) == limit
            for fetched, standard in zip(fetched, created[::-1][skip:][:limit]):
                assert fetched == models.PostOutline(**standard.dict())

    @with_table_cleared(schemas.Post)
    def test_get_notice(self):
        response = tested.get(f"/notices/1")
        assert response.status_code == 404
        count = 5
        created = self.create_post(models.PostType.notice, models.PostCreate(
            title="asdf",
            content="qwr",
            attached=[
                TestUploadedFile.create_uploaded_file().id for _ in range(count)]
        ))
        response = tested.get(f"/notices/{created.no}")
        assert response.status_code == 200
        fetched = models.Post(**response.json())
        assert created == fetched

    @with_table_cleared(schemas.Post)
    def test_create_notice(self):
        count = 10
        attached = [TestUploadedFile.create_uploaded_file()
                    for _ in range(count)]
        post = models.PostCreate(
            title="new notice",
            content="asdf",
            attached=[file.id for file in attached]
        )
        today = date.today()
        response = tested.post("/notices", json=post.dict())
        assert response.status_code == 401
        response = tested.post(
            "/notices", json=post.dict(), headers=jwt(member()))
        assert response.status_code == 403
        writer = board()
        response = tested.post(
            "/notices", json=post.dict(), headers=jwt(writer))
        assert response.status_code == 200
        parsed = models.Post(**response.json())
        assert parsed.title == post.title
        assert parsed.content == post.content
        assert [file.id for file in parsed.attached] == post.attached
        assert parsed.author == writer.real_name
        assert parsed.published == today
        assert parsed.modified == None
        assert parsed.modifier == None

    @with_table_cleared(schemas.Post)
    def test_update_notice(self):
        count = 7
        attached = [TestUploadedFile.create_uploaded_file()
                    for _ in range(count)]
        existing = self.create_post(models.PostType.notice, models.PostCreate(
            title="asdf",
            content="qwer",
            attached=[file.id for file in attached]
        ))
        modified = models.PostCreate(
            title=existing.title + "foo",
            content=existing.content + "bar",
            attached=[file.id for file in existing.attached[:1]]
        )
        response = tested.put(f"/notices/{existing.no}", json=modified.dict())
        assert response.status_code == 401
        response = tested.put(
            f"/notices/{existing.no}", json=modified.dict(), headers=jwt(member()))
        assert response.status_code == 403
        modifier = board()
        response = tested.put(
            f"/notices/{existing.no}", json=modified.dict(), headers=jwt(modifier))
        assert response.status_code == 200
        updated = models.Post(**response.json())
        assert updated.title == modified.title
        assert updated.content == modified.content
        assert [file.id for file in updated.attached] == modified.attached
        assert updated.modified == date.today()
        assert updated.modifier == modifier.real_name

    @with_table_cleared(schemas.Post)
    def test_delete_notice(self):
        count = 7
        attached = [TestUploadedFile.create_uploaded_file()
                    for _ in range(count)]
        deleted = self.create_post(models.PostType.notice, models.PostCreate(
            title="gonna be",
            content="deleted",
            attached=[file.id for file in attached]
        ))
        response = tested.delete(
            f"/notices/{deleted.no}")
        assert response.status_code == 401
        response = tested.delete(
            f"/notices/{deleted.no}", headers=jwt(member()))
        assert response.status_code == 403
        response = tested.delete(
            f"/notices/{deleted.no}", headers=jwt(board()))
        assert response.status_code == 200
        response = tested.get(f"/notices/{deleted.no}")
        assert response.status_code == 404
        for file in attached:
            response = tested.get(f"/uploaded/{file.id}")
            assert response.status_code == 404


class TestMember:
    @with_table_cleared(schemas.Member)
    def test_get_me(self):
        me = member()
        response = tested.get("/me")
        assert response.status_code == 401
        response = tested.get("/me", headers=jwt(me))
        assert models.Member(**response.json()) == me.model

    @with_table_cleared(schemas.Member)
    def test_get_members(self):
        response = tested.get("/members")
        assert response.status_code == 401
        response = tested.get("/members", headers=jwt(member()))
        assert response.status_code == 403
        response = tested.get("/members", headers=jwt(board()))
        assert response.status_code == 200

    @with_table_cleared(schemas.Member)
    def test_get_member(self):
        queried = FakeMember(models.Role.member)
        response = tested.get(f"/members/{queried.student_id}")
        assert response.status_code == 401
        response = tested.get(
            f"/members/{queried.student_id}", headers=jwt(member()))
        assert response.status_code == 403
        response = tested.get(
            f"/members/{queried.student_id}", headers=jwt(board()))
        assert response.status_code == 200
        assert models.Member(**response.json()) == queried.model

    @with_table_cleared(schemas.Member)
    def test_update_member(self):
        updated = FakeMember(models.Role.member)
        data = models.MemberModify(
            role=models.Role.board,
        )
        response = tested.put(
            f"/members/{updated.student_id}", json=data.dict())
        assert response.status_code == 401
        response = tested.put(
            f"/members/{updated.student_id}", headers=jwt(member()), json=data.dict())
        assert response.status_code == 403
        response = tested.put(
            f"/members/{updated.student_id}", headers=jwt(board()), json=data.dict())
        assert response.status_code == 200
        assert models.Member(**response.json()).role == data.role
        response = tested.get(
            f"/members/{updated.student_id}", headers=jwt(board()))
        assert models.Member(**response.json()).role == data.role

        rejected = models.MemberModify(password="1234")
        assert not re.match(auth.password_pattern, rejected.password)
        response = tested.put(
            f"/members/{updated.student_id}", json=rejected.dict())
        assert response.status_code == 401
        response = tested.put(
            f"/members/{updated.student_id}", headers=jwt(member()), json=rejected.dict())
        assert response.status_code == 403
        response = tested.put(
            f"/members/{updated.student_id}", headers=jwt(board()), json=rejected.dict())
        assert response.status_code == 400
        accepted = models.MemberModify(
            password="this is a pattern-matching password 1234.")
        assert re.match(auth.password_pattern, accepted.password)
        response = tested.put(
            f"/members/{updated.student_id}", headers=jwt(board()), json=accepted.dict())
        response = tested.post(
            f"/token", data={
                "username": updated.username,
                "password": accepted
            })
        assert response.status_code == 200

    @with_table_cleared(schemas.Member)
    def test_delete_member(self):
        deleted = member()
        response = tested.delete(f"/members/{deleted.student_id}")
        assert response.status_code == 401
        response = tested.delete(
            f"/members/{deleted.student_id}", headers=jwt(member()))
        assert response.status_code == 403
        response = tested.delete(
            f"/members/{deleted.student_id}", headers=jwt(deleted))
        assert response.status_code == 200
        with pytest.raises(AssertionError):
            jwt(deleted)
        response = tested.get(
            f"/members/{deleted.student_id}", headers=jwt(board()))
        assert response.status_code == 404


class TestMagazine:
    year = itertools.count(2000)

    def create_magazine_content(self):
        return models.MagazineContentCreate(
            type=str(uuid.uuid4()),
            title=str(uuid.uuid4()),
            author=str(uuid.uuid4()),
            language=str(uuid.uuid4())
        )

    def create_magazine(self):
        data = models.MagazineCreate(
            year=self.year.__next__(),
            cover=TestUploadedFile.create_uploaded_file().id,
            published=date(self.year.__next__(), 1, 1),
            contents=[self.create_magazine_content() for _ in range(30)]
        ).dict()
        data["published"] = data["published"].strftime("%Y-%m-%d")
        response = tested.post("/magazines", headers=jwt(board()), json=data)
        return models.Magazine(**response.json())

    @with_table_cleared(schemas.Magazine)
    def test_get_magazines(self):
        limit = 30
        magazines = [self.create_magazine() for _ in range(limit*2)]
        for skip in range(limit):
            response = tested.get(
                "/magazines", params={"skip": skip, "limit": limit})
            assert response.status_code == 200
            for fetched, standard in zip(response.json(), magazines[::-1][skip:][:limit]):
                assert models.MagazineOutline(
                    **fetched) == models.MagazineOutline(**standard.dict())

    @with_table_cleared(schemas.Magazine)
    def test_get_magazine(self):
        created = self.create_magazine()
        response = tested.get(f"/magazines/{created.published}")
        assert response.status_code == 200
        assert models.Magazine(**response.json()) == created

    @with_table_cleared(schemas.Magazine)
    def test_create_magazine(self):
        model = models.MagazineCreate(
            year=self.year.__next__(),
            cover=TestUploadedFile.create_uploaded_file().id,
            published=date(self.year.__next__(), 1, 1),
            contents=[self.create_magazine_content() for _ in range(50)]
        )
        data = model.dict()
        data["published"] = data["published"].strftime("%Y-%m-%d")
        response = tested.post("/magazines", json=data)
        assert response.status_code == 401
        response = tested.post(
            "/magazines", json=data, headers=jwt(member()))
        assert response.status_code == 403
        response = tested.post(
            "/magazines", json=data, headers=jwt(board()))
        assert response.status_code == 200
        response = tested.get(f"/magazines/{model.published}")
        assert response.status_code == 200
        assert models.MagazineCreate(**response.json()) == model

    @with_table_cleared(schemas.Magazine)
    def test_get_recent_magazines(self):
        count = 30
        magazines = [self.create_magazine()]*count
        for limit in range(count):
            response = tested.get("/magazines/recent", params={"limit": limit})
            assert response.status_code == 200
            for fetched, standard in zip(response.json(), magazines[::-1][:limit]):
                assert models.MagazineOutline(
                    **fetched) == models.MagazineOutline(**standard.dict())

    @with_table_cleared(schemas.Magazine)
    def test_update_magazine(self):
        updated = self.create_magazine()
        model = models.MagazineCreate(
            year=self.year.__next__(),
            cover=TestUploadedFile.create_uploaded_file().id,
            published=date(self.year.__next__(), 1, 1),
            contents=[self.create_magazine_content()] * 5
        )
        data = model.dict()
        data["published"] = data["published"].strftime("%Y-%m-%d")
        response = tested.put(f"/magazines/{updated.published}", json=data)
        assert response.status_code == 401
        response = tested.put(
            f"/magazines/{updated.published}", headers=jwt(member()), json=data)
        assert response.status_code == 403
        response = tested.put(
            f"/magazines/{updated.published}", headers=jwt(board()), json=data)
        assert response.status_code == 200
        assert models.MagazineCreate(**response.json()) == model
        response = tested.get(f"/magazines/{updated.published}")
        assert response.status_code == 404
        response = tested.get(f"/magazines/{data['published']}")
        assert response.status_code == 200
        assert models.MagazineCreate(**response.json()) == model

    @with_table_cleared(schemas.Magazine)
    def test_delete_magazine(self):
        deleted = self.create_magazine()
        response = tested.delete(f"/magazines/{deleted.published}")
        assert response.status_code == 401
        response = tested.delete(
            f"/magazines/{deleted.published}", headers=jwt(member()))
        assert response.status_code == 403
        response = tested.delete(
            f"/magazines/{deleted.published}", headers=jwt(board()))
        assert response.status_code == 200
        response = tested.get(f"/magazines/{deleted.published}")
        assert response.status_code == 404


# def test_get_classes():
#     response = tested.get("/classes")
#     assert response.status_code == 200
#     names = set(models.ClassName)
#     for data in response.json():
#         assert data["name"] in names
#         assert "korean" in data


# def test_update_class():
#     with TestClient(main.app) as tested:
#         eng2kor = {
#             models.ClassName.poetry: "시반",
#             models.ClassName.novel: "소설반",
#             models.ClassName.critique: "합평반",
#             models.ClassName.reading: "독서반",
#         }
#         for name in models.ClassName:
#             class_data["korean"] = eng2kor[name]
#             expected = class_data.copy()
#             expected["name"] = name
#             response = tested.put(f"/classes/{name}", json=class_data)
#             assert response.status_code == 401

#             change_role(models.Role.member)
#             response = tested.put(
#                 f"/classes/{name}", json=class_data, headers=get_jwt_header()
#             )
#             assert response.status_code == 403

#             change_role(models.Role.board)
#             response = tested.put(
#                 f"/classes/{name}", json=class_data, headers=get_jwt_header()
#             )
#             assert response.status_code == 200
#             assert response.json() == expected

#             response = tested.get(f"/classes/{name}")
#             assert response.status_code == 200
#             assert response.json() == expected

#             modified = class_data
#             modified["moderator"] = expected["moderator"] = "이몽룡"
#             modified["description"] = expected["description"] = "성춘향 환영"
#             response = tested.put(
#                 f"/classes/{name}", json=modified, headers=get_jwt_header()
#             )
#             assert response.status_code == 200
#             assert response.json() == expected
#             response = tested.get(f"/classes/{name}")
#             assert response.status_code == 200
#             assert response.json() == expected


# def test_get_class():
#     eng2kor = {
#         models.ClassName.poetry: "시반",
#         models.ClassName.novel: "소설반",
#         models.ClassName.critique: "합평반",
#         models.ClassName.reading: "독서반",
#     }
#     for name in models.ClassName:
#         class_data["korean"] = eng2kor[name]
#         expected = class_data.copy()
#         expected["name"] = name
#         response = tested.get(f"/classes/{name}")
#         assert response.status_code == 200
#         assert response.json() == expected


# def test_get_class_records():
#     for name in models.ClassName:
#         change_role(models.Role.board)
#         data = {
#             "topic": "뒤치닥, 『투명드래곤』",
#             "content": "본 회차 독서반에서 우리는 뒤치닥이 톨킨보다 위대한 이유를 명쾌히 논증해냈으나 여백이 부족해 그 내용을 적지 않는다.",
#         }
#         for d in range(1, 10):
#             data["conducted"] = f"200{d}-0{d}-0{d}"
#             tested.post(f"/classes/{name}/records",
#                         headers=get_jwt_header(), json=data)
#         response = tested.get(f"/classes/{name}/records")
#         assert response.status_code == 200
#         for d, row in enumerate(response.json()[::-1]):
#             d += 1
#             assert row["topic"] == data["topic"]
#             assert row["moderator"] == settings.test_real_name
#             assert row["conducted"] == f"200{d}-0{d}-0{d}"


# def test_create_class_record():
#     for name in models.ClassName:
#         response = tested.post(
#             f"/classes/{name}/records", json=class_record_data)
#         assert response.status_code == 401

#         change_role(models.Role.member)
#         response = tested.post(
#             f"/classes/{name}/records", json=class_record_data, headers=get_jwt_header()
#         )
#         assert response.status_code == 403

#         change_role(models.Role.board)
#         response = tested.post(
#             f"/classes/{name}/records", json=class_record_data, headers=get_jwt_header()
#         )
#         assert response.status_code == 200
#         parsed = response.json()
#         assert parsed["conducted"] == class_record_data["conducted"]
#         assert parsed["topic"] == class_record_data["topic"]
#         assert parsed["content"] == class_record_data["content"]

#         response = tested.get(
#             f"/classes/{name}/records/{class_record_data['conducted']}",
#             headers=get_jwt_header(),
#         )
#         assert response.status_code == 200
#         parsed = response.json()
#         assert parsed["conducted"] == class_record_data["conducted"]
#         assert parsed["topic"] == class_record_data["topic"]
#         assert parsed["content"] == class_record_data["content"]


# def test_update_class_record():
#     class_record_data["topic"] = "One Day in the Life of Ivan Denisovich"
#     class_record_data[
#         "content"
#     ] = "Death is the solution to all problems; no man, no problem."
#     original_conducted = class_record_data["conducted"]
#     class_record_data["conducted"] = "1962-01-01"
#     for name in models.ClassName:
#         response = tested.put(
#             f"/classes/{name}/records/{original_conducted}", json=class_record_data
#         )
#         assert response.status_code == 401

#         change_role(models.Role.member)
#         response = tested.put(
#             f"/classes/{name}/records/{original_conducted}",
#             json=class_record_data,
#             headers=get_jwt_header(),
#         )
#         assert response.status_code == 403

#         change_role(models.Role.board)
#         response = tested.put(
#             f"/classes/{name}/records/{original_conducted}",
#             json=class_record_data,
#             headers=get_jwt_header(),
#         )
#         assert response.status_code == 200
#         parsed = response.json()
#         assert parsed["topic"] == class_record_data["topic"]
#         assert parsed["conducted"] == class_record_data["conducted"]
#         assert parsed["content"] == class_record_data["content"]

#         response = tested.get(
#             f"/classes/{name}/records/{class_record_data['conducted']}",
#             headers=get_jwt_header(),
#         )
#         assert response.json() == parsed
#         response = tested.get(
#             f"/classes/{name}/records/{original_conducted}", headers=get_jwt_header()
#         )
#         assert response.status_code == 404


# def test_get_class_record():
#     for name in models.ClassName:
#         response = tested.get(
#             f"/classes/{name}/records/{class_record_data['conducted']}"
#         )
#         assert response.status_code == 401

#         change_role(models.Role.board)
#         response = tested.get(
#             f"/classes/{name}/records/{class_record_data['conducted']}",
#             headers=get_jwt_header(),
#         )
#         assert response.status_code == 200
#         parsed = response.json()
#         assert parsed["topic"] == class_record_data["topic"]
#         assert parsed["conducted"] == class_record_data["conducted"]
#         assert parsed["content"] == class_record_data["content"]

#         change_role(models.Role.member)
#         response = tested.get(
#             f"/classes/{name}/records/{class_record_data['conducted']}",
#             headers=get_jwt_header(),
#         )
#         assert response.status_code == 200
#         parsed = response.json()
#         assert parsed["topic"] == class_record_data["topic"]
#         assert parsed["conducted"] == class_record_data["conducted"]
#         assert parsed["content"] == class_record_data["content"]


# def test_delete_class_record():
#     for name in models.ClassName:
#         response = tested.delete(
#             f"/classes/{name}/records/{class_record_data['conducted']}"
#         )
#         assert response.status_code == 401

#         change_role(models.Role.member)
#         response = tested.delete(
#             f"/classes/{name}/records/{class_record_data['conducted']}",
#             headers=get_jwt_header(),
#         )
#         assert response.status_code == 403

#         change_role(models.Role.board)
#         response = tested.delete(
#             f"/classes/{name}/records/{class_record_data['conducted']}",
#             headers=get_jwt_header(),
#         )
#         assert response.status_code == 200
#         response = tested.delete(
#             f"/classes/{name}/records/{class_record_data['conducted']}",
#             headers=get_jwt_header(),
#         )
#         assert response.status_code == 404
#         for record in tested.get(f"/classes/{name}/records").json():
#             response = tested.delete(
#                 f"/classes/{name}/records/{record['conducted']}",
#                 headers=get_jwt_header(),
#             )
#             assert response.status_code == 200
#             response = tested.delete(
#                 f"/classes/{name}/records/{record['conducted']}",
#                 headers=get_jwt_header(),
#             )
#             assert response.status_code == 404
#         response = tested.get(f"/classes/{name}/records")
#         assert response.status_code == 200
#         assert response.json() == []


class TestAuth:
    @with_table_cleared(schemas.Member)
    def test_register(self):
        data = RegisterForm(
            portal_id=settings.PORTAL_ID,
            portal_pw=settings.PORTAL_PW,
            username=settings.USERNAME,
            password=settings.PASSWORD
        )
        response = tested.post("/register", json=data.dict())
        assert response.status_code == 200
        created = models.Member(**response.json())
        assert created.student_id == settings.PORTAL_ID
        assert created.real_name == settings.REAL_NAME
        assert created.username == settings.USERNAME
        assert created.role == models.Role.member

    @with_table_cleared(schemas.Member)
    def test_login(self):
        logging_in = member()
        response = tested.post("/token", data={
            "username": logging_in.username,
            "password": logging_in.password
        })
        assert response.status_code == 200

    @with_table_cleared(schemas.Member)
    def test_find_ID(self):
        self.test_register()
        response = tested.post(
            "/find/id",
            json=FindIDForm(portal_id=settings.PORTAL_ID, portal_pw="").dict()
        )
        assert response.status_code == 777
        response = tested.post(
            "/find/id",
            json=FindIDForm(portal_id=settings.PORTAL_ID,
                            portal_pw=settings.PORTAL_PW).dict()
        )
        assert response.status_code == 200
        assert response.json() == settings.USERNAME

    @with_table_cleared(schemas.Member)
    def test_find_ID_nonexistent(self):
        response = tested.post(
            "/find/id",
            json=FindIDForm(portal_id=settings.PORTAL_ID, portal_pw="").dict()
        )
        assert response.status_code == 777
        response = tested.post(
            "/find/id",
            json=FindIDForm(portal_id=settings.PORTAL_ID,
                            portal_pw=settings.PORTAL_PW).dict()
        )
        assert response.status_code == 404

    @with_table_cleared(schemas.Member)
    def test_find_PW(self):
        self.test_register()
        failing = "asdf"
        assert re.match(auth.password_pattern, failing) is None
        response = tested.post(
            "/find/pw",
            json=FindPWForm(portal_id=settings.PORTAL_ID,
                            portal_pw=failing, new_pw=settings.NEW_PW).dict()
        )
        assert response.status_code == 777
        response = tested.post(
            "/find/pw",
            json=FindPWForm(portal_id=settings.PORTAL_ID,
                            portal_pw=settings.PORTAL_PW,
                            new_pw=failing).dict()
        )
        assert response.status_code == 400
        response = tested.post(
            "/find/pw",
            json=FindPWForm(portal_id=settings.PORTAL_ID,
                            portal_pw=settings.PORTAL_PW,
                            new_pw=settings.NEW_PW).dict()
        )
        assert response.status_code == 200

    @with_table_cleared(schemas.Member)
    def test_find_PW_nonexistent(self):
        response = tested.post(
            "/find/pw",
            json=FindPWForm(portal_id=settings.PORTAL_ID,
                            portal_pw="", new_pw=settings.NEW_PW).dict()
        )
        assert response.status_code == 777
        response = tested.post(
            "/find/pw",
            json=FindPWForm(portal_id=settings.PORTAL_ID,
                            portal_pw=settings.PORTAL_PW,
                            new_pw=settings.NEW_PW).dict()
        )
        assert response.status_code == 404
