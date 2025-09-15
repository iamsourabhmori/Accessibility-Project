import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key from environment
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("Google API key not found. Please set GOOGLE_API_KEY in your .env file.")

# Configure Gemini
genai.configure(api_key=api_key)

def summarize_timesheet_with_gemini(timesheet_text):
    """
    Summarize timesheet data using Gemini 1.5 Flash (latest).
    
    Args:
        timesheet_text (str): Raw timesheet data as text.
    
    Returns:
        str: Summarized timesheet output.
    """
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(
        f"Summarize this timesheet data clearly and concisely for reporting:\n\n{timesheet_text}"
    )
    return response.text

# Example usage for standalone testing
if __name__ == "__main__":
    sample_text = """
    2025-07-21, Project Planning, 4, Initial project kickoff meeting
    2025-07-21, Coding Module A, 3, Developed main algorithm
    2025-07-22, Code Review, 2, Reviewed teammate's code
    """
    summary = summarize_timesheet_with_gemini(sample_text)
    print("Gemini 1.5 Flash Summary:\n", summary)
