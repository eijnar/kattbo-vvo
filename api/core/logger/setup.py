import logging
import logging.handlers
import pathlib
import json
import queue
import atexit
from logging import config as logging_config

import ecs_logging
from elasticapm.contrib.starlette import make_apm_client

from core.config import settings


log_queue = queue.Queue()


def setup_logging():
    current_dir = pathlib.Path(__file__).parent
    config_file = current_dir / "config.json"

    try:
        with open(config_file) as f_in:
            config = json.load(f_in)
    except FileNotFoundError as e:
        raise ValueError("Logging configuration file not found") from e
    except json.JSONDecodeError as e:
        raise ValueError("Failed to parse logging configuration file") from e

    if settings.ENVIRONMENT == 'development':
        config['root']['level'] = 'DEBUG'
        config['handlers']['file_json']['level'] = 'DEBUG'
    elif settings.ENVIRONMENT == 'production':
        config['root']['level'] = 'INFO'
        config['handlers']['file_json']['level'] = 'INFO'

    logging.config.dictConfig(config)
    file_json_handler_config = config['handlers']['file_json']

    file_json_handler = logging.handlers.RotatingFileHandler(
        filename=file_json_handler_config['filename'],
        maxBytes=file_json_handler_config['maxBytes'],
        backupCount=file_json_handler_config['backupCount']
    )
    file_json_handler.setLevel(file_json_handler_config['level'])
    file_json_formatter = ecs_logging.StdlibFormatter(
        exclude_fields=["log.original"], stack_trace_limit=0)
    file_json_handler.setFormatter(file_json_formatter)

    # Start QueueListener with these handlers
    queue_listener = logging.handlers.QueueListener(
        log_queue, file_json_handler)
    queue_listener.start()

    atexit.register(queue_listener.stop)
    return queue_listener


def get_log_handlers(config):
    """
    Returns the handlers that should be used to listen to the queue.
    """
    handlers = []
    if "handlers" not in config:
        raise ValueError("Handlers not found in the logging configuration")
    handler_configs = config["handlers"]
    for handler_name, handler_config in handler_configs.items():
        if handler_name != "queue":
            try:
                handler = logging_config.DictConfigurator(
                    config).configure_handler(handler_config)
                handlers.append(handler)
            except Exception as e:
                raise ValueError(
                    f"Error configuring handler {handler_name}: {str(e)}")
    return handlers


apm_client = make_apm_client({
    'SERVICE_NAME': settings.SERVICE_NAME,
    'ENVIRONMENT': settings.ENVIRONMENT,
    'SERVER_URL': settings.APM_SERVER_URL,
    'SECRET_TOKEN': settings.APM_SECRET_TOKEN,
    'API_KEY': settings.APM_API_KEY,
    'LOG_LEVEL': 'off'
})
