import logging
from datetime import datetime

# Set up basic logging configuration
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class RequestLoggingMiddleware:
    """
    Middleware that logs all incoming HTTP requests.
    Logs the method, path, and timestamp.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request details
        logging.info(f"{request.method} request to {request.path}")

        # Continue processing
        response = self.get_response(request)
        return response
