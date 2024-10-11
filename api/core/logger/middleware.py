from fastapi import Request
import logging
import time

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    start_time = time.time()

    headers = dict(request.headers)
    if 'authorization' in headers:
        headers['authorization'] = '[FILTERED]'

    # Capture request details and store them in request.state
    request.state.http_request = {
        "http.request.method": request.method,
        "http.request.path": request.url.path,
        "http.request.headers": headers
    }

    response = await call_next(request)

    # Capture response details and store them as well
    duration = time.time() - start_time
    request.state.http_response = {
        "http.response.status_code": response.status_code,
        "http.response.time": duration
    }

    return response
