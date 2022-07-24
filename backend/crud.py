import re
import bcrypt
from datetime import datetime, date
from pathlib import Path
from sqlalchemy.sql import case
from sqlalchemy.orm import Session, joinedload
from fastapi import UploadFile
import auth
import asyncio
import uuid
from database import SessionLocal, get_db
import models
import schemas


def get_member(db: Session, student_id: int) -> schemas.Member:
    return db.query(schemas.Member).filter(schemas.Member.student_id == student_id).first()


def get_member_by_username(db: Session, username: str) -> schemas.Member:
    return db.query(schemas.Member).filter(schemas.Member.username == username).first()


def get_members(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.Member]:
    return db.query(schemas.Member).offset(skip).limit(limit).all()


def create_member(db: Session, student_id: int, member: models.MemberCreate):
    db_member = schemas.Member(
        student_id=student_id,
        real_name=member.real_name,
        username=member.username,
        password=auth.pwd_context.hash(member.password),
        role=models.Role.member.value
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def update_member(db: Session, student_id: int, member: models.MemberModify):
    updated = db.query(schemas.Member).filter(
        schemas.Member.student_id == student_id)
    actual_object: schemas.Member = updated.first()
    if member.password:
        if not re.match(auth.password_pattern, member.password):
            raise ValueError("Password do not match the required pattern")
        member.password = auth.pwd_context.hash(member.password)
    to = {key:value for key, value in member.dict().items() if value is not None}
    updated.update(to)
    db.commit()
    db.refresh(actual_object)
    return actual_object


def delete_member(db: Session, student_id: int):
    if db.query(schemas.Member).filter(schemas.Member.student_id == student_id).delete():
        db.commit()
        return True
    return False


def get_posts(db: Session, type: models.PostType, skip: int = 0, limit: int = 100):
    return db.query(schemas.Post.no, schemas.Post.author, schemas.Post.title, schemas.Post.published).filter(schemas.Post.type == type.value).order_by(schemas.Post.no.desc()).offset(skip).limit(limit).all()


def get_post(db: Session, type: models.PostType, no: int = None):
    return db.query(schemas.Post).options(joinedload(schemas.Post.attached)).filter(schemas.Post.no == no if no else schemas.Post.type == type.value).first()


def create_post(db: Session, author: models.Member, post: models.PostCreate, type: models.PostType):
    db_post = schemas.Post(
        type=type.value,
        title=post.title,
        author=author.real_name,
        content=post.content,
        published=datetime.today().date(),
        attached=db.query(schemas.UploadedFile)
        .filter(schemas.UploadedFile.uuid.in_(
            [str(id) for id in post.attached]
        )).all()
    )
    db.add(db_post)
    db.commit()
    return db_post


def update_post(db: Session, post: models.PostCreate, modifier: models.Member, no: int = None,  type: models.PostType = None):
    """`no`가 있으면 `no`번 `Post`를, 없으면 `type`이 `type`인 `Post`를 수정합니다."""
    if no:
        updated = db.query(schemas.Post).filter(schemas.Post.no == no)
        updated.update({
            "title": post.title,
            "content": post.content,
            "modified": datetime.today().date(),
            "modifier": modifier.real_name,
        })
        updated.first().attached = db.query(schemas.UploadedFile).filter(
            schemas.UploadedFile.uuid.in_([str(id) for id in post.attached])).all()
        db.commit()
        return updated.first()
    db.query(schemas.Post).filter(schemas.Post.type == type.value).delete()
    new = schemas.Post(
        type=type.value,
        title=post.title,
        author=modifier.real_name,
        content=post.content,
        published=datetime.today().date(),
        attached=db.query(schemas.UploadedFile).filter(
            schemas.UploadedFile.uuid.in_([str(id) for id in post.attached])).all()
    )
    db.add(new)
    db.commit()
    return new


def delete_post(db: Session, type: models.PostType, no: int):
    deleted = db.query(schemas.Post).filter(
        schemas.Post.no == no and schemas.Post.type == type).delete()
    db.commit()
    return deleted


def get_club_information(db: Session):
    return {row.key: row.value for row in db.query(schemas.ClubInformation).all()}


def update_club_information(db: Session, info: models.ClubInformationCreate):
    token_excluded = models.ClubInformation(**info.dict()).dict()
    db.query(schemas.ClubInformation).delete()
    db.add_all([schemas.ClubInformation(key=key, value=value)
               for key, value in token_excluded.items()])
    db.commit()
    return get_club_information(db)


def get_uploaded_file(db: Session, uuid: uuid.UUID) -> schemas.UploadedFile:
    return db.query(schemas.UploadedFile).filter(schemas.UploadedFile.uuid == str(uuid)).first()


async def create_uploaded_file(db: Session, file: UploadFile):
    name = file.filename
    content_type = file.content_type
    internal_uuid = uuid.uuid4()
    with open(f"uploaded/{internal_uuid}", "wb") as f:
        f.write(await file.read())
    row = schemas.UploadedFile(
        uuid=str(internal_uuid),
        name=name,
        content_type=content_type
    )
    db.add(row)
    db.commit()
    return row


async def delete_uploaded_file(db: Session, uuid: uuid.UUID):
    deleted = db.query(schemas.UploadedFile).filter(
        schemas.UploadedFile.uuid == str(uuid)).delete()
    if deleted:
        db.commit()
        Path.unlink(Path("uploaded/"+str(uuid)))
    return deleted


def get_magazine(db: Session, published: date):
    return db.query(schemas.Magazine).filter(schemas.Magazine.published == published).first()


def get_magazines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(schemas.Magazine).order_by(schemas.Magazine.published.desc()).offset(skip).limit(limit).all()


def create_magazine(db: Session, magazine: models.MagazineCreate):
    db_magazine = schemas.Magazine(
        year=magazine.year,
        cover=str(magazine.cover),
        published=magazine.published,
    )
    db.add(db_magazine)
    db.add_all([
        schemas.MagazineContent(
            published=magazine.published,
            type=c.type,
            title=c.title,
            author=c.author,
            language=c.language
        )
        for c in magazine.contents])
    db.commit()
    return db_magazine


def update_magazine(db: Session, published: date, magazine: models.MagazineCreate):
    db.query(schemas.MagazineContent).filter(
        schemas.MagazineContent.published == published).delete()
    updated = db.query(schemas.Magazine).filter(
        schemas.Magazine.published == published)
    if not updated.first():
        return False
    updated.update({
        "year": magazine.year,
        "cover": str(magazine.cover),
        "published": magazine.published
    })
    db.add_all([
        schemas.MagazineContent(
            published=magazine.published,
            type=c.type,
            title=c.title,
            author=c.author,
            language=c.language
        )
        for c in magazine.contents])
    db.commit()
    return magazine


def delete_magazine(db: Session, published: date):
    db.query(schemas.MagazineContent).filter(
        schemas.MagazineContent.published == published).delete()
    if db.query(schemas.Magazine).filter(schemas.Magazine.published == published).delete():
        db.commit()
        return True
    return False


def get_magazine_content(db: Session, published: date):
    return db.query(schemas.MagazineContent).filter(schemas.MagazineContent.published == published).all()


def get_class(db: Session, name: models.ClassName):
    return db.query(schemas.Class).filter(schemas.Class.name == name).first()


def get_classes(db: Session):
    return db.query(schemas.Class).all()


def create_classes_with_default_values(db: Session):
    created = [schemas.Class(
        name=name,
        korean=models.ClassKoreanName[name],
        moderator="홍길동",
        schedule="매주 월요일 오후 5시",
        description="이러쿵저러쿵"
    ) for name in models.ClassName]
    db.add_all(created)
    db.commit()
    return created


def update_class(db: Session, name: models.ClassName, class_data: models.ClassCreate):
    queried = db.query(schemas.Class).filter(schemas.Class.name == name)
    if existing := queried.first():
        queried.update(class_data.dict())
        db.commit()
        return existing


def create_class_record(db: Session, class_name: models.ClassName, moderator: models.Member, record: models.ClassRecordCreate):
    new_record = schemas.ClassRecord(
        class_name=class_name,
        conducted=record.conducted,
        moderator=moderator.real_name,
        topic=record.topic,
        content=record.content,
    )
    db.add(new_record)
    db.commit()
    return new_record


def update_class_record(db: Session, class_name: models.ClassName, conducted: date, record: models.ClassRecordCreate):
    deleted = db.query(schemas.ClassRecord).filter(
        schemas.ClassRecord.class_name == class_name, schemas.ClassRecord.conducted == conducted)
    original: schemas.ClassRecord = deleted.first()
    if not original:
        return False
    deleted.delete()
    moderator = original.moderator
    updated = schemas.ClassRecord(
        class_name=class_name,
        conducted=record.conducted,
        moderator=moderator,
        topic=record.topic,
        content=record.content
    )
    db.add(updated)
    db.commit()
    db.refresh(updated)
    return updated


def get_class_record(db: Session, class_name: models.ClassName, conducted: date) -> schemas.ClassRecord:
    return db.query(schemas.ClassRecord).filter(schemas.ClassRecord.class_name == class_name, schemas.ClassRecord.conducted == conducted).first()


def get_class_records(db: Session, class_name: models.ClassName, skip: int = 0, limit: int = 100):
    return db.query(schemas.ClassRecord).filter(schemas.ClassRecord.class_name == class_name).order_by(schemas.ClassRecord.conducted.desc()).offset(skip).limit(limit).all()


def delete_class_record(db: Session, class_name: models.ClassName, conducted: date):
    deleted = db.query(schemas.ClassRecord).filter(schemas.ClassRecord.class_name ==
                                                   class_name, schemas.ClassRecord.conducted == conducted).delete()
    db.commit()
    return deleted
