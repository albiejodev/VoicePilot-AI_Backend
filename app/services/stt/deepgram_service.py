import websockets
import asyncio
import json
from app.core.config import settings
from app.core.logger import logger


class DeepgramService:

    def __init__(self,transcript_callback=None,interim_callback=None):
        self.websocket = None
        self.receiver_task = None
        self.transcript_callback=transcript_callback
        self.interim_callback=interim_callback



    async def connect(self):

        url = (
            "wss://api.deepgram.com/v1/listen"
            "?model=nova-3"
            "&language=en"
            "&encoding=opus"
            "&interim_results=true"
            "&smart_format=true"
            "&endpointing=300"
        )

        self.websocket = await websockets.connect(
            url,
            additional_headers={
                "Authorization": f"Token {settings.DEEPGRAM_API_KEY}"
            },
        )

        logger.info("deepgram_connected")

        self.receiver_task = asyncio.create_task(self.receive_transcripts())




    async def send_audio(self, audio_bytes: bytes):

        if self.websocket:

            await self.websocket.send(audio_bytes)




    async def receive_transcripts(self):

        while True:
            try:
                message = await self.websocket.recv()

                data = json.loads(message)

                transcript = (
                    data.get("channel", {})
                    .get("alternatives", [{}])[0]
                    .get("transcript", "")
                )

                is_final = data.get("is_final", False)

                if transcript:

                    logger.info(
                        "transcript_received",
                        transcript=transcript,
                        is_final=is_final,
                    )

                    if self.interim_callback:

                        await self.interim_callback(
                            transcript,
                            is_final,
                        )

                    if (
                        is_final
                        and self.transcript_callback
                    ):

                        await self.transcript_callback(
                            transcript
                        )

                        logger.info("final transcript processed")

                        break


            except asyncio.CancelledError:

                logger.info(
                    "deepgram_receiver_cancelled"
                )
                break

            except websockets.ConnectionClosed:
                logger.info("deepgram_connection_closed")
                break



    async def disconnect(self):

        if self.receiver_task:

            self.receiver_task.cancel()

            try:
                await self.receiver_task
            except asyncio.CancelledError:
                pass

            self.receiver_task = None

        if self.websocket:

            await self.websocket.close()

            self.websocket = None

            logger.info(
                "deepgram_disconnected"
            )



    async def finalize(self):

        if self.websocket:

            await self.websocket.send(
                json.dumps(
                    {
                        "type": "Finalize"
                    }
                )
            )

            logger.info(
                "deepgram_finalize_sent"
            )