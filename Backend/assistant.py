

# assistant.py
import os
import threading
import time
from io import BytesIO
import streamlit as st
import torch
from typing import Optional

from speech import take_command, talk  # take_command may write small UI messages; exceptions handled there
from modules.audio_handler import convert_to_wav, resample_audio_to_16k, extract_audio_from_video
from modules.huggingface_model import load_wav2vec2_model
from modules import file_picker  # <-- audio + video picker; must implement pick_file_from_command, pick_video_from_command, upload_file_to_streamlit, switch_to_browser_tab

# Downloads folder path
DOWNLOADS_PATH = "/home/digi2/Downloads"
VIDEO_EXTENSIONS = (".mp4", ".mkv", ".mov", ".avi", ".flv", ".webm")

# ----------------------------
# Helpers for safe Streamlit usage
# ----------------------------
def append_debug(msg: str):
    """Append debug message to session_state safe (no crash if no Streamlit context)."""
    try:
        if "voice_debug_logs" not in st.session_state:
            st.session_state["voice_debug_logs"] = []
        st.session_state["voice_debug_logs"].append(msg)
    except Exception:
        # If called from background thread where st isn't available, ignore but still print
        pass
    print("[assistant-debug]", msg)


def safe_set_session(key: str, value):
    """Set st.session_state key safely (catch missing ScriptRunContext)."""
    try:
        st.session_state[key] = value
    except Exception as e:
        # Log it; background threads may not have ScriptRunContext
        append_debug(f"safe_set_session failed for {key} -> {e}")


# ----------------------------
# Load ASR model (Wav2Vec2)
# ----------------------------
@st.cache_resource
def get_asr():
    return load_wav2vec2_model()


def transcribe_audio_bytes(audio_bytes: BytesIO, progress_prefix="Transcribing"):
    """
    Transcribe audio from BytesIO using cached Wav2Vec2 model.
    (This is the same implementation used in app.py; kept here to allow local use)
    """
    audio_bytes.seek(0)
    wav_io = resample_audio_to_16k(audio_bytes)
    if wav_io is None:
        raise RuntimeError("Failed to convert/resample audio to 16k WAV.")

    import soundfile as sf
    wav_io.seek(0)
    with sf.SoundFile(wav_io) as f:
        audio_data = f.read(dtype="float32")
        samplerate = f.samplerate

    processor, model = get_asr()
    inputs = processor(audio_data, sampling_rate=samplerate, return_tensors="pt", padding=True).input_values

    predicted_ids = []
    chunk_size = 16000 * 5  # 5-second chunks
    start = 0
    total_len = inputs.shape[1]

    # NOTE: UI progress bars should be created in the main Streamlit script.
    # We provide these here but they will only display if called from the main thread.
    try:
        progress_bar = st.progress(0)
        progress_text = st.empty()
    except Exception:
        progress_bar = None
        progress_text = None

    while start < total_len:
        end = min(start + chunk_size, total_len)
        input_chunk = inputs[:, start:end]
        with torch.no_grad():
            logits = model(input_chunk).logits
        preds = torch.argmax(logits, dim=-1)
        out = preds.squeeze().tolist()
        if isinstance(out, list):
            predicted_ids.extend(out)
        else:
            predicted_ids.append(out)
        start = end
        pct = min(int(start / total_len * 100), 100)
        if progress_bar:
            try:
                progress_bar.progress(pct)
            except Exception:
                pass
        if progress_text:
            try:
                progress_text.text(f"⏳ {progress_prefix}... {pct}%")
            except Exception:
                pass

    try:
        transcript = processor.decode(predicted_ids)
    except Exception:
        import torch as _torch
        transcript = processor.batch_decode(_torch.tensor([predicted_ids]))[0]

    if progress_bar:
        try:
            progress_bar.progress(100)
        except Exception:
            pass
    if progress_text:
        try:
            progress_text.text(f"✅ {progress_prefix} complete")
        except Exception:
            pass

    return transcript.strip()


