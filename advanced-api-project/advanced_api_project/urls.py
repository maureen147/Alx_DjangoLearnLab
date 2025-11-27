from django.contrib import admin
from django.urls import path, include  # Add include import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Now include is defined
]