from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = 'Kattbo_VVO-API'
    ENVIRONMENT: str
    
    # General site settings
    SITE_URL: str = 'localhost:8000' # Without any http:// or https://
    HTTP_PROTOCOL: str = 'http'
    
    SESSION_SECRET_KEY: str
    
    AUTH0_DOMAIN: str
    API_AUDIENCE: str
    ALGORITHMS: list = ["RS256"]
    
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    
    APP_NAME: str = 'Kättbo VVO API'
    DEBUG_MODE: bool = False
    
    # Database settings
    SQL_DEBUG_MODE: bool = False
    SQL_DATABASE_URL: str
    
    # Eleasticsearch APM client settings
    APM_SERVER_URL: str
    APM_SECRET_TOKEN: str
    APM_API_KEY: str
    
    # Messaging settings
    SMTP_SERVER: str
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    TELEGRAM_BOT_TOKEN: str
    
    # # RabbitMQ settings
    # RABBITMQ_USERNAME: str
    # RABBITMQ_PASSWORD: str
    # RABBITMQ_HOSTNAME: str = 'localhost'
    # RABBITMQ_PORT: int = 5672
    # RABBITMQ_VHOST: str
    
    # # Redis settings
    # REDIS_HOSTNAME: str = 'localhost'
    # REDIS_PORT: int = 6379
    # REDIS_PASSWORD: str = ''
    # REDIS_SSL: bool = False
    # REDIS_CELERY_DB: int = 1
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()