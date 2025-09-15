
# #ai_agent.py

# import google.generativeai as genai

# # Your Gemini API Key
# API_KEY = "AIzaSyAUa8DX4ilkKFvnoVEJ17Y1Mg_qaiKtvnc"

# # Configure Gemini
# genai.configure(api_key=API_KEY)

# # Load model (Gemini-pro is the text model)
# model = genai.GenerativeModel("gemini-pro")

# def ask_ai(query):
#     """Send user query to Gemini AI and return response"""
#     try:
#         response = model.generate_content(query)
#         return response.text
#     except Exception as e:
#         return f"Error: {str(e)}"

#------------------------------------------------------------------------------------------------------------


# ai_agent.py

import os
import google.generativeai as genai

# ----------------------------
# Gemini API Key Configuration
# ----------------------------
# Load API key from environment variable for security
API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_FALLBACK_API_KEY")

if not API_KEY or API_KEY == "YOUR_FALLBACK_API_KEY":
    raise ValueError("Gemini API key not found. Please set GEMINI_API_KEY in your environment.")

# Configure Gemini client
genai.configure(api_key=API_KEY)

# Load Gemini model (gemini-pro is text-based)
model = genai.GenerativeModel("gemini-pro")

# ----------------------------
# Function to query Gemini
# ----------------------------
def ask_ai(query: str) -> str:
    """
    Send user query to Gemini AI and return response as text.
    
    Args:
        query (str): The input query or prompt from user.
    
    Returns:
        str: Gemini AI's response or error message.
    """
    try:
        response = model.generate_content(query)
        return response.text.strip() if response and response.text else "No response from AI."
    except Exception as e:
        return f"Error communicating with Gemini API: {str(e)}"
