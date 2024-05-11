from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Kättbo VVO API"
    
    DEBUG_MODE: bool = False
    SQL_DEBUG_MODE: bool = False
    
    DATABASE_URL: str
    
    APM_SERVICE_NAME: str
    APM_ENVIRONMENT: str
    APM_SERVER_URL: str
    APM_SECRET_TOKEN: str
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()