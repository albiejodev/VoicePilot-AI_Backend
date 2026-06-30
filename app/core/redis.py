from redis.asyncio import Redis

from app.core.config import settings
from app.core.logger import logger


redis_client = Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)