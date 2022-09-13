from msilib import schema
import re
from typing import Union
from datetime import datetime, date
import sqlalchemy
from sqlalchemy.orm import Session, joinedload
from fastapi import UploadFile, HTTPException
import auth
import models
import schemas


def get_member(db: Session, student_id: str) -> schemas.Member:
    return (
        db.query(schemas.Member).filter(
            schemas.Member.student_id == student_id).first()
    )


def get_member_by_username(db: Session, username: str) -> schemas.Member:
    return db.query(schemas.Member).filter(schemas.Member.username == username).first()


def get_members(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.Member]:
    return db.query(schemas.Member).offset(skip).limit(limit).all()


def create_member(db: Session, student_id: str, member: models.MemberCreate):
    db_member = schemas.Member(
        student_id=student_id,
        real_name=member.real_name,
        username=member.username,
        password=auth.pwd_context.hash(member.password),
        role=models.Role.member,
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def update_member(db: Session, student_id: str, member: models.MemberModify):
    """`password`는 평문으로 주세요. 이 함수에서 `hash`해줍니다."""
    if member.password:
        if not re.match(auth.password_pattern, member.password):
            raise HTTPException(400, "비밀번호가 규칙에 맞지 않습니다.")
        member.password = auth.pwd_context.hash(member.password)
    updated = db.query(schemas.Member).filter(
        schemas.Member.student_id == student_id)
    actual_object: schemas.Member = updated.first()
    if actual_object is None:
        return actual_object
    to = {key: value for key, value in member.dict().items()
          if value is not None}
    updated.update(to)
    db.commit()
    db.refresh(actual_object)
    return actual_object


def delete_member(db: Session, student_id: str):
    if (
        db.query(schemas.Member)
        .filter(schemas.Member.student_id == student_id)
        .delete()
    ):
        db.commit()
        return True
    return False


def get_posts(
    db: Session, type: models.PostType, skip: int = 0, limit: Union[int, None] = None
):
    return (
        db.query(
            schemas.Post.no,
            schemas.Post.author,
            schemas.Post.title,
            schemas.Post.published,
        )
        .filter(schemas.Post.type == type.name)
        .order_by(schemas.Post.no.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_post_count(db: Session, type: models.PostType):
    return db.query(schemas.Post).filter(schemas.Post.type == type.name).count()


def get_post(db: Session, type: models.PostType, no: int = None):
    return (
        db.query(schemas.Post)
        .options(joinedload(schemas.Post.attached))
        .filter(schemas.Post.no == no if no else schemas.Post.type == type.name)
        .first()
    )


def create_post(
    db: Session, author: models.Member, post: models.PostCreate, type: models.PostType
):
    db_post = schemas.Post(
        type=type.value,
        title=post.title,
        author=author.real_name,
        content=post.content,
        published=datetime.today().date(),
        attached=db.query(schemas.UploadedFile)
        .filter(schemas.UploadedFile.id.in_(post.attached))
        .all(),
    )
    db.add(db_post)
    db.commit()
    return db_post


def update_post(
    db: Session,
    post: models.PostCreate,
    modifier: models.Member,
    no: int = None,
    type: models.PostType = None,
):
    """`no`가 있으면 `no`번 `Post`를, 없으면 `type`이 `type`인 `Post`를 수정합니다."""
    if no:
        updated = db.query(schemas.Post).filter(schemas.Post.no == no)
        updated.update(
            {
                "title": post.title,
                "content": post.content,
                "modified": datetime.today().date(),
                "modifier": modifier.real_name,
            }
        )
        updated.first().attached = (
            db.query(schemas.UploadedFile)
            .filter(schemas.UploadedFile.id.in_(post.attached))
            .all()
        )
        db.commit()
        return updated.first()
    db.query(schemas.Post).filter(schemas.Post.type == type.value).delete()
    new = schemas.Post(
        type=type.value,
        title=post.title,
        author=modifier.real_name,
        content=post.content,
        published=datetime.today().date(),
        attached=db.query(schemas.UploadedFile)
        .filter(schemas.UploadedFile.id.in_(post.attached))
        .all(),
    )
    db.add(new)
    db.commit()
    return new


def delete_post(db: Session, type: models.PostType, no: int):
    deleted = (
        db.query(schemas.Post)
        .filter(schemas.Post.no == no and schemas.Post.type == type)
        .delete()
    )
    db.commit()
    return deleted


def get_club_information(db: Session):
    return {row.key: row.value for row in db.query(schemas.ClubInformation).all()}


def update_club_information(db: Session, info: dict[str, str]):
    db.query(schemas.ClubInformation).delete()
    db.add_all(
        [
            schemas.ClubInformation(key=key, value=value)
            for key, value in info.items()
        ]
    )
    db.commit()
    return get_club_information(db)


def get_uploaded_file(db: Session, id: int) -> schemas.UploadedFile:
    return (
        db.query(schemas.UploadedFile)
        .filter(schemas.UploadedFile.id == id)
        .first()
    )


async def create_uploaded_file(db: Session, file: UploadFile):
    name = file.filename
    content_type = file.content_type
    row = schemas.UploadedFile(
        name=name, content_type=content_type, binary=file.file.read()
    )
    db.add(row)
    db.commit()
    return row


async def delete_uploaded_file(db: Session, id: int):
    try:
        return db.query(schemas.UploadedFile).filter(schemas.UploadedFile.id == id).delete()
    finally:
        db.commit()


def get_magazine(db: Session, published: date):
    return (
        db.query(schemas.Magazine)
        .filter(schemas.Magazine.published == published)
        .first()
    )


def get_magazines(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(schemas.Magazine)
        .order_by(schemas.Magazine.published.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_magazine(db: Session, magazine: models.MagazineCreate):
    db_magazine = schemas.Magazine(
        year=magazine.year,
        cover=magazine.cover,
        published=magazine.published,
    )
    db.add(db_magazine)
    db.add_all(
        [
            schemas.MagazineContent(
                published=magazine.published,
                type=c.type,
                title=c.title,
                author=c.author,
                language=c.language,
            )
            for c in magazine.contents
        ]
    )
    db.commit()
    return db_magazine


def update_magazine(db: Session, published: date, magazine: models.MagazineCreate):
    db.query(schemas.MagazineContent).filter(
        schemas.MagazineContent.published == published
    ).delete()
    updated = db.query(schemas.Magazine).filter(
        schemas.Magazine.published == published)
    if not updated.first():
        return False
    updated.update(
        {
            "year": magazine.year,
            "cover": magazine.cover,
            "published": magazine.published,
        }
    )
    db.add_all(
        [
            schemas.MagazineContent(
                published=magazine.published,
                type=c.type,
                title=c.title,
                author=c.author,
                language=c.language,
            )
            for c in magazine.contents
        ]
    )
    db.commit()
    return magazine


def delete_magazine(db: Session, published: date):
    if db.query(schemas.Magazine).filter(schemas.Magazine.published == published).delete():
        db.commit()
        return True
    return False


def get_magazine_content(db: Session, published: date):
    return (
        db.query(schemas.MagazineContent)
        .filter(schemas.MagazineContent.published == published)
        .all()
    )


def get_class(db: Session, name: str):
    return db.query(schemas.Class).filter(schemas.Class.name == name).first()


def get_classes(db: Session):
    return db.query(schemas.Class).order_by(schemas.Class.order).all()


def create_class(db: Session, cls: models.ClassCreate):
    instance = schemas.Class(**cls.dict())
    db.add(instance)
    db.commit()
    return instance


def delete_class(db: Session, name: str):
    if deleted := db.query(schemas.Class).filter(schemas.Class.name == name).delete():
        db.commit()
    return deleted


def update_class(db: Session, cls: models.ClassModify, name: str):
    updated = db.query(schemas.Class).filter(
        schemas.Class.name == name)
    updated.update(cls.dict())
    db.commit()
    return updated.first()


def create_class_record(db: Session, name: str, record: models.ClassRecordCreate, moderator: models.Member):
    if db.query(schemas.ClassRecord).filter(schemas.ClassRecord.cls == name, schemas.ClassRecord.conducted == record.conducted).one_or_none():
        raise HTTPException(409)
    instance = schemas.Post(
        type=models.PostType.class_record,
        title=record.topic,
        author=moderator.real_name,
        content=record.content,
        published=record.conducted,
    )
    db.add(instance)
    db.commit()
    db.refresh(instance)
    relation = schemas.ClassRecord(
        cls=name, conducted=record.conducted, post_no=instance.no)
    db.add(relation)
    db.commit()
    return models.ClassRecord(
        conducted=record.conducted,
        topic=record.topic,
        content=record.content,
        moderator=moderator.real_name
    )


def update_class_record(db: Session, name: str, conducted: date, record: models.ClassRecordCreate):
    if db.query(schemas.ClassRecord).filter(schemas.ClassRecord.cls == name, schemas.ClassRecord.conducted == conducted).one_or_none() is None:
        raise HTTPException(404)
    post = db.query(schemas.Post).filter(schemas.Post.no == db.query(schemas.ClassRecord).filter(
        schemas.ClassRecord.cls == name,
        schemas.ClassRecord.conducted == conducted
    ).one().post_no)
    post.update({
        "title": record.topic,
        "content": record.content,
        "published": record.conducted
    })
    db.commit()
    row = post.first()
    return models.ClassRecord(
        conducted=row.published,
        topic=row.title,
        content=row.content,
        moderator=row.author
    )


def get_class_record(db: Session, name: str, conducted: date):
    try:
        post_instance: schemas.Post = db.query(schemas.Post).filter(
            schemas.Post.no == db.query(
                schemas.ClassRecord
            ).filter(
                schemas.ClassRecord.cls == name,
                schemas.ClassRecord.conducted == conducted
            ).one().post_no).one()
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(404)
    return models.ClassRecord(
        conducted=post_instance.published,
        topic=post_instance.title,
        content=post_instance.content,
        moderator=post_instance.author,
    )


def get_class_records(db: Session, name: str, limit: int, skip: int):
    rows = db.query(schemas.ClassRecord).filter(
        schemas.ClassRecord.cls == name).offset(skip).limit(limit).all()
    results: list[schemas.Post] = db.query(schemas.Post).filter(
        schemas.Post.no.in_({int(row.post_no) for row in rows})).order_by(schemas.Post.published.desc()).all()
    return [models.ClassRecordOutline(
        moderator=r.author,
        conducted=r.published,
        topic=r.title
    ) for r in results]


def delete_class_record(db: Session, name: str, conducted: date):
    if deleted := db.query(schemas.Post).filter(schemas.Post.no == db.query(schemas.ClassRecord).filter(
            schemas.ClassRecord.cls == name, schemas.ClassRecord.conducted == conducted).one().post_no).delete():
        db.commit()
    return deleted
