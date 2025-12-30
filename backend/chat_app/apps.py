"""
Django app configuration for chat_app.

Command: Registered in INSTALLED_APPS in settings.py
"""

from django.apps import AppConfig


class ChatAppConfig(AppConfig):
    """
    Configuration for the chat_app Django application.
    
    Command: Auto-configured when app is added to INSTALLED_APPS
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat_app'
