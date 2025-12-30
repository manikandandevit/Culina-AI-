"""
Culina AI Agent - Production-ready AI agent for cooking assistance.
Handles AI interactions with Google Gemini API with proper error handling and logging.

Command: python manage.py runserver
"""

import os
import re
import logging
from google.genai import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging for production
logger = logging.getLogger('chat_app')

# Initialize Gemini API client
# Command: Set GEMINI_API_KEY environment variable or add to .env file
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    logger.warning("GEMINI_API_KEY not found in environment variables")

try:
    client = Client(api_key=GOOGLE_API_KEY) if GOOGLE_API_KEY else None
except Exception as e:
    logger.error(f"Failed to initialize Gemini client: {e}")
    client = None


def _format_response_with_line_breaks(text: str) -> str:
    """
    Post-process AI response to ensure proper line breaks between steps.
    Ensures each 'Step X:' is on its own line with proper spacing.
    
    Args:
        text: Raw AI response text
        
    Returns:
        Formatted text with proper line breaks
    """
    if not text:
        return text
    
    # Pattern to match "Step X:" where X is a number (case-insensitive)
    # First, ensure there's a line break before each step if not already present
    formatted = re.sub(r'([^\n])(Step\s+\d+:)', r'\1\n\n\2', text, flags=re.IGNORECASE)
    
    # Ensure steps are separated by line breaks (handle cases where steps are in same paragraph)
    formatted = re.sub(r'(Step\s+\d+:[^\n]+?)(Step\s+\d+:)', r'\1\n\n\2', formatted, flags=re.IGNORECASE)
    
    # Ensure there's a line break after "Instructions:" before the first step
    formatted = re.sub(r'(Instructions:\s*)(Step\s+\d+:)', r'\1\n\n\2', formatted, flags=re.IGNORECASE)
    
    # Clean up excessive line breaks (more than 2 consecutive)
    formatted = re.sub(r'\n\n\n+', r'\n\n', formatted)
    
    # Ensure each step starts on a new line (handle any remaining inline steps)
    formatted = re.sub(r'(\S)(\s+Step\s+\d+:)', r'\1\n\n\2', formatted, flags=re.IGNORECASE)
    
    return formatted


def get_recipe_ai_response(user_message: str) -> str:
    """
    Send user message to Gemini AI and return formatted response.
    Culina AI - Production-ready cooking assistant for recipes and cooking questions.
    
    Command: Called via /api/chat/?message=<user_message>
    
    Args:
        user_message: User's question or message about cooking/recipes
        
    Returns:
        AI response string or error message
        
    Raises:
        Logs errors but returns user-friendly error messages
    """
    if not user_message or not user_message.strip():
        return "Please provide a question or message about recipes or cooking."
    
    if not client:
        logger.error("Gemini client not initialized. Check GEMINI_API_KEY.")
        return "Error: AI service is not available. Please check API configuration."
    
    # System context for Culina AI - Hyper active cooking assistant
    system_context = (
        "You are Culina AI, an enthusiastic and hyperactive cooking assistant! 🍳✨ "
        "You are EXCLUSIVELY designed to help with cooking and food-related questions. "
        "Be energetic, friendly, passionate, and highly interactive with users! "
        "\n\n"
        "CRITICAL RULE: If a user asks about ANYTHING that is NOT related to cooking, recipes, "
        "ingredients, meal planning, nutrition, food safety, kitchen techniques, or food culture, "
        "you MUST politely redirect them. Say: "
        "'I'm Culina AI, and I'm here exclusively to help with cooking and food-related questions! "
        "What would you like to cook today?' "
        "Be warm, polite, and encouraging - never rude or dismissive. "
        "\n\n"
        "RESPONSE FORMATTING RULES (CRITICAL - MUST FOLLOW EXACTLY): "
        "- Keep answers CONCISE and ACCURATE - avoid long paragraphs "
        "- ALWAYS format responses line-by-line with proper structure "
        "- Use bullet points (-) or numbered lists for steps and lists "
        "- CRITICAL: Each bullet point MUST be on its own separate line - one bullet point complete, then come to another line "
        "- NEVER put multiple bullet points on the same line "
        "- For recipes: Format ingredients and instructions in clear line-by-line format "
        "- Use line breaks (\\n) to separate different sections "
        "- Be direct and to the point - no unnecessary explanations "
        "- For recipe instructions: ALWAYS use corporate/FAANG-level formatting with 'Step 1:', 'Step 2:', etc. (not just numbers) "
        "- CRITICAL FORMATTING: Each 'Step X:' instruction MUST be on its own separate line with a line break before it "
        "- NEVER put multiple steps in the same paragraph or line "
        "- After 'Instructions:' text, ALWAYS add a line break, then start 'Step 1:' on a new line "
        "- After each step, ALWAYS add a line break before the next step "
        "- Example format for recipes (EXACT format to follow): "
        "  Ingredients: "
        "  - Item 1 "
        "  - Item 2 "
        "  - Item 3 "
        "  Instructions: "
        "  "
        "  Step 1: Step one description here "
        "  Step 2: Step two description here "
        "  Step 3: Step three description here "
        "\n\n"
        "When answering cooking questions: "
        "- Be enthusiastic but keep it brief "
        "- Provide accurate, practical cooking advice "
        "- Format all information clearly line-by-line "
        "- Always prioritize food safety "
        "- Use emojis sparingly (1-2 max per response) "
        "\n\n"
        "Remember: You are Culina AI - concise, accurate, and properly formatted! "
        "Stay focused on cooking topics and always redirect non-cooking questions politely."
    )
    
    full_message = f"{system_context}\n\nUser Question: {user_message.strip()}"
    
    try:
        logger.info(f"Processing cooking query: {user_message[:50]}...")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_message
        )
        
        if hasattr(response, 'text') and response.text:
            logger.info("Successfully received AI response")
            formatted_response = _format_response_with_line_breaks(response.text)
            return formatted_response
        else:
            logger.warning("Received empty response from AI")
            return "I apologize, but I couldn't generate a response. Please try again."
            
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}", exc_info=True)
        
        # Fallback: try alternative API structure
        try:
            logger.info("Attempting fallback API method...")
            messages = [
                {"role": "system", "content": system_context},
                {"role": "user", "content": user_message.strip()}
            ]
            response = client.models.chat(
                model="gemini-1.5-pro",
                messages=messages
            )
            
            if hasattr(response, 'text') and response.text:
                logger.info("Fallback method succeeded")
                formatted_response = _format_response_with_line_breaks(response.text)
                return formatted_response
            else:
                return "I apologize, but I couldn't generate a response. Please try again."
                
        except Exception as e2:
            logger.error(f"Fallback method also failed: {e2}", exc_info=True)
            return (
                "I'm sorry, I encountered an error while processing your request. "
                "Please try again in a moment. If the problem persists, check your API configuration."
            )
