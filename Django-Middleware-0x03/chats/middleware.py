import logging
from datetime import datetime
from django.http import JsonResponse

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
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to /chats/ between 6AM and 9PM server time.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/chats/'):
            current_hour = datetime.now().hour
            if current_hour < 6 or current_hour >= 21:
                return JsonResponse(
                    {'error': 'Chat access is only allowed between 06:00 and 21:00.'},
                    status=403
                )
        return self.get_response(request)
