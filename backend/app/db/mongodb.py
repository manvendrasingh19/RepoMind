
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import settings


class MongoDB:
    client: AsyncMongoClient | None = None
    database: AsyncDatabase | None = None

    @classmethod
    async def connect(cls) -> None:
        if cls.client is not None:
            return

        client = AsyncMongoClient(
            settings.mongodb_uri,
            serverSelectionTimeoutMS=5000,
            maxPoolSize=50,
            minPoolSize=5,
        )

        try:
            await client.admin.command("ping")
        except Exception:
            await client.close()
            raise

        cls.client = client
        cls.database = client[settings.mongodb_database]

        print("MongoDB connection established.")

    @classmethod
    async def close(cls) -> None:
        if cls.client is not None:
            await cls.client.close()
            cls.client = None
            cls.database = None

            print("MongoDB connection closed.")

    @classmethod
    def get_database(cls) -> AsyncDatabase:
        if cls.database is None:
            raise RuntimeError("MongoDB is not connected.")

        return cls.database
