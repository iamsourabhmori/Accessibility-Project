
# # modules/video_utils.py

# import streamlit as st
# from moviepy.editor import VideoFileClip
# from io import BytesIO
# import tempfile

# # ----------------------
# # Existing helpers
# # ----------------------
# def get_video_info(video_bytes: BytesIO) -> dict:
#     video_bytes.seek(0)
#     try:
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
#             tmp_video.write(video_bytes.read())
#             tmp_video_path = tmp_video.name

#         clip = VideoFileClip(tmp_video_path)
#         info = {
#             "duration": clip.duration,
#             "fps": clip.fps,
#             "resolution": clip.size,
#         }
#         clip.close()
#         return info
#     except Exception as e:
#         st.error(f"❌ Failed to get video info: {e}")
#         return {"duration": 0, "fps": 0, "resolution": (0, 0)}

# def is_video_length_supported(video_bytes: BytesIO, max_duration_sec=3600) -> bool:
#     info = get_video_info(video_bytes)
#     return 0 < info["duration"] <= max_duration_sec

# def is_supported_video_format(filename: str, allowed_ext=None) -> bool:
#     if allowed_ext is None:
#         allowed_ext = (".mp4", ".mov", ".mkv", ".avi", ".webm")
#     return filename.lower().endswith(allowed_ext)

# def check_video_audio_presence(video_bytes: BytesIO) -> bool:
#     try:
#         video_bytes.seek(0)
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
#             tmp_video.write(video_bytes.read())
#             tmp_video_path = tmp_video.name
#         clip = VideoFileClip(tmp_video_path)
#         has_audio = clip.audio is not None
#         clip.close()
#         return has_audio
#     except Exception as e:
#         st.error(f"❌ Error checking audio track in video: {e}")
#         return False

# # ----------------------
# # Functions required by API
# # ----------------------
# def extract_audio_from_video(video_bytes: BytesIO) -> BytesIO:
#     """Extract audio from video and return WAV bytes"""
#     try:
#         video_bytes.seek(0)
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
#             tmp_video.write(video_bytes.read())
#             tmp_video_path = tmp_video.name

#         clip = VideoFileClip(tmp_video_path)
#         if clip.audio is None:
#             clip.close()
#             return None

#         with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
#             clip.audio.write_audiofile(tmp_audio.name)
#             tmp_audio_path = tmp_audio.name

#         clip.close()
#         with open(tmp_audio_path, "rb") as f:
#             audio_bytes = BytesIO(f.read())
#         audio_bytes.seek(0)
#         return audio_bytes
#     except Exception as e:
#         st.error(f"❌ Failed to extract audio: {e}")
#         return None

# def is_valid_video_file(filename: str) -> bool:
#     """Check if the uploaded file is a supported video format"""
#     return is_supported_video_format(filename)

# def is_valid_video_url(url: str) -> bool:
#     """Check if URL has supported video extension"""
#     supported_ext = (".mp4", ".mov", ".mkv", ".avi", ".webm")
#     return url.lower().endswith(supported_ext)



#-------------------------------------------------------------------------------------------------------------------


# modules/video_utils.py

import streamlit as st
from moviepy.editor import VideoFileClip
from io import BytesIO
import tempfile
import os


# ----------------------
# Existing helpers
# ----------------------
def get_video_info(video_bytes: BytesIO) -> dict:
    video_bytes.seek(0)
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
            tmp_video.write(video_bytes.read())
            tmp_video_path = tmp_video.name

        clip = VideoFileClip(tmp_video_path)
        info = {
            "duration": clip.duration,
            "fps": clip.fps,
            "resolution": clip.size,
        }
        clip.close()
        return info
    except Exception as e:
        st.error(f"❌ Failed to get video info: {e}")
        return {"duration": 0, "fps": 0, "resolution": (0, 0)}


def is_video_length_supported(video_bytes: BytesIO, max_duration_sec=3600) -> bool:
    info = get_video_info(video_bytes)
    return 0 < info["duration"] <= max_duration_sec


def is_supported_video_format(filename: str, allowed_ext=None) -> bool:
    if allowed_ext is None:
        allowed_ext = (".mp4", ".mov", ".mkv", ".avi", ".webm")
    return filename.lower().endswith(allowed_ext)


def check_video_audio_presence(video_bytes: BytesIO) -> bool:
    try:
        video_bytes.seek(0)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
            tmp_video.write(video_bytes.read())
            tmp_video_path = tmp_video.name
        clip = VideoFileClip(tmp_video_path)
        has_audio = clip.audio is not None
        clip.close()
        return has_audio
    except Exception as e:
        st.error(f"❌ Error checking audio track in video: {e}")
        return False


# ----------------------
# Fixed extract_audio_from_video
# ----------------------
def extract_audio_from_video(video_bytes):
    """
    Extract audio from a video and save to a temporary WAV file.

    Returns:
        (bool, str) → (success flag, .wav file path or error message)
    """
    try:
        video_bytes.seek(0)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
            tmp_video.write(video_bytes.read())
            video_path = tmp_video.name

        video_clip = VideoFileClip(video_path)
        if not video_clip.audio:
            video_clip.close()
            return False, "No audio track found in video"

        audio_path = video_path.replace(".mp4", ".wav")
        video_clip.audio.write_audiofile(audio_path, codec="pcm_s16le", verbose=False, logger=None)
        video_clip.close()

        return True, audio_path   # ✅ Always tuple

    except Exception as e:
        return False, str(e)      # ✅ Always tuple


def is_valid_video_file(filename: str) -> bool:
    """Check if the uploaded file is a supported video format"""
    return is_supported_video_format(filename)


def is_valid_video_url(url: str) -> bool:
    """Check if URL has supported video extension"""
    supported_ext = (".mp4", ".mov", ".mkv", ".avi", ".webm")
    return url.lower().endswith(supported_ext)
