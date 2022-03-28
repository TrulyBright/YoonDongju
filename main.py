import re
from functools import lru_cache
from datetime import date, timedelta
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, BaseSettings
import models
import crud
import auth
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
    real_name: str
    username: str
    password: str

@app.get("/club-information", response_model=models.ClubInformation)
async def get_club_information(db: Session=Depends(get_db)):
    return crud.get_club_information(db=db)

@app.put("/club-information", response_model=models.ClubInformation)
async def update_club_information(info: models.ClubInformationCreate, db: Session=Depends(get_db)):
    updater = await auth.get_current_member(db=db, token=info.token)
    if updater.role in {
        models.Role.board,
        models.Role.president
    }:
        return crud.update_club_information(db=db, info=info)
    raise HTTPException(status_code=403, detail="권한이 없습니다.")

@app.get("/recent-notices", response_model=list[models.Post])
async def get_recent_notices(limit: int=4, db: Session=Depends(get_db)):
    return crud.get_recent_notices(db=db, limit=limit)

@app.get("/recent-magazines", response_model=list[models.Magazine])
async def get_recent_magazines():
    return []

@app.get("/about", response_model=models.Post)
async def get_about(db: Session=Depends(get_db)):
    return crud.get_post(db=db, type=models.PostType.about)

@app.put("/about", response_model=models.Post)
async def update_about(about: models.PostCreate, db: Session=Depends(get_db)):
    modifier = await auth.get_current_member(db=db, token=about.token)
    if modifier.role in {
        models.Role.board,
        models.Role.president
    }:
        return crud.update_post(db=db, type=models.PostType.about, post=about, modifier=modifier)
    raise HTTPException(status_code=403, detail="권한이 없습니다.")

@app.get("/rules", response_model=models.Post)
async def get_rules(db: Session=Depends(get_db)):
    return crud.get_post(db=db,type=models.PostType.rules)

@app.put("/rules", response_model=models.Post)
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
    author = await auth.get_current_member(db=db, token=post.token)
    if author.role in {
        models.Role.board,
        models.Role.president
    }:
        return await crud.create_post(db=db, post=post, author=author, type=models.PostType.notice)
    raise HTTPException(
            status_code=403,
            detail="권한이 없습니다."
        )
    
@app.patch("/notices/{no:int}", response_model=models.Post)
async def update_notice(no: int, post: models.PostCreate, db: Session=Depends(get_db)):
    modifier = await auth.get_current_member(db=db, token=post.token)
    if modifier.role in {
        models.Role.board,
        models.Role.president
    }:
        if updated := crud.update_post(db=db, post=post, modifier=modifier, type=models.PostType.notice, no=no):
            return updated
        raise HTTPException(404, "그런 글이 없습니다.")
    raise HTTPException(
            status_code=403,
            detail="권한이 없습니다."
        )

@app.delete("/notices/{no:int}")
async def delete_notice(no: int, token: str, db: Session=Depends(get_db)):
    deleter = await auth.get_current_member(db=db, token=token)
    if deleter.role in {
        models.Role.board,
        models.Role.president
    }:
        if not crud.delete_post(db=db, type=models.PostType.notice, no=no):
            raise HTTPException(404, "그런 글이 없습니다.")
    else:
        raise HTTPException(
            status_code=403,
            detail="권한이 없습니다."
        )

@app.get("/members", response_model=list[models.Member])
async def get_members(skip: int, limit: int, db: Session=Depends(get_db)):
    return crud.get_members(db, skip, limit)

@app.get("/members/{student_id:int}", response_model=models.Member)
async def get_member(student_id: int, db: Session=Depends(get_db)):
    db_member = crud.get_member(db, student_id)
    if db_member is None:
        raise HTTPException(404, "가입되지 않은 학번입니다.")
    return db_member

@app.patch("/members/{student_id:int}", response_model=models.Member)
async def update_member(student_id: int, token: str, member: models.MemberModify, db: Session=Depends(get_db)):
    author = await auth.get_current_member(db=db, token=token)
    if author.role in {
        models.Role.board,
        models.Role.president
    }:
        return await crud.update_member(db=db, student_id=student_id, member=member)

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

@app.post("/register", response_model=models.Member)
async def register(form: RegisterForm, db: Session=Depends(get_db)):
    password_pattern = "^(?=.*[0-9])(?=.*[a-zA-Z]).{10,}$"
    if str(form.portal_id)[4]!="1":
        raise HTTPException(
            status_code=403,
            detail="신촌캠만 가입할 수 있습니다."
        )
    if not re.match(password_pattern, form.password):
        raise HTTPException(
            status_code=403,
            detail="비밀번호가 안전하지 않습니다."
        )
    if crud.get_member_by_username(db=db, username=form.username):
        raise HTTPException(
            status_code=400,
            detail="이미 있는 ID입니다."
        )
    if not auth.is_yonsei_member(int(form.portal_id), form.portal_pw):
        raise HTTPException(
            status_code=403,
            detail="해당 ID와 비밀번호로 연세포탈에 로그인할 수 없습니다."
        )
    if crud.get_member(db=db, student_id=form.portal_id):
        raise HTTPException(
            status_code=400,
            detail="이미 이 학번으로 가입된 계정이 있습니다."
        )
    return crud.create_member(
        db=db,
        student_id=form.portal_id,
        member=models.MemberCreate(
            real_name=form.real_name,
            username=form.username,
            password=form.password
        )
    )

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    member = auth.authenticate(db, form.username, form.password)
    if not member:
        raise HTTPException(
            status_code=401,
            detail="ID나 비밀번호가 틀렸습니다.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": member.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}