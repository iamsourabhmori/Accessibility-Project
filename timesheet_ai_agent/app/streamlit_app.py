
#---------------------------------------------------------------------------------------------------------------------------------------------------------

# import streamlit as st
# import sys
# import os
# import importlib.util
# import glob

# # ==========================
# # Fix Python path for tools module
# # ==========================
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# # ==========================
# # Dynamically load file_screenshot_tool.py
# # ==========================
# file_screenshot_tool_path = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), '../tools/file_screenshot_tool.py')
# )
# spec = importlib.util.spec_from_file_location("file_screenshot_tool", file_screenshot_tool_path)
# file_screenshot_tool = importlib.util.module_from_spec(spec)
# sys.modules["file_screenshot_tool"] = file_screenshot_tool
# spec.loader.exec_module(file_screenshot_tool)

# # Access function
# capture_file_screenshot = file_screenshot_tool.capture_file_screenshot

# # ==========================
# # Streamlit Page Config & Styling
# # ==========================
# st.set_page_config(page_title="Timesheet AI Agent Dashboard", layout="wide")

# st.markdown("""
#     <style>
#         .header {
#             background: linear-gradient(90deg, #ff4b5c, #ffffff, #1982c4);
#             padding: 20px;
#             border-radius: 10px;
#             color: black;
#             text-align: center;
#             border: 2px solid #00000030;
#         }
#         .footer {
#             background: linear-gradient(90deg, #1982c4, #ffffff, #ff4b5c);
#             padding: 10px;
#             border-radius: 10px;
#             color: black;
#             text-align: center;
#             border: 2px solid #00000030;
#             margin-top: 50px;
#         }
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
# # Main Content - File Selection
# # ==========================
# st.markdown('<div class="main-content">', unsafe_allow_html=True)

# st.write("Welcome to the **Timesheet AI Agent**. Select a CSV file from Downloads to capture its screenshot and extract data.")

# # 🔧 List all CSV files from /home/digi2/Downloads
# csv_files = glob.glob('/home/digi2/Downloads/*.csv')

# # Insert a default placeholder option at the top
# csv_files_display = ["-- Select a CSV file --"] + csv_files

# # Show as selectbox with placeholder
# selected_csv = st.selectbox("Select a CSV file from Downloads folder", csv_files_display)

# # Check selection validity
# if selected_csv == "-- Select a CSV file --":
#     selected_csv = None

# # ==========================
# # Action Buttons
# # ==========================
# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     if st.button("📸 Capture CSV Screenshot"):
#         if selected_csv:
#             st.write(f"Opening {selected_csv} and capturing screenshot...")
#             try:
#                 screenshot_path = capture_file_screenshot(selected_csv)
#                 st.success(f"Screenshot captured and saved at: {screenshot_path}")
#                 st.image(screenshot_path, caption="CSV Screenshot")

#                 # 🔧 OCR processing placeholder
#                 st.info("Sending screenshot to OCR tool for data extraction...")
#                 # extracted_data = extract_data_from_screenshot(screenshot_path)
#                 # st.write(extracted_data)

#             except Exception as e:
#                 st.error(f"Error capturing CSV screenshot: {e}")
#         else:
#             st.warning("Please select a CSV file first.")

# with col2:
#     if st.button("🔍 Extract Data (OCR)"):
#         st.success("Timesheet data extracted. (Simulated)")

# with col3:
#     if st.button("✅ Verify Data"):
#         st.success("Data verified across systems. (Simulated)")

# with col4:
#     if st.button("🔄 Update Systems"):
#         st.success("Timesheet data updated. (Simulated)")

# # ==========================
# # Footer
# # ==========================
# st.markdown('</div>', unsafe_allow_html=True)
# st.markdown('<div class="footer">Developed by Digiprima Technologies | Timesheet AI Agent © 2025</div>', unsafe_allow_html=True)



#-------------------------------------------------------------------------------------------------------------------------------------------------------


# import streamlit as st
# import sys
# import os
# import importlib.util
# import tkinter as tk
# from tkinter import filedialog

# # ==========================
# # Fix Python path for tools module
# # ==========================
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# # ==========================
# # Dynamically load file_screenshot_tool.py
# # ==========================
# file_screenshot_tool_path = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), '../tools/file_screenshot_tool.py')
# )
# spec = importlib.util.spec_from_file_location("file_screenshot_tool", file_screenshot_tool_path)
# file_screenshot_tool = importlib.util.module_from_spec(spec)
# sys.modules["file_screenshot_tool"] = file_screenshot_tool
# spec.loader.exec_module(file_screenshot_tool)

