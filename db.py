import sqlite3
from pathlib import Path

query = {
    "posts": """
        CREATE TABLE IF NOT EXISTS posts (
            no integer not null primary key,
            type text default null,
            title text not null,
            author integer not null,
            content text not null,
            published date not null, 
            attached text -- 파일 이름입니다.
        )
    """,
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            id integer not null primary key unique, -- 학번입니다.
            username text not null unique,
            real_name text not null,
            password text not null,
            role text not null
        )
    """,
    "class-archive": [
        f"""
        CREATE TABLE IF NOT EXISTS {name} (
            no integer not null primary key,
            moderator text not null,
            conducted date not null,
            topic text not null,
            content text not null,
            hide_participants bool not null
        )
        """ for name in {"poetry", "novel", "critique", "reading"}],
    "magazines": """
        CREATE TABLE IF NOT EXISTS magazines (
            no integer not null primary key,
            year integer not null,
            season text not null,
            cover text not null,
            published date not null
        )
    """,
    "clubInfo": """
        CREATE TABLE IF NOT EXISTS clubInfo (
            location text not null ,
            email text not null,
            president_name text not null,
            president_tel text not null
        );
    """
}

def initalize():
    global query
    Path("sql").mkdir(exist_ok=True)
    for name, query in query.items():
        with sqlite3.connect(f"sql/{name}.db") as DB:
            for q in query if isinstance(query, list) else [query]:
                DB.execute(q)