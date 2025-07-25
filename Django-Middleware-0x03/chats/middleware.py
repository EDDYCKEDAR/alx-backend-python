import logging
import time
from datetime import datetime
from collections import defaultdict
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware that logs each user's requests to a file,
    including timestamp, user, and request path.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logging
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s',
            filemode='a'
        )
        self.logger = logging.getLogger(__name__)
    
    def __call__(self, request):
        # Get user information
        user = request.user if request.user.is_authenticated else 'Anonymous'
        
        # Log the request
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware(MiddlewareMixin):
    """
    Middleware that restricts access to the messaging app
    during certain hours (outside 9 AM to 6 PM).
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get current hour (24-hour format)
        current_hour = datetime.now().hour
        
        # Check if current time is outside allowed hours (9 AM to 6 PM)
        if current_hour < 9 or current_hour >= 18:
            return HttpResponseForbidden(
                "Access to the messaging app is restricted outside business hours (9 AM - 6 PM)."
            )
        
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware(MiddlewareMixin):
    """
    Middleware that limits the number of chat messages a user can send
    within a certain time window based on their IP address.
    Note: This middleware is named for offensive language detection but
    implements rate limiting as per the instructions.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to store IP addresses and their request timestamps
        self.ip_requests = defaultdict(list)
        self.max_requests = 5  # Maximum requests per time window
        self.time_window = 60  # Time window in seconds (1 minute)
    
    def __call__(self, request):
        # Only apply rate limiting to POST requests (messages)
        if request.method == 'POST':
            # Get client IP address
            ip_address = self.get_client_ip(request)
            current_time = time.time()
            
            # Clean old requests outside the time window
            self.ip_requests[ip_address] = [
                req_time for req_time in self.ip_requests[ip_address]
                if current_time - req_time < self.time_window
            ]
            
            # Check if user has exceeded the limit
            if len(self.ip_requests[ip_address]) >= self.max_requests:
                return HttpResponseForbidden(
                    f"Rate limit exceeded. You can only send {self.max_requests} messages per minute."
                )
            
            # Add current request timestamp
            self.ip_requests[ip_address].append(current_time)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get the client's IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolePermissionMiddleware(MiddlewareMixin):
    """
    Middleware that checks the user's role before allowing access
    to specific actions. Only admin and moderator users are allowed.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip authentication check for login/logout pages
        if request.path in ['/admin/login/', '/admin/logout/', '/login/', '/logout/']:
            response = self.get_response(request)
            return response
        
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Authentication required.")
        
        # Check if user has admin or moderator role
        user = request.user
        
        # Check if user is superuser (admin)
        if user.is_superuser:
            response = self.get_response(request)
            return response
        
        # Check if user has moderator role (you can customize this based on your User model)
        # This assumes you have a way to identify moderators
        # Option 1: Check if user is staff
        if user.is_staff:
            response = self.get_response(request)
            return response
        
        # Option 2: Check user groups (uncomment if you use groups)
        # if user.groups.filter(name__in=['admin', 'moderator']).exists():
        #     response = self.get_response(request)
        #     return response
        
        # Option 3: Check custom user profile field (uncomment if you have a custom profile)
        # if hasattr(user, 'profile') and user.profile.role in ['admin', 'moderator']:
        #     response = self.get_response(request)
        #     return response
        
        # If user doesn't have required permissions
        return HttpResponseForbidden(
            "Access denied. Only admin and moderator users are allowed."
        )
