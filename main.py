from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database.config import settings
from database.session import engine   #new
from database.base_class import Base  #new
from router import user,teamidea

app = FastAPI()

Base.metadata.create_all(bind=engine)

#cors 
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(teamidea.router)