from datetime import date
from enum import Enum
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
import crud
import schemas
from database import SessionLocal, engine

schemas.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RegisterForm(BaseModel):
    portal_id: int
    portal_pw: str
    realname: str
    username: str
    password: str

class LoginForm(BaseModel):
    username: str
    password: str

@app.get("/club-information", response_model=models.ClubInformation)
async def get_club_information():
    pass

@app.patch("/club-information", response_model=models.ClubInformation)
async def update_club_information(info: models.ClubInformation):
    pass

@app.get("/recent-notices", response_model=list[models.Post])
async def get_recent_notices(limit: int=4, db: Session=Depends(get_db)):
    return crud.get_recent_notices(db=db, limit=limit)

@app.get("/recent-magazines", response_model=list[models.Magazine])
async def get_recent_magazines():
    return []

@app.get("/about", response_model=models.Post)
async def get_about(db: Session=Depends(get_db)):
    return crud.get_post(db=db, type=models.PostType.about)

@app.patch("/about", response_model=models.Post)
async def update_about(about: models.PostCreate, db: Session=Depends(get_db)):
    return crud.update_post(db=db, type=models.PostType.about, post=about)

@app.get("/rules", response_model=models.Post)
async def get_rules(db: Session=Depends(get_db)):
    return crud.get_post(db=db,type=models.PostType.rules)

@app.patch("/rules", response_model=models.Post)
async def update_rules(rules: models.PostCreate, db: Session=Depends(get_db)):
    return crud.update_post(db=db, type=models.PostType.rules, post=rules)

@app.get("/notices", response_model=list[models.Post])
async def get_notices(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    return crud.get_posts(db=db, type=models.PostType.notice, skip=skip, limit=limit)

@app.get("/notices/{no:int}", response_model=models.Post)
async def get_notice(no: int, db: Session=Depends(get_db)):
    db_notice = crud.get_post(db=db, type=models.PostType.notice, no=no)
    if db_notice is None:
        raise HTTPException(404, "그런 글이 없습니다.")
    return db_notice

@app.post("/notices", response_model=models.Post)
async def create_notice(post: models.PostCreate, db: Session=Depends(get_db)):
    return crud.create_post(db=db, post=post)

@app.patch("/notices/{no:int}", response_model=models.Post)
async def update_notice(no: int, post: models.PostCreate, db: Session=Depends(get_db)):
    updated = crud.update_post(db, models.PostType.notice, post, no)
    if updated is None:
        raise HTTPException(404, "그런 글이 없습니다.")
    return updated

@app.delete("/notices/{no:int}")
async def delete_notice(no: int, db: Session=Depends(get_db)):
    if not crud.delete_post(db, models.PostType.notice, no):
        raise HTTPException(404, "그런 글이 없습니다.")

@app.get("/members", response_model=list[models.Member])
async def get_members(skip: int, limit: int, db: Session=Depends(get_db)):
    return crud.get_members(db, skip, limit)

@app.get("/members/{student_id:int}", response_model=models.Member)
async def get_member(student_id: int, db: Session=Depends(get_db)):
    db_member = crud.get_member(db, student_id)
    if db_member is None:
        raise HTTPException(404, "가입되지 않은 학번입니다.")
    return db_member

@app.post("/members", response_model=models.Member)
async def create_member(member: models.MemberCreate, db: Session=Depends(get_db)):
    if crud.get_member(db, member.stduent_id):
        raise HTTPException(400, "이미 가입된 학번입니다.")
    return crud.create_member(db, member)

@app.patch("/members/{student_id:int}", response_model=models.Member)
async def update_member(student_id: int, member: models.MemberCreate):
    pass

@app.delete("/members/{student_id:int}")
async def delete_member(student_id: int):
    pass

@app.get("/magazines", response_model=list[models.Magazine])
async def get_magazines():
    return []

@app.get("/magazines/{published}", response_model=models.Magazine)
async def get_magazine(published: date):
    pass

@app.post("/magazines", response_model=models.Magazine)
async def create_magazine(magazine: models.MagazineCreate):
    pass

@app.patch("/magazines/{published}", response_model=models.Magazine)
async def update_magazine(published: date, magazine: models.MagazineCreate):
    pass

@app.delete("/magazines/{published}")
async def delete_magazine(published:date):
    pass

@app.get("/classes", response_model=list[models.Class])
async def get_classes():
    return None

@app.get("/classes/{class_name}", response_model=models.Class)
async def get_class(class_name: models.ClassName):
    return None

@app.patch("/classes/{class_name}", response_model=models.Class)
async def update_class(class_name: models.ClassName):
    pass

@app.get("/classes/{class_name}/records", response_model=list[models.ClassRecord])
async def get_class_records(class_name: models.ClassName):
    pass

@app.get("/classes/{class_name}/records/{id:int}", response_model=models.ClassRecord)
async def get_class_record(class_name: models.ClassName, id: int):
    pass

@app.post("/classes/{class_name}/records", response_model=models.ClassRecord)
async def create_class_record(class_name: models.ClassName, records: models.ClassRecord):
    pass

@app.patch("/classes/{class_name}/records/{id:int}", response_model=models.ClassRecord)
async def update_class_record(class_name: models.ClassName, id: int):
    pass

@app.delete("/classes/{class_name}/records/{id:int}")
async def delete_class_record(class_name: models.ClassName, id: int):
    pass

@app.post("/register")
async def register(form: RegisterForm):
    return None

@app.post("/login")
async def login(form: LoginForm):
    pass