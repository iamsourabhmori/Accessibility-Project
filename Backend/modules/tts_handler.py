# modules/tts_handler.py
import pyttsx3
import threading

# Initialize TTS engine once
_engine = pyttsx3.init()
_engine.setProperty('rate', 180)  # speech speed
_engine.setProperty('volume', 1.0)  # max volume

# Threaded speaking so it doesn't block Streamlit
def speak_text(text: str):
    def _speak():
        try:
            _engine.say(text)
            _engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
    threading.Thread(target=_speak, daemon=True).start()
