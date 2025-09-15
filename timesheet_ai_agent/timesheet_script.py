# '''
# timesheet_ai_agent/
# ├── agents/
# │   └── timesheet_agent.py
# ├── app/
# │   └── streamlit_app.py
# ├── tasks/
# │   └── timesheet_tasks.py
# ├── tools/
# │   ├── screenshot_tool.py
# │   ├── ocr_tool.py
# │   ├── timesheet_verifier.py
# │   └── timesheet_updater.py
# |   |__gemini_tools.py
# ├── crew.py
# ├── main.py
# ├── requirements.txt
# └── README.md

# '''

# #  timesheet_agent.py
# from crewai import Agent

# timesheet_agent = Agent(
#     role="Timesheet Data Verifier and Updater",
#     goal="Ensure timesheet data consistency across multiple systems for consultants.",
#     backstory=(
#         "This agent helps consultants avoid data mismatch issues by capturing timesheet entries, "
#         "verifying them across required systems, and updating them when needed."
#     ),
#     tools=[
#         "screenshot_capture_tool",
#         "ocr_extraction_tool",
#         "timesheet_verification_tool",
#         "timesheet_update_tool"
#     ]
# )


# #----------------------------------------------------------------------------------------------------------------------------

# # streamlit_app.py
# import streamlit as st

# # ==========================
# # Dashboard Styling
# # ==========================

# st.set_page_config(page_title="Timesheet AI Agent Dashboard", layout="wide")

# # Inject custom CSS for header and footer styling
# st.markdown("""
#     <style>
#         /* Header styling */
#         .header {
#             background: linear-gradient(90deg, #ff4b5c, #ffffff, #1982c4);
#             padding: 20px;
#             border-radius: 10px;
#             color: black;
#             text-align: center;
#             border: 2px solid #00000030;
#         }
#         /* Footer styling */
#         .footer {
#             background: linear-gradient(90deg, #1982c4, #ffffff, #ff4b5c);
#             padding: 10px;
#             border-radius: 10px;
#             color: black;
#             text-align: center;
#             border: 2px solid #00000030;
#             margin-top: 50px;
#         }
#         /* Main content styling */
#         .main-content {
#             padding: 20px;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # ==========================
# # Header
# # ==========================
# st.markdown('<div class="header"><h1>🕒 Timesheet AI Agent Dashboard</h1></div>', unsafe_allow_html=True)

# # ==========================
# # Main Content
# # ==========================
# st.markdown('<div class="main-content">', unsafe_allow_html=True)

# st.write("Welcome to the **Timesheet AI Agent**. This agent helps ensure your timesheet data is consistent across multiple systems by capturing, verifying, and updating entries seamlessly.")

# # Buttons for each function (link these to your actual agent triggers)
# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     if st.button("📸 Capture Screenshot"):
#         st.success("Screenshot captured successfully. (Simulated)")

# with col2:
#     if st.button("🔍 Extract Data (OCR)"):
#         st.success("Timesheet data extracted. (Simulated)")

# with col3:
#     if st.button("✅ Verify Data"):
#         st.success("Data verified across systems. (Simulated)")

# with col4:
#     if st.button("🔄 Update Systems"):
#         st.success("Timesheet data updated. (Simulated)")

# # Display current status (placeholder)
# st.info("All systems are synchronized. No mismatches found. (Simulated)")

# st.markdown('</div>', unsafe_allow_html=True)

# # ==========================
# # Footer
# # ==========================
# st.markdown('<div class="footer">Developed by Your Team | Timesheet AI Agent © 2025</div>', unsafe_allow_html=True)


# #----------------------------------------------------------------------------------------------------------------------------

# # timesheet_tasks.py
# from crewai import Task
# from tools.screenshot_tool import capture_screenshot
# from tools.ocr_tool import extract_timesheet_data
# from tools.timesheet_verifier import verify_timesheet
# from tools.timesheet_updater import update_timesheet

# # Task 1: Capture Screenshot
# capture_timesheet_task = Task(
#     description="Capture the timesheet screenshot from the user device.",
#     tool=capture_screenshot
# )

# # Task 2: Extract Data
# extract_timesheet_task = Task(
#     description="Extract timesheet data using OCR from the screenshot.",
#     tool=extract_timesheet_data
# )

# # Task 3: Verify Data
# verify_timesheet_task = Task(
#     description="Verify extracted timesheet data across systems.",
#     tool=verify_timesheet
# )

# # Task 4: Update Data
# update_timesheet_task = Task(
#     description="Update timesheet data in systems if mismatched.",
#     tool=update_timesheet
# )


# #----------------------------------------------------------------------------------------------------------------------------

# #  screenshot_tool.py
# from crewai_tools import tool
# import pyautogui

# @tool("screenshot_capture_tool")
# def capture_screenshot(filename="timesheet.png"):
#     """
#     Captures a screenshot and saves it as 'timesheet.png' by default.
#     """
#     screenshot = pyautogui.screenshot()
#     screenshot.save(filename)
#     return f"Screenshot saved as {filename}"

