import asyncio
import pathlib
from datetime import datetime, timedelta
from uuid import UUID
import swiftclient
from keystoneauth1 import session
from keystoneauth1.identity import v3
from database import SessionLocal
from settings import get_settings
from main import get_uploaded_file_info

endpoint = "https://kr.archive.ncloudstorage.com:5000/v3"
settings = get_settings()
username = settings.ncloud_access_key
password = settings.ncloud_secret_key
domain_id = settings.ncloud_archive_storage_domain_id
project_id = settings.ncloud_archive_storage_project_id
container_name = "yonseimunhak"
auth = v3.Password(
    auth_url=endpoint,
    username=username,
    password=password,
    project_id=project_id,
    user_domain_id=domain_id,
)
auth_session = session.Session(auth=auth)
swift_connection = swiftclient.Connection(retries=5, session=auth_session)


async def backup_file(file_name: UUID | str, directory: str, db, is_db=False):
    with open(
        "sql/YoonDong-ju.db" if is_db else f"uploaded/{file_name}",
        mode="rb",
    ) as f:
        if not is_db:
            file_info = await get_uploaded_file_info(uuid=file_name, db=db)
            if file_info is None:
                return
        swift_connection.put_object(
            container_name,
            directory + "/" + (file_name if is_db else file_info.name),
            contents=f.read(),
            content_type="application/x-sqlite3" if is_db else file_info.content_type,
        )


def create_directory(today: datetime):
    directory = today.strftime("%Y-%m-%d %H:%M:%S")
    swift_connection.put_object(
        container_name,
        directory,
        contents="",
        content_type="application/directory",
        headers={"X-Delete-After": timedelta(days=30).seconds},  # 30일까지만 보관
    )
    return directory


async def backup_all_uploaded_files(directory: str, db=SessionLocal()):
    await asyncio.gather(
        *[
            backup_file(file.name, directory, db)
            for file in {
                x for x in pathlib.Path("uploaded").glob("**/*") if x.is_file()
            }
        ]
    )


async def backup_database(directory: str):
    await backup_file("YoonDong-ju.db", directory=directory, db=None, is_db=True)


async def backup():
    directory = create_directory(datetime.today())
    await asyncio.gather(
        *[backup_database(directory), backup_all_uploaded_files(directory)]
    )


asyncio.run(backup())
