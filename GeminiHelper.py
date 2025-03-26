import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create the model
model = genai.GenerativeModel('gemini-2.0-flash')
chat=model.start_chat(history=[])

def get_gemini_response(question):
    """
    Generate a response from the Gemini AI model.

    Args:
        question (str): The input question or prompt.

    Returns:
        str: The generated response text, or None if an error occurs.
    """
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None