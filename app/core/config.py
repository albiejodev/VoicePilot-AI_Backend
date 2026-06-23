#app configuration file 


from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    APP_NAME: str = "VoicePilot-AI"

    OPENAI_API_KEY: str

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    LOG_LEVEL: str = "INFO"

    DEEPGRAM_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings() 