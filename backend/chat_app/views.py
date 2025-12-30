"""
Django views for Culina AI chat application.
Handles HTTP requests and responses for the chat interface.
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import logging

from .agent import get_recipe_ai_response

logger = logging.getLogger('chat_app')


@require_http_methods(["GET"])
def index(request):
    """
    Render the main chat interface page.
    
    Args:
        request: Django HTTP request object
        
    Returns:
        Rendered HTML template for the chat interface
    """
    return render(request, 'chat_app/index.html')


@require_http_methods(["GET"])
def chat_api(request):
    """
    API endpoint for processing chat messages.
    
    Args:
        request: Django HTTP request object with 'message' query parameter
        
    Returns:
        JSON response containing AI-generated response or error message
    """
    try:
        user_message = request.GET.get('message', '').strip()
        
        if not user_message:
            return JsonResponse(
                {'response': 'Please provide a message.'},
                status=400
            )
        
        logger.info(f"Received chat request: {user_message[:50]}...")
        ai_response = get_recipe_ai_response(user_message)
        
        return JsonResponse({'response': ai_response})
        
    except Exception as e:
        logger.error(f"Error in chat_api: {e}", exc_info=True)
        return JsonResponse(
            {'response': 'An error occurred while processing your request. Please try again.'},
            status=500
        )