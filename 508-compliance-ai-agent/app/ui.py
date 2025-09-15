# app/ui.py

# import streamlit as st
# from agents.source_and_validation import SourceAndValidationAgent
# from agents.compliance_scan import ComplianceScanAgent
# from agents.reporting import ReportingAgent
# from agents.suggestion_and_fix import SuggestionAndFixAgent
# from agents.interaction import InteractionAgent
# from tools.speech import text_to_speech, speech_to_text

# def run_app():
#     st.title("508 Compliance AI Agent (Voice-first)")

#     source_agent = SourceAndValidationAgent()
#     compliance_agent = ComplianceScanAgent()
#     reporting_agent = ReportingAgent()
#     suggestion_agent = SuggestionAndFixAgent()
#     interaction_agent = InteractionAgent()

#     # Step 1: Get source input (URL or file)
#     st.header("Step 1: Provide Source for 508 Compliance Check")
#     explanation = source_agent.explain_508_compliance()
#     st.info(explanation)

#     source_type = st.radio("Select source type", options=["URL", "File Upload"])

#     source = None
#     if source_type == "URL":
#         url = st.text_input("Enter URL to check")
#         if url:
#             valid, result = source_agent.run(url)
#             if valid:
#                 source = url
#             else:
#                 st.error(f"Invalid URL: {result}")
#     else:
#         uploaded_file = st.file_uploader("Upload a file (PDF, DOCX, HTML)")
#         if uploaded_file:
#             valid, result = source_agent.run(uploaded_file)
#             if valid:
#                 source = result
#             else:
#                 st.error(f"File error: {result}")

#     if source:
#         st.success("Source accepted for scanning.")
#         # Step 2 + Step 4: Scan and highlight
#         st.header("Step 2 & 4: Run Compliance Scan and Highlight Issues")
#         issues_df = compliance_agent.run(source, source_type.lower())
#         st.dataframe(issues_df)

#         annotated = compliance_agent.highlight_issues(source, issues_df)
#         st.text(f"Annotated source preview:\n{annotated}")

#         # Step 3 + Step 7: Generate reports and comparison
#         st.header("Step 3 & 7: Generate Findings and Comparison Reports")
#         summary_df = reporting_agent.generate_findings_report(issues_df)
#         st.dataframe(summary_df)

#         # Placeholder for original and fixed data comparison
#         # In practice, this would use real fixed data
#         comparison_df = reporting_agent.generate_comparison_report(issues_df, issues_df)
#         st.dataframe(comparison_df)

#         # Step 5 + Step 6: Generate suggestions and apply fixes
#         st.header("Step 5 & 6: Suggestions and Fix Application")
#         suggestions_df = suggestion_agent.generate_suggestions(issues_df)
#         st.dataframe(suggestions_df)

#         fixed_source = suggestion_agent.apply_fixes(source, suggestions_df)
#         st.text(fixed_source)

#         # Step 8: Next steps prompt
#         st.header("Step 8: What would you like to do next?")
#         prompt = interaction_agent.prompt_next_steps()
#         st.text(prompt)

#         # Voice interaction placeholder
#         st.info("(Voice interaction not implemented in this prototype)")



# app/ui.py
import streamlit as st
import base64

def display_report_placeholder():
    st.write("Compliance report will appear here after running the check.")
    # You can replace this with a DataFrame or rich text report later.

def display_annotated_source_placeholder():
    st.write("Annotated source file with highlights will appear here.")

def audio_player(audio_file_path):
    try:
        with open(audio_file_path, "rb") as f:
            audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
    except Exception:
        st.warning("No audio file found to play.")

def accessible_button(label, key=None):
    """
    Button that can be focused and operated with keyboard
    """
    return st.button(label, key=key)

def accessible_text_input(label, key=None, **kwargs):
    """
    Text input with clear label and keyboard accessible
    """
    return st.text_input(label, key=key, **kwargs)

def accessible_file_uploader(label, key=None, type=None):
    """
    File uploader accessible with keyboard and screen readers
    """
    return st.file_uploader(label, key=key, type=type)

def display_voice_command_instructions():
    st.info("To use voice commands, click the 'Start Voice Command' button and speak clearly. Supported commands include:\n"
            "- 'Run compliance check'\n"
            "- 'Show report'\n"
            "- 'Export results'\n"
            "- 'Next steps'\n")

