# app/streamlit_app.py
"""
Streamlit UI for the 508 Compliance AI Agent.
This is the "chef" that uses the workflow_controller_task to run Steps 1..8
and presents the results with accessible controls + voice I/O.
"""

# import os
# import streamlit as st
# import pandas as pd
# from pathlib import Path
# from datetime import datetime

# # workflow controller (make sure path is correct; file above is crew/workflow_controller_task.py)
# from crew.workflow_controller_task import run_full_workflow

# # UI helpers
# from app import ui as ui_helpers

# # speech tools (two possible API shapes supported)
# from tools import speech as speech_tools

# # File ops
# from tools.file_ops import save_uploaded_file

# st.set_page_config(page_title="508 Compliance AI Agent", layout="wide", initial_sidebar_state="auto")

# # Ensure output dirs exist
# OUTPUT_ROOT = os.getenv("OUTPUT_DIR", "outputs")
# REPORTS_DIR = Path(OUTPUT_ROOT) / "reports"
# AUDIO_DIR = Path(OUTPUT_ROOT) / "audio"
# REPORTS_DIR.mkdir(parents=True, exist_ok=True)
# AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# # Helper to speak text (robust to different tools.speech implementations)
# def speak(text: str):
#     try:
#         # try function
#         if hasattr(speech_tools, "text_to_speech"):
#             mp3 = speech_tools.text_to_speech(text)
#             # If it returns a path, play it
#             if mp3 and os.path.exists(mp3):
#                 with open(mp3, "rb") as f:
#                     st.audio(f.read(), format="audio/mp3")
#                 return
#         # try class interface
#         if hasattr(speech_tools, "TextToSpeech"):
#             tts = speech_tools.TextToSpeech()
#             maybe_path = tts.speak(text)
#             if maybe_path and os.path.exists(maybe_path):
#                 with open(maybe_path, "rb") as f:
#                     st.audio(f.read(), format="audio/mp3")
#                 return
#     except Exception:
#         st.warning("TTS failed — showing text instead.")
#     # Fallback: show text and use browser TTS via alt text
#     st.info(text)


# def listen_once(timeout=6):
#     """
#     Try to use speech_tools.speech_to_text or SpeechRecognizer class if present.
#     Returns recognized string or None.
#     """
#     try:
#         if hasattr(speech_tools, "speech_to_text"):
#             return speech_tools.speech_to_text(None)  # many implementations expect file path; placeholder
#         if hasattr(speech_tools, "SpeechRecognizer"):
#             recognizer = speech_tools.SpeechRecognizer()
#             return recognizer.listen_command()
#     except Exception:
#         return None


# def main():
#     st.title("508 Compliance AI Agent — Voice-first, Accessible")
#     st.markdown("**Goal:** Fully automated 508 compliance scanning, remediation suggestions and before/after reporting. Voice-first and keyboard friendly.")

#     # Sidebar: controls & settings
#     st.sidebar.header("Controls")
#     enable_voice = st.sidebar.checkbox("Enable Voice Commands", value=True)
#     auto_run_after_upload = st.sidebar.checkbox("Auto-run on upload", value=False)

#     # Step 1: Input selection
#     st.header("Step 1 — Provide source for evaluation")
#     with st.form("source_form", clear_on_submit=False):
#         col1, col2 = st.columns([2, 1])
#         with col1:
#             input_method = st.radio("Choose input method", options=["URL", "File upload"], index=0)
#             if input_method == "URL":
#                 url_input = st.text_input("Enter URL to scan", placeholder="https://example.com")
#             else:
#                 uploaded_file = st.file_uploader("Upload PDF / DOCX / HTML", type=["pdf", "docx", "html"], accept_multiple_files=False)
#         with col2:
#             st.write("Quick commands:")
#             st.markdown("- Say: **'Run compliance check'** to start the workflow (with voice enabled).")
#             st.markdown("- Use **Tab** to navigate — UI is keyboard-friendly.")
#         submitted = st.form_submit_button("Confirm source")

#     source_to_scan = None
#     source_type = None

#     if submitted or (auto_run_after_upload and uploaded_file):
#         if input_method == "URL":
#             if url_input:
#                 source_to_scan = url_input.strip()
#                 source_type = "url"
#             else:
#                 st.error("Please provide a valid URL.")
#         else:
#             if uploaded_file is not None:
#                 # save uploaded file and pass path to workflow
#                 file_path = save_uploaded_file(uploaded_file)
#                 source_to_scan = file_path
#                 source_type = "file"
#             else:
#                 st.error("Please upload a file to proceed.")

