import bcrypt
from datetime import datetime
from sqlalchemy.orm import Session
import models
import schemas

def get_member(db: Session, student_id: int):
    return db.query(schemas.Member).filter(schemas.Member.student_id == student_id).first()

def get_members(db: Session, skip: int=0, limit: int=100):
    return db.query(schemas.Member).offset(skip).limit(limit).all()

def create_member(db: Session, member: models.MemberCreate):
    db_member = schemas.Member(
        student_id=member.stduent_id,
        real_name=member.real_name,
        username=member.username,
        password=bcrypt.hashpw(member.password, bcrypt.gensalt()),
        role=models.Role.member.value
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

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

def create_post(db: Session, author: models.Member, post: models.PostCreate):
    db_post = schemas.Post(
        type=post.type.value,
        title=post.title,
        author=author.real_name,
        content=post.content,
        published=datetime.today().date(),
        attached=post.attached
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, type: models.PostType, post: models.PostCreate, no: int=None):
    """변경된 `Post`를 반환합니다."""
    updated = db.query(schemas.Post).filter(schemas.Post.no==no or schemas.Post.type==type.value)
    updated.update(post.dict())
    return updated.first()

def delete_post(db: Session, type: models.PostType, no: int):
    """삭제에 성공하면 `True`, 못 하면 `False`"""
    deleted = db.query(schemas.Post).filter(schemas.Post.no==no and schemas.Post.type==type)
    deleted.delete()
    return deleted.first() is not None