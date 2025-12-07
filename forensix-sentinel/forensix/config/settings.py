from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Forensix Sentinel"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
