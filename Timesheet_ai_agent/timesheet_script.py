# '''
# >agents
#     --correction_agent.py
#     --notification_agent.py
#     --ocr_extraction_agent.py
#     --screenshot_agent.py
#     --system_update_agent.py
#     --timesheet_agent.py
#     --verification_agent.py
# >app
#     --streamlit_app.py
# >crew
#     --main.py
# >data
#     >outputys
# >myenv
# >tasks
#     --tasks_sheet.py
# >tools
#     --file_screenshot_tool.py
#     --gemini_client.py
#     --ocr_tool.py
#     --system_api.py
#     --timesheet_verifier.py
# >uploads
    
# '''

# #here is the all updated files of  this timesheet agents

# # correction_agent.py
# class CorrectionAgent:
#     def __init__(self):
#         pass

#     def run(self, verified_df):
#         print("[CorrectionAgent] Correcting mismatched data.")
#         corrected_df = verified_df.copy()
#         corrected_df.loc[corrected_df['Hours'] < 7, 'Hours'] = 8
#         corrected_df['Corrected'] = True
#         return corrected_df

# #--------------------------------------------------------------------------------------------------------------------------------
# # notification_agent.py
# class NotificationAgent:
#     def __init__(self):
#         pass

#     def run(self, message):
#         print(f"[NotificationAgent] Sending notification: {message}")
#         # 🔧 Dummy notification result
#         return "Notification sent."

# #--------------------------------------------------------------------------------------------------------------------------------

# # ocr_extraction_agent.py
# import pandas as pd

# class OCRExtractionAgent:
#     def __init__(self):
#         pass

#     def run(self, screenshot_path):
#         print(f"[OCRExtractionAgent] Extracting data from {screenshot_path}")
#         # 🔧 Dummy DataFrame for scaffold
#         data = {
#             'Employee': ['John', 'Sarah'],
#             'Hours': [8, 6]
#         }
#         return pd.DataFrame(data)

# #--------------------------------------------------------------------------------------------------------------------------------

# # screenshot_agent.py

# class ScreenshotCaptureAgent:
#     def __init__(self):
#         pass

#     def run(self, file_path):
#         # 🔧 Placeholder logic for screenshot capture
#         print(f"[ScreenshotCaptureAgent] Capturing screenshot for {file_path}")
#         screenshot_path = f"{file_path}_screenshot.png"
#         return screenshot_path

# #--------------------------------------------------------------------------------------------------------------------------------

# # system_update_agent.py
# class SystemUpdateAgent:
#     def __init__(self):
#         pass

#     def run(self, corrected_df):
#         print("[SystemUpdateAgent] Updating systems with corrected data.")
#         # 🔧 Dummy update confirmation
#         return "System updated successfully."

# #--------------------------------------------------------------------------------------------------------------------------------

# # timesheet_agent.py
# # agents/timesheet_agent.py

# from tools.gemini_client import gemini_generate, gemini_chat

# class TimesheetAgent:
#     def __init__(self):
#         pass

#     def summarize_timesheet(self, extracted_df):
#         """
#         Uses gemini_generate to summarize the extracted timesheet data.
#         """
#         prompt = f"Summarize this timesheet data:\n{extracted_df.to_string(index=False)}"
#         summary = gemini_generate(prompt)
#         return summary

#     def explain_verification(self, verified_df):
#         """
#         Uses gemini_chat for an interactive explanation of verification.
#         """
#         prompt = f"Explain the verification results in detail:\n{verified_df.to_string(index=False)}"
#         explanation = gemini_chat(prompt)
#         return explanation

# #--------------------------------------------------------------------------------------------------------------------------------

# # verification_agent.py

# from tools.gemini_client import gemini_generate

# class TimesheetVerificationAgent:
#     def __init__(self):
#         pass

#     def run(self, extracted_df):
#         print("[TimesheetVerificationAgent] Verifying extracted data with Gemini.")
        
#         # 🔧 Convert dataframe to string for prompt context
#         table_text = extracted_df.to_string()
        
#         prompt = f"""
#         You are a timesheet verification AI agent.
#         Below is the timesheet data:

#         {table_text}

