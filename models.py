from __future__ import annotations
from typing import Union
from datetime import date
from enum import Enum
from pydantic import BaseModel


class Role(str, Enum):
    member = "member"
    board = "board"
    president = "president"


class PostType(str, Enum):
    notice = "notice"
    about = "about"
    rules = "rules"
    class_record = "class_record"


class TokenData(BaseModel):
    student_id: Union[str, None] = None


class UploadedFileBase(BaseModel):
    name: str
    content_type: str


class UploadedFileCreate(UploadedFileBase):
    pass


class UploadedFile(UploadedFileBase):
    id: int

    class Config:
        orm_mode = True


class MemberBase(BaseModel):
    username: str


class MemberCreate(MemberBase):
    real_name: str
    password: str


class MemberModify(BaseModel):
    role: Union[Role, None] = None
    password: Union[str, None] = None


class Member(MemberBase):
    """사이트 회원."""

    student_id: str
    role: Role = Role.member
    real_name: str

    class Config:
        orm_mode = True


class ClubMemberBase(BaseModel):
    tel: str
    invite_informal_chat: bool


class ClubMember(BaseModel):
    """동아리 회원."""

    status: str
    student_id: str
    name: str
    dept_and_major: str


class ClubMemberCreate(ClubMemberBase):
    portal_id: str
    portal_pw: str


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    attached: list[int]


class Post(PostBase):
    type: PostType
    no: int
    author: str
    published: date
    modified: Union[date, None] = None
    modifier: Union[str, None] = None
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
    order: int


class ClassCreate(ClassBase):
    name: str


class ClassModify(ClassBase):
    pass


class Class(ClassBase):
    name: str

    class Config:
        orm_mode = True


class ClassRecordBase(BaseModel):
    conducted: date
    topic: str
    content: str


class ClassRecordCreate(ClassRecordBase):
    pass


class ClassRecord(ClassRecordBase):
    moderator: str

    class Config:
        orm_mode = True


class ClassRecordOutline(BaseModel):
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
    cover: int
    published: date


class MagazineCreate(MagazineBase):
    contents: list[MagazineContentCreate]


class Magazine(MagazineBase):
    contents: list[MagazineContent]

    class Config:
        orm_mode = True


class MagazineOutline(BaseModel):
    published: date
    cover: int

    class Config:
        orm_mode = True


class ClubInformation(BaseModel):
    key: str
    value: str
    public: bool

    class Config:
        orm_mode = True


class FunctionSwitch(BaseModel):
    name: str
    on: bool

    class Config:
        orm_mode = True
