
# modules/voice_commands.py

import torch
import soundfile as sf
from io import BytesIO
from rapidfuzz import process
from modules.huggingface_model import load_wav2vec2_model
import streamlit as st
import speech_recognition as sr

# ------------------------
# Intent mapping
# ------------------------
VOICE_COMMANDS = {
    "upload document file": "doc_file",
    "upload documents from the url": "doc_url",
    "upload audio file": "audio_file",
    "upload audio from the url": "audio_url",
    "upload video file": "video_file",
    "upload video from the url": "video_url",
    "upload image file": "image_file",
    "upload image from the url": "image_url",
}

FUZZY_THRESHOLD = 75  # % match threshold for fuzzy matching


# ------------------------
# Option 1: HuggingFace Wav2Vec2 (offline transcription)
# ------------------------
def transcribe_command_audio(audio_bytes: BytesIO, display_callback=None) -> str:
    """Use Wav2Vec2 to transcribe a short voice command."""
    processor, model = load_wav2vec2_model()

    audio_bytes.seek(0)
    speech, rate = sf.read(audio_bytes)
    if len(speech.shape) > 1:
        speech = speech.mean(axis=1)  # convert to mono

    inputs = processor(speech, sampling_rate=rate, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits

    pred_ids = torch.argmax(logits, dim=-1)
    transcript = processor.batch_decode(pred_ids)[0]

    if display_callback:
        for word in transcript.split():
            display_callback(word)

    return transcript.strip().lower()


# ------------------------
# Option 2: Google SpeechRecognition (online, mic input)
# ------------------------
def recognize_speech_from_mic() -> str:
    """Recognize speech directly from microphone using Google API."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Please speak now")
        audio = recognizer.listen(source, phrase_time_limit=8)

    try:
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        return "⚠️ Could not understand audio"
    except sr.RequestError:
        return "⚠️ Speech API unavailable"


# ------------------------
# Intent Mapper
# ------------------------
def map_command_to_intent(command_text: str) -> str:
    """Map transcribed text to one of the predefined intents."""
    if command_text in VOICE_COMMANDS:
        return VOICE_COMMANDS[command_text]

    best_match, score = process.extractOne(command_text, VOICE_COMMANDS.keys())
    if score >= FUZZY_THRESHOLD:
        return VOICE_COMMANDS[best_match]

    return "unknown"


# ------------------------
# Main entrypoint
# ------------------------
def run_voice_command(audio_bytes: BytesIO = None, use_google: bool = False, display_callback=None) -> dict:
    """
    Run a voice command either from audio file (Wav2Vec2) or microphone (Google API).
    Args:
        audio_bytes: BytesIO of recorded audio (for Wav2Vec2).
        use_google: If True, will capture mic and use Google Speech API instead.
    Returns:
        dict with {"intent": str, "transcript": str}
    """
    if use_google:
        transcript = recognize_speech_from_mic()
    else:
        transcript = transcribe_command_audio(audio_bytes, display_callback=display_callback)

    intent = map_command_to_intent(transcript)

    st.session_state.voice_banner = f"🗣️ Voice Command Detected: {transcript}"

    return {"intent": intent, "transcript": transcript}


# ------------------------
# Backward compatibility wrapper
# ------------------------
def handle_voice_command(audio_bytes: BytesIO = None, use_google: bool = False, display_callback=None) -> dict:
    """
    Wrapper for backward compatibility.
    Calls run_voice_command() internally.
    """
    return run_voice_command(audio_bytes=audio_bytes, use_google=use_google, display_callback=display_callback)