#         Identify rows where Reported_Hours and System_Hours do not match.
#         Return instructions to correct them clearly in tabular format.
#         """

#         correction_instructions = gemini_generate(prompt)

#         # For now, print instructions. Later parse and apply corrections.
#         print("Gemini correction instructions:\n", correction_instructions)

#         # Dummy logic – flag hours < 7 as mismatched and correct to 8
#         extracted_df['Verified'] = extracted_df['Hours'] >= 7
#         return extracted_df

# #--------------------------------------------------------------------------------------------------------------------------------
# # streamlit_app.py


# import streamlit as st
# import pandas as pd
# import os
# import sys
# import time
# from PIL import Image
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# load_dotenv(dotenv_path="../.env")

# # Add root path for module imports
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from tools.file_screenshot_tool import capture_csv_as_image, load_clean_csv
# from tools.ocr_tool import extract_table_from_image
# from tools.timesheet_verifier import verify_timesheet
# from tools.system_api import apply_corrections
# from tools.gemini_client import gemini_generate, gemini_chat

# st.set_page_config(page_title="Timesheet AI Agent", layout="wide")

# st.markdown("""
#     <style>
#         .header {
#             background: linear-gradient(90deg, #87CEEB, #ffffff, #ff4b5c);
#             padding: 25px;
#             border-radius: 10px;
#             color: black;
#             text-align: center;
#             border: 2px solid #00000030;
#             margin-bottom: 30px;
#         }
#         .footer {
#             background: linear-gradient(90deg, #ff4b5c, #ffffff, #87CEEB);
#             padding: 15px;
#             border-radius: 10px;
#             color: black;
#             text-align: center;
#             border: 2px solid #00000030;
#             margin-top: 50px;
#         }
#         .stButton>button {
#             background-color: #1982c4;
#             color: white;
#             border-radius: 8px;
#             height: 3em;
#             width: 100%;
#         }
#     </style>
# """, unsafe_allow_html=True)

# st.markdown('<div class="header"><h1>🕒 Timesheet AI Agent Dashboard</h1></div>', unsafe_allow_html=True)

# # Upload Master Timesheet
# st.subheader("📥 Upload Master Timesheet")
# master_csv = st.file_uploader("Upload Master Timesheet CSV", type=["csv"], key="master")

# if master_csv is not None:
#     os.makedirs("uploads", exist_ok=True)
#     master_path = os.path.join("uploads", master_csv.name)
#     with open(master_path, "wb") as f:
#         f.write(master_csv.getbuffer())
#     st.success(f"✅ Master file uploaded: {master_csv.name}")
# else:
#     st.warning("⚠️ Please upload the Master Timesheet CSV before proceeding.")

# # Select File from Downloads Folder
# csv_folder = "/home/digi2/Downloads"
# csv_files = [f for f in os.listdir(csv_folder) if f.endswith(".csv")]
# selected_csv = st.selectbox("📂 Select a CSV file from Downloads", csv_files)

# # Screenshot and Process
# if st.button("📸 Capture Screenshot and Process"):

#     if master_csv is None:
#         st.error("❌ Upload the master CSV first.")
#         st.stop()

#     progress = st.progress(0, text="Initializing...")

#     try:
#         progress.progress(10, text="🔍 Reading selected file...")
#         csv_path = os.path.join(csv_folder, selected_csv)
#         st.info(f"Selected file: `{selected_csv}`")

#         # Step 1: Screenshot
#         progress.progress(25, text="📸 Taking screenshot...")
#         image_path = capture_csv_as_image(csv_path)
#         st.session_state["screenshot_path"] = image_path

#         # Step 2: Load and Clean
#         progress.progress(50, text="🧹 Cleaning CSV data...")
#         df_extracted = pd.read_csv(csv_path)  # Use original headers as-is

#         if df_extracted.empty or df_extracted.shape[1] < 2:
#             raise ValueError("No valid rows match header length. Check OCR output formatting.")

#         st.session_state["extracted_df"] = df_extracted

