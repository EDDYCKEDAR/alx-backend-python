#!/usr/bin/env python
"""
Test script to verify middleware functionality
Run this after setting up the Django project
"""

import requests
import time
from datetime import datetime
from datetime import datetime
from django.http import JsonResponse

class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to /chats/ between 6AM and 9PM server time.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is targeting the chat endpoint
        if request.path.startswith('/chats/'):
            current_hour = datetime.now().hour

            # Allow only between 6AM (06:00) and 9PM (21:00)
            if current_hour < 6 or current_hour >= 21:
                return JsonResponse(
                    {'error': 'Chat access is only allowed between 06:00 and 21:00.'},
                    status=403
                )

        # Otherwise continue processing
        return self.get_response(request)

def test_middleware():
    """Test all middleware components"""
    base_url = "http://127.0.0.1:8000"
    
    print("Testing Django Middleware Components...")
    print("=" * 50)
    
    # Test 1: Request Logging Middleware
    print("1. Testing Request Logging Middleware")
    print("Making requests to different endpoints...")
    
    endpoints = ["/", "/chats/", "/admin/"]
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"   GET {endpoint} - Status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"   GET {endpoint} - Server not running")
    
    print("   Check 'requests.log' file for logged requests\n")
    
    # Test 2: Time Restriction Middleware
    print("2. Testing Time Restriction Middleware")
    current_hour = datetime.now().hour
    if 9 <= current_hour < 18:
        print(f"   Current time: {datetime.now().strftime('%H:%M')} - Access should be ALLOWED")
    else:
        print(f"   Current time: {datetime.now().strftime('%H:%M')} - Access should be FORBIDDEN")
    print()
    
    # Test 3: Rate Limiting Middleware (OffensiveLanguageMiddleware)
    print("3. Testing Rate Limiting Middleware")
    print("Sending multiple POST requests to test rate limiting...")
    
    chat_url = f"{base_url}/chats/"
    for i in range(7):  # Send 7 requests (limit is 5)
        try:
            response = requests.post(chat_url, data={'message': f'Test message {i+1}'})
            print(f"   POST Request {i+1} - Status: {response.status_code}")
            if response.status_code == 403:
                print(f"   Rate limit triggered: {response.text}")
                break
        except requests.exceptions.ConnectionError:
            print(f"   POST Request {i+1} - Server not running")
        time.sleep(0.5)  # Small delay between requests
    print()
    
    # Test 4: Role Permission Middleware
    print("4. Testing Role Permission Middleware")
    print("This middleware checks user roles (admin/moderator)")
    print("You'll need to:")
    print("   - Create a superuser: python manage.py createsuperuser")
    print("   - Login through Django admin or your app")
    print("   - Test with different user roles")
    print()
    
    print("Test completed! Check the console and requests.log for results.")

if __name__ == "__main__":
    test_middleware()