#     # Offer voice capture for commands
#     if enable_voice:
#         st.markdown("---")
#         st.subheader("Voice Command")
#         if st.button("Start voice command (listen)"):
#             speak("Listening for command. Say 'run compliance check' to start.")
#             cmd = listen_once()
#             if cmd:
#                 st.success(f"Recognized: {cmd}")
#                 cmd_lower = cmd.lower()
#                 # simple command parsing
#                 if "run" in cmd_lower and "compliance" in cmd_lower:
#                     if not source_to_scan:
#                         st.warning("No source selected yet. Please provide URL or upload file first.")
#                     else:
#                         st.info("Voice-triggered: running workflow.")
#                         result = run_and_display_workflow(source_to_scan, source_type)
#                         st.session_state["last_result"] = result
#                 elif "export" in cmd_lower:
#                     st.info("Voice command: export requested — use UI export buttons.")
#                 else:
#                     st.info("Command not recognized for workflow control.")
#             else:
#                 st.warning("No speech recognized. Try again or use manual controls.")

#     # Manual trigger
#     st.markdown("---")
#     st.subheader("Run workflow (manual control)")
#     cola, colb = st.columns([1, 1])
#     if cola.button("Run 508 Compliance Check"):
#         if not source_to_scan:
#             st.error("No source selected. Provide a URL or upload a file first.")
#         else:
#             result = run_and_display_workflow(source_to_scan, source_type)
#             st.session_state["last_result"] = result

#     if colb.button("Clear last results"):
#         st.session_state.pop("last_result", None)
#         st.success("Cleared.")

#     # Show last results if present
#     if "last_result" in st.session_state:
#         st.markdown("---")
#         st.header("Last Run Results")
#         show_workflow_results(st.session_state["last_result"])


# def run_and_display_workflow(source, source_type):
#     """
#     Run the workflow controller and display progress + artifacts.
#     """
#     with st.spinner("Running full 508 compliance workflow — this may take a while..."):
#         result = run_full_workflow(source, source_type)
#     if result.get("status") != "success":
#         st.error("Workflow failed: " + str(result.get("error", "Unknown error")))
#         return result

#     artifacts = result.get("artifacts", {})
#     st.success("Workflow completed successfully.")
#     # Display findings summary CSV if exists
#     findings_path = artifacts.get("findings_report_path")
#     if findings_path and Path(findings_path).exists():
#         try:
#             df = pd.read_csv(findings_path)
#             st.subheader("Findings Summary")
#             st.dataframe(df)
#         except Exception:
#             st.info("Findings summary saved to: " + str(findings_path))

#     # Display issues list
#     issues_path = artifacts.get("issues_df_path")
#     if issues_path and Path(issues_path).exists():
#         try:
#             df_issues = pd.read_csv(issues_path)
#             st.subheader("Detected Issues")
#             st.dataframe(df_issues)
#         except Exception:
#             st.info("Issues file saved to: " + str(issues_path))

#     # Annotated source
#     annotated_path = artifacts.get("annotated_path")
#     if annotated_path and Path(annotated_path).exists():
#         st.subheader("Annotated Source Preview")
#         try:
#             with open(annotated_path, "r", encoding="utf-8") as f:
#                 text = f.read()
#             st.text_area("Annotated content", value=text, height=300)
#         except Exception:
#             st.info("Annotated artifact saved to: " + str(annotated_path))

#     # Suggestions
#     suggestions_path = artifacts.get("suggestions_path")
#     if suggestions_path and Path(suggestions_path).exists():
#         st.subheader("Suggested Fixes")
#         try:
#             df_sugg = pd.read_csv(suggestions_path)
#             st.dataframe(df_sugg)
#         except Exception:
#             st.info("Suggestions saved to: " + str(suggestions_path))

#     # Comparison
#     comparison_path = artifacts.get("comparison_path")
#     if comparison_path and Path(comparison_path).exists():
#         st.subheader("Before vs After Comparison")
#         try:
#             df_comp = pd.read_csv(comparison_path)
#             st.dataframe(df_comp)
#         except Exception:
#             st.info("Comparison saved to: " + str(comparison_path))

#     # Audio summary playback
#     audio_path = artifacts.get("audio_summary_path")
#     if audio_path:
#         st.subheader("Audio Summary")
#         if Path(audio_path).exists():
#             with open(audio_path, "rb") as f:
#                 st.audio(f.read(), format="audio/mp3")
#         else:
#             # sometimes audio summary may be text fallback
#             try:
#                 with open(audio_path, "r", encoding="utf-8") as f:
#                     st.text_area("Summary (no audio available)", value=f.read(), height=200)
#             except Exception:
#                 st.info("Audio summary saved to: " + str(audio_path))

#     # Offer export buttons
#     st.markdown("---")
#     st.subheader("Export / Download Artifacts")
#     for name, path in artifacts.items():
#         if path and Path(path).exists():
#             try:
#                 with open(path, "rb") as f:
#                     st.download_button(label=f"Download {Path(path).name}", data=f, file_name=Path(path).name)
#             except Exception:
#                 st.write(f"Artifact available at: {path}")

