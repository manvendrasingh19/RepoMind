
from qdrant_client import AsyncQdrantClient

from app.core.config import settings


class QdrantDB:
    client: AsyncQdrantClient | None = None

    @classmethod
    async def connect(cls) -> None:
        if cls.client is not None:
            return

        client = AsyncQdrantClient(
            url=settings.qdrant_url,
            timeout=5,
        )

        try:
            await client.get_collections()
        except Exception:
            await client.close()
            raise

        cls.client = client
        print("Qdrant connection established.")

    @classmethod
    async def close(cls) -> None:
        if cls.client is not None:
            await cls.client.close()
            cls.client = None
            print("Qdrant connection closed.")

    @classmethod
    def get_client(cls) -> AsyncQdrantClient:
        if cls.client is None:
            raise RuntimeError("Qdrant is not connected.")

        return cls.client
