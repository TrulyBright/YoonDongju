from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy.event as sqlevent
from pathlib import Path

Path("sql").mkdir(exist_ok=True)
SQLALCHEMY_DATEBASE_URL = "sqlite:///./sql/YoonDong-ju.db"
engine = create_engine(
    SQLALCHEMY_DATEBASE_URL, connect_args={"check_same_thread": False}
)
sqlevent.listen(engine, "connect", lambda conn,
                rec: conn.execute("PRAGMA foreign_keys=ON;"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
