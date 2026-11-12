from collections.abc import Generator

from pymongo.asynchronous.database import AsyncDatabase

from app.db.mongodb import MongoDB


def get_database() -> Generator[AsyncDatabase, None, None]:
    yield MongoDB.get_database()