from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    UniqueConstraint,
    PrimaryKeyConstraint,
    ForeignKeyConstraint
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
    class_name = Column(String, ForeignKey("classes.name"), index=True)
    conducted = Column(Date, index=True)
    moderator = Column(String)
    topic = Column(String)
    content = Column(String)
    participants = relationship("ClassParticipant")
    __table_args__ = (PrimaryKeyConstraint("class_name", 'conducted'),)

class ClassParticipant(Base):
    __tablename__ = "classParticipants"
    no = Column(Integer, primary_key=True)
    class_name = Column(String, index=True)
    conducted = Column(Date, index=True)
    name = Column(String)
    __table_args__ = (
        ForeignKeyConstraint(
            [class_name, conducted],
            [ClassRecord.class_name, ClassRecord.conducted]
        ),
    )

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
    no = Column(Integer, primary_key=True)
    published = Column(Integer, ForeignKey("magazines.published"), index=True)
    type = Column(String)
    title = Column(String)
    author = Column(String)
    language = Column(String)