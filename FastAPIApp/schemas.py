from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    LargeBinary
)
from sqlalchemy.orm import relationship

from FastAPIApp.database import Base


class ClubInformation(Base):
    __tablename__ = "clubInformations"
    key = Column(String, primary_key=True)
    value = Column(String)


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
    uuid = Column(String, primary_key=True, index=True)
    name = Column(String)
    content_type = Column(String)
    blob = Column(LargeBinary)
    post_no = Column(Integer, ForeignKey(
        "posts.no", ondelete="CASCADE"), nullable=True)


class Class(Base):
    __tablename__ = "classes"
    name = Column(String, primary_key=True)
    korean = Column(String, unique=True)
    moderator = Column(String)
    schedule = Column(String)
    description = Column(String)
    records = relationship("ClassRecord")


class ClassRecord(Base):
    __tablename__ = "classRecords"
    class_name = Column(
        String, ForeignKey("classes.name"), index=True, primary_key=True
    )
    conducted = Column(Date, index=True, primary_key=True)
    moderator = Column(String)
    topic = Column(String)
    content = Column(String)


class Magazine(Base):
    __tablename__ = "magazines"
    cover = Column(String, ForeignKey("uploadedFiles.uuid"))  # 표지 파일 UUID
    published = Column(Date, primary_key=True)
    contents = relationship("MagazineContent")


class MagazineContent(Base):
    __tablename__ = "magazineContents"
    no = Column(Integer, primary_key=True)
    published = Column(Date, ForeignKey("magazines.published"), index=True)
    type = Column(String)
    title = Column(String)
    author = Column(String)
    language = Column(String)