# # Access function
# capture_file_screenshot = file_screenshot_tool.capture_file_screenshot

# # ==========================
# # Streamlit Page Config & Styling
# # ==========================
# st.set_page_config(page_title="Timesheet AI Agent Dashboard", layout="wide")

# st.markdown("""
#     <style>
#         .header {
#             background: linear-gradient(90deg, #ff4b5c, #ffffff, #1982c4);
#             padding: 20px;
#             border-radius: 10px;
#             color: black;
#             text-align: center;
#             border: 2px solid #00000030;
#         }
#         .footer {
#             background: linear-gradient(90deg, #1982c4, #ffffff, #ff4b5c);
#             padding: 10px;
#             border-radius: 10px;
#             color: black;
#             text-align: center;
#             border: 2px solid #00000030;
#             margin-top: 50px;
#         }
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

# st.write("Welcome to the **Timesheet AI Agent**. Click the button below to select a CSV file from Downloads for screenshot and extraction.")

# # ==========================
# # Action Buttons
# # ==========================
# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     if st.button("📸 Capture CSV Screenshot"):
#         # Use tkinter filedialog for native file picker
#         root = tk.Tk()
#         root.withdraw()  # hide main window

#         # Open file dialog in specified folder
#         file_path = filedialog.askopenfilename(
#             initialdir="/home/digi2/Downloads",
#             title="Select a CSV file",
#             filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
#         )
#         root.destroy()

#         if file_path:
#             st.write(f"Selected file: {file_path}. Capturing screenshot...")
#             try:
#                 screenshot_path = capture_file_screenshot(file_path)
#                 st.success(f"Screenshot captured and saved at: {screenshot_path}")
#                 st.image(screenshot_path, caption="CSV Screenshot")

#                 # 🔧 OCR processing placeholder
#                 st.info("Sending screenshot to OCR tool for data extraction...")
#                 # extracted_data = extract_data_from_screenshot(screenshot_path)
#                 # st.write(extracted_data)

#             except Exception as e:
#                 st.error(f"Error capturing CSV screenshot: {e}")
#         else:
#             st.warning("No file selected.")

# with col2:
#     if st.button("🔍 Extract Data (OCR)"):
#         st.success("Timesheet data extracted. (Simulated)")

# with col3:
#     if st.button("✅ Verify Data"):
#         st.success("Data verified across systems. (Simulated)")

# with col4:
#     if st.button("🔄 Update Systems"):
#         st.success("Timesheet data updated. (Simulated)")

# # ==========================
# # Footer
# # ==========================
# st.markdown('</div>', unsafe_allow_html=True)
# st.markdown('<div class="footer">Developed by Digiprima Technologies | Timesheet AI Agent © 2025</div>', unsafe_allow_html=True)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

# import streamlit as st
# import sys
# import os
# import importlib.util
# import tkinter as tk
# from tkinter import filedialog
# import pandas as pd

# # ==========================
# # Fix Python path for tools module
# # ==========================
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# # ==========================
# # Dynamically load file_screenshot_tool.py
# # ==========================
# file_screenshot_tool_path = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), '../tools/file_screenshot_tool.py')
# )
# spec = importlib.util.spec_from_file_location("file_screenshot_tool", file_screenshot_tool_path)
# file_screenshot_tool = importlib.util.module_from_spec(spec)
# sys.modules["file_screenshot_tool"] = file_screenshot_tool
# spec.loader.exec_module(file_screenshot_tool)

# capture_file_screenshot = file_screenshot_tool.capture_file_screenshot

# # ==========================
# # Dummy OCR Tool
# # ==========================
# def extract_data_from_screenshot(screenshot_path):
#     """
#     🔧 Placeholder OCR function: returns dummy DataFrame simulating extracted data.
#     Replace with your actual OCR implementation.
#     """
#     # Example dummy table data
#     data = {'Name': ['Alice', 'Bob'], 'Hours': [8, 6]}
#     df = pd.DataFrame(data)
#     return df

