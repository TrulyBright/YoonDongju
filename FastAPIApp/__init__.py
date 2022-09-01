import fastapi
from FastAPIApp import schemas
from FastAPIApp import database

app = fastapi.FastAPI()

schemas.Base.metadata.create_all(bind=database.engine)
