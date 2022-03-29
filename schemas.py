from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    UniqueConstraint,
    PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship

from database import Base

class ClubInformation(Base):
    __tablename__ = "clubInformations"
    key = Column(String, primary_key=True)
    value = Column(String)

class Member(Base):
    __tablename__ = "members"
    student_id = Column(Integer, primary_key=True, index=True)
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
    # attached_files = relationship("AttachedFile") TODO

class UploadedFile(Base):
    __tablename__ = "uploadedFiles"
    uuid = Column(String, primary_key=True)
    name = Column(String)
    content_type = Column(String)

class Class(Base):
    __tablename__ = "classes"
    name = Column(String, primary_key=True)
    moderator = Column(String)
    schedule = Column(String)
    description = Column(String)
    records = relationship("ClassRecord")

class ClassRecord(Base):
    __tablename__ = "classRecords"
    id = Column(Integer, primary_key=True)
    class_name = Column(String, ForeignKey("classes.name"))
    conducted = Column(Date)
    moderator = Column(String)
    topic = Column(String)
    content = Column(String)
    participants = relationship("ClassParticipant")
    __table_args__ = (UniqueConstraint("class_name", 'conducted'),)

class ClassParticipant(Base):
    __tablename__ = "classParticipants"
    record_id = Column(String, ForeignKey("classRecords.id"))
    index = Column(Integer)
    name = Column(String)
    __table_args__ = (PrimaryKeyConstraint("record_id", "index"),)

class Magazine(Base):
    __tablename__ = "magazines"
    year = Column(Integer)
    season = Column(Integer)
    cover = Column(String, ForeignKey("uploadedFiles.uuid")) # 표지 파일 UUID
    published = Column(Date, primary_key=True)
    contents = relationship("MagazineContent")
    __table_args__ = (UniqueConstraint('year', 'season'),)

class MagazineContent(Base):
    __tablename__ = "magazineContents"
    published = Column(Integer, ForeignKey("magazines.published"), index=True)
    index = Column(Integer)
    type = Column(String)
    title = Column(String)
    author = Column(String)
    language = Column(String)
    __table_args__ = (PrimaryKeyConstraint("published", "index"),)