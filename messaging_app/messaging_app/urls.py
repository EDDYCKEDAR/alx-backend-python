from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Your app API routes under /api/
    path('api/', include('chats.urls')),

    # DRF's login/logout views for the browsable API
    path('api-auth/', include('rest_framework.urls')),
]