# # ==========================
# # Dummy Verification Tool
# # ==========================
# def verify_timesheet_data(extracted_df):
#     """
#     🔧 Dummy verification: flags hours < 7 as mismatched, corrects them to 8.
#     Returns: (verified_df, mismatches_found)
#     """
#     verified_df = extracted_df.copy()
#     mismatches = verified_df['Hours'] < 7
#     if mismatches.any():
#         verified_df.loc[mismatches, 'Hours'] = 8  # auto-correct
#         return verified_df, True
#     else:
#         return verified_df, False

# # ==========================
# # Streamlit UI Styling
# # ==========================
# st.set_page_config(page_title="Timesheet AI Agent Dashboard", layout="wide")

# st.markdown("""
#     <style>
#         .header {
#             background: linear-gradient(90deg, #ff4b5c, #ffffff, #1982c4);
#             padding: 20px;
#             border-radius: 10px;
#             color: black;
#             text-align: center;
#             border: 2px solid #00000030;
#         }
#         .footer {
#             background: linear-gradient(90deg, #1982c4, #ffffff, #ff4b5c);
#             padding: 10px;
#             border-radius: 10px;
#             color: black;
#             text-align: center;
#             border: 2px solid #00000030;
#             margin-top: 50px;
#         }
#         .main-content {
#             padding: 20px;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # ==========================
# # Header
# # ==========================
# st.markdown('<div class="header"><h1>🕒 Timesheet AI Agent Dashboard</h1></div>', unsafe_allow_html=True)

# st.markdown('<div class="main-content">', unsafe_allow_html=True)
# st.write("Welcome to the **Timesheet AI Agent**. Follow the steps below to capture, extract, verify, and update timesheet data seamlessly.")

# # ==========================
# # Session State Initialization
# # ==========================
# if 'screenshot_path' not in st.session_state:
#     st.session_state.screenshot_path = None
# if 'extracted_df' not in st.session_state:
#     st.session_state.extracted_df = None
# if 'verified_df' not in st.session_state:
#     st.session_state.verified_df = None
# if 'mismatches_found' not in st.session_state:
#     st.session_state.mismatches_found = False

# # ==========================
# # Action Buttons Pipeline
# # ==========================
# col1, col2, col3, col4 = st.columns(4)

# # Step 1: Capture Screenshot
# with col1:
#     if st.button("📸 Capture CSV Screenshot"):
#         root = tk.Tk()
#         root.withdraw()
#         file_path = filedialog.askopenfilename(
#             initialdir="/home/digi2/Downloads",
#             title="Select a CSV file",
#             filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
#         )
#         root.destroy()

#         if file_path:
#             st.write(f"Selected file: {file_path}. Capturing screenshot...")
#             try:
#                 screenshot_path = capture_file_screenshot(file_path)
#                 st.session_state.screenshot_path = screenshot_path
#                 st.success(f"Screenshot captured at: {screenshot_path}")
#                 st.image(screenshot_path, caption="CSV Screenshot")
#             except Exception as e:
#                 st.error(f"Error capturing CSV screenshot: {e}")
#         else:
#             st.warning("No file selected.")

# # Step 2: Extract Data (OCR)
# with col2:
#     if st.button("🔍 Extract Data (OCR)"):
#         if st.session_state.screenshot_path:
#             extracted_df = extract_data_from_screenshot(st.session_state.screenshot_path)
#             st.session_state.extracted_df = extracted_df
#             st.success("OCR extraction completed. Extracted table:")
#             st.dataframe(extracted_df)
#         else:
#             st.warning("Please capture a CSV screenshot first.")

# # Step 3: Verify Data
# with col3:
#     if st.button("✅ Verify Data"):
#         if st.session_state.extracted_df is not None:
#             verified_df, mismatches_found = verify_timesheet_data(st.session_state.extracted_df)
#             st.session_state.verified_df = verified_df
#             st.session_state.mismatches_found = mismatches_found

#             if mismatches_found:
#                 st.warning("Data mismatches found and corrected:")
#             else:
#                 st.success("No mismatches found. Data verified successfully.")

#             st.dataframe(verified_df)
#         else:
#             st.warning("Please extract data first.")

# # Step 4: Update Systems
# with col4:
#     if st.button("🔄 Update Systems"):
#         if st.session_state.verified_df is not None:
#             st.success("System updated with verified data.")

#             if st.session_state.mismatches_found:
#                 st.write("⚠️ **Before Update (Extracted Data):**")
#                 st.dataframe(st.session_state.extracted_df)

