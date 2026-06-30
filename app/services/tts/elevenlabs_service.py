from app.core.logger import logger
import httpx

from app.core.config import settings


VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"


class ElevenLabsService:

    async def generate_audio(
        self,
        text: str,
    ) -> bytes:

        url = (
            f"https://api.elevenlabs.io/v1/text-to-speech/"
            f"{VOICE_ID}"
        )

        headers = {
            "xi-api-key": settings.ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
        }

        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
        }

        async with httpx.AsyncClient() as client:
            
            logger.info("calling eleven labs")

            response = await client.post(
                url,
                headers=headers,
                json=payload,
            )

            logger.info("elevenlabs finished")
            
            response.raise_for_status()

            return response.content



elevenlabs_service = ElevenLabsService()