# ----------------------------
# Voice command parsing and handlers
# ----------------------------
def _is_tab_command(cmd: str) -> Optional[str]:
    """
    Return the tab key if the command requests a tab switch.
    Accepts many variants like 'video tab', 'switch to video', 'go to image', 'image'.
    """
    if not cmd:
        return None
    s = cmd.lower().strip()

    # Map keywords -> tab keys
    if "audio tab" in s or "switch to audio" in s or s.strip() == "audio" or "go to audio" in s:
        return "audio"
    if "video tab" in s or "switch to video" in s or s.strip() == "video" or "go to video" in s or "play video" in s:
        return "video"
    if "image tab" in s or "switch to image" in s or s.strip() == "image" or "go to image" in s or "open image" in s:
        return "image"
    if "document tab" in s or "switch to document" in s or s.strip() in ("document", "docs", "document tab") or "go to document" in s:
        return "document"
    return None


def handle_voice_command(command: str):
    """
    Handles dynamic voice commands for audio/video uploads and tab switching.
    This function is safe to call from the main thread; when called from background threads
    we avoid direct UI calls that raise ScriptRunContext errors.
    """
    if not command:
        return

    cmd = command.lower().strip()
    append_debug(f"Handling voice command: {cmd}")
    safe_set_session("last_voice_command", cmd)

    # 1) Open Downloads folder
    if "open download" in cmd or "open downloads" in cmd or "open download folder" in cmd:
        try:
            if os.name == "nt":
                os.startfile(DOWNLOADS_PATH)
            elif hasattr(os, "uname") and os.uname().sysname == "Darwin":
                os.system(f"open '{DOWNLOADS_PATH}'")
            else:
                # non-blocking open in background
                os.system(f"xdg-open '{DOWNLOADS_PATH}' &")
            talk("Opened your downloads folder.")
        except Exception as e:
            append_debug(f"Failed to open downloads: {e}")
            talk("Unable to open downloads folder on this machine.")
        return

    # 2) Tab switching (audio/video/image/document)
    tab_key = _is_tab_command(cmd)
    if tab_key:
        append_debug(f"Recognized tab switch -> {tab_key}")
        # set session_state safely; UI can read this and rerender
        safe_set_session("active_tab", tab_key)
        # Announce
        talk(f"Switched to {tab_key.capitalize()} tab.")
        return

    # 3) Video file pick (explicit)
    if "upload video" in cmd or "open video" in cmd or cmd.endswith(VIDEO_EXTENSIONS):
        append_debug("Video pick requested")
        safe_set_session("active_tab", "video")
        # file_picker should provide intelligent matching; returns full path or None
        try:
            file_path = file_picker.pick_video_from_command(cmd)
        except Exception as e:
            append_debug(f"file_picker.pick_video_from_command failed: {e}")
            file_path = None

        if file_path:
            append_debug(f"Video chosen: {file_path}")
            try:
                # Bring browser to front and upload via automation (pyautogui) in file_picker
                file_picker.switch_to_browser_tab()
            except Exception as e:
                append_debug(f"switch_to_browser_tab failed: {e}")

            try:
                file_picker.upload_file_to_streamlit(file_path)
                # set state that app.py can use to auto-process if needed
                safe_set_session("video_bytes", BytesIO(open(file_path, "rb").read()))
                talk(f"Video file {os.path.basename(file_path)} loaded and processing started.")
            except Exception as e:
                append_debug(f"upload_file_to_streamlit failed: {e}")
                talk("Failed to upload the selected video file to the web UI.")
        else:
            talk(f"No video file matching '{cmd}' found in Downloads.")
        return

    # 4) Audio file pick (explicit/general "upload", "open")
    if "upload" in cmd or "open" in cmd:
        append_debug("Audio pick requested")
        safe_set_session("active_tab", "audio")
        try:
            file_path = file_picker.pick_file_from_command(cmd)
        except Exception as e:
            append_debug(f"file_picker.pick_file_from_command failed: {e}")
            file_path = None

        if file_path:
            append_debug(f"Audio chosen: {file_path}")
            try:
                file_picker.switch_to_browser_tab()
            except Exception as e:
                append_debug(f"switch_to_browser_tab failed: {e}")

            try:
                # Upload using automation
                file_picker.upload_file_to_streamlit(file_path)
                # Set session state so app.py can auto-transcribe from bytes (preferred over forcing rerun)
                safe_set_session("audio_bytes", BytesIO(open(file_path, "rb").read()))
                safe_set_session("auto_transcribe_audio", True)
                talk(f"Audio file {os.path.basename(file_path)} loaded and transcription started.")
            except Exception as e:
                append_debug(f"upload_file_to_streamlit failed: {e}")
                talk("Failed to upload the selected audio file to the web UI.")
        else:
            talk(f"No audio file matching '{cmd}' found in Downloads.")
        return

    # Unknown / fallback
    talk(f"You said: {command}. Try 'upload <exact file name>' or 'switch to <tab name>'.")
    append_debug("No handler matched the command.")


