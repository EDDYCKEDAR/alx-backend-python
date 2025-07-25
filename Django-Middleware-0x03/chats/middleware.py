from datetime import datetime
from django.http import JsonResponse

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
