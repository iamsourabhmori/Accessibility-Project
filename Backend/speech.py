# speech.py
import speech_recognition as sr
import pyttsx3
import streamlit as st
import os
from difflib import get_close_matches
from typing import Optional

# Path to Downloads folder
DOWNLOADS_PATH = "/home/digi2/Downloads"

# Initialize text-to-speech engine only once (best-effort; may fail on headless servers)
try:
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)  # speaking speed
    engine.setProperty("volume", 1.0)
except Exception:
    engine = None


# ---------- Utilities ----------
def append_debug(msg: str):
    """
    Append a message to streamlit session debug log and also print it.
    """
    try:
        if "voice_debug_logs" not in st.session_state:
            st.session_state["voice_debug_logs"] = []
        st.session_state["voice_debug_logs"].append(msg)
    except Exception:
        # If Streamlit context not available, still print
        pass
    print("[VOICE-DEBUG]", msg)


def safe_tts(text: str):
    """
    Try to speak text using pyttsx3 if available, but do not raise on failure.
    """
    global engine
    if not text:
        return
    if engine is None:
        return
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        append_debug(f"TTS error: {e}")


# ---------- High-level voice helpers ----------
def talk(text: str):
    """
    Speak text (best-effort) and display it in the Streamlit UI.
    Also logs to session_state debug logs.
    """
    try:
        # show in Streamlit when available
        st.write(f"🗣️ Assistant: {text}")
    except Exception:
        # no Streamlit context (background thread) — skip UI write
        pass

    append_debug(f"Assistant: {text}")
    try:
        safe_tts(text)
    except Exception:
        # never crash the app because of tts
        append_debug("TTS failed (ignored).")


def take_command(timeout: int = 5, phrase_time_limit: int = 7) -> str:
    """
    Listen for a voice command and return it as text.
    If running in an environment without microphone, returns empty string.
    """
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            try:
                # Show a small message in UI if possible
                try:
                    st.write("🎤 Listening... (Speak now)")
                except Exception:
                    pass
                voice = listener.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                command = listener.recognize_google(voice)
                command = command.lower().strip()
                try:
                    st.write(f"👉 You said: {command}")
                except Exception:
                    pass
                append_debug(f"Recognized: {command}")
                return command
            except sr.WaitTimeoutError:
                append_debug("No speech detected (timeout).")
                try:
                    st.warning("⏳ No speech detected, try again...")
                except Exception:
                    pass
                return ""
            except sr.UnknownValueError:
                append_debug("Speech not understood.")
                try:
                    st.warning("❌ Could not understand audio")
                except Exception:
                    pass
                return ""
            except sr.RequestError as e:
                append_debug(f"STT request error: {e}")
                try:
                    st.error("⚠️ Could not request results, check internet connection")
                except Exception:
                    pass
                return ""
    except Exception as e:
        # Microphone not available or other platform error — return empty
        append_debug(f"Microphone/listening error: {e}")
        try:
            st.warning("🎤 Microphone not available or permission denied.")
        except Exception:
            pass
        return ""


# ---------- Command / filename parsing ----------
PREFIXES = [
    "open ",
    "open the ",
    "upload ",
    "upload the ",
    "please open ",
    "please upload ",
    "play ",
    "pick ",
    "load "
]


def _strip_prefixes(s: str) -> str:
    """
    Remove common prefixes and leading/trailing quotes/spaces.
    """
    if not s:
        return ""
    s = s.strip()
    # Remove surrounding quotes if present
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        s = s[1:-1].strip()
    # Remove prefixes
    lowered = s.lower()
    for p in PREFIXES:
        if lowered.startswith(p):
            s = s[len(p):].strip()
            lowered = s.lower()
            break
    # Many users say 'george.mp3' or 'george dot mp3' — normalize obvious ' dot ' occurrences
    s = s.replace(" dot ", ".")
    s = s.replace(" point ", ".")
    return s.strip()


def parse_filename_from_command(command: str) -> str:
    """
    Try extract a filename from spoken command.
    Examples:
        "open george.mp3" -> "george.mp3"
        "upload george" -> "george"
        "'IAS.mp4'" -> "IAS.mp4"
    """
    if not command:
        return ""
    cmd = command.strip()
    # If user said "<tab name> tab" we shouldn't parse file
    lower = cmd.lower()
    if lower.endswith(" tab"):
        return ""
    # Remove 'open download folder' full command -> no filename
    if "download folder" in lower or lower == "open downloads" or lower == "open download":
        return ""
    # remove prefixes and quotes
    return _strip_prefixes(cmd)


