# core/logger/middleware.py

from fastapi import Request, HTTPException
import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()

        # Extract and sanitize headers
        headers = dict(request.headers)
        if 'authorization' in headers:
            headers['authorization'] = '[FILTERED]'

        # Capture request details
        request_info = {
            "http.request.method": request.method,
            "http.request.path": request.url.path,
            "http.request.headers": headers
        }

        # Set request.state.http_request for route handlers
        request.state.http_request = request_info

        try:
            # Process the request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time

            # Capture response details
            response_info = {
                "http.response.status_code": response.status_code,
                "http.response.time": round(duration, 4)  # Rounded for readability
            }

            # Combine request and response info
            log_entry = {**request_info, **response_info}

            # If user.id is set in request.state, include it
            user_id = getattr(request.state, 'user_id', 'N/A')
            log_entry["user.id"] = user_id

            # Log the request and response
            logger.debug("Request processed", extra=log_entry)

            return response

        except HTTPException as e:
            # Calculate duration
            duration = time.time() - start_time

            # Capture error details
            error_info = {
                "http.response.status_code": e.status_code,
                "http.response.time": round(duration, 4),
                "error": e.detail
            }

            # Combine request and error info
            log_entry = {**request_info, **error_info}

            # If user.id is set in request.state, include it
            user_id = getattr(request.state, 'user_id', 'N/A')
            log_entry["user.id"] = user_id

            # Log the error
            logger.error("Request resulted in an error", extra=log_entry)

            # Re-raise the exception to be handled by FastAPI
            raise e

        except Exception as e:
            # Calculate duration
            duration = time.time() - start_time

            # Capture error details
            error_info = {
                "http.response.status_code": 500,
                "http.response.time": round(duration, 4),
                "error": str(e)
            }

            # Combine request and error info
            log_entry = {**request_info, **error_info}

            # If user.id is set in request.state, include it
            user_id = getattr(request.state, 'user_id', 'N/A')
            log_entry["user.id"] = user_id

            # Log the error
            logger.error("Request resulted in an error", extra=log_entry)

            # Re-raise the exception to be handled by FastAPI
            raise e
