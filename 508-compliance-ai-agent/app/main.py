# app/main.py

# import streamlit as st
# from agents.source_and_validation import SourceAndValidationAgent
# from agents.compliance_scan import ComplianceScanAgent
# from agents.reporting import ReportingAgent
# from agents.suggestion_and_fix import SuggestionAndFixAgent
# from agents.interaction import InteractionAgent
# from app.ui import run_app

# def main():
#     st.set_page_config(page_title="508 Compliance AI Agent", layout="wide")
#     run_app()

# if __name__ == "__main__":
#     main()



# app/main.py

import sys
import os


import streamlit as st
# import u/i
from app import ui

from tools.speech import TextToSpeech, SpeechRecognizer


# Now you can import tools
import tools.some_tool_module



def main():
    st.set_page_config(
        page_title="508 Compliance AI Agent",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("508 Compliance AI Agent — Voice-First Accessibility")

    # Initialize TTS and ASR
    tts = TextToSpeech()
    asr = SpeechRecognizer()

    # Sidebar: Voice input toggle
    use_voice = st.sidebar.checkbox("Enable Voice Commands (Mic)", value=True)

    # Input: file upload or URL
    input_type = st.radio("Select input type:", ["Upload file", "Enter URL"])
    if input_type == "Upload file":
        uploaded_file = st.file_uploader("Upload PDF, DOCX, or HTML file", type=['pdf', 'docx', 'html'])
        source_url = None
    else:
        uploaded_file = None
        source_url = st.text_input("Enter URL of the webpage to scan")

    # Voice command input
    voice_command = None
    if use_voice:
        st.info("Click 'Start Voice Command' and speak your command.")
        if st.button("Start Voice Command"):
            voice_command = asr.listen_command()
            if voice_command:
                st.success(f"Recognized command: {voice_command}")
                # TODO: parse and trigger steps based on command

    # Buttons for manual trigger (fallback)
    st.markdown("---")
    st.header("Manual Controls")

    if st.button("Run 508 Compliance Check"):
        # Trigger the whole workflow here
        st.info("Running compliance check... (placeholder)")
        tts.speak("Starting 508 compliance check.")

        # TODO: integrate actual agent calls here

        st.success("Compliance check completed.")
        tts.speak("Compliance check completed. Please review the results below.")

    # Display placeholders for reports and highlights
    st.markdown("---")
    st.header("Compliance Report")
    ui.display_report_placeholder()

    st.header("Annotated Source")
    ui.display_annotated_source_placeholder()

    st.header("Audio Playback")
    audio_file = "outputs/audio/compliance_summary.mp3"
    ui.audio_player(audio_file)

if __name__ == "__main__":
    main()
