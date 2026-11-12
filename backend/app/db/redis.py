
from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.core.config import settings


class RedisDB:
    client: Redis | None = None

    @classmethod
    async def connect(cls) -> None:
        if cls.client is not None:
            return

        client = Redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            health_check_interval=30,
        )

        try:
            await client.ping()
        except RedisError:
            await client.aclose()
            raise

        cls.client = client
        print("Redis connection established.")

    @classmethod
    async def close(cls) -> None:
        if cls.client is not None:
            await cls.client.aclose()
            cls.client = None
            print("Redis connection closed.")

    @classmethod
    def get_client(cls) -> Redis:
        if cls.client is None:
            raise RuntimeError("Redis is not connected.")

        return cls.client
