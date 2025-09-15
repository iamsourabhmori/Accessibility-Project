import streamlit as st
from tools.speech import speech_to_text, text_to_speech, play_audio
from agents.voice_controller import VoiceControllerAgent
import time
import os
# Inject CSS for accessibility and style
st.markdown("""
<style>
    .main {background-color: #f4f7f8;}
    .stButton > button {
        background-color: #005a9c;
        color: white;
        font-size: 24px;
        height: 60px;
        width: 100%;
        border-radius: 12px;
        margin-bottom: 10px;
    }
    .stDataFrame div {
        font-size: 20px !important;
        color: #333333;
    }
    .stAlert {
        font-size: 20px;
        color: #d9534f;
        background-color: #f2dede;
        border-radius: 12px;
        padding: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔊 508 Compliance AI Agent - Voice Controlled")
st.markdown("## Voice commands control the whole workflow.\n"
            "Speak clearly into your microphone to navigate each step.\n"
            "Supported commands include: \n"
            "- 'Start scan'\n"
            "- 'Show report'\n"
            "- 'Generate suggestions'\n"
            "- 'Apply fixes'\n"
            "- 'Compare'\n"
            "- 'Next steps'\n"
            "- 'Exit'\n")

agent = VoiceControllerAgent()

if "last_command" not in st.session_state:
    st.session_state.last_command = ""

if st.button("🎤 Start Voice Command"):
    user_command = speech_to_text()
    if user_command:
        st.success(f"🎙 You said: {user_command}")
        response_text, df = agent.process_command(user_command)
        
        audio_file = text_to_speech(response_text)
        play_audio(audio_file)
        os.remove(audio_file)

        st.info(response_text)

        if df is not None:
            st.dataframe(df, use_container_width=True)
    else:
        st.error("Could not understand your speech. Please try again.")