# ----------------------------
# BACKGROUND VOICE ASSISTANT THREAD
# ----------------------------
def run_voice_assistant_in_thread(stop_flag: threading.Event):
    """
    Continuous voice assistant loop. Should be run in a daemon thread.
    This loop calls take_command(), then handle_voice_command().
    We do not call Streamlit UI functions from here (except via talk which handles exceptions).
    """
    # Short initial announcement (safe because talk manages exceptions)
    try:
        talk("Voice assistant started. Say a command.")
    except Exception:
        append_debug("Could not announce assistant start via talk().")

    while not stop_flag.is_set():
        try:
            command = take_command()
            if command:
                # handle voice command; avoid heavy UI calls directly from this thread
                handle_voice_command(command)
        except Exception as e:
            append_debug(f"Error in assistant loop: {e}")
            try:
                talk("An error occurred while listening.")
            except Exception:
                pass
        # small delay to avoid CPU spin
        time.sleep(0.25)


# ----------------------------
# START / STOP BUTTONS (UI)
# ----------------------------
def init_voice_assistant_controls():
    """
    Place start/stop buttons in the Streamlit sidebar.
    Pressing start will spawn a daemon thread that runs run_voice_assistant_in_thread.
    """
    st.sidebar.subheader("🎙️ Voice Assistant")
    if "assistant_stop_event" not in st.session_state:
        safe_set_session("assistant_stop_event", None)
    if "assistant_thread" not in st.session_state:
        safe_set_session("assistant_thread", None)

    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_btn = st.button("Start Voice Assistant")
    with col2:
        stop_btn = st.button("Stop Voice Assistant")

    if start_btn:
        # start background assistant
        current_thread = st.session_state.get("assistant_thread", None)
        if current_thread is None or not getattr(current_thread, "is_alive", lambda: False)():
            stop_evt = threading.Event()
            safe_set_session("assistant_stop_event", stop_evt)
            t = threading.Thread(target=run_voice_assistant_in_thread, args=(stop_evt,), daemon=True)
            t.start()
            safe_set_session("assistant_thread", t)
            st.sidebar.success("Voice assistant running (background).")
            append_debug("Voice assistant thread started.")
        else:
            st.sidebar.info("Voice assistant is already running.")

    if stop_btn:
        evt = st.session_state.get("assistant_stop_event", None)
        if evt:
            evt.set()
            safe_set_session("assistant_thread", None)
            safe_set_session("assistant_stop_event", None)
            st.sidebar.info("Stopping voice assistant...")
            append_debug("Voice assistant stop requested.")
        else:
            st.sidebar.info("Voice assistant is not running.")


# ----------------------------
# Optionally: single-command helper for manual test
# ----------------------------
def single_command_test():
    """
    Run a single voice command (blocking), useful for quick testing from main thread:
    command = take_command()
    handle_voice_command(command)
    """
    cmd = take_command()
    if cmd:
        handle_voice_command(cmd)

