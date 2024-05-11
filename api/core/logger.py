import os
import structlog
from elasticapm.handlers.structlog import structlog_processor
from elasticapm.contrib.starlette import make_apm_client

from .config import settings

# Create and configure the APM client
apm_client = make_apm_client({
    'SERVICE_NAME': settings.APM_SERVICE_NAME,
    'ENVIRONMENT': settings.APM_ENVIRONMENT,
    'SERVER_URL': settings.APM_SERVER_URL,
    'SECRET_TOKEN': settings.APM_SECRET_TOKEN,
    'ELASTIC_APM_USE_STRUCTLOG': True,
})

def setup_logging():
    """Configures structlog based logging."""
    log_path = "logs/api_log.log"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Open the log file safely for appending text
    log_file = open(log_path, "a")

    # Create a logger that prints to stdout
    wrapped_logger = structlog.PrintLogger(file=log_file)
    
    # Configure structlog
    logger = structlog.wrap_logger(
        wrapped_logger,
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog_processor,  # Adds Elastic APM tracing info to logs
            structlog.processors.JSONRenderer()  # Outputs log as JSON
        ],
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    return logger.new()  # Return a new logger instance

logger = setup_logging()
