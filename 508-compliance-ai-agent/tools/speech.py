
#-----------------------------------------------------------------------------

# import streamlit as st
# import speech_recognition as sr
# from gtts import gTTS
# import tempfile
# import os

# def speech_to_text():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.info("Listening... Please speak now.")
#         audio = r.listen(source, timeout=5, phrase_time_limit=10)
#     try:
#         text = r.recognize_google(audio)
#         return text.lower()
#     except sr.UnknownValueError:
#         st.warning("Could not understand audio.")
#         return ""
#     except sr.RequestError as e:
#         st.error(f"Speech Recognition service error: {e}")
#         return ""

# def text_to_speech(text):
#     tts = gTTS(text=text, lang="en")
#     temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
#     tts.save(temp_file.name)
#     return temp_file.name

# def play_audio(file_path):
#     with open(file_path, "rb") as f:
#         audio_bytes = f.read()
#     st.audio(audio_bytes, format="audio/mp3")
#     os.unlink(file_path)

#---------------------------------------------------------------------------------------------------------------------------------

import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os

# --- Functions ---
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak now.")
        audio = r.listen(source, timeout=5, phrase_time_limit=10)
    try:
        text = r.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name

def play_audio(file_path):
    with open(file_path, "rb") as f:
        audio_bytes = f.read()
    st.audio(audio_bytes, format="audio/mp3")


# --- Backward Compatibility Classes ---
class TextToSpeech:
    def speak(self, text):
        file_path = text_to_speech(text)
        play_audio(file_path)
        os.unlink(file_path)  # cleanup

class SpeechRecognizer:
    def listen_command(self):
        return speech_to_text()
