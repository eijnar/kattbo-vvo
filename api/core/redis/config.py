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
    'cache': 0,
    'tokens': 2,
    'authorize': 3,
    'unconfirmed_users': 4
}