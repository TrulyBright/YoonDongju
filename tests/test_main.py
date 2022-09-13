from __future__ import annotations
from faker import Faker
import itertools
import random
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
import auth
from main import app
import schemas
import database
import models
import crud
from main import RegisterForm, FindIDForm, FindPWForm

random.seed()
fake = Faker()


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


# class TestClubInformation:
#     info = [models.ClubInformation(**data) for data in [
#         {"key": "주소", "value": "어딘가", "public": True},
#         {"key": "이메일", "value": "someone@some.where", "public": True},
#         {"key": "회장 실명", "value": "홍길동", "public": True},
#         {"key": "회장 전화번호", "value": "010-0000-0000", "public": True},
#         {"key": "인사행정팀장 전화번호", "value": settings.HR_MANAGER_TEL, "public": False}
#     ]]

#     @with_table_cleared(schemas.ClubInformation)
#     def test_update_club_information(self):
#         response = tested.put("/club-information", json=self.info.dict())
#         assert response.status_code == 401
#         response = tested.put("/club-information", json=self.info.dict(),
#                               headers=jwt(member()))
#         assert response.status_code == 403
#         response = tested.put("/club-information", json=self.info.dict(),
#                               headers=jwt(board()))
#         assert response.status_code == 200
#         updated = models.ClubInformation(**response.json())
#         assert updated == self.info

#     @with_table_cleared(schemas.ClubInformation)
#     def test_get_club_information(self):
#         self.test_update_club_information()
#         response = tested.get("/club-information")
#         assert response.status_code == 200
#         assert models.ClubInformation(**response.json()) == self.info


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
        for fetched, standard in zip(fetched, created[::-1][:limit], strict=True):
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
            for fetched, standard in zip(fetched, created[::-1][skip:][:limit], strict=True):
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
            for fetched, standard in zip(response.json(), magazines[::-1][skip:][:limit], strict=True):
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