# #----------------------------------------------------------------------------------------------------------------------------

# #  ocr_tool.py
# from crewai_tools import tool
# import pytesseract
# from PIL import Image

# @tool("ocr_extraction_tool")
# def extract_timesheet_data(image_path):
#     """
#     Extracts text data from a screenshot image.
#     """
#     img = Image.open(image_path)
#     text = pytesseract.image_to_string(img)
#     return text

# #----------------------------------------------------------------------------------------------------------------------------

# #  timesheet_verifier.py
# from crewai_tools import tool

# @tool("timesheet_verification_tool")
# def verify_timesheet(data, systems=[]):
#     """
#     Verifies timesheet data against multiple systems.
#     Returns a list of mismatches or confirmation.
#     """
#     # Placeholder: Implement API calls / web automation to check data in systems
#     results = {}
#     for system in systems:
#         results[system] = f"Verified in {system}"  # Simulated response
#     return results

# #----------------------------------------------------------------------------------------------------------------------------

# #  timesheet_updater.py
# from crewai_tools import tool

# @tool("timesheet_update_tool")
# def update_timesheet(data, systems=[]):
#     """
#     Updates timesheet data in multiple systems.
#     Returns status of each update.
#     """
#     # Placeholder: Implement API calls or browser automation to update entries
#     updates = {}
#     for system in systems:
#         updates[system] = f"Updated in {system}"  # Simulated response
#     return updates

# #----------------------------------------------------------------------------------------------------------------------------

# #  gemini_tools.py
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load environment variables from .env file
# load_dotenv()

# # Get Gemini API key from environment
# api_key = os.getenv("GOOGLE_API_KEY")

# if not api_key:
#     raise ValueError("Google API key not found. Please set GOOGLE_API_KEY in your .env file.")

# # Configure Gemini
# genai.configure(api_key=api_key)

# def summarize_timesheet_with_gemini(timesheet_text):
#     """
#     Summarize timesheet data using Gemini 1.5 Flash (latest).
    
#     Args:
#         timesheet_text (str): Raw timesheet data as text.
    
#     Returns:
#         str: Summarized timesheet output.
#     """
#     model = genai.GenerativeModel("gemini-1.5-flash-latest")
#     response = model.generate_content(
#         f"Summarize this timesheet data clearly and concisely for reporting:\n\n{timesheet_text}"
#     )
#     return response.text

# # Example usage for standalone testing
# if __name__ == "__main__":
#     sample_text = """
#     2025-07-21, Project Planning, 4, Initial project kickoff meeting
#     2025-07-21, Coding Module A, 3, Developed main algorithm
#     2025-07-22, Code Review, 2, Reviewed teammate's code
#     """
#     summary = summarize_timesheet_with_gemini(sample_text)
#     print("Gemini 1.5 Flash Summary:\n", summary)

# #----------------------------------------------------------------------------------------------------------------------------

# #  crew.py
# from crewai import Crew
# from agents.timesheet_agent import timesheet_agent
# from tasks.timesheet_tasks import (
#     capture_timesheet_task,
#     extract_timesheet_task,
#     verify_timesheet_task,
#     update_timesheet_task
# )

# timesheet_crew = Crew(
#     agents=[timesheet_agent],
#     tasks=[
#         capture_timesheet_task,
#         extract_timesheet_task,
#         verify_timesheet_task,
#         update_timesheet_task
#     ]
# )

# #----------------------------------------------------------------------------------------------------------------------------

# #  main.py
# from crew import timesheet_crew

# if __name__ == "__main__":
#     result = timesheet_crew.kickoff()
#     print("Timesheet Agent Workflow Result:")
#     print(result)

# #----------------------------------------------------------------------------------------------------------------------------

# #  requirements.txt
# # Core AI agent framework
# crewai

# # Streamlit for dashboard UI
# streamlit

# # OCR dependencies
# pytesseract
# Pillow

# # Screenshot capture
# pyautogui

# # For structured file operations and APIs (if needed later)
# requests

# # Optional: If your OCR tool requires tesseract installed on system
# # Make sure tesseract is installed in your environment
# # For Ubuntu: sudo apt install tesseract-ocr

# # Optional: Selenium if browser automation is planned
# # selenium
# google-generativeai
# crewai
# #----------------------------------------------------------------------------------------------------------------------------

# #  README.md

# # Timesheet AI Agent

# ## Purpose
# Ensures consultants' timesheet data is consistent across multiple systems by capturing, verifying, and updating entries using Crew AI workflows.

# ## Folder Structure
# - agents/ : Timesheet agent definition
# - tasks/ : Tasks for screenshot capture, OCR, verification, update
# - tools/ : Tools for screenshot, OCR, verification, update
# - crew.py : Assembles agent and tasks
# - main.py : Runs the agent

# ## Run
# ```bash
# pip install -r requirements.txt
# python main.py

# #----------------------------------------------------------------------------------------------------------------------------
