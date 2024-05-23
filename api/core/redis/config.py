from core.config import settings

REDIS_SETTINGS = {
    'host': settings.REDIS_HOSTNAME,
    'port': settings.REDIS_PORT,
    'password': settings.REDIS_PASSWORD,
    'ssl': settings.REDIS_SSL,
    'encoding': 'utf-8',
    'decode_responses': True,
    'max_connections': 10
}

REDIS_DBS = {
    'tokens': settings.REDIS_TOKEN_DB,
    'authorize': settings.REDIS_AUTH_DB,
    'unconfirmed_users': settings.REDIS_UNCONFIRMED_USER_DB,
}