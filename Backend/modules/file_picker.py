
#file_picker.py
import os
import pyautogui
import pyperclip
import time
import difflib

# ----------------------------
# Paths and constants
# ----------------------------
DOWNLOADS_PATH = "/home/digi2/Downloads"
PREFIXES = ["open", "upload", "please open", "please upload", "play", "pick"]
VIDEO_EXTENSIONS = (".mp4", ".mkv", ".mov", ".avi", ".flv", ".webm")
AUDIO_EXTENSIONS = (".wav", ".mp3", ".m4a", ".ogg", ".flac", ".aac")

# ----------------------------
# Helpers
# ----------------------------
def get_file_name_from_command(command):
    """
    Extracts the actual file name from the voice command by removing known prefixes.
    """
    cmd = command.lower().strip()
    for p in PREFIXES:
        if cmd.startswith(p):
            cmd = cmd[len(p):].strip()
    return cmd

# ----------------------------
# Audio picker
# ----------------------------
def pick_file_from_command(command, downloads_path=DOWNLOADS_PATH):
    """
    Return full path of audio file matching command exactly, partially, or closely.
    """
    file_name = get_file_name_from_command(command)
    if not file_name:
        return None

    files = [f for f in os.listdir(downloads_path) if f.lower().endswith(AUDIO_EXTENSIONS)]

    # Exact match first
    for f in files:
        if f.lower() == file_name.lower():
            return os.path.join(downloads_path, f)

    # Partial match
    for f in files:
        if file_name.lower() in f.lower():
            return os.path.join(downloads_path, f)

    # Fallback: difflib closest match
    matches = difflib.get_close_matches(file_name, files, n=1, cutoff=0.7)
    if matches:
        return os.path.join(downloads_path, matches[0])

    return None

# ----------------------------
# Video picker
# ----------------------------
def pick_video_from_command(command, downloads_path=DOWNLOADS_PATH):
    """
    Pick a video file from Downloads folder based on voice command.
    """
    cmd = get_file_name_from_command(command)
    if not cmd:
        return None

    files = [f for f in os.listdir(downloads_path) if f.lower().endswith(VIDEO_EXTENSIONS)]

    # Exact match first
    for f in files:
        if f.lower() == cmd.lower():
            return os.path.join(downloads_path, f)

    # Partial match
    for f in files:
        if cmd.lower() in f.lower():
            return os.path.join(downloads_path, f)

    # Fallback to closest match using difflib
    matches = difflib.get_close_matches(cmd, files, n=1, cutoff=0.6)
    if matches:
        return os.path.join(downloads_path, matches[0])

    return None

# ----------------------------
# Switch tab
# ----------------------------
def switch_to_browser_tab():
    """
    Switch to browser tab using Alt+Tab (Linux/Windows).
    """
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')
    time.sleep(0.5)

# ----------------------------
# Upload file to Streamlit
# ----------------------------
def upload_file_to_streamlit(file_path):
    """
    Paste file path into Streamlit uploader and press enter, then optionally trigger button.
    """
    if not os.path.exists(file_path):
        return
    pyperclip.copy(file_path)
    # Click on Streamlit file uploader coordinates (adjust if needed)
    pyautogui.click(500, 400)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(0.3)
    # Click Transcribe / Process button (adjust coordinates)
    pyautogui.click(600, 500)