# ---------- File matching & picking ----------
EXTENSIONS = {
    "audio": [".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac"],
    "video": [".mp4", ".mov", ".mkv", ".avi", ".webm", ".flv"],
    "image": [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"],
    "document": [".pdf", ".docx", ".txt"]
}


def _list_files_of_type(file_type: str):
    exts = EXTENSIONS.get(file_type, [])
    try:
        files = [f for f in os.listdir(DOWNLOADS_PATH) if any(f.lower().endswith(ext) for ext in exts)]
    except Exception as e:
        append_debug(f"Error listing Downloads: {e}")
        files = []
    return files


def match_file_by_name(spoken_name: str, file_type: str = "audio") -> str:
    """
    Match a spoken file name to the closest file in Downloads folder
    and store in Streamlit session_state.
    Returns full path or empty string on no-match.
    """
    spoken_name = (spoken_name or "").strip()
    if not spoken_name:
        append_debug("match_file_by_name: no spoken name provided")
        return ""

    name = parse_filename_from_command(spoken_name)
    if not name:
        append_debug("match_file_by_name: parsed name empty after stripping")
        return ""

    files = _list_files_of_type(file_type)
    append_debug(f"Looking for '{name}' among {len(files)} {file_type} files")

    if not files:
        talk(f"No {file_type} files found in Downloads folder.")
        return ""

    # Exact match (case-insensitive)
    for f in files:
        if f.lower() == name.lower():
            full_path = os.path.join(DOWNLOADS_PATH, f)
            append_debug(f"Exact match: {full_path}")
            st.session_state[f"voice_{file_type}_file_path"] = full_path
            # Let UI react; caller may call st.experimental_rerun() if needed
            return full_path

    # If user provided extension and exact didn't match, try to match removing spaces
    # e.g., user said "george mp3" -> "george.mp3"
    if "." not in name:
        for f in files:
            if f.lower().startswith(name.lower()):
                full_path = os.path.join(DOWNLOADS_PATH, f)
                append_debug(f"Prefix match: {full_path}")
                st.session_state[f"voice_{file_type}_file_path"] = full_path
                return full_path

    # Partial substring match
    for f in files:
        if name.lower() in f.lower():
            full_path = os.path.join(DOWNLOADS_PATH, f)
            append_debug(f"Partial substring match: {full_path}")
            st.session_state[f"voice_{file_type}_file_path"] = full_path
            return full_path

    # Fuzzy match using difflib
    matches = get_close_matches(name.lower(), [f.lower() for f in files], n=1, cutoff=0.6)
    if matches:
        matched_file = matches[0]
        full_path = os.path.join(DOWNLOADS_PATH, matched_file)
        append_debug(f"Fuzzy match: {full_path}")
        st.session_state[f"voice_{file_type}_file_path"] = full_path
        return full_path

    # No match
    append_debug(f"No match found for '{name}'")
    talk(f"Could not find a {file_type} file matching '{name}'")
    return ""


def match_file_by_name_debug(spoken_name: str, file_type: str = "audio") -> str:
    """
    Debug version that prints lots of internal state and returns the matched path.
    """
    append_debug(f"[DEBUG] Spoken name raw: {spoken_name}")
    append_debug(f"[DEBUG] Requested file type: {file_type}")
    files = _list_files_of_type(file_type)
    append_debug(f"[DEBUG] Available files ({len(files)}): {files}")

    if not files:
        talk(f"No {file_type} files found in Downloads folder.")
        return ""

    name = parse_filename_from_command(spoken_name)
    append_debug(f"[DEBUG] Parsed name: {name}")

    # exact
    for f in files:
        if f.lower() == name.lower():
            full_path = os.path.join(DOWNLOADS_PATH, f)
            append_debug(f"[DEBUG] Exact match found: {full_path}")
            st.session_state[f"voice_{file_type}_file_path"] = full_path
            return full_path

    # substring
    for f in files:
        if name.lower() in f.lower():
            full_path = os.path.join(DOWNLOADS_PATH, f)
            append_debug(f"[DEBUG] Substring match found: {full_path}")
            st.session_state[f"voice_{file_type}_file_path"] = full_path
            return full_path

    matches = get_close_matches(name.lower(), [f.lower() for f in files], n=3, cutoff=0.4)
    append_debug(f"[DEBUG] difflib matches: {matches}")
    if matches:
        full_path = os.path.join(DOWNLOADS_PATH, matches[0])
        append_debug(f"[DEBUG] Chosen fuzzy match: {full_path}")
        st.session_state[f"voice_{file_type}_file_path"] = full_path
        return full_path

    append_debug("[DEBUG] No match found")
    talk(f"Could not find a {file_type} file matching '{name}'")
    return ""


def pick_file_from_command(command: str, file_type: str = "audio") -> Optional[str]:
    """
    Convenience wrapper: parse command and attempt to pick the file.
    Returns full path or None.
    """
    if not command:
        return None
    # Try to extract a filename first
    parsed = parse_filename_from_command(command)
    if not parsed:
        # maybe the command was just the filename (no prefix)
        parsed = command.strip()
    path = match_file_by_name(parsed, file_type=file_type)
    return path or None


# ---------- Tab switching ----------
TAB_KEYWORDS = {
    "audio": ["audio", "audio tab", "audio tab please", "go to audio"],
    "video": ["video", "video tab", "video tab please", "go to video", "play video"],
    "image": ["image", "image tab", "image tab please", "go to image", "open image"],
    "document": ["document", "document tab", "document tab please", "go to document", "open document", "docs", "documento"]
}


def switch_tab_from_command(command: str) -> Optional[str]:
    """
    If the user asked to switch tabs (e.g., "video tab"), update st.session_state['active_tab']
    and return the tab key. Does nothing if no tab keyword detected.
    """
    if not command:
        return None
    cmd = command.lower().strip()

    # explicit phrase variations: check exact and contains
    for tab_key, keywords in TAB_KEYWORDS.items():
        for kw in keywords:
            if cmd == kw or kw in cmd:
                try:
                    st.session_state["active_tab"] = tab_key
                except Exception:
                    # If we are in a background thread, writing session_state may fail — still return the tab
                    pass
                talk(f"Switched to {tab_key} tab.")
                append_debug(f"switch_tab_from_command: switched to {tab_key}")
                return tab_key
    return None


# ---------- End of file ----------


