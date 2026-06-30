from app.services.memory.redis_memory_service import (
    RedisMemoryService,
)
from app.services.llm.gemini_service import GeminiService
from app.core.logger import logger
from app.services.tools.tool_executor import (
    tool_executor,
)


class AIService:

    def __init__(self):

        self.gemini = GeminiService()
        self.memory = RedisMemoryService()


    async def generate_response(
        self,
        session_id: str,
        message: str,
    ):

        # Save user's message
        await self.memory.add_message(
            session_id,
            "user",
            message,
        )

        # Get conversation history
        history = await self.memory.get_history(
            session_id
        )

        summary = await self.memory.get_summary(
            session_id
        )

        logger.info(
            "conversation_history",
            history=history,
        )

        try:

            logger.info("calling gemini")

            # Ask Gemini using history
            messages = []

            if summary:

                messages.append(
                    {
                        "role": "system",
                        "content": f"""
            Conversation Summary:

            {summary}
            """
                    }
                )

            messages.extend(history)

            logger.info("before_gemini")

            answer = await self.gemini.generate_response(
                messages
            )

            logger.info(
                "after_gemini",
                answer=answer,
            )

            tool_result = await tool_executor.execute(
                answer
            )

            logger.info(
                "after_tool_executor",
                result=tool_result,
            )

            if tool_result:

                answer = await self.gemini.generate_confirmation(tool_result)

            logger.info("gemini finished ")
        
        except Exception as e:
            logger.exception("gemini error",error=str(e))
            raise 

        # Save AI response
        await self.memory.add_message(
            session_id,
            "assistant",
            answer,
        )

        history = await self.memory.get_history(
            session_id
        )

        if len(history) > 10:

            summary = await self.gemini.summarize(
                history[:-6]
            )

            await self.memory.save_summary(
                session_id,
                summary,
            )



        return {
            "session_id": session_id,
            "user_message": message,
            "answer": answer,
            "tool_result":tool_result
        }


ai_service = AIService()