#         # Show Screenshot + Table
#         st.markdown("### 📸 Screenshot and Extracted Data")
#         col1, col2 = st.columns([1, 2])
#         with col1:
#             st.markdown("**Screenshot of Timesheet:**")
#             screenshot_img = Image.open(image_path)
#             st.image(screenshot_img, caption="📸 Captured Timesheet", use_container_width=True)
#         with col2:
#             st.markdown("**Extracted Timesheet Table:**")
#             st.dataframe(df_extracted, use_container_width=True)

#         # Step 3: Load Master
#         progress.progress(65, text="📂 Loading Master Timesheet...")
#         master_df = pd.read_csv(master_path)
#         st.subheader("🗂️ Master Timesheet")
#         st.dataframe(master_df, use_container_width=True)

#         # Step 4: Verify Timesheet
#         progress.progress(80, text="🧪 Verifying for mismatches...")
#         discrepancies = verify_timesheet(df_extracted, master_df)

#         if isinstance(discrepancies, list) and discrepancies:
#             st.warning("⚠️ Discrepancies Found!")
#             st.subheader("📌 Discrepancies (as JSON):")
#             st.json(discrepancies)

#             prompt = f"These discrepancies were found in the timesheet data:\n{discrepancies}\n\nSummarize and suggest corrections."
#             suggestion = gemini_generate(prompt)
#             st.markdown("### 🤖 Gemini Suggestion:")
#             st.info(suggestion)

#             corrected_df = apply_corrections(df_extracted, discrepancies)
#             st.subheader("✅ Corrected Timesheet")
#             st.dataframe(corrected_df, use_container_width=True)
#             st.session_state["corrected_df"] = corrected_df

#         elif isinstance(discrepancies, str) and "Error" in discrepancies:
#             st.error(discrepancies)
#         else:
#             st.success("✅ No discrepancies found.")

#         progress.progress(100, text="✅ Done.")

#     except Exception as e:
#         st.error(f"❌ Error during verification: {str(e)}")
#         progress.empty()

# # Summarize Extracted Data
# if st.button("📝 Summarize Extracted Data"):
#     if 'extracted_df' in st.session_state:
#         progress = st.progress(0, text="Sending data to Gemini...")
#         try:
#             time.sleep(1)
#             sample_df = st.session_state.extracted_df.head(10)
#             prompt = (
#                 "You are a Timesheet AI Agent.\n\n"
#                 "Below is a table of timesheet data. Summarize this in plain language:\n\n"
#                 f"{sample_df.to_string(index=False)}"
#             )
#             summary = gemini_generate(prompt)
#             progress.progress(100, text="✅ Summary complete.")
#             st.subheader("📄 Gemini Summary")
#             st.write(summary)
#         except Exception as e:
#             st.error(f"❌ Gemini summarization failed: {e}")
#             progress.empty()
#     else:
#         st.warning("⚠️ Please extract data first.")

# # Explain Corrections
# if st.button("💬 Explain Corrections"):
#     if 'corrected_df' in st.session_state:
#         progress = st.progress(0, text="Explaining corrections...")
#         try:
#             time.sleep(1)
#             explanation = gemini_chat(
#                 f"Explain the corrections made to this timesheet data:\n{st.session_state.corrected_df.to_string(index=False)}"
#             )
#             progress.progress(100)
#             st.subheader("💡 Gemini Explanation")
#             st.write(explanation)
#         except Exception as e:
#             st.error(f"❌ Gemini explanation failed: {e}")
#             progress.empty()
#     else:
#         st.warning("⚠️ No corrected data to explain.")

# # Footer
# st.markdown('<div class="footer">Developed by Digiprima Technologies | Timesheet AI Agent © 2025</div>', unsafe_allow_html=True)

# #--------------------------------------------------------------------------------------------------------------------------------
# # main.py


# from tasks.tasks_sheet import define_tasks

# def run_timesheet_pipeline():
#     """
#     Runs the Timesheet AI Agent pipeline sequentially using defined tasks.
#     Returns:
#         dict: Outputs from each task.
#     """

#     # Initialize inputs (replace this with dynamic user input in production)
#     inputs = {
#         "file_path": "/path/to/timesheet.csv"  # 🔧 Replace with user input or upload in your Streamlit app
#     }
#     outputs = {}

