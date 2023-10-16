from django.urls import path
from . import views

urlpatterns = [
    # Dashboard view url.
    path('', views.dashboard_view, name='dashboard'),
]
