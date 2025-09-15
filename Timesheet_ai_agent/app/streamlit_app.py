

#----------------------------------------------------------------------------------------------------------------------------------------

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
#         df_extracted = load_clean_csv(csv_path)

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


#-----------------------------------------------------------------------------------------------------------------------------------------------

import streamlit as st
import pandas as pd
import os
import sys
import time
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add root path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.file_screenshot_tool import capture_csv_as_image, load_clean_csv
from tools.timesheet_verifier import verify_timesheet
from tools.system_api import apply_corrections
from tools.gemini_client import gemini_generate, gemini_chat

st.set_page_config(page_title="Timesheet AI Agent", layout="wide")

st.markdown("""
    <style>
        .header { background: linear-gradient(90deg, #87CEEB, #ffffff, #ff4b5c);
            padding: 25px; border-radius: 10px; color: black; text-align: center;
            border: 2px solid #00000030; margin-bottom: 30px; }
        .footer { background: linear-gradient(90deg, #ff4b5c, #ffffff, #87CEEB);
            padding: 15px; border-radius: 10px; color: black; text-align: center;
            border: 2px solid #00000030; margin-top: 50px; }
        .stButton>button { background-color: #1982c4; color: white; border-radius: 8px;
            height: 3em; width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"><h1>🕒 Timesheet AI Agent Dashboard</h1></div>', unsafe_allow_html=True)

# Upload Master Timesheet
st.subheader("📥 Upload Master Timesheet")
master_csv = st.file_uploader("Upload Master Timesheet CSV", type=["csv"], key="master")

if master_csv is not None:
    os.makedirs("uploads", exist_ok=True)
    master_path = os.path.join("uploads", master_csv.name)
    with open(master_path, "wb") as f:
        f.write(master_csv.getbuffer())
    st.success(f"✅ Master file uploaded: {master_csv.name}")
else:
    st.warning("⚠️ Please upload the Master Timesheet CSV before proceeding.")

# Select File from Downloads Folder
csv_folder = "/home/digi2/Downloads"
csv_files = [f for f in os.listdir(csv_folder) if f.endswith(".csv")]
selected_csv = st.selectbox("📂 Select a CSV file from Downloads", csv_files)

# Screenshot and Process
if st.button("📸 Capture Screenshot and Process"):

    if master_csv is None:
        st.error("❌ Upload the master CSV first.")
        st.stop()

    progress = st.progress(0, text="Initializing...")

    try:
        progress.progress(10, text="🔍 Reading selected file...")
        csv_path = os.path.join(csv_folder, selected_csv)
        st.info(f"Selected file: `{selected_csv}`")

        # Step 1: Screenshot (create image from csv)
        progress.progress(25, text="📸 Taking screenshot...")
        image_path = capture_csv_as_image(csv_path)
        st.session_state["screenshot_path"] = image_path

        # Step 2: Load and Clean CSV
        progress.progress(50, text="🧹 Cleaning CSV data...")
        df_extracted = load_clean_csv(csv_path)

        if df_extracted.empty or df_extracted.shape[1] < 2:
            raise ValueError("No valid rows match header length. Check CSV formatting.")

        st.session_state["extracted_df"] = df_extracted

        # Show Screenshot + Table
        st.markdown("### 📸 Screenshot and Extracted Data")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("**Screenshot of Timesheet:**")
            from PIL import Image
            screenshot_img = Image.open(image_path)
            st.image(screenshot_img, caption="📸 Captured Timesheet", use_container_width=True)
        with col2:
            st.markdown("**Extracted Timesheet Table:**")
            st.dataframe(df_extracted, use_container_width=True)

        # Step 3: Load Master Timesheet
        progress.progress(65, text="📂 Loading Master Timesheet...")
        master_df = pd.read_csv(master_path)
        st.subheader("🗂️ Master Timesheet")
        st.dataframe(master_df, use_container_width=True)

        # Step 4: Verify timesheet and find discrepancies
        progress.progress(80, text="🧪 Verifying for mismatches...")
        discrepancies = verify_timesheet(df_extracted, master_df)

        if discrepancies:
            st.warning("⚠️ Discrepancies Found!")
            st.subheader("📌 Discrepancies Details")
            st.json(discrepancies)

            # Step 5: Apply corrections
            corrected_df = apply_corrections(df_extracted, discrepancies)

            st.subheader("✅ Corrected Timesheet")
            st.dataframe(corrected_df, use_container_width=True)
            st.session_state["corrected_df"] = corrected_df

            # Optional: Gemini explanation
            prompt = f"These discrepancies were found in the timesheet data:\n{discrepancies}\n\nSummarize and explain corrections."
            suggestion = gemini_generate(prompt)
            st.markdown("### 🤖 Gemini Suggestion:")
            st.info(suggestion)

        else:
            st.success("✅ No discrepancies found.")

        progress.progress(100, text="✅ Done.")

    except Exception as e:
        st.error(f"❌ Error during verification: {str(e)}")
        progress.empty()


#--------------------------------------------------------------------------------------------------------------------------

# app/streamlit_app.py

# import streamlit as st
# import pandas as pd
# import os
# import sys
# import time
# from PIL import Image
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Add root path for module imports
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from tools.file_screenshot_tool import capture_csv_as_image, load_clean_csv
# from tools.timesheet_verifier import verify_timesheet
# from tools.system_api import apply_corrections
# from tools.gemini_client import gemini_generate, gemini_chat

# st.set_page_config(page_title="Timesheet AI Agent", layout="wide")

# st.markdown("""
#     <style>
#         .header { background: linear-gradient(90deg, #87CEEB, #ffffff, #ff4b5c);
#             padding: 25px; border-radius: 10px; color: black; text-align: center;
#             border: 2px solid #00000030; margin-bottom: 30px; }
#         .footer { background: linear-gradient(90deg, #ff4b5c, #ffffff, #87CEEB);
#             padding: 15px; border-radius: 10px; color: black; text-align: center;
#             border: 2px solid #00000030; margin-top: 50px; }
#         .stButton>button { background-color: #1982c4; color: white; border-radius: 8px;
#             height: 3em; width: 100%; }
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

#         # Step 1: Screenshot (create image from csv)
#         progress.progress(25, text="📸 Taking screenshot...")
#         image_path = capture_csv_as_image(csv_path)
#         st.session_state["screenshot_path"] = image_path

#         # Step 2: Load and Clean CSV
#         progress.progress(50, text="🧹 Cleaning CSV data...")
#         df_extracted = load_clean_csv(csv_path)

#         if df_extracted.empty or df_extracted.shape[1] < 2:
#             raise ValueError("No valid rows match header length. Check CSV formatting.")

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

#         # Step 3: Load Master Timesheet
#         progress.progress(65, text="📂 Loading Master Timesheet...")
#         master_df = pd.read_csv(master_path)
#         st.subheader("🗂️ Master Timesheet")
#         st.dataframe(master_df, use_container_width=True)

#         # Step 4: Verify timesheet and find discrepancies
#         progress.progress(80, text="🧪 Verifying for mismatches...")
#         discrepancies = verify_timesheet(df_extracted, master_df)

#         if discrepancies:
#             st.warning("⚠️ Discrepancies Found!")
#             st.subheader("📌 Discrepancies Details")
#             st.json(discrepancies)

#             # Step 5: Apply corrections
#             corrected_df = apply_corrections(df_extracted, discrepancies)

#             st.subheader("✅ Corrected Timesheet")
#             st.dataframe(corrected_df, use_container_width=True)
#             st.session_state["corrected_df"] = corrected_df

#             # Optional: Gemini explanation
#             prompt = f"These discrepancies were found in the timesheet data:\n{discrepancies}\n\nSummarize and explain corrections."
#             suggestion = gemini_generate(prompt)
#             st.markdown("### 🤖 Gemini Suggestion:")
#             st.info(suggestion)

#         else:
#             st.success("✅ No discrepancies found.")

#         progress.progress(100, text="✅ Done.")

#     except Exception as e:
#         st.error(f"❌ Error during verification: {str(e)}")
#         progress.empty()

# # 🔁 New: Push updates to external system
# if st.button("📤 Push Updates to External System"):
#     if 'corrected_df' in st.session_state:
#         from agents.system_update_agent import SystemUpdateAgent

#         update_method = st.selectbox("Select update method", ["api", "ui"])
#         if update_method == "api":
#             token = st.text_input("Enter API Token", type="password")
#             api_credentials = {"token": token}
#             updater = SystemUpdateAgent(method='api', api_credentials=api_credentials)
#         else:
#             st.warning("⚠️ Make sure the timesheet site is open and focused for automation.")
#             updater = SystemUpdateAgent(method='ui')

#         updater.run(st.session_state["corrected_df"])
#         st.success("✅ Data pushed to external system successfully.")
#     else:
#         st.error("❌ No corrected data to push. Please process a timesheet first.")
