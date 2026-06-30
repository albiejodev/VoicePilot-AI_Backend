import asyncio

from app.core.logger import logger


class UtteranceAggregator:

    def __init__(self):

        self.buffer = ""
        self.task = None


    async def add_transcript(
    self,
    transcript: str,
    callback,
    ):

        self.buffer += " " + transcript
        self.buffer = self.buffer.strip()



        if self.task and not self.task.done():

            self.task.cancel()


        self.task = asyncio.create_task(
            self.flush(callback)
        )


    async def flush(
        self,
        callback,
    ):
        try:

            logger.info("aggregator sleep start")

            await asyncio.sleep(0.5)
            
            logger.info("aggregator sleep finished")

            message = self.buffer.strip()

            logger.info("aggregator flushing",message=message)

            self.buffer = ""

            if not message:
                return
            
            logger.info("calling callback ")
            await callback(message)
            logger.info("callback finished")
            self.task=None

        except asyncio.CancelledError:

            logger.info(
                "aggregator_cancelled"
            )

        except Exception as e:

            logger.exception(
                "aggregator_error",
                error=str(e),
            )