#     return result


# def show_workflow_results(result):
#     """Show results from a previous run (stored in session_state)."""
#     artifacts = result.get("artifacts", {})
#     if not artifacts:
#         st.info("No artifacts available in the result.")
#         return
#     st.write("Run ID:", result.get("metadata", {}).get("run_id"))
#     st.write("Started:", result.get("metadata", {}).get("started_at"))
#     # Reuse the display logic to show saved artifacts
#     # Findings
#     if artifacts.get("findings_report_path"):
#         try:
#             df = pd.read_csv(artifacts["findings_report_path"])
#             st.subheader("Findings Summary")
#             st.dataframe(df)
#         except Exception:
#             st.write("Findings saved at:", artifacts["findings_report_path"])
#     # Issues
#     if artifacts.get("issues_df_path"):
#         try:
#             df = pd.read_csv(artifacts["issues_df_path"])
#             st.subheader("Detected Issues")
#             st.dataframe(df)
#         except Exception:
#             st.write("Issues saved at:", artifacts["issues_df_path"])

# if __name__ == "__main__":
#     main()


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import os
# import streamlit as st
# import pandas as pd
# from pathlib import Path
# from datetime import datetime

# # Replace with your actual workflow controller import:
# # from crew.workflow_controller_task import run_full_workflow

# # Dummy placeholder for run_full_workflow so this file runs standalone:
# def run_full_workflow(source, source_type):
#     # Simulate a workflow result with dummy artifact CSV paths (replace with real logic)
#     return {
#         "status": "success",
#         "artifacts": {
#             "findings_report_path": "outputs/reports/findings_report.csv",
#             "issues_df_path": "outputs/reports/issues.csv",
#             "annotated_path": "outputs/annotated.txt",
#             "suggestions_path": "outputs/reports/suggestions.csv",
#             "comparison_path": "outputs/reports/comparison.csv",
#             "audio_summary_path": None,
#         },
#         "metadata": {
#             "run_id": "dummy_run_001",
#             "started_at": datetime.now().isoformat(),
#         },
#     }


# # CSS injected once at the top
# st.markdown(
#     """
#     <style>
#     /* Header and footer styling */
#     .custom-header {
#         background-color: #cce6ff;
#         color: #003366;
#         font-weight: 700;
#         padding: 18px 32px;
#         font-size: 2.2rem;
#         border-radius: 8px;
#         margin-bottom: 24px;
#         text-align: center;
#         font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
#         box-shadow: 0 3px 6px rgba(0,0,0,0.1);
#     }
#     .custom-footer {
#         background-color: #cce6ff;
#         color: #003366;
#         font-weight: 600;
#         padding: 14px 32px;
#         font-size: 1rem;
#         border-radius: 8px;
#         margin-top: 40px;
#         text-align: center;
#         font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
#         box-shadow: 0 -3px 6px rgba(0,0,0,0.1);
#         position: relative;
#     }
#     /* Workflow steps bar */
#     .progress-container {
#         display: flex;
#         justify-content: space-between;
#         margin-bottom: 24px;
#         font-weight: 600;
#         font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
#     }
#     .step {
#         flex-grow: 1;
#         padding: 10px 6px;
#         margin: 0 4px;
#         border-radius: 20px;
#         text-align: center;
#         font-size: 0.85rem;
#         color: white;
#         background-color: #0073e6;
#         box-shadow: 0 2px 5px rgba(0, 115, 230, 0.5);
#         transition: background-color 0.3s ease;
#     }
#     .step.current {
#         background-color: #004a99;
#         box-shadow: 0 4px 10px rgba(0, 74, 153, 0.7);
#     }
#     .step.completed {
#         background-color: #99ccff;
#         color: #003366;
#         box-shadow: none;
#     }
#     /* Table styling */
#     table {
#         border-collapse: collapse;
#         width: 100%;
#         font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
#     }
#     th, td {
#         border: 1px solid #004080;
#         padding: 8px;
#         text-align: center;
#     }
#     th {
#         background-color: #0073e6;
#         color: white;
#         font-weight: 700;
#     }
#     tr:nth-child(even) {
#         background-color: #e6f0ff;
#     }
#     tr:nth-child(odd) {
#         background-color: white;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )


# def display_workflow_progress(current_step):
#     steps = [
#         "Step 1: Input Source",
#         "Step 2: Compliance Check",
#         "Step 3: Findings Report",
#         "Step 4: Annotated Source",
#         "Step 5: Suggested Fixes",
#         "Step 6: Fixed Source",
#         "Step 7: Comparison",
#         "Step 8: Export & Summary"
#     ]
#     html = '<div class="progress-container">'
#     for i, step in enumerate(steps, 1):
#         cls = ""
#         if i < current_step:
#             cls = "completed"
#         elif i == current_step:
#             cls = "current"
#         html += f'<div class="step {cls}">{step}</div>'
#     html += "</div>"
#     st.markdown(html, unsafe_allow_html=True)


