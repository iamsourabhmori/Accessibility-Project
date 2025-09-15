
# modules/audio_handler.py

from pydub import AudioSegment
from io import BytesIO
import requests
import tempfile
import streamlit as st
import mimetypes
import os
import moviepy.editor as mp  # For video handling

# ------------------------
# Ensure MoviePy uses a TMP folder with enough space
# ------------------------
TMP_DIR = "/home/digi2/Downloads/tmp"
os.makedirs(TMP_DIR, exist_ok=True)
os.environ["TMPDIR"] = TMP_DIR

# ------------------------
# Audio Handlers
# ------------------------
def load_audio_file(uploaded_file):
    """
    Load uploaded audio file into memory as BytesIO.
    """
    try:
        return BytesIO(uploaded_file.read())
    except Exception as e:
        st.error(f"❌ Error reading uploaded file: {e}")
        return None


def validate_audio_url(url: str) -> bool:
    """
    Validate that the URL is reachable and points to an audio file.
    """
    try:
        head = requests.head(url, allow_redirects=True, timeout=5)
        content_type = head.headers.get("Content-Type", "")
        if "audio" in content_type:
            return True
        st.error(
            "❌ The provided URL is not an audio file. "
            "Please provide a direct audio link (.mp3, .wav, .m4a, etc.)"
        )
        return False
    except requests.exceptions.RequestException:
        st.error("❌ Invalid or unreachable URL. Please check the link and try again.")
        return False


def download_audio_from_url(url: str):
    """
    Download audio from a validated URL into a BytesIO object.
    """
    if not validate_audio_url(url):
        return None
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        return BytesIO(response.content)
    except Exception as e:
        st.error(f"❌ Failed to download audio file: {e}")
        return None


def convert_to_wav(file_bytes):
    """
    Convert audio (BytesIO or file path) to WAV format in-memory.
    Returns a BytesIO object.
    """
    try:
        if isinstance(file_bytes, BytesIO):
            file_bytes.seek(0)
            audio = AudioSegment.from_file(file_bytes)
        else:
            audio = AudioSegment.from_file(file_bytes)
        wav_io = BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        return wav_io
    except Exception as e:
        st.error(f"❌ Error converting file to WAV: {e}")
        return None


def resample_audio_to_16k(file_bytes):
    """
    Convert audio to WAV format, resample to 16 kHz, and mono.
    """
    try:
        file_bytes.seek(0)
        audio = AudioSegment.from_file(file_bytes)
        audio = audio.set_frame_rate(16000).set_channels(1)
        wav_io = BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        return wav_io
    except Exception as e:
        st.error(f"❌ Error resampling audio to 16 kHz: {e}")
        return None


def save_uploaded_file(uploaded_file):
    """
    Save uploaded file temporarily and return the path.
    """
    try:
        suffix = os.path.splitext(uploaded_file.name)[1] or ".tmp"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=TMP_DIR) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            return tmp_file.name
    except Exception as e:
        st.error(f"❌ Error saving uploaded file: {e}")
        return None


# ------------------------
# Video Handlers
# ------------------------
def load_video_file(uploaded_file):
    """
    Load uploaded video file into temporary path.
    """
    try:
        return save_uploaded_file(uploaded_file)
    except Exception as e:
        st.error(f"❌ Error reading uploaded video file: {e}")
        return None


def download_video_from_url(url: str):
    """
    Download video from a validated URL into a temporary file path.
    """
    try:
        response = requests.get(url, stream=True, timeout=15)
        response.raise_for_status()
        suffix = os.path.splitext(url)[1] or ".mp4"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=TMP_DIR) as tmp_file:
            for chunk in response.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
            return tmp_file.name
    except Exception as e:
        st.error(f"❌ Failed to download video file: {e}")
        return None


# def extract_audio_from_video(video_input) -> BytesIO:
#     """
#     Extract audio from a video input (BytesIO or file path) and return as BytesIO WAV.
#     """
#     try:
#         # Determine if input is BytesIO or file path
#         if isinstance(video_input, BytesIO):
#             # Save to temporary file
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4", dir=TMP_DIR) as tmp_video_file:
#                 tmp_video_file.write(video_input.read())
#                 video_path = tmp_video_file.name
#         else:
#             video_path = video_input

#         clip = mp.VideoFileClip(video_path)
#         if clip.audio is None:
#             st.warning("⚠️ No audio track found in this video.")
#             clip.close()
#             if isinstance(video_input, BytesIO):
#                 os.remove(video_path)
#             return None

#         # Save audio to temporary WAV file
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir=TMP_DIR) as tmp_audio_file:
#             clip.audio.write_audiofile(
#                 tmp_audio_file.name,
#                 codec="pcm_s16le",
#                 fps=16000,
#                 verbose=False,
#                 logger=None
#             )
#             tmp_audio_path = tmp_audio_file.name

#         # Read WAV into BytesIO
#         audio_bytes = BytesIO()
#         with open(tmp_audio_path, "rb") as f:
#             audio_bytes.write(f.read())
#         audio_bytes.seek(0)

#         # Clean up
#         clip.audio.close()
#         clip.close()
#         os.remove(tmp_audio_path)
#         if isinstance(video_input, BytesIO):
#             os.remove(video_path)

#         return audio_bytes

#     except Exception as e:
#         st.error(f"❌ Failed to extract audio from video: {e}")
#         return None

def extract_audio_from_video(video_input):
    """
    Extract audio from a video (BytesIO or file path).
    
    Args:
        video_input (BytesIO | str): Video file in memory (BytesIO) or path to video file.
    
    Returns:
        tuple: (success, result)
            - On success: (True, BytesIO of WAV audio)
            - On failure: (False, error message string)
    """
    tmp_video_path = None
    tmp_audio_path = None

    try:
        # Handle BytesIO vs file path
        if isinstance(video_input, BytesIO):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video_file:
                tmp_video_file.write(video_input.read())
                tmp_video_path = tmp_video_file.name
        else:
            tmp_video_path = video_input

        # Open video
        clip = mp.VideoFileClip(tmp_video_path)

        if clip.audio is None:
            clip.close()
            if isinstance(video_input, BytesIO) and tmp_video_path:
                os.remove(tmp_video_path)
            return False, "No audio track found in this video."

        # Save audio to temp WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio_file:
            tmp_audio_path = tmp_audio_file.name
            clip.audio.write_audiofile(
                tmp_audio_path,
                codec="pcm_s16le",
                fps=16000,
                verbose=False,
                logger=None
            )

        # Load into BytesIO
        audio_bytes = BytesIO()
        with open(tmp_audio_path, "rb") as f:
            audio_bytes.write(f.read())
        audio_bytes.seek(0)

        # Cleanup
        clip.audio.close()
        clip.close()
        if tmp_audio_path and os.path.exists(tmp_audio_path):
            os.remove(tmp_audio_path)
        if isinstance(video_input, BytesIO) and tmp_video_path and os.path.exists(tmp_video_path):
            os.remove(tmp_video_path)

        return True, audio_bytes

    except Exception as e:
        # Cleanup in case of failure
        if tmp_audio_path and os.path.exists(tmp_audio_path):
            os.remove(tmp_audio_path)
        if isinstance(video_input, BytesIO) and tmp_video_path and os.path.exists(tmp_video_path):
            os.remove(tmp_video_path)
        return False, f"Failed to extract audio: {e}"