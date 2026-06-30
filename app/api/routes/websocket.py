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
from app.services.conversation.conversation_service import conversation_service
from app.services.aggregation.utterance_aggregator import (
    UtteranceAggregator,
)
import traceback


router = APIRouter()




@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket,session_id:str):
    await manager.connect(session_id,websocket)
    aggregator = UtteranceAggregator()

    #nested helper function 
    async def process_transcript(
    transcript: str,
    ):
        await aggregator.add_transcript(
            transcript,
            process_complete_transcript,
        )


    async def process_complete_transcript(
    transcript: str
    ):
        logger.info(
            "processing_transcript",
            transcript=transcript
        )

        result,audio = await conversation_service.process_message(
            session_id=session_id,
            message=transcript,
        )

        logger.info(
            "graph_response",
            response=result
        )
        
        await manager.send_message(
            session_id,
            {
                "type": "ai_response",
                "data": result,
            },
        )
        
        logger.info(
            "sending_audio_to_client",
            size=len(audio)
        )
        await manager.send_audio(
            session_id,
            audio
        )
    
    #nested helper function 2
    async def process_interim_transcript(
    transcript: str,
    is_final: bool,
    ):
        await manager.send_message(
            session_id,
            {
                "type": "transcript",
                "data": {
                    "text": transcript,
                    "is_final": is_final,
                },
            },
        )

    deepgram_service = None

    try:

        while True:

            raw_message = await websocket.receive_text()
            payload = json.loads(raw_message)

            logger.info(
            "message_received",
            session_id=session_id,
            message_type=payload.get("type")
            )

            if payload["type"] == "start_recording":

                logger.info(
                    "starting_deepgram_session"
                )

                deepgram_service = DeepgramService(
                    transcript_callback=process_transcript,
                    interim_callback=process_interim_transcript,
                )

                await deepgram_service.connect()

                continue


            if payload["type"] == "stop_recording":

                logger.info(
                    "recording_stopped"
                )

                if deepgram_service:

                    await deepgram_service.finalize()

                continue



            if payload["type"] == "audio":

                audio_bytes = decode_base64_audio(
                    payload["audio"]
                )

                if deepgram_service:

                    await deepgram_service.send_audio(
                        audio_bytes
                    )

                    logger.info(
                        "audio_sent_to_deepgram",
                        size=len(audio_bytes)
                    )

                continue


    except WebSocketDisconnect:

        logger.info(
            "client_disconnected",
            session_id=session_id
        )

        if deepgram_service:
            await deepgram_service.disconnect()

        manager.disconnect(session_id)

    except Exception as e:

        logger.error(
            "websocket_error",
            session_id=session_id,
            error=str(e),
            traceback=traceback.format_exc(),
        )

        if deepgram_service:
            await deepgram_service.disconnect()

        manager.disconnect(session_id)