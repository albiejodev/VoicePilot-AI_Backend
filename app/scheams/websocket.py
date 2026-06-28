from pydantic import BaseModel


class AudioMessage(BaseModel):
    type: str
    audio: str