from __future__ import annotations
from datetime import date
from enum import Enum
import json
from uuid import UUID
from pydantic import BaseModel
from fastapi import UploadFile


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


class TokenData(BaseModel):
    student_id: int | None = None


class UploadedFileBase(BaseModel):
    name: str


class UploadedFileCreate(UploadedFileBase):
    pass


class UploadedFile(UploadedFileBase):
    uuid: UUID
    content_type: str

    class Config:
        orm_mode = True


class ClubInformationBase(BaseModel):
    address: str
    email: str
    president_name: str
    president_tel: str
    join_form_url: str


class ClubInformationCreate(ClubInformationBase):
    pass


class ClubInformation(ClubInformationBase):
    class Config:
        orm_mode = True


class MemberBase(BaseModel):
    username: str
    real_name: str


class MemberCreate(MemberBase):
    password: str


class MemberModify(BaseModel):
    role: Role | None = None


class Member(MemberBase):
    student_id: int
    role: Role = Role.member

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    attached: list[UUID]


class Post(PostBase):
    type: PostType
    no: int
    author: str
    published: date
    modified: date | None = None
    modifier: str | None = None
    attached: list[UploadedFile]

    class Config:
        orm_mode = True


class PostOutline(BaseModel):
    no: int
    title: str
    author: str
    published: date

    class Config:
        orm_mode = True


class ClassBase(BaseModel):
    moderator: str
    schedule: str
    description: str


class ClassCreate(ClassBase):
    pass


class Class(ClassBase):
    name: ClassName

    class Config:
        orm_mode = True


class ClassRecordBase(BaseModel):
    conducted: date
    topic: str
    content: str


class ClassRecordCreate(ClassRecordBase):
    pass

class ClassRecord(ClassRecordBase):
    class_name: ClassName
    moderator: str

    class Config:
        orm_mode = True


class ClassRecordOutline(BaseModel):
    class_name: ClassName
    moderator: str
    conducted: date
    topic: str

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
    class Config:
        orm_mode = True


class MagazineBase(BaseModel):
    year: int
    cover: UUID
    published: date


class MagazineCreate(MagazineBase):
    contents: list[MagazineContentCreate]


class Magazine(MagazineBase):
    contents: list[MagazineContent]

    class Config:
        orm_mode = True


class MagazineOutline(BaseModel):
    published: date
    cover: UUID

    class Config:
        orm_mode = True
