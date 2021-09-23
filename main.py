from fastapi import FastAPI
from core.config import Settings

from db.session import engine
from db.base import Base

from apis.base import api_router


def create_tables():
    Base.metadata.create_all(bind=engine)   

def include_router(app):
    app.include_router(api_router)


def start_application():
    app = FastAPI(title=Settings.PROJECT_NAME,version=Settings.PROJECT_VERSION)
    create_tables()
    include_router(app)
    return app



app = start_application()


@app.get("/")
def hello_api():
    return{"detail":"Hello world"}