#     try:
#         tasks = define_tasks()

#         for task in tasks:
#             agent = task["agent"]
#             input_data = inputs.get(task["input_key"]) or outputs.get(task["input_key"])

#             # Ensure input data is available before running agent
#             if input_data is None:
#                 raise ValueError(f"Missing input for task: {task['name']}")

#             result = agent.run(input_data)
#             outputs[task["output_key"]] = result

#         return outputs

#     except Exception as e:
#         # Return error details for Streamlit display
#         return {"error": str(e)}

# #--------------------------------------------------------------------------------------------------------------------------------
# # tasks_sheet.py

# from agents.screenshot_agent import ScreenshotCaptureAgent
# from agents.ocr_extraction_agent import OCRExtractionAgent
# from agents.verification_agent import TimesheetVerificationAgent
# from agents.correction_agent import CorrectionAgent
# from agents.system_update_agent import SystemUpdateAgent

# def define_tasks():
#     return [
#         {
#             "name": "Capture Screenshot",
#             "agent": ScreenshotCaptureAgent(),
#             "input_key": "file_path",
#             "output_key": "screenshot_path"
#         },
#         {
#             "name": "Extract Data",
#             "agent": OCRExtractionAgent(),
#             "input_key": "screenshot_path",
#             "output_key": "extracted_df"
#         },
#         {
#             "name": "Verify Data",
#             "agent": TimesheetVerificationAgent(),
#             "input_key": "extracted_df",
#             "output_key": "verified_df"
#         },
#         {
#             "name": "Correct Data",
#             "agent": CorrectionAgent(),
#             "input_key": "verified_df",
#             "output_key": "corrected_df"
#         },
#         {
#             "name": "Update Systems",
#             "agent": SystemUpdateAgent(),
#             "input_key": "corrected_df",
#             "output_key": "update_status"
#         }
#     ]

# #--------------------------------------------------------------------------------------------------------------------------------
# # file_screenshoot_tool.py


# import pandas as pd
# from PIL import Image, ImageDraw, ImageFont
# import os
# from datetime import datetime

# def capture_csv_as_image(csv_path, output_dir="uploads"):
#     # ✅ Step 1: Load and clean CSV
#     try:
#         df = pd.read_csv(csv_path, encoding="utf-8", on_bad_lines='skip')
#     except Exception as e:
#         raise ValueError(f"Error reading CSV: {e}")

#     df.dropna(how='all', inplace=True)
#     df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
#     df = df.dropna(how='any')
#     df = df[~(df == '').any(axis=1)]

#     if df.empty:
#         raise ValueError("CSV has no valid data rows after cleaning.")

#     # ✅ Step 2: Set font
#     try:
#         font = ImageFont.load_default()
#     except Exception as e:
#         raise RuntimeError("Font loading failed.") from e

#     padding = 10
#     row_height = 25
#     col_widths = []

#     # ✅ Step 3: Calculate column widths
#     for col in df.columns:
#         max_len = max(df[col].astype(str).apply(len).max(), len(col))
#         col_widths.append((max_len + 2) * 8)  # Adjust width per character

#     table_width = sum(col_widths) + padding * 2
#     table_height = (len(df) + 1) * row_height + padding * 2

#     image = Image.new("RGB", (table_width, table_height), "white")
#     draw = ImageDraw.Draw(image)

#     # ✅ Step 4: Draw headers
#     x = padding
#     y = padding
#     for i, col in enumerate(df.columns):
#         draw.rectangle([x, y, x + col_widths[i], y + row_height], outline="black")
#         draw.text((x + 5, y + 5), col, fill="black", font=font)
#         x += col_widths[i]

#     # ✅ Step 5: Draw rows
#     for row_idx, row in df.iterrows():
#         x = padding
#         y += row_height
#         for i, col in enumerate(df.columns):
#             cell_value = str(row[col])
#             draw.rectangle([x, y, x + col_widths[i], y + row_height], outline="gray")
#             draw.text((x + 5, y + 5), cell_value, fill="black", font=font)
#             x += col_widths[i]

