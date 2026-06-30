from app.graph.workflow import graph
from app.core.logger import logger
from app.services.tts.elevenlabs_service import (elevenlabs_service)
from app.services.ai.ai_service import ai_service


class ConversationService:

    def __init__(self):

        self.tts = elevenlabs_service
        self.ai = ai_service



    async def process_message(
        self,
        session_id: str,
        message: str,
    ):
        logger.info("conversation_service_started")

        try:

            result = await self.ai.generate_response(
                session_id,
                message,
            )

            audio = await self.tts.generate_audio(
                result["answer"]
            )

            logger.info(
                "graph_response",
                response=result,
            )

            return result,audio
        
        except Exception as e:

            logger.exception("conversation_service_error",error=str(e))
            raise



conversation_service = ConversationService()