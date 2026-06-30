import json

from app.core.redis import redis_client
from app.core.logger import logger


class RedisMemoryService:

    async def get_history(
        self,
        session_id: str,
    ):

        data = await redis_client.get(
            f"chat:{session_id}"
        )

        if not data:
            return []

        return json.loads(data)


    async def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ):

        history = await self.get_history(
            session_id
        )

        history.append(
            {
                "role": role,
                "content": content,
            }
        )

        # Keep only the latest 20 messages
        history = history[-20:]

        await redis_client.set(
            f"chat:{session_id}",
            json.dumps(history),
            ex=1800,   # 30 minutes
        )

        logger.info(
            "memory_updated",
            session_id=session_id,
            total_messages=len(history),
        )


    async def clear_history(
        self,
        session_id: str,
    ):

        await redis_client.delete(
            f"chat:{session_id}"
        )

        logger.info(
            "memory_cleared",
            session_id=session_id,
        )


    async def get_summary(
    self,
    session_id: str,
    ):

        return await redis_client.get(
            f"summary:{session_id}"
        )


    async def save_summary(
        self,
        session_id: str,
        summary: str,
    ):

        await redis_client.set(
            f"summary:{session_id}",
            summary,
            ex=1800,
        )