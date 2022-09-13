from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    LargeBinary,
    Boolean,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from database import Base


class ClubInformation(Base):
    __tablename__ = "clubInformations"
    key = Column(String, primary_key=True)
    value = Column(String)
    public = Column(Boolean)


class FunctionSwitch(Base):
    __tablename__ = "functionSwitch"
    name = Column(String, primary_key=True)
    on = Column(Boolean)


class Member(Base):
    __tablename__ = "members"
    student_id = Column(String, primary_key=True, index=True)
    real_name = Column(String)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)


class Post(Base):
    __tablename__ = "posts"
    no = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String)
    title = Column(String)
    author = Column(String)
    content = Column(String)
    published = Column(Date)
    modified = Column(Date, nullable=True)
    modifier = Column(String, nullable=True)
    attached = relationship(
        "UploadedFile",
        cascade="all,delete",
        passive_deletes=True,
    )


class UploadedFile(Base):
    __tablename__ = "uploadedFiles"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    content_type = Column(String)
    binary = Column(LargeBinary)
    post_no = Column(Integer, ForeignKey(
        "posts.no", ondelete="CASCADE"), nullable=True)


class Class(Base):
    __tablename__ = "classes"
    name = Column(String, primary_key=True)
    moderator = Column(String)
    schedule = Column(String)
    description = Column(String)
    order = Column(Integer)
    records = relationship(
        "ClassRecord",
        cascade="all,delete",
        passive_deletes=True,
    )


class ClassRecord(Base):
    __tablename__ = "classPostRelationship"
    cls = Column(String, ForeignKey("classes.name", ondelete="CASCADE"))
    conducted = Column(Date)
    post_no = Column(String, ForeignKey(
        "posts.no", ondelete="CASCADE"), primary_key=True)
    __table_args__ = (UniqueConstraint("cls", "conducted"),)


class Magazine(Base):
    __tablename__ = "magazines"
    year = Column(Integer)
    cover = Column(Integer, ForeignKey("uploadedFiles.id"))  # 표지 파일 ID
    published = Column(Date, primary_key=True)
    contents = relationship("MagazineContent",
                            cascade="all,delete",
                            passive_deletes=True,)


class MagazineContent(Base):
    __tablename__ = "magazineContents"
    no = Column(Integer, primary_key=True)
    published = Column(Date, ForeignKey(
        "magazines.published", ondelete="CASCADE"), index=True)
    type = Column(String)
    title = Column(String)
    author = Column(String)
    language = Column(String)
