from functools import cache

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..settings import get_settings
from .model import get_db_metadata

settings = get_settings()


def engine(read_only: bool):
    return create_engine(
        settings.db_uri(read_only=read_only), future=True, pool_pre_ping=True
    )


@cache
def _get_session(read_only: bool):
    return sessionmaker(autoflush=True, future=True, bind=engine(read_only=read_only))


def get_db(read_only: bool) -> Session:
    return _get_session(read_only=read_only)()


def create_db():
    metadata = get_db_metadata()
    metadata.create_all(bind=engine(read_only=False))  # type: ignore


def drop_db():
    metadata = get_db_metadata()
    metadata.drop_all(bind=engine(read_only=False))  # type: ignore
