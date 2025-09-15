# modules/gemini_client.py
import os
from dotenv import load_dotenv
import requests

# Load .env variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = "https://api.gemini.google.com/v1/summarize"  # hypothetical endpoint

def ask_gemini(prompt: str) -> str:
    """
    Sends a prompt to Google Gemini and returns the generated summary.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set in .env")

    try:
        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": prompt,
            "max_output_tokens": 300,  # adjust for 5-6 line summary
            "temperature": 0.5
        }
        response = requests.post(GEMINI_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        # assume response contains {"summary": "..."} key
        return data.get("summary", "No summary returned.")
    except Exception as e:
        return f"Gemini API request failed: {e}"
