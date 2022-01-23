import uuid
import sqlite3
import pytz
import math
import flask
from pathlib import Path
from datetime import datetime
from typing import Optional, Union
from marko.ext.gfm import gfm
from flask import abort, redirect, flash, send_from_directory, request
from flask import current_app as app
from werkzeug.datastructures import FileStorage

NOT_FOUND = 404

class UnableToSaveFile(Exception):
    """파일을 저장할 수 없는 오류."""

def render_template(template_name_or_list: str, **context):
    # layout에 들어갈 데이터를 항상 주도록 커스터마이징
    layout_data = {
        "location": "대강당 109호",
        "email": "roompennoyeah@gmail.com",
        "president-name": "서혜빈",
        "president-tel": "010-5797-4309"
    } # TODO: 하드코딩 제거
    return flask.render_template(
        template_name_or_list,
        datetime=datetime,
        layout_data=layout_data,
        gfm=gfm,
        **context
    )

def index() -> str:
    """첫 화면."""
    with sqlite3.connect(f"sql/notices.db") as DB:
        query = f"SELECT no, title, published FROM notices ORDER BY no DESC LIMIT 4"
        fetched = DB.execute(query).fetchall()
        recent_notices = [{col_name:row[i] for i, col_name in enumerate(("no", "title", "published"))} for row in fetched]
        return render_template("index.html", recent_notices=recent_notices, len=len)

def about() -> str:
    """소개 화면."""
    with sqlite3.connect(f"sql/special_posts.db") as DB:
        query = f"SELECT title, content FROM special_posts WHERE title=='about'"
        title, content = DB.execute(query).fetchone()
        data = {"title": title, "content": content}
        return render_template("about.html", categories={"소개":"about"}, data=data)

def upload(file: FileStorage):
    """파일을 `app.config["UPLOAD_DIR"]`에 저장하고 파일 이름을 반환합니다.
    해당 디렉터리가 없다면 디렉터리도 생성합니다.
    파일 이름은 `uuid.uuid4()`로 생성된 무작위 `UUID`로 변경됩니다.
    확장자는 그대로 남습니다.
    이 함수는 파일 이름에 `.`가 있음을 전제합니다.

    Raises:
        `UnableToSaveFile`: 1000번 시도했는데도 `UUID`가 겹쳐서 저장을 못한 경우.
    """
    # werkzeug.utils.secure_filename()는 사용하지 않는데,
    # 한글을 못 받기 때문입니다.
    upload_dir = Path(app.config["UPLOAD_DIR"])
    upload_dir.mkdir(exist_ok=True)
    for _ in range(1000):
        extension = file.filename.split(".")[-1]
        name = Path(str(uuid.uuid4())+"."+extension)
        at = upload_dir / name
        if not at.exists():
            file.save(at)
            return at.name
    raise UnableToSaveFile("Can't get any unique name with uuid.uuid4()")

def write_notice(no: int=None) -> Union[str, redirect]:
    if request.method == "GET":
        if no is None:
            return render_template("write.html", categories={"공지":"notices"}, editing=False)
        with sqlite3.connect(f"sql/notices.db") as DB:
            query = f"SELECT no, title, content, published, attached FROM notices WHERE no=?"
            fetched = DB.execute(query, [no]).fetchone()
            if fetched is None: # no번째 공지가 없음.
                abort(NOT_FOUND)
            data = {key: fetched[i] for i, key in enumerate(("no", "title", "content", "published", "attached"))}
            return render_template("write.html", categories={"공지":"notices"}, this_is="공지", data=data, editing=True)
    elif request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        author = "sample author"
        published = datetime.now(pytz.timezone("Asia/Seoul")).date()
        attached = request.files["attached"]
        # NOTE: <form> 태그에 enctype="multipart/form-data"가 설정되지 않으면
        # 파일을 받을 수 없습니다.
        try:
            if attached.filename:
                attached = str(upload(attached))
            else:
                attached = None
            with sqlite3.connect("sql/notices.db") as DB:
                query = """
                INSERT INTO notices
                (title, content, author, published, attached)
                values (?, ?, ?, ?, ?)
                """
                DB.execute(query, [title, content, author, published, attached])
                no = DB.execute("SELECT no FROM notices order by no desc limit 1").fetchone()[0]
                return redirect(f"/notices/{no}")
        except:
            app.logger.exception("Exception publishing notice")
            # flash("Failed")
            return redirect(request.url)

def delete_notice(no: int):
    pass

def download(name: str):
    return send_from_directory(app.config["UPLOAD_DIR"], name)

def notices(no: Optional[int]=None) -> str:
    """`no`번째 공지를 열람합니다. `no==None`이면 공지 목록을 봅니다."""
    # NOTE: sqlite3 라이브러리는 parameter substitution을
    # table name에는 지원하지 않습니다.
    # 참고: https://stackoverflow.com/questions/39196462/how-to-use-variable-for-sqlite-table-name
    NAME = notices.__name__
    with sqlite3.connect(f"sql/{NAME}.db") as DB:
        if no is not None:
            query = f"SELECT no, title, content, author, published, attached FROM {NAME} WHERE no=?"
            fetched = DB.execute(query, [no]).fetchone()
            if fetched is None: # no번째 공지가 없음.
                abort(NOT_FOUND)
            data = {key: fetched[i] for i, key in enumerate(("no", "title", "content", "author", "published", "attached"))}
            return render_template("post.html", categories={"공지":"notices"}, this_is="공지", data=data)
        else:
            skip = int(request.args.get("skip", 0))
            query = f"SELECT no, title, author, published FROM {NAME} ORDER BY no DESC LIMIT 10 OFFSET ?"
            fetched = DB.execute(query, [skip]).fetchall()
            data = [{col_name:row[i] for i, col_name in enumerate(("no", "title", "author", "published"))} for row in fetched]
            return render_template(
                "list.html",
                categories={"공지":"notices"},
                this_is="공지",
                data=data,
                list_size=DB.execute("SELECT COUNT(0) FROM notices").fetchone()[0],
                skip=skip,
                math=math
            )

def magazines(no: Optional[int]=None) -> str:
    """`no`호 문집 정보를 열람합니다. `no==None`이면 문집 목록을 봅니다."""
    NAME = magazines.__name__
    with sqlite3.connect(f"sql/{NAME}.db") as DB:
        if no is not None:
            query = f"SELECT *FROM {NAME} WHERE no=?"
            fetched = DB.execute(query, [no]).fetchone()
            if fetched is None: # no번째 문집이 없음.
                abort(NOT_FOUND)
            return render_template("magazine.html", fetched=fetched)
        else:
            offset = int(request.args.get("offset", 0))
            query = f"SELECT id, title, author, attached FROM {NAME} ORDER BY no DESC LIMIT 10 OFFSET ?"""
            fetched = DB.execute(query, [NAME, offset*10]).fetchall()
            return render_template("magazine-list.html", fetched=fetched)

def sector(name: Optional[str]=None) -> str:
    """코드가 `name`인 분반 정보를 열람합니다. `name==None`이면 분반 목록을 봅니다.

    `name` 목록:
        시반: `poetry`
        소설반: `novella`
        합평반: `critique`
        독서반: `reading`
    """
    return render_template("sector.html", name=name)

def workspace() -> str:
    """관리자 화면."""