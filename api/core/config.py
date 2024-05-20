from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # General site settings
    SITE_URL: str = 'localhost:8000' # Without any http:// or https://
    HTTP_PROTOCOL: str = 'http'
    
    APP_NAME: str = 'Kättbo VVO API'
    DEBUG_MODE: bool = False
    
    # Database settings
    SQL_DEBUG_MODE: bool = False
    SQL_DATABASE_URL: str
    
    # Eleasticsearch APM client settings
    APM_SERVICE_NAME: str = 'vvo-api'
    APM_ENVIRONMENT: str = 'dev'
    APM_SERVER_URL: str
    APM_SECRET_TOKEN: str
    
    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_LIFESPAN_MINUTES: int = 15
    PASSWORD_RESET_TOKEN_LIFESPAN_MINUTES: int = 30
    REFRESH_TOKEN_LIFESPAN_DAYS: int = 7
    
    # Messaging settings
    SMTP_SERVER: str
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    TELEGRAM_BOT_TOKEN: str
    
    # RabbitMQ settings
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOSTNAME: str = 'localhost'
    RABBITMQ_PORT: int = 5672
    RABBITMQ_VHOST: str
    
    # Redis settings
    REDIS_HOSTNAME: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_TOKEN_DB: int = 0
    REDIS_UNCONFIRMED_USER_DB: int = 1
    REDIS_CELERY_DB: int = 5
    REDIS_PASSWORD: str = ''
    REDIS_SSL: bool = False
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()