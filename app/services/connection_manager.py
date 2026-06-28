from fastapi import WebSocket
from app.core.logger import logger 
from app.core.metrics import ACTIVE_CONNECTIONS
from typing import Any


class ConnectionManager:

    def __init__(self):
        self.active_connections: dict[
            str,
            WebSocket
            ] = {}

    async def connect(
    self,
    session_id: str,
    websocket: WebSocket
    ):
        await websocket.accept()

        if session_id in self.active_connections:
            await self.active_connections[
                session_id
            ].close() 

        self.active_connections[
            session_id
        ] = websocket

        ACTIVE_CONNECTIONS.inc()


        logger.info(
            "websocket connected",
            session_id=session_id,
            total_connections=len(self.active_connections)
        )


    def disconnect(
        self,
        session_id: str
    ):

        if session_id in self.active_connections:

            del self.active_connections[
                session_id
            ]

            ACTIVE_CONNECTIONS.dec()

            logger.info(
                "websocket_disconnected",
                session_id=session_id,
                total_connections=len(
                    self.active_connections
                )
            )

    async def send_message(
        self,
        session_id:str,
        data:dict[str,Any]
    ):

        websocket = self.active_connections.get(
            session_id
        )

        if websocket:

            await websocket.send_json(data)


    def get_connection_count(
        self
    ):

        return len(
            self.active_connections
        )



    

manager = ConnectionManager() 