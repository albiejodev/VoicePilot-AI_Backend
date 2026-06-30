from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.websocket import router as ws_router
from app.api.routes.metrics import router as metric_router
from app.core.startup import validate_services
from app.middleware.request_id import (RequestIdMiddleware)
from app.middleware.logging import (LoggingMiddleware)
from app.core.exceptions import (global_exception_handler)
from app.core.redis import redis_client
from app.core.logger import logger

app = FastAPI()


app.add_middleware(RequestIdMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_exception_handler(Exception,global_exception_handler)




app.include_router(health_router)
app.include_router(ws_router)
app.include_router(metric_router)



@app.on_event("startup")
async def startup():

    await redis_client.ping()
    logger.info("redis connected")
    validate_services()



@app.on_event("shutdown")
async def shutdown():

    await redis_client.close()
    logger.info("redis disconnected")