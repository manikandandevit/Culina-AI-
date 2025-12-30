"""
URL configuration for chat_app.
Defines URL patterns for the Culina AI chat application.

Command: python manage.py runserver
"""

from django.urls import path
from . import views

# URL patterns for chat application
urlpatterns = [
    # Command: Main chat interface - GET /
    path('', views.index, name='index'),
    
    # Command: Chat API endpoint - GET /api/chat/?message=<message>
    path('api/chat/', views.chat_api, name='chat_api'),
]
