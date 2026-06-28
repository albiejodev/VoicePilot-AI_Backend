from fastapi import (APIRouter,WebSocket,WebSocketDisconnect)
from app.core.logger import logger
from app.graph.workflow import graph
import time
from app.services.connection_manager import manager
from app.core.metrics import (
    GRAPH_EXECUTIONS,
    GRAPH_EXECUTION_TIME,
    MESSAGES_RECEIVED,
    MESSAGES_SENT
)
import json
from app.services.stt.deepgram_service import DeepgramService
from app.utils.audio import decode_base64_audio 


router = APIRouter()




@router.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id:str
):
    await manager.connect(
        session_id,
        websocket
    )

    async def process_transcript(
    transcript: str
    ):
        logger.info(
            "processing_transcript",
            transcript=transcript
        )

        result = graph.invoke(
            {
                "session_id": session_id,
                "user_message": transcript,
                "answer": ""
            }
        )

        logger.info(
            "graph_response",
            response=result
        )
        
        await manager.send_message(
        session_id,
        json.dumps(
            {
                "type":"ai_response",
                "data":result
            }
        )
        )
    deepgram_service = DeepgramService(transcript_callback=process_transcript)

    await deepgram_service.connect()

    try:

        while True:

            raw_message = await websocket.receive_text()
            payload = json.loads(raw_message)

            logger.info(
            "message_received",
            session_id=session_id,
            message_type=payload.get("type")
            )

            if payload["type"] == "audio":

                audio_bytes = decode_base64_audio(
                    payload["audio"]
                )

                await deepgram_service.send_audio(
                    audio_bytes
                )

                logger.info(
                    "audio_sent_to_deepgram",
                    size=len(audio_bytes)
                )

                continue

            # MESSAGES_RECEIVED.inc()

            # start_time = time.time()

            # GRAPH_EXECUTIONS.inc()

            # result = graph.invoke(
            #     {
            #         "session_id":session_id,
            #         "user_message":raw_message,
            #         "answer":""
            #     }
            # )

            # execution_time = (
            #     time.time() - start_time
            # )

            # GRAPH_EXECUTION_TIME.observe(
            #     execution_time
            # )

            # await manager.send_message(
            #     session_id,
            #     result
            # )

            # MESSAGES_SENT.inc()




    except Exception as e:

        logger.error(
            "websocket_error",
            session_id=session_id,
            error=str(e)
        )
        await deepgram_service.disconnect()
        manager.disconnect(session_id)

        logger.info(
            "client_disconnected",
            session_id=session_id
        )
