
#--------------------------------------------------------------------------------------------------------------------------------


# import os
# import google.generativeai as genai
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Get Gemini API Key
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # Configure Gemini client
# genai.configure(api_key=GEMINI_API_KEY)

# # ===================================
# # 🔧 Function 1: gemini_generate
# # ===================================
# def gemini_generate(prompt_text, model_name="gemini-1.5-flash"):
#     """
#     Generates single-shot content completion for the provided prompt_text.
#     Suitable for summarization, extraction, analysis tasks.
#     """
#     model = genai.GenerativeModel(model_name)
#     response = model.generate_content(prompt_text)
#     return response.text

# # ===================================
# # 🔧 Function 2: gemini_chat
# # ===================================
# def gemini_chat(prompt_text, model_name="gemini-1.5-flash"):
#     """
#     Starts a chat session with Gemini and sends prompt_text as the first message.
#     Suitable for multi-turn reasoning, conversational workflows.
#     """
#     model = genai.GenerativeModel(model_name)
#     chat = model.start_chat(history=[])
#     response = chat.send_message(prompt_text)
#     return response.text

# # ===================================
# # ✨ Function 3: get_gemini_correction
# # ===================================
# def get_gemini_correction(discrepancies, model_name="gemini-1.5-flash"):
#     """
#     Sends mismatched timesheet rows to Gemini for correction recommendations.
#     """
#     prompt = (
#         "You are a Timesheet AI Agent.\n\n"
#         "Correct the following timesheet discrepancies:\n\n"
#         f"{discrepancies}\n\n"
#         "Explain what needs to be corrected and suggest fixes in plain language."
#     )
#     return gemini_generate(prompt, model_name)

# # ===================================
# # ✅ Example test usage
# # ===================================
# if __name__ == "__main__":
#     test_prompt = "Hello Gemini, summarize this as a test."
#     print("=== Gemini Generate ===")
#     print(gemini_generate(test_prompt))

#     print("\n=== Gemini Chat ===")
#     print(gemini_chat(test_prompt))

#     print("\n=== Gemini Correction Example ===")
#     test_discrepancy = """Employee: John Doe | Date: 2024-07-10 | Hours: 6 | System_Hours: 8"""
#     print(get_gemini_correction(test_discrepancy))


#-------------------------------------------------------------------------------------------------------------------------------------


import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ✅ Validate API Key
if not GEMINI_API_KEY:
    raise EnvironmentError("❌ GEMINI_API_KEY is not set or is invalid. Please update your .env file with a valid API key.")

# Configure Gemini client
genai.configure(api_key=GEMINI_API_KEY)

# ===================================
# 🔧 Function 1: gemini_generate
# ===================================
def gemini_generate(prompt_text, model_name="gemini-1.5-flash"):
    """
    Generates a single-shot response using Gemini for the provided prompt.
    """
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"❌ Gemini generate error: {str(e)}"

# ===================================
# 🔧 Function 2: gemini_chat
# ===================================
def gemini_chat(prompt_text, model_name="gemini-1.5-flash"):
    """
    Sends a message in a new chat session with Gemini (multi-turn reasoning).
    """
    try:
        model = genai.GenerativeModel(model_name)
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt_text)
        return response.text
    except Exception as e:
        return f"❌ Gemini chat error: {str(e)}"

# ===================================
# ✨ Function 3: get_gemini_correction
# ===================================
def get_gemini_correction(discrepancies, model_name="gemini-1.5-flash"):
    """
    Prompts Gemini to correct timesheet discrepancies and suggest explanations.
    """
    prompt = (
        "You are a Timesheet AI Agent.\n\n"
        "Correct the following timesheet discrepancies:\n\n"
        f"{discrepancies}\n\n"
        "Explain what needs to be corrected and suggest fixes in plain language."
    )
    return gemini_generate(prompt, model_name)

# ===================================
# ✅ Example test usage
# ===================================
if __name__ == "__main__":
    test_prompt = "Hello Gemini, summarize this as a test."
    print("=== Gemini Generate ===")
    print(gemini_generate(test_prompt))

    print("\n=== Gemini Chat ===")
    print(gemini_chat(test_prompt))

    print("\n=== Gemini Correction Example ===")
    test_discrepancy = """Employee: John Doe | Date: 2024-07-10 | Hours: 6 | System_Hours: 8"""
    print(get_gemini_correction(test_discrepancy))


#-----------------------------------------------------------------------------------------------------------------------------------------------

# import google.generativeai as genai
# import os

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Store your key in .env
# genai.configure(api_key=GOOGLE_API_KEY)

# # Use latest fast and stable model
# MODEL_NAME = "gemini-1.5-flash"

# def gemini_generate(prompt: str) -> str:
#     try:
#         model = genai.GenerativeModel(MODEL_NAME)
#         response = model.generate_content(prompt)
#         return response.text.strip()
#     except Exception as e:
#         return f"❌ Gemini generate error: {str(e)}"

# def gemini_chat(prompt: str) -> str:
#     try:
#         model = genai.GenerativeModel(MODEL_NAME)
#         chat = model.start_chat()
#         response = chat.send_message(prompt)
#         return response.text.strip()
#     except Exception as e:
#         return f"❌ Gemini chat error: {str(e)}"

