import uuid
import time
from flask_login import current_user, login_required, login_user, logout_user
import httpx
import sqlite3
import pytz
import math
import flask
import auth
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
    if not hasattr(current_user, "is_mod"):
        current_user.is_mod = lambda: False
    return flask.render_template(
        template_name_or_list,
        datetime=datetime,
        layout_data=layout_data,
        current_user=current_user,
        gfm=gfm,
        **context
    )

def index():
    """첫 화면."""
    with sqlite3.connect(f"sql/posts.db") as DB:
        query = f"SELECT no, title, published FROM posts WHERE type='notice' ORDER BY no DESC LIMIT 4"
        fetched = DB.execute(query).fetchall()
        recent_notices = [{col_name:row[i] for i, col_name in enumerate(("no", "title", "published"))} for row in fetched]
        return render_template("index.html", recent_notices=recent_notices, len=len)

def about():
    """소개 화면."""
    with sqlite3.connect(f"sql/posts.db") as DB:
        query = f"SELECT title, author, published, content FROM posts WHERE type='about'"
        fetched = DB.execute(query).fetchone()
        if fetched is None:
            data = {"content": "소개가 없습니다. 우상단 '글쓰기'를 눌러 소개문을 쓸 수 있습니다."}
        else:
            title, author, published, content = fetched
            data = {"title": title, "author": author, "published": published, "content": content}
        return render_template("about.html", categories={"소개":"about"}, data=data, nonexistent=fetched is None)

@login_required
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

@login_required
def write_post(no: int=None):
    editing = request.path.endswith("/edit")
    editing_about = request.path.startswith("/about")
    if request.method == "GET":
        if not editing_about and no is None:
            return render_template("write.html", categories={"공지":"notices"}, this_is="공지", editing=False)
        with sqlite3.connect(f"sql/posts.db") as DB:
            condition = "type='about'" if editing_about else "type='notice' and no=?"
            query = f"SELECT no, title, content, published, attached FROM posts WHERE {condition}"
            fetched = DB.execute(query, [] if editing_about else [no]).fetchone()
            if not editing_about and fetched is None: # no번째 공지가 없음.
                abort(NOT_FOUND)
            data = dict() if fetched is None else {key: fetched[i] for i, key in enumerate(("no", "title", "content", "published", "attached"))}
            return render_template(
                "write.html",
                categories={"소개":"about"} if editing_about else {"공지":"notices"},
                this_is="소개" if editing_about else "공지",
                data=data,
                editing=fetched is not None
            )
    elif request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        author = "sample author" # TODO
        published = datetime.now(pytz.timezone("Asia/Seoul")).date()
        attached = request.files["attached"]
        # NOTE: <form> 태그에 enctype="multipart/form-data"가 붙지 않으면
        # 파일을 받을 수 없습니다.
        if attached.filename:
            attached = str(upload(attached))
        else:
            attached = None
        with sqlite3.connect("sql/posts.db") as DB:
            condition = "type='about'" if editing_about else "type='notice' and no=?"
            query = f"""
            UPDATE posts
            SET title=?,
                content=?,
                author=?,
                published=?,
                attached=?
            WHERE {condition}
            """ if editing else """
            INSERT INTO posts
            (type, title, content, author, published, attached)
            values (?, ?, ?, ?, ?, ?)
            """
            if editing:
                DB.execute(query, [title, content, author, published, attached] if editing_about else [title, content, author, published, attached, no])
            else:
                cursor = DB.execute(query, ["about" if editing_about else "notice", title, content, author, published, attached])
            return redirect("/about" if editing_about else f"/notices/{no if editing else cursor.lastrowid}")

@login_required
def delete_post(no: int): # TODO: 권한
    with sqlite3.connect("sql/posts.db") as DB:
        query = """
        DELETE FROM posts
        WHERE no=?
        """
        DB.execute(query, [no])
        return "meaningless dummy value" # 의미없이 그냥 리턴하는 값.

