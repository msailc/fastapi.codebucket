from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database.config import settings
from database.session import engine   #new
from database.base_class import Base  #new
from router import user

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)