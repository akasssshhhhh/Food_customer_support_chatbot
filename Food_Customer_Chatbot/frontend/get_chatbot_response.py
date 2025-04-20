import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_chatbot_response(user_query: str, api_url: str = "http://chatbot_backend:8000/get_response/"):
    """
    Sends a user query to the FastAPI chatbot backend and returns the response.

    Parameters:
        user_query (str): The user's input query.
        api_url (str): The FastAPI endpoint URL.

    Returns:
        dict: A dictionary with matched_question, intent, tone, and response.
    """
    try:
        logger.info(f"Sending query: {user_query} to {api_url}")
        response = requests.post(api_url, json={"query": user_query}, timeout=10)
        response.raise_for_status()  
        logger.info(f"Response received: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to connect to chatbot backend: {e}")
        return {
            "error": "Failed to connect to chatbot backend.",
            "details": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            "error": "An unexpected error occurred.",
            "details": str(e)
        }