def notices(no: Optional[int]=None):
    """`no`번째 공지를 열람합니다. `no==None`이면 공지 목록을 봅니다."""
    with sqlite3.connect(f"sql/posts.db") as DB:
        if no is not None:
            query = f"SELECT no, title, content, author, published, attached FROM posts WHERE no=? and type='notice'"
            fetched = DB.execute(query, [no]).fetchone()
            if fetched is None: # no번째 공지가 없음.
                abort(NOT_FOUND)
            data = {key: fetched[i] for i, key in enumerate(("no", "title", "content", "author", "published", "attached"))}
            return render_template("post.html", categories={"공지":"notices"}, this_is="공지", data=data)
        else:
            skip = int(request.args.get("skip", 0))
            query = f"SELECT no, title, author, published FROM posts WHERE type='notice' ORDER BY no DESC LIMIT 10 OFFSET ?"
            fetched = DB.execute(query, [skip]).fetchall()
            data = [{col_name:row[i] for i, col_name in enumerate(("no", "title", "author", "published"))} for row in fetched]
            return render_template(
                "list.html",
                categories={"공지":"notices"},
                this_is="공지",
                data=data,
                list_size=DB.execute("SELECT COUNT(0) FROM posts").fetchone()[0],
                skip=skip,
                math=math
            )

def magazines():
    with sqlite3.connect(f"sql/magazines.db") as DB, sqlite3.connect("sql/contents-per-magazines.db") as contentsDB:
        query = f"SELECT no, year, season, published, cover FROM magazines ORDER BY no DESC"""
        fetched = DB.execute(query).fetchall()
        data = [{col:row[i] for i, col in enumerate(("no", "year", "season", "published", "cover"))} for row in fetched]
        for volume in data:
            query = f"""
            SELECT type, author, title, language
            FROM "{volume["no"]}"
            """
            volume["contents"] = [{col:row[i] for i, col in enumerate(("type", "author", "title", "language"))} for row in contentsDB.execute(query).fetchall()]
        return render_template("magazines.html", data=data, range=range)

@login_required
def write_magazine(no: int=None):
    editing = request.path.endswith("/edit")
    with sqlite3.connect("sql/magazines.db") as DB, sqlite3.connect("sql/contents-per-magazines.db") as contentsDB:
        if request.method == "GET":
            return render_template("write-magazine.html")
        elif request.method == "POST":
            year = request.form["year"]
            season = {"sangbangi":1, "habangi": 2}[request.form["season"]]
            published = request.form["published"]
            cover = str(upload(request.files["cover"]))
            types = [type for key, type in request.form.items() if key.endswith("type")]
            authors = [author for key, author in request.form.items() if key.endswith("author")]
            titles = [title for key, title in request.form.items() if key.endswith("title")]
            languages = [language for key, language in request.form.items() if key.endswith("language")]
            contents = [[types[i], authors[i], titles[i], languages[i]] for i in range(len(authors))]
            query = f"""
            UPDATE magazines
            SET year=?,
                season=?,
                published=?,
                cover=?
            WHERE no=?
            """ if editing else """
            INSERT INTO magazines
            (year, season, published, cover)
            VALUES (?, ?, ?, ?)
            """
            if editing:
                DB.execute(query, [year, season, published, cover, no])
            else:
                cursor = DB.execute(query, [year, season, published, cover])
            if editing:
                query = f"""
                DROP TABLE IF EXISTS {no}
                """
                contentsDB.execute(query)
            query = f"""
            CREATE TABLE "{no if editing else DB.execute(f"SELECT COUNT(0) FROM magazines").fetchone()[0]}" (
                type text not null,
                author text not null,
                title text not null,
                language text not null
            )
            """
            contentsDB.execute(query)
            for c in contents:
                query = f"""
                INSERT INTO "{no if editing else DB.execute(f"SELECT COUNT(0) FROM magazines").fetchone()[0]}"
                (type, author, title, language)
                VALUES ({", ".join(["?"]*len(c))})
                """
                print(query)
                contentsDB.execute(query, c)
            return redirect(f"/magazines#vol{no if editing else cursor.lastrowid}")

