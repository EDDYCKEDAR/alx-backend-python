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

class OffensiveLanguageMiddleware:
    """
    Middleware to block requests that contain offensive language.
    """

    OFFENSIVE_WORDS = ['badword1', 'badword2', 'exampleword']  # Replace with real words

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/chats/"):
            body = request.POST.dict()

            # Combine all values in POST data to scan for bad words
            combined_text = " ".join(str(value).lower() for value in body.values())

            if any(word in combined_text for word in self.OFFENSIVE_WORDS):
                return JsonResponse(
                    {'error': 'Your message contains offensive language.'},
                    status=403
                )

        return self.get_response(request)

class RolepermissionMiddleware:
    """
    Middleware that restricts access to /chats/ based on user roles.
    Only users with role 'admin' or 'moderator' are allowed.
    """

    ALLOWED_ROLES = ['admin', 'moderator']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply to chat paths
        if request.path.startswith('/chats/'):
            user = request.user
            if user.is_authenticated:
                # Check if user role (group name or custom field) is allowed
                user_groups = user.groups.values_list('name', flat=True)
                if not any(role in self.ALLOWED_ROLES for role in user_groups):
                    return JsonResponse(
                        {'error': 'Access denied. You do not have the required role.'},
                        status=403
                    )
            else:
                return JsonResponse(
                    {'error': 'Authentication required.'},
                    status=403
                )

        return self.get_response(request)