class TestClass:
    def get_class_list(self):
        return [models.Class(**data) for data in tested.get("/classes").json()]

    def create_class():
        return models.Class(**tested.post("/classes", json=models.ClassCreate(
            name=str(uuid.uuid4()),
            moderator=str(uuid.uuid4()),
            schedule=str(uuid.uuid4()),
            description=str(uuid.uuid4()),
            order=random.randint(1, 0x7fffffff)
        ).dict(), headers=jwt(board())).json())

    def create_class_record_serialized():
        instance = models.ClassRecordCreate(
            conducted=fake.date_between(
                start_date="today", end_date="+100y"),
            topic=str(uuid.uuid4()),
            content=str(uuid.uuid4())
        ).dict()
        instance["conducted"] = instance["conducted"].strftime("%Y-%m-%d")
        return instance

    @with_table_cleared(schemas.Class)
    def test_get_classes(self):
        response = tested.get("/classes")
        assert response.status_code == 200
        assert response.json() == []
        length = 5
        classes = sorted([TestClass.create_class()
                         for _ in range(length)], key=lambda info: info.order)
        response = tested.get("/classes")
        assert response.status_code == 200
        assert len(response.json()) == length
        for fetched, standard in zip(response.json(), classes, strict=True):
            assert models.Class(**fetched) == standard

    @with_table_cleared(schemas.Class)
    def test_create_class(self):
        classInfo = models.ClassCreate(
            name="합평회",
            moderator="홍길동",
            schedule="매주 월요일 오후 7시",
            description="합평회는 회원의 작품을 합평합니다.",
            order=1
        )
        response = tested.post("/classes", json=classInfo.dict())
        assert response.status_code == 401
        response = tested.post(
            "/classes", json=classInfo.dict(), headers=jwt(member()))
        assert response.status_code == 403
        response = tested.post(
            "/classes", json=classInfo.dict(), headers=jwt(board()))
        assert response.status_code == 200
        assert models.Class(
            **response.json()) == models.Class(**classInfo.dict())

    @with_table_cleared(schemas.Class)
    def test_get_class(self):
        created = TestClass.create_class()
        response = tested.get(f"/classes/{created.name}")
        assert response.status_code == 200
        assert models.Class(**response.json()) == created

    @with_table_cleared(schemas.Class)
    def test_update_class(self):
        created = TestClass.create_class()
        info = models.ClassCreate(
            name=created.name,
            moderator=created.moderator + "asdf",
            schedule=created.schedule + "asdf",
            description=created.description + "asdf",
            order=0
        )
        response = tested.put(f"/classes/{created.name}", json=info.dict())
        assert response.status_code == 401
        response = tested.put(
            f"/classes/{created.name}", json=info.dict(), headers=jwt(member()))
        assert response.status_code == 403
        response = tested.put(
            f"/classes/{created.name}", json=info.dict(), headers=jwt(board()))
        assert response.status_code == 200
        assert models.Class(**response.json()) == models.Class(**info.dict())
        response = tested.get(f"/classes/{created.name}")
        assert response.status_code == 200
        assert models.Class(**response.json()) == models.Class(**info.dict())

    @with_table_cleared(schemas.Class)
    def test_delete_class(self):
        created = TestClass.create_class()
        response = tested.delete(f"/classes/{created.name}")
        assert response.status_code == 401
        response = tested.delete(
            f"/classes/{created.name}", headers=jwt(member()))
        assert response.status_code == 403
        response = tested.delete(
            f"/classes/{created.name}", headers=jwt(board()))
        assert response.status_code == 200
        response = tested.get(f"/classes/{created.name}")
        assert response.status_code == 404

    @with_table_cleared(schemas.Class)
    def test_create_class_record(self):
        cls = TestClass.create_class()
        record = TestClass.create_class_record_serialized()
        response = tested.post(
            f"/classes/{cls.name}/records", json=record)
        assert response.status_code == 401
        response = tested.post(
            f"/classes/{cls.name}/records", json=record, headers=jwt(member()))
        assert response.status_code == 403
        moderator = board()
        response = tested.post(
            f"/classes/{cls.name}/records", json=record, headers=jwt(moderator))
        assert response.status_code == 200
        response = tested.get(
            f"/classes/{cls.name}/records/{models.ClassRecord(**response.json()).conducted}", headers=jwt(member()))
        assert response.status_code == 200
        assert models.ClassRecordCreate(
            **response.json()) == models.ClassRecordCreate(**record)
        assert models.ClassRecord(
            **response.json()).moderator == moderator.real_name
        response = tested.post(
            f"/classes/{cls.name}/records", json=record, headers=jwt(board()))
        assert response.status_code == 409

    @with_table_cleared(schemas.Class)
    def test_update_class_record(self):
        cls = TestClass.create_class()
        record = TestClass.create_class_record_serialized()
        updated = TestClass.create_class_record_serialized()
        assert tested.post(
            f"/classes/{cls.name}/records", json=record, headers=jwt(board()))
        response = tested.put(
            f"/classes/{cls.name}/records/{record['conducted']}", json=updated)
        assert response.status_code == 401
        response = tested.put(
            f"/classes/{cls.name}/records/{record['conducted']}", json=updated, headers=jwt(member()))
        assert response.status_code == 403
        modifier = board()
        response = tested.put(
            f"/classes/{cls.name}/records/{record['conducted']}", json=updated, headers=jwt(modifier))
        assert response.status_code == 200
        assert models.ClassRecordCreate(
            **response.json()) == models.ClassRecordCreate(**updated)
        response = tested.get(
            f"/classes/{cls.name}/records/{record['conducted']}", headers=jwt(member()))
        assert response.status_code == 200
        assert models.ClassRecordCreate(
            **response.json()) == models.ClassRecordCreate(**updated)

    @with_table_cleared(schemas.Class)
    def test_get_class_record(self):
        cls = TestClass.create_class()
        record = TestClass.create_class_record_serialized()
        record_model = models.ClassRecordCreate(**record)
        response = tested.get(
            f"/classes/{cls.name}/records/{record_model.conducted}", headers=jwt(member()))
        assert response.status_code == 404
        moderator = board()
        tested.post(
            f"/classes/{cls.name}/records", json=record, headers=jwt(moderator))
        response = tested.get(
            f"/classes/{cls.name}/records/{record_model.conducted}", headers=jwt(member()))
        assert response.status_code == 200
        assert models.ClassRecordCreate(**response.json()) == record_model

    @with_table_cleared(schemas.Class)
    def test_get_class_records(self):
        cls = TestClass.create_class()
        count = 10
        records = sorted([
            models.ClassRecordOutline(
                **tested.post(
                    f"/classes/{cls.name}/records",
                    json=TestClass.create_class_record_serialized(),
                    headers=jwt(board()),
                    params={"limit": count, "skip": 0}
                ).json()
            ) for _ in range(count)],
            key=lambda data: data.conducted
        )
        response = tested.get(f"/classes/{cls.name}/records")
        assert response.status_code == 200
        for fetched, standard in zip(response.json(), records[::-1], strict=True):
            assert models.ClassRecordOutline(**fetched) == standard

    @ with_table_cleared(schemas.Class)
    def test_delete_class_record(self):
        cls = TestClass.create_class()
        record = TestClass.create_class_record_serialized()
        instance = models.ClassRecord(
            **record, cls=cls, moderator=cls.moderator)
        tested.post(
            f"/classes/{cls.name}/records", json=record, headers=jwt(board()))
        response = tested.delete(
            f"/classes/{cls.name}/records/{instance.conducted}")
        assert response.status_code == 401
        response = tested.delete(
            f"/classes/{cls.name}/records/{instance.conducted}", headers=jwt(member()))
        assert response.status_code == 403
        response = tested.delete(
            f"/classes/{cls.name}/records/{instance.conducted}", headers=jwt(board()))
        assert response.status_code == 200
        response = tested.get(
            f"/classes/{cls.name}/records/{instance.conducted}", headers=jwt(member()))
        assert response.status_code == 404


class TestAuth:
    @ with_table_cleared(schemas.Member)
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

    @ with_table_cleared(schemas.Member)
    def test_login(self):
        logging_in = member()
        response = tested.post("/token", data={
            "username": logging_in.username,
            "password": logging_in.password
        })
        assert response.status_code == 200

    @ with_table_cleared(schemas.Member)
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

    @ with_table_cleared(schemas.Member)
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

    @ with_table_cleared(schemas.Member)
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

    @ with_table_cleared(schemas.Member)
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