def classes(name: Optional[str]=None, no: Optional[int]=None):
    """코드가 `name`인 분반의 no번째 활동 기록을 봅니다.
    `no==None`이면 코드가 `name`인 분반의 활동 목록을 봅니다.
    `name`도 `None`이면 분반 목록을 봅니다.
    """
    # TODO: 하드코딩 제거
    categories = {"시반": "poetry", "소설반": "novel", "합평반": "critique", "독서반": "reading"}
    description = {
        "시반": "시를 씁니다.",
        "소설반": "소설을 씁니다.",
        "합평반": "회원이 쓴 작품을 합평합니다. 회원들이 평을 하는 동안 작가는 단 한 마디도 할 수 없습니다.",
        "독서반": "기성 작가가 쓴 작품을 읽고 감상을 나눕니다.",
    }
    moderator = {
        "시반": "이상명",
        "소설반": "이주한",
        "합평반": "석범진",
        "독서반": "이진명",
    }
    schedule = {
        "시반": "모요일 모 시",
        "소설반": "모요일 모 시",
        "합평반": "모요일 모 시",
        "독서반": "모요일 모 시",
    }
    if name is None:
        return render_template(
            "classes.html",
            categories=categories,
            description=description,
            moderator=moderator,
            schedule=schedule,
        )
    with sqlite3.connect("sql/class-archive.db") as DB, sqlite3.connect(f"sql/participants-{name}.db") as participantsDB:
        if no is None:
            skip = int(request.args.get("skip", 0))
            query = f"""
            SELECT
                no,
                moderator,
                conducted,
                topic
            FROM {name}
            ORDER BY no
            DESC
            LIMIT 10
            OFFSET ?
            """
            fetched = DB.execute(query, [skip]).fetchall()
            data = [{
                col_name:row[i]
                for i, col_name
                in enumerate(("no", "moderator", "conducted", "topic"))
                } for row in fetched
            ]
            for row in data:
                row["number_of_participants"] = participantsDB.execute(f"SELECT COUNt(0) FROM '{row['no']}'").fetchone()[0]
            return render_template(
                "class-list.html",
                categories=categories,
                this_is={value:key for key, value in categories.items()}[name],
                data=data,
                list_size=DB.execute(f"SELECT COUNT(0) FROM {name}").fetchone()[0],
                skip=skip,
                math=math
            )
        query = f"""
        SELECT no, moderator, conducted, topic, content, hide_participants
        FROM {name}
        WHERE no=?
        """
        row = DB.execute(query, [no]).fetchone()
        if row is None:
            abort(NOT_FOUND)
        query = f"""
        SELECT name from "{no}"
        """
        participants = [row[0] for row in participantsDB.execute(query).fetchall()]
        data = {col_name:row[i] for i, col_name in enumerate(["no", "moderator", "conducted", "topic", "content", "hide_participants"])}
        if data["hide_participants"]:
            pass # TODO: 임원진에게만 보이도록
        data["participants"] = participants
        return render_template("class-activity-post.html", categories=categories, data=data, this_is={value:key for key, value in categories.items()}[name])

