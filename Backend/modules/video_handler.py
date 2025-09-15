
# modules/video_handler.py

import streamlit as st
from io import BytesIO
import requests
import tempfile
import os
from moviepy.editor import VideoFileClip


# ------------------------
# Video Handlers
# ------------------------
def load_video_file(uploaded_file):
    """
    Load uploaded video file into memory as BytesIO.
    """
    try:
        return BytesIO(uploaded_file.read())
    except Exception as e:
        st.error(f"❌ Error reading uploaded video file: {e}")
        return None


def validate_video_url(url: str) -> bool:
    """
    Validate that the URL is reachable and points to a video file.
    """
    try:
        head = requests.head(url, allow_redirects=True, timeout=5)
        content_type = head.headers.get("Content-Type", "")
        if "video" in content_type:
            return True
        else:
            st.error(
                "❌ The provided URL is not a video file. "
                "Please provide a direct video link (.mp4, .mov, .mkv, etc.)"
            )
            return False
    except requests.exceptions.RequestException:
        st.error("❌ Invalid or unreachable video URL. Please check the link and try again.")
        return False


def download_video_from_url(url: str):
    """
    Download video from a validated URL into a BytesIO object.
    """
    if not validate_video_url(url):
        return None
    try:
        response = requests.get(url, stream=True, timeout=15)
        response.raise_for_status()
        return BytesIO(response.content)
    except Exception as e:
        st.error(f"❌ Failed to download video file: {e}")
        return None


def extract_audio_from_video(video_bytes: BytesIO, target_format="wav") -> BytesIO:
    """
    Extract audio from video and return as BytesIO in WAV (or target) format.
    Ensures audio is mono and 16 kHz for ASR (Wav2Vec2 compatibility).
    """
    try:
        # Save video BytesIO to a temporary file
        video_bytes.seek(0)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
            tmp_video.write(video_bytes.read())
            tmp_video_path = tmp_video.name

        clip = VideoFileClip(tmp_video_path)
        if clip.audio is None:
            st.warning("⚠️ No audio track found in this video.")
            clip.close()
            os.remove(tmp_video_path)
            return None

        # Extract audio to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{target_format}") as tmp_audio_file:
            clip.audio.write_audiofile(
                tmp_audio_file.name,
                codec="pcm_s16le",
                fps=16000,
                verbose=False,
                logger=None
            )
            tmp_audio_file_path = tmp_audio_file.name

        # Read audio into BytesIO
        wav_io = BytesIO()
        with open(tmp_audio_file_path, "rb") as f:
            wav_io.write(f.read())
        wav_io.seek(0)

        # Cleanup
        clip.audio.close()
        clip.close()
        os.remove(tmp_video_path)
        os.remove(tmp_audio_file_path)

        return wav_io

    except Exception as e:
        st.error(f"❌ Failed to extract audio from video: {e}")
        return None


def get_video_duration(video_bytes: BytesIO) -> float:
    """
    Returns video duration in seconds.
    """
    try:
        video_bytes.seek(0)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
            tmp_video.write(video_bytes.read())
            tmp_video_path = tmp_video.name

        clip = VideoFileClip(tmp_video_path)
        duration = clip.duration
        clip.close()
        os.remove(tmp_video_path)
        return duration
    except Exception:
        return 0.0


def save_uploaded_video_file(uploaded_file):
    """
    Save uploaded video temporarily and return path.
    """
    try:
        suffix = os.path.splitext(uploaded_file.name)[1] or ".tmp"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            return tmp_file.name
    except Exception as e:
        st.error(f"❌ Error saving uploaded video file: {e}")
        return None


