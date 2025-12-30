"""
URL configuration for chat_backend project - Main URL routing.

Command: python manage.py runserver
Command: Access admin panel at /admin/
Command: Main app routes defined in chat_app/urls.py

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

# Command: Main URL patterns for the application
urlpatterns = [
    # Command: Django admin interface - /admin/
    path('admin/', admin.site.urls),
    
    # Command: Include chat_app URLs - routes to / and /api/chat/
    path('', include('chat_app.urls')),
]