#                 st.write("✅ **After Update (Corrected Data):**")
#                 st.dataframe(st.session_state.verified_df)
#             else:
#                 st.write("✅ **Updated Data (No corrections needed):**")
#                 st.dataframe(st.session_state.verified_df)
#         else:
#             st.warning("Please verify data before updating systems.")

# # ==========================
# # Footer
# # ==========================
# st.markdown('</div>', unsafe_allow_html=True)
# st.markdown('<div class="footer">Developed by Digiprima Technologies | Timesheet AI Agent © 2025</div>', unsafe_allow_html=True)


#-----------------------------------------------------------------------------------------------------------------------------------
import streamlit as st
import sys
import os
import importlib.util
import tkinter as tk
from tkinter import filedialog
import pandas as pd

# ==========================
# Fix Python path for tools modules
# ==========================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ==========================
# Dynamically load file_screenshot_tool.py
# ==========================
file_screenshot_tool_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../tools/file_screenshot_tool.py')
)
spec = importlib.util.spec_from_file_location("file_screenshot_tool", file_screenshot_tool_path)
file_screenshot_tool = importlib.util.module_from_spec(spec)
sys.modules["file_screenshot_tool"] = file_screenshot_tool
spec.loader.exec_module(file_screenshot_tool)

capture_file_screenshot = file_screenshot_tool.capture_file_screenshot

# ==========================
# Dynamically load timesheet_verifier.py
# ==========================
timesheet_verifier_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../tools/timesheet_verifier.py')
)
spec2 = importlib.util.spec_from_file_location("timesheet_verifier", timesheet_verifier_path)
timesheet_verifier = importlib.util.module_from_spec(spec2)
sys.modules["timesheet_verifier"] = timesheet_verifier
spec2.loader.exec_module(timesheet_verifier)

verify_and_correct_timesheet = timesheet_verifier.verify_and_correct_timesheet

# ==========================
# Dummy OCR Tool (placeholder)
# ==========================
def extract_data_from_screenshot(screenshot_path):
    """
    🔧 Placeholder OCR function: returns dummy DataFrame simulating extracted data.
    Replace with your actual OCR implementation.
    """
    data = {
        'Employee': ['John', 'Sarah', 'Mike', 'Lisa', 'Alex'],
        'Date': ['2025-07-20']*5,
        'Task': ['Development', 'Testing', 'Documentation', 'Design', 'Review'],
        'Reported_Hours': [8, 7, 5, 6, 4],
        'System_Hours': [8, 8, 5, 6, 5],
        'Final_Hours': [8, 8, 5, 6, 5],
    }
    df = pd.DataFrame(data)
    return df

# ==========================
# Streamlit UI Styling
# ==========================
st.set_page_config(page_title="Timesheet AI Agent Dashboard", layout="wide")