#     # ✅ Step 6: Save image
#     os.makedirs(output_dir, exist_ok=True)
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     image_path = os.path.join(output_dir, f"csv_screenshot_{timestamp}.png")
#     image.save(image_path)

#     return image_path

# # Optional: Return cleaned DataFrame for further use
# def load_clean_csv(csv_path):
#     df = pd.read_csv(csv_path, encoding="utf-8", on_bad_lines='skip')
#     df.dropna(how='all', inplace=True)
#     df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
#     df = df.dropna(how='any')
#     df = df[~(df == '').any(axis=1)]
#     return df

# #--------------------------------------------------------------------------------------------------------------------------------

# # gemini_client.py


# import os
# import google.generativeai as genai
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Get Gemini API Key
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # ✅ Validate API Key
# if not GEMINI_API_KEY:
#     raise EnvironmentError("❌ GEMINI_API_KEY is not set or is invalid. Please update your .env file with a valid API key.")

# # Configure Gemini client
# genai.configure(api_key=GEMINI_API_KEY)

# # ===================================
# # 🔧 Function 1: gemini_generate
# # ===================================
# def gemini_generate(prompt_text, model_name="gemini-1.5-flash"):
#     """
#     Generates a single-shot response using Gemini for the provided prompt.
#     """
#     try:
#         model = genai.GenerativeModel(model_name)
#         response = model.generate_content(prompt_text)
#         return response.text
#     except Exception as e:
#         return f"❌ Gemini generate error: {str(e)}"

# # ===================================
# # 🔧 Function 2: gemini_chat
# # ===================================
# def gemini_chat(prompt_text, model_name="gemini-1.5-flash"):
#     """
#     Sends a message in a new chat session with Gemini (multi-turn reasoning).
#     """
#     try:
#         model = genai.GenerativeModel(model_name)
#         chat = model.start_chat(history=[])
#         response = chat.send_message(prompt_text)
#         return response.text
#     except Exception as e:
#         return f"❌ Gemini chat error: {str(e)}"

# # ===================================
# # ✨ Function 3: get_gemini_correction
# # ===================================
# def get_gemini_correction(discrepancies, model_name="gemini-1.5-flash"):
#     """
#     Prompts Gemini to correct timesheet discrepancies and suggest explanations.
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


# #--------------------------------------------------------------------------------------------------------------------------------

# # ocr_tool.py

# import pytesseract
# import cv2 
# import pandas as pd

# def extract_table_from_image(image_path):
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # OCR extraction
#     text = pytesseract.image_to_string(gray)

#     # Split into lines and then into cells (by whitespace or tabs)
#     lines = text.strip().split("\n")
#     rows = [line.strip().split() for line in lines if line.strip()]

#     if not rows:
#         return pd.DataFrame()  # Return empty if no rows found

#     header = rows[0]
#     valid_data_rows = [row for row in rows[1:] if len(row) == len(header)]

#     if not valid_data_rows:
#         raise ValueError("No valid rows match header length. Check OCR output formatting.")

#     df = pd.DataFrame(valid_data_rows, columns=header)
#     return df


# #--------------------------------------------------------------------------------------------------------------------------------

# # system_api.py

# def apply_corrections(df, discrepancies):
#     for d in discrepancies:
#         df.loc[df["Employee_ID"] == d["Employee_ID"], "Hours"] = d["Expected"]
#     return df

# #--------------------------------------------------------------------------------------------------------------------------------

# # timesheet_verifier.py


# def verify_timesheet(screenshot_df, master_df):
#     discrepancies = []

#     for i, row in screenshot_df.iterrows():
#         emp_name = row["Employee"]
#         date = row["Date"]
#         hours = row["Hours"]

#         # Match on Employee name and Date
#         master_row = master_df[(master_df["Employee"] == emp_name) & (master_df["Date"] == date)]

#         if not master_row.empty:
#             expected_hours = master_row.iloc[0]["Hours"]
#             if str(expected_hours) != str(hours):
#                 discrepancies.append({
#                     "Employee": emp_name,
#                     "Date": date,
#                     "Expected": expected_hours,
#                     "Found": hours
#                 })

#     return discrepancies

# #--------------------------------------------------------------------------------------------------------------------------------