@login_required
def write_class_activity(name: str, no: Optional[int]=None):
    editing = request.path.endswith("/edit")
    categories = {"시반": "poetry", "소설반": "novel", "합평반": "critique", "독서반": "reading"}
    if request.method == "GET":
        if editing:
            with sqlite3.connect(f"sql/class-archive.db") as DB, sqlite3.connect(f"sql/participants-{name}.db") as participantsDB:
                query = f"""
                SELECT no, moderator, conducted, topic, content
                FROM {name}
                WHERE no=?
                """
                fetched = DB.execute(query, [no]).fetchone()
                if fetched is None:
                    abort(NOT_FOUND)
                data = {key:fetched[i] for i, key in enumerate(("no", "moderator", "conducted", "topic", "content"))}
                query = f"""
                SELECT name
                FROM "{no}"
                """
                data["participants"] = [row[0] for row in participantsDB.execute(query).fetchall()]
                return render_template(
                    "write.html",
                    categories=categories,
                    this_is={value:key for key, value in categories.items()}[name],
                    data=data,
                    editing=editing,
                    for_class_activity=True,
                    enumerate=enumerate
                )
        return render_template("write.html", categories=categories, this_is={value:key for key, value in categories.items()}[name], editing=False, for_class_activity=True)
    elif request.method == "POST":
        topic = request.form["topic"]
        conducted = request.form["conducted"]
        content = request.form["content"]
        participants = [participant_name for form_name, participant_name in request.form.items() if form_name.startswith("participant")]
        hide_participants = bool(int(request.form["hide-participants"]))
        with sqlite3.connect("sql/class-archive.db") as DB, sqlite3.connect(f"sql/participants-{name}.db") as participantsDB:
            query = f"""
            UPDATE {name}
            SET topic=?,
                conducted=?,
                content=?,
                hide_participants=?
            WHERE no=?
            """ if editing else f"""
            INSERT INTO {name}
            (topic, conducted, content, moderator, hide_participants)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor = DB.execute(query, [topic, conducted, content, no, hide_participants] if editing else [topic, conducted, content, "sample moderator", hide_participants])
            if editing:
                query = f"""
                DROP TABLE IF EXISTS "{no}"
                """
                participantsDB.execute(query)
            query = f"""
            CREATE TABLE "{no if editing else DB.execute(f"SELECT COUNT(0) FROM {name}").fetchone()[0]}" (
                name text not null -- TODO: 학번으로 대체? 그러나 분반장이 회원에게 학번을 물어봐야 하는 번거로움이 있음.
            )
            """
            participantsDB.execute(query)
            query = f"""
            INSERT INTO "{no if editing else DB.execute(f"SELECT COUNT(0) FROM {name}").fetchone()[0]}" (name)
            VALUES {", ".join(["(?)"]*len(participants))}
            """
            participantsDB.execute(query, participants)
            return redirect(f"/classes/{name}/{no if editing else cursor.lastrowid}")

@login_required
def delete_class_activity(name: str, no: int):
    with sqlite3.connect("sql/class-archive.db") as DB, sqlite3.connect(f"sql/participants-{name}.db") as participantsDB:
        DB.execute(f"DELETE FROM {name} WHERE no=?", [no])
        participantsDB.execute(f"DROP TABLE '{no}'")
        return "meaningless dummy value"

def workspace():
    """관리자 화면."""
    return render_template("workspace.html")

def uploaded(filename: str):
    return send_from_directory(app.config["UPLOAD_DIR"], filename)

def rules():
    with sqlite3.connect(f"sql/posts.db") as DB:
        query = f"SELECT title, author, published, content FROM posts WHERE type='rules'"
        fetched = DB.execute(query).fetchone()
        if fetched is None:
            data = {"content": "회칙이 없습니다. 우상단 '글쓰기'를 눌러 회칙을 기재할 수 있습니다."}
        else:
            title, author, published, content = fetched
            data = {"title": title, "author": author, "published": published, "content": content}
        return render_template("rules.html", categories={"회칙":"rules"}, data=data, nonexistent=fetched is None)

@login_required
def write_rules():
    editing = request.path.endswith("/edit")
    if request.method == "GET":
        with sqlite3.connect("sql/posts.db") as DB:
            query = "SELECT title, content, published FROM posts WHERE type='rules'"
            fetched = DB.execute(query).fetchone()
            data = dict() if fetched is None else {key:fetched[i] for i, key in enumerate(("title", "content", "published"))}
            return render_template("write-rules.html", categories={"회칙":"rules"}, this_is="회칙", data=data, editing=fetched is not None)
    elif request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        author = "sample author"
        published = datetime.now(pytz.timezone("Asia/Seoul")).date()
        with sqlite3.connect("sql/posts.db") as DB:
            query = """
            UPDATE posts
            SET title=?,
                content=?,
                author=?,
                published=?
            WHERE type='rules'
            """ if editing else """
            INSERT INTO posts
            (type, title, content, author, published)
            VALUES (?, ?, ?, ?, ?)
            """
            DB.execute(query, [title, content, author, published] if editing else ["rules", title, content, author, published])
            return redirect("/rules")

def register():
    id = request.form["id"]
    pw = request.form["pw"]
    with sqlite3.connect("users.db") as DB:
        query = """
        INSERT INTO users (id, username, password, role)
        VALUES (?, ?, ?, ?)
        """
        now = int(time.time())
        print(now)
        DB.execute(query, [now, id, pw, "user"])
        flask.flash("사이트 회원으로 가입됐습니다. 로그인해주세요.")
        return redirect("/")

def login():
    username = request.form["username"]
    password = request.form["password"]
    with sqlite3.connect("sql/users.db") as DB:
        query = """
        SELECT id, username, role, password FROM users WHERE username=?
        """
        fetched = DB.execute(query, [username]).fetchone()
        if fetched is None:
            pass
        elif fetched[3] != password:
            pass
        else:
            login_user(auth.User(fetched[0], fetched[1], fetched[2]))
            flask.flash(f"{fetched[1]}님 환영합니다.")
            return redirect(request.referrer)

@login_required
def logout():
    logout_user()
    flask.flash("무사히 로그아웃되었습니다.")
    return redirect("/")