from sqlalchemy import create_engine
from sqlalchemy.orm import joinedload, sessionmaker

from core.config import settings
from typing import Generator

# This is for Postges
# SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
# engine = create_engine(SQLALCHEMY_DATABASE_URL)


# IF you don't want to install Postgres then use SqlLite, a file based system

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread" : False}
)


SessionLocal = sessionmaker(autocommit = False,autoflush = False,bind = engine)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
