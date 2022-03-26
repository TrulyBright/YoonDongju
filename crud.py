import bcrypt
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import UploadFile
import auth
import asyncio
import uuid
import models
import schemas

def get_member(db: Session, student_id: int) -> schemas.Member:
    return db.query(schemas.Member).filter(schemas.Member.student_id==student_id).first()

def get_member_by_username(db: Session, username: str) -> schemas.Member:
    return db.query(schemas.Member).filter(schemas.Member.username==username).first()

def get_members(db: Session, skip: int=0, limit: int=100):
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
    return models.Member(
        student_id=db_member.student_id,
        real_name=db_member.real_name,
        username=db_member.username,
        role=db_member.role
    )

def update_member(db: Session, student_id: int, member: models.MemberModify):
    updated = db.query(schemas.Member).filter(schemas.Member.student_id==student_id)
    actual_object = updated.first()
    to = member.dict()
    updated.update(to)
    db.commit()
    db.refresh(actual_object)
    return actual_object

def get_posts(db: Session, type: models.PostType, skip: int=0, limit: int=100):
    return db.query(schemas.Post).filter(schemas.Post.type==type.value).offset(skip).limit(limit).all()

def get_post(db: Session, type: models.PostType, no: int=0):
    return db.query(schemas.Post).filter((type != models.PostType.notice or schemas.Post.no==no) and schemas.Post.type==type.value).first()

def get_recent_notices(db: Session, limit: int=4):
    return (
        db
        .query(schemas.Post)
        .filter(schemas.Post.type == models.PostType.notice)
        .order_by(schemas.Post.no.desc())
        .limit(limit)
        .all()
    )

async def create_post(db: Session, author: models.Member, post: models.PostCreate, type: models.PostType):
    # Path("sql").mkdir(exist_ok=True)
    # async def __upload(file: UploadFile):
    #     content = await file.read()
    #     internal_uuid = uuid.uuid4()
    #     with open(f"sql/{internal_uuid}", "wb") as f:
    #         f.write(content)
    #     db.add(schemas.AttachedFile(
    #         uuid=internal_uuid,
    #         type=file.content_type,
    #         name=file.filename
    #     ))
    # await asyncio.gather(*[__upload(file) for file in post.attached])
    db_post = schemas.Post(
        type=type.value,
        title=post.title,
        author=author.real_name,
        content=post.content,
        published=datetime.today().date(),
        # attached_files=
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return models.Post(
        title=db_post.title,
        content=db_post.content,
        no=db_post.no,
        author=db_post.author,
        published=db_post.published,
        modified=db_post.modified,
        modifier=db_post.modifier,
        type=db_post.type
    )

def update_post(db: Session, type: models.PostType, post: models.PostCreate, modifier: models.Member, no: int=None):
    """변경된 `Post`를 반환합니다."""
    updated = db.query(schemas.Post).filter(schemas.Post.no==no if no else schemas.Post.type==type.value)
    original: schemas.Post = updated.first()
    modified = models.Post(
        title=post.title,
        content=post.content,
        no=original.no,
        author=original.author,
        published=original.published,
        modified=datetime.today().date(),
        modifier=modifier.real_name,
        type=original.type
    )
    updated.update(modified.dict())
    db.commit()
    db.refresh(original)
    return modified

def delete_post(db: Session, type: models.PostType, no: int):
    """삭제에 성공하면 `True`, 못 하면 `False`"""
    deleted = db.query(schemas.Post).filter(schemas.Post.no==no and schemas.Post.type==type)
    victim: schemas.Post = deleted.first()
    deleted.delete()
    db.commit()
    return victim is not None