st.markdown("""
    <style>
        .header {
            background: linear-gradient(90deg, #ff4b5c, #ffffff, #1982c4);
            padding: 20px;
            border-radius: 10px;
            color: black;
            text-align: center;
            border: 2px solid #00000030;
        }
        .footer {
            background: linear-gradient(90deg, #1982c4, #ffffff, #ff4b5c);
            padding: 10px;
            border-radius: 10px;
            color: black;
            text-align: center;
            border: 2px solid #00000030;
            margin-top: 50px;
        }
        .main-content {
            padding: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================
# Header
# ==========================
st.markdown('<div class="header"><h1>🕒 Timesheet AI Agent Dashboard</h1></div>', unsafe_allow_html=True)

st.markdown('<div class="main-content">', unsafe_allow_html=True)
st.write("Welcome to the **Timesheet AI Agent**. Follow the steps below to capture, extract, verify, and update timesheet data seamlessly.")

# ==========================
# Session State Initialization
# ==========================
if 'screenshot_path' not in st.session_state:
    st.session_state.screenshot_path = None
if 'extracted_df' not in st.session_state:
    st.session_state.extracted_df = None
if 'verified_df' not in st.session_state:
    st.session_state.verified_df = None
if 'corrected_df' not in st.session_state:
    st.session_state.corrected_df = None

# ==========================
# Action Buttons Pipeline
# ==========================
col1, col2, col3, col4 = st.columns(4)

# Step 1: Capture Screenshot
with col1:
    if st.button("📸 Capture CSV Screenshot"):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            initialdir="/home/digi2/Downloads",
            title="Select a CSV file",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        root.destroy()

        if file_path:
            st.write(f"Selected file: {file_path}. Capturing screenshot...")
            try:
                screenshot_path = capture_file_screenshot(file_path)
                st.session_state.screenshot_path = screenshot_path
                st.success(f"Screenshot captured at: {screenshot_path}")
                st.image(screenshot_path, caption="CSV Screenshot")
            except Exception as e:
                st.error(f"Error capturing CSV screenshot: {e}")
        else:
            st.warning("No file selected.")

# Step 2: Extract Data (OCR)
with col2:
    if st.button("🔍 Extract Data (OCR)"):
        if st.session_state.screenshot_path:
            extracted_df = extract_data_from_screenshot(st.session_state.screenshot_path)
            st.session_state.extracted_df = extracted_df
            st.success("OCR extraction completed. Extracted table:")
            st.dataframe(extracted_df)
        else:
            st.warning("Please capture a CSV screenshot first.")

# Step 3: Verify and Correct Data
with col3:
    if st.button("✅ Verify and Correct Data"):
        if st.session_state.extracted_df is not None:
            corrected_df = verify_and_correct_timesheet(st.session_state.extracted_df)
            st.session_state.corrected_df = corrected_df
            st.success("✅ Data verification and correction completed.")
            st.subheader("🛠️ Corrected Timesheet Data")
            st.dataframe(corrected_df)

            # Download corrected file
            corrected_csv = corrected_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "⬇️ Download Corrected CSV",
                corrected_csv,
                "timesheet_corrected.csv",
                "text/csv",
                key='download-corrected-csv'
            )
        else:
            st.warning("Please extract data first.")

# Step 4: Update Systems
with col4:
    if st.button("🔄 Update Systems"):
        if st.session_state.corrected_df is not None:
            st.success("System updated with verified and corrected data.")
            st.write("✅ **Updated Data:**")
            st.dataframe(st.session_state.corrected_df)
        else:
            st.warning("Please verify and correct data before updating systems.")

# ==========================
# Footer
# ==========================
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="footer">Developed by Digiprima Technologies | Timesheet AI Agent © 2025</div>', unsafe_allow_html=True)


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# import streamlit as st
# import sys
# import os
# import importlib.util
# import pandas as pd

# # ==========================
# # Fix Python path for tools modules
# # ==========================
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# # ==========================
# # Dynamically load file_screenshot_tool.py
# # ==========================
# file_screenshot_tool_path = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), '../tools/file_screenshot_tool.py')
# )
# spec = importlib.util.spec_from_file_location("file_screenshot_tool", file_screenshot_tool_path)
# file_screenshot_tool = importlib.util.module_from_spec(spec)
# sys.modules["file_screenshot_tool"] = file_screenshot_tool
# spec.loader.exec_module(file_screenshot_tool)

# capture_file_screenshot = file_screenshot_tool.capture_file_screenshot

# # ==========================
# # Dynamically load timesheet_verifier.py
# # ==========================
# timesheet_verifier_path = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), '../tools/timesheet_verifier.py')
# )
# spec2 = importlib.util.spec_from_file_location("timesheet_verifier", timesheet_verifier_path)
# timesheet_verifier = importlib.util.module_from_spec(spec2)
# sys.modules["timesheet_verifier"] = timesheet_verifier
# spec2.loader.exec_module(timesheet_verifier)

# verify_and_correct_timesheet = timesheet_verifier.verify_and_correct_timesheet

# # ==========================
# # Dummy OCR Tool (placeholder)
# # ==========================
# def extract_data_from_screenshot(screenshot_path):
#     """
#     🔧 Placeholder OCR function: returns dummy DataFrame simulating extracted data.
#     Replace with your actual OCR implementation.
#     """
#     data = {
#         'Employee': ['John', 'Sarah', 'Mike', 'Lisa', 'Alex'],
#         'Date': ['2025-07-20']*5,
#         'Task': ['Development', 'Testing', 'Documentation', 'Design', 'Review'],
#         'Reported_Hours': [8, 7, 5, 6, 4],
#         'System_Hours': [8, 8, 5, 6, 5],
#         'Final_Hours': [8, 8, 5, 6, 5],
#     }
#     df = pd.DataFrame(data)
#     return df

# # ==========================
# # Streamlit UI Styling
# # ==========================
# st.set_page_config(page_title="Timesheet AI Agent Dashboard", layout="wide")

# st.markdown("""
#     <style>
#         .header {
#             background: linear-gradient(90deg, #ff4b5c, #ffffff, #1982c4);
#             padding: 20px;
#             border-radius: 10px;
#             color: black;
#             text-align: center;
#             border: 2px solid #00000030;
#         }
#         .footer {
#             background: linear-gradient(90deg, #1982c4, #ffffff, #ff4b5c);
#             padding: 10px;
#             border-radius: 10px;
#             color: black;
#             text-align: center;
#             border: 2px solid #00000030;
#             margin-top: 50px;
#         }
#         .main-content {
#             padding: 20px;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # ==========================
# # Header
# # ==========================
# st.markdown('<div class="header"><h1>🕒 Timesheet AI Agent Dashboard</h1></div>', unsafe_allow_html=True)

# st.markdown('<div class="main-content">', unsafe_allow_html=True)
# st.write("Welcome to the **Timesheet AI Agent**. Follow the steps below to capture, extract, verify, and update timesheet data seamlessly.")

# # ==========================
# # Session State Initialization
# # ==========================
# if 'screenshot_path' not in st.session_state:
#     st.session_state.screenshot_path = None
# if 'extracted_df' not in st.session_state:
#     st.session_state.extracted_df = None
# if 'corrected_df' not in st.session_state:
#     st.session_state.corrected_df = None

# # ==========================
# # Action Buttons Pipeline
# # ==========================
# col1, col2, col3, col4 = st.columns(4)

# # Step 1: Capture Screenshot using file uploader
# with col1:
#     uploaded_file = st.file_uploader("Upload or select a CSV file", type=["csv"])
#     if uploaded_file is not None:
#         # Save uploaded file to temporary location
#         file_path = os.path.join("/tmp", uploaded_file.name)
#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.read())

#         st.write(f"Selected file saved at: {file_path}. Capturing screenshot...")
#         try:
#             screenshot_path = capture_file_screenshot(file_path)
#             st.session_state.screenshot_path = screenshot_path
#             st.success(f"Screenshot captured at: {screenshot_path}")
#             st.image(screenshot_path, caption="CSV Screenshot")
#         except Exception as e:
#             st.error(f"Error capturing CSV screenshot: {e}")
#     else:
#         st.warning("No file selected yet.")

# # Step 2: Extract Data (OCR)
# with col2:
#     if st.button("🔍 Extract Data (OCR)"):
#         if st.session_state.screenshot_path:
#             extracted_df = extract_data_from_screenshot(st.session_state.screenshot_path)
#             st.session_state.extracted_df = extracted_df
#             st.success("OCR extraction completed. Extracted table:")
#             st.dataframe(extracted_df)
#         else:
#             st.warning("Please capture a CSV screenshot first.")

# # Step 3: Verify and Correct Data
# with col3:
#     if st.button("✅ Verify and Correct Data"):
#         if st.session_state.extracted_df is not None:
#             corrected_df = verify_and_correct_timesheet(st.session_state.extracted_df)
#             st.session_state.corrected_df = corrected_df
#             st.success("✅ Data verification and correction completed.")
#             st.subheader("🛠️ Corrected Timesheet Data")
#             st.dataframe(corrected_df)

#             # Download corrected file
#             corrected_csv = corrected_df.to_csv(index=False).encode('utf-8')
#             st.download_button(
#                 "⬇️ Download Corrected CSV",
#                 corrected_csv,
#                 "timesheet_corrected.csv",
#                 "text/csv",
#                 key='download-corrected-csv'
#             )
#         else:
#             st.warning("Please extract data first.")

# # Step 4: Update Systems
# with col4:
#     if st.button("🔄 Update Systems"):
#         if st.session_state.corrected_df is not None:
#             st.success("System updated with verified and corrected data.")
#             st.write("✅ **Updated Data:**")
#             st.dataframe(st.session_state.corrected_df)
#         else:
#             st.warning("Please verify and correct data before updating systems.")

# # ==========================
# # Footer
# # ==========================
# st.markdown('</div>', unsafe_allow_html=True)
# st.markdown('<div class="footer">Developed by Digiprima Technologies | Timesheet AI Agent © 2025</div>', unsafe_allow_html=True)
