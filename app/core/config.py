from pydantic import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str = ""
    environment: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