# def run_and_display_workflow(source, source_type):
#     with st.spinner("Running full 508 compliance workflow — this may take a while..."):
#         result = run_full_workflow(source, source_type)

#     if result.get("status") != "success":
#         st.error("Workflow failed: " + str(result.get("error", "Unknown error")))
#         return result

#     artifacts = result.get("artifacts", {})
#     st.success("Workflow completed successfully.")

#     # Show workflow progress at Step 8 (finished)
#     display_workflow_progress(8)

#     # Show CSV artifacts as styled HTML tables
#     def show_csv_table(path, title):
#         if path and Path(path).exists():
#             try:
#                 df = pd.read_csv(path)
#                 st.subheader(title)
#                 html = (
#                     df.style
#                     .set_table_styles([
#                         {'selector': 'th', 'props': [('background-color', '#0073e6'), ('color', 'white'), ('border', '1px solid #004080')]},
#                         {'selector': 'td', 'props': [('border', '1px solid #004080')]},
#                         {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#e6f0ff')]},
#                     ])
#                     .hide_index()
#                     .to_html()
#                 )
#                 st.markdown(html, unsafe_allow_html=True)
#             except Exception:
#                 st.info(f"{title} saved at: {path}")

#     show_csv_table(artifacts.get("findings_report_path"), "Findings Summary")
#     show_csv_table(artifacts.get("issues_df_path"), "Detected Issues")
#     show_csv_table(artifacts.get("suggestions_path"), "Suggested Fixes")
#     show_csv_table(artifacts.get("comparison_path"), "Before vs After Comparison")

#     # Annotated Source Preview (text file)
#     annotated_path = artifacts.get("annotated_path")
#     if annotated_path and Path(annotated_path).exists():
#         st.subheader("Annotated Source Preview")
#         try:
#             with open(annotated_path, "r", encoding="utf-8") as f:
#                 text = f.read()
#             st.text_area("Annotated content", value=text, height=300)
#         except Exception:
#             st.info(f"Annotated source saved at: {annotated_path}")

#     # Audio summary (optional)
#     audio_path = artifacts.get("audio_summary_path")
#     if audio_path:
#         st.subheader("Audio Summary")
#         if Path(audio_path).exists():
#             with open(audio_path, "rb") as f:
#                 st.audio(f.read(), format="audio/mp3")
#         else:
#             try:
#                 with open(audio_path, "r", encoding="utf-8") as f:
#                     st.text_area("Summary (no audio available)", value=f.read(), height=200)
#             except Exception:
#                 st.info(f"Audio summary saved at: {audio_path}")

#     # Export / Download buttons
#     st.markdown("---")
#     st.subheader("Export / Download Artifacts")
#     for name, path in artifacts.items():
#         if path and Path(path).exists():
#             try:
#                 with open(path, "rb") as f:
#                     st.download_button(label=f"Download {Path(path).name}", data=f, file_name=Path(path).name)
#             except Exception:
#                 st.write(f"Artifact available at: {path}")

#     return result


# def main():
#     st.markdown('<div class="custom-header">508 Compliance AI Agent — Voice-first, Accessible</div>', unsafe_allow_html=True)

#     st.markdown("**Goal:** Fully automated 508 compliance scanning, remediation suggestions and before/after reporting. Voice-first and keyboard friendly.")

#     # Show initial workflow progress (step 1)
#     display_workflow_progress(1)

#     # Input selection
#     input_method = st.radio("Choose input method", options=["URL", "File upload"], index=0)

#     source_to_scan = None
#     source_type = None

#     if input_method == "URL":
#         url_input = st.text_input("Enter URL to scan", placeholder="https://example.com")
#         if st.button("Confirm URL"):
#             if url_input:
#                 source_to_scan = url_input.strip()
#                 source_type = "url"
#             else:
#                 st.error("Please enter a valid URL")
#     else:
#         uploaded_file = st.file_uploader("Upload PDF / DOCX / HTML", type=["pdf", "docx", "html"], accept_multiple_files=False)
#         if uploaded_file is not None:
#             file_path = Path("uploads") / uploaded_file.name
#             file_path.parent.mkdir(parents=True, exist_ok=True)
#             with open(file_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
#             source_to_scan = str(file_path)
#             source_type = "file"
#             st.success(f"Uploaded file saved to {file_path}")

#     if source_to_scan:
#         if st.button("Run 508 Compliance Check"):
#             run_and_display_workflow(source_to_scan, source_type)

#     st.markdown('<div class="custom-footer">© 2025 508 Compliance AI Agent. All rights reserved.</div>', unsafe_allow_html=True)


# if __name__ == "__main__":
#     main()



#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

