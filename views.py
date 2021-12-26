import uuid
import sqlite3
import pytz
import markdown
from pathlib import Path
from datetime import datetime
from typing import Optional, Union
from flask import render_template, abort, redirect, flash, send_from_directory, request
from flask import current_app as app
from werkzeug.datastructures import FileStorage

NOT_FOUND = 404

class UnableToSaveFile(Exception):
    """파일을 저장할 수 없는 오류."""

def index() -> str:
    """첫 화면."""
    return render_template("index.html")

def about() -> str:
    """소개 화면."""
    return render_template("about.html")

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

def write_notice() -> Union[str, redirect]:
    if request.method == "GET":
        return render_template("notice-write.html")
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
                at = str(upload(attached))
            else:
                at = None
            with sqlite3.connect("sql/notices.db") as DB:
                query = """
                INSERT INTO notices
                (title, content, author, published, attached)
                values (?, ?, ?, ?, ?)
                """
                DB.execute(query, [title, content, author, published, at])
                no = DB.execute("SELECT no FROM notices order by no desc limit 1").fetchone()[0]
                return redirect(f"/notices/{no}")
        except:
            app.logger.exception("Exception publishing notice")
            # flash("Failed")
            return redirect(request.url)

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
            if fetched is None: # id번째 공지가 없음.
                abort(NOT_FOUND)
            data = {key: fetched[i] for i, key in enumerate(("no", "title", "content", "author", "published", "attached"))}
            return render_template("notice.html", data=data, markdown=markdown.markdown)
        else:
            offset = int(request.args.get("offset", 0))
            query = f"SELECT no, title, author, published FROM {NAME} ORDER BY no DESC LIMIT 10 OFFSET ?"
            fetched = DB.execute(query, [offset*10]).fetchall()
            data = [{col_name:row[i] for i, col_name in enumerate(("no", "title", "author", "published"))} for row in fetched]
            return render_template("notices.html", data=data, markdown=markdown.markdown)

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