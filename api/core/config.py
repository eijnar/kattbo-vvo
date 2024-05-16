from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # General FastAPI settings
    APP_NAME: str = "Kättbo VVO API"
    DEBUG_MODE: bool = False
    
    # Database settings
    SQL_DEBUG_MODE: bool = False
    DATABASE_URL: str
    
    # Eleasticsearch APM client settings
    APM_SERVICE_NAME: str
    APM_ENVIRONMENT: str
    APM_SERVER_URL: str
    APM_SECRET_TOKEN: str
    
    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # Redis settings
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ''
    REDIS_SSL: bool = False
    
    # Access token expiration settings
    ACCESS_TOKEN_LIFESPAN_MINUTES: int = 15
    PASSWORD_RESET_TOKEN_LIFESPAN_MINUTES: int = 30
    REFRESH_TOKEN_LIFESPAN_DAYS: int = 7
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()