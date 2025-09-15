
# # modules/utils.py

# import streamlit as st
# from io import BytesIO
# import mimetypes
# from PIL import Image

# # --- Audio & Video Helpers ---

# def display_words_streamlit(word, placeholder=None):
#     """
#     Display words in real-time in Streamlit.
#     Works for audio/video transcriptions or voice command display.
#     """
#     if placeholder:
#         try:
#             current_text = placeholder.text_area("Real-time transcription:", "", height=150)
#             placeholder.text_area("Real-time transcription:", current_text + " " + word, height=150)
#         except Exception:
#             st.write(word, end=" ")
#     else:
#         st.write(word, end=" ")


# def download_transcript(text, filename="transcript.txt"):
#     """
#     Provide a download button for the transcript.
#     Works for audio/video transcription or voice command transcript.
#     """
#     st.download_button(
#         label="⬇️ Download Transcript",
#         data=text,
#         file_name=filename,
#         mime="text/plain"
#     )


# def save_transcript(text, audio_file=None, output_dir=None):
#     """
#     Save transcript to a local file optionally in a specific directory.
#     Args:
#         text (str): transcript text
#         audio_file (str): optional, original file name for naming transcript
#         output_dir (str): optional, directory to save transcript
#     Returns:
#         str: path to saved transcript
#     """
#     import os

#     if audio_file:
#         base_name = os.path.splitext(os.path.basename(audio_file))[0]
#         filename = f"{base_name}_transcript.txt"
#     else:
#         filename = "transcript.txt"

#     if output_dir:
#         os.makedirs(output_dir, exist_ok=True)
#         filename = os.path.join(output_dir, filename)

#     with open(filename, "w", encoding="utf-8") as f:
#         f.write(text)

#     return filename


# # --- Video-specific helpers ---

# def get_video_info(file_bytes: BytesIO):
#     """
#     Get video metadata: duration (seconds), fps, mime type.
#     """
#     try:
#         import cv2
#         import tempfile

#         file_bytes.seek(0)
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
#             tmp_file.write(file_bytes.read())
#             tmp_file_path = tmp_file.name

#         cap = cv2.VideoCapture(tmp_file_path)
#         if not cap.isOpened():
#             return None

#         fps = cap.get(cv2.CAP_PROP_FPS)
#         frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
#         duration = frame_count / fps if fps > 0 else 0

#         cap.release()
#         mimetype, _ = mimetypes.guess_type(tmp_file_path)

#         return {
#             "duration_sec": duration,
#             "fps": fps,
#             "mime_type": mimetype or "video/mp4"
#         }

#     except Exception:
#         return None


# def display_video_info(file_bytes: BytesIO, placeholder=None):
#     """
#     Display video metadata in Streamlit.
#     """
#     info = get_video_info(file_bytes)
#     if info:
#         msg = f"🎬 Video Info: Duration: {info['duration_sec']:.2f}s | FPS: {info['fps']:.1f} | Type: {info['mime_type']}"
#         if placeholder:
#             placeholder.text(msg)
#         else:
#             st.info(msg)


# # --- Image-specific helpers ---

# def display_image_with_caption(image_bytes, caption=None):
#     """
#     Display image in Streamlit with optional caption below it.
#     """
#     if isinstance(image_bytes, (bytes, bytearray)):
#         image_bytes = BytesIO(image_bytes)
#     image = Image.open(image_bytes).convert("RGB")

#     st.image(image, use_column_width=True)
#     if caption:
#         st.caption(caption if caption.startswith("📝") else f"📝 Caption: {caption}")


# def download_caption(caption_text, filename="caption.txt"):
#     """
#     Provide a download button for image captions.
#     """
#     st.download_button(
#         label="⬇️ Download Caption",
#         data=caption_text,
#         file_name=filename,
#         mime="text/plain"
#     )


# modules/utils.py

