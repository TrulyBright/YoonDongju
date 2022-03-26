from __future__ import annotations
from datetime import date
from enum import Enum
from pydantic import BaseModel

class Role(str, Enum):
    president = "president"
    board = "board"
    member = "member"

class PostType(str, Enum):
    notice = "notice"
    about = "about"
    rules = "rules"

class ClassName(str, Enum):
    poetry = "poetry"
    novel = "novel"
    critique = "critique"
    reading = "reading"

class ClubInformationBase(BaseModel):
    address: str
    email: str
    president_name: str
    president_tel: str
    join_form_url: str

class ClubInformationCreate(BaseModel):
    pass

class ClubInformation(ClubInformationBase):
    pass

class MemberBase(BaseModel):
    stduent_id: int
    real_name: str
    username: str

class MemberCreate(MemberBase):
    password: str

class Member(MemberBase):
    role: Role = Role.member
    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    attached: bytes | None = None
    type: PostType

class Post(PostBase):
    no: str
    author: str
    published: date
    modified: date | None = None
    modifier: str | None = None
    attached: str | None = None

    class Config:
        orm_mode = True

class ClassBase(BaseModel):
    name: ClassName
    moderator: str
    schedule: str
    description: str

class ClassCreate(ClassBase):
    pass

class Class(ClassBase):
    pass

class ClassParticipantBase(BaseModel):
    name: str

class ClassParticipantCreate(ClassParticipantBase):
    pass

class ClassParticipant(ClassParticipantBase):
    pass

class ClassRecordBase(BaseModel):
    conducted: date
    topic: str
    content: str
    participants: list[ClassParticipant]

class ClassRecordCreate(ClassRecordBase):
    class_name: str

class ClassRecord(ClassRecordBase):
    id: int
    moderator: str
    class Config:
        orm_mode = True

class MagazineContentBase(BaseModel):
    type: str
    title: str
    author: str
    language: str

class MagazineContentCreate(MagazineContentBase):
    pass

class MagazineContent(MagazineContentBase):
    pass

class MagazineBase(BaseModel):
    year: int
    season: int
    cover: str
    published: date
    contents: list[MagazineContent]

class MagazineCreate(MagazineBase):
    class Config:
        orm_mode = True

class Magazine(MagazineBase):
    pass