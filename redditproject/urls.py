from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('redditapp.urls')),  # directing root URL to the app's urls
]