import os
import io
import re
import mimetypes
import requests
import streamlit as st
from io import BytesIO
from PIL import Image

# ----------------------
# Audio & Transcription Helpers
# ----------------------

def display_words_streamlit(word, placeholder=None):
    """
    Display words in real-time in Streamlit.
    Works for audio/video transcriptions or voice command display.
    """
    if placeholder:
        try:
            current_text = placeholder.text_area("Real-time transcription:", "", height=150)
            placeholder.text_area("Real-time transcription:", current_text + " " + word, height=150)
        except Exception:
            st.write(word, end=" ")
    else:
        st.write(word, end=" ")

def download_transcript(text, filename="transcript.txt"):
    """
    Provide a download button for the transcript.
    Works for audio/video transcription or voice command transcript.
    """
    st.download_button(
        label="⬇️ Download Transcript",
        data=text,
        file_name=filename,
        mime="text/plain"
    )

def save_transcript(text, audio_file=None, output_dir=None):
    """
    Save transcript to a local file optionally in a specific directory.
    Args:
        text (str): transcript text
        audio_file (str): optional, original file name for naming transcript
        output_dir (str): optional, directory to save transcript
    Returns:
        str: path to saved transcript
    """
    if audio_file:
        base_name = os.path.splitext(os.path.basename(audio_file))[0]
        filename = f"{base_name}_transcript.txt"
    else:
        filename = "transcript.txt"

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, filename)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

    return filename

# ----------------------
# Video Helpers
# ----------------------

def get_video_info(file_bytes: BytesIO):
    """
    Get video metadata: duration (seconds), fps, mime type.
    """
    try:
        import cv2
        import tempfile

        file_bytes.seek(0)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
            tmp_file.write(file_bytes.read())
            tmp_file_path = tmp_file.name

        cap = cv2.VideoCapture(tmp_file_path)
        if not cap.isOpened():
            return None

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps if fps > 0 else 0

        cap.release()
        mimetype, _ = mimetypes.guess_type(tmp_file_path)

        return {
            "duration_sec": duration,
            "fps": fps,
            "mime_type": mimetype or "video/mp4"
        }

    except Exception:
        return None

def display_video_info(file_bytes: BytesIO, placeholder=None):
    """
    Display video metadata in Streamlit.
    """
    info = get_video_info(file_bytes)
    if info:
        msg = f"🎬 Video Info: Duration: {info['duration_sec']:.2f}s | FPS: {info['fps']:.1f} | Type: {info['mime_type']}"
        if placeholder:
            placeholder.text(msg)
        else:
            st.info(msg)

# ----------------------
# Image Helpers
# ----------------------

def display_image_with_caption(image_bytes, caption=None):
    """
    Display image in Streamlit with optional caption below it.
    """
    if isinstance(image_bytes, (bytes, bytearray)):
        image_bytes = BytesIO(image_bytes)
    image = Image.open(image_bytes).convert("RGB")

    st.image(image, use_column_width=True)
    if caption:
        st.caption(caption if caption.startswith("📝") else f"📝 Caption: {caption}")

def download_caption(caption_text, filename="caption.txt"):
    """
    Provide a download button for image captions.
    """
    st.download_button(
        label="⬇️ Download Caption",
        data=caption_text,
        file_name=filename,
        mime="text/plain"
    )

# ----------------------
# Document & URL Helpers
# ----------------------

def safe_requests_get(url: str, timeout=10) -> bytes:
    """
    Fetch raw content from a URL safely.
    Returns bytes of content or raises exception if failed.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch URL {url}: {e}")

def is_valid_document_url(url: str) -> bool:
    """
    Check if the URL points to a supported document type (PDF/DOCX/TXT)
    """
    return bool(re.search(r"\.(pdf|docx|txt)$", url, re.IGNORECASE))

def show_error(message: str):
    """
    Display an error in Streamlit and optionally log it.
    """
    st.error(f"❌ {message}")

