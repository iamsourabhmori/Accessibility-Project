
# validators.py

import re
import requests

# ------------------------
# Audio Validators
# ------------------------
def is_valid_audio_url(url: str) -> bool:
    """
    Checks if the provided URL is valid and points to a supported audio file.
    Supported extensions: .wav, .mp3, .flac, .ogg, .m4a, .aac
    """
    url_regex = re.compile(
        r'^(https?://)'                 
        r'([A-Za-z0-9\-]+\.)+[A-Za-z]{2,6}'  
        r'(/[^\s]*)?$'                  
    )
    if not url_regex.match(url):
        return False

    allowed_ext = (".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac")
    if not url.lower().endswith(allowed_ext):
        return False

    try:
        resp = requests.get(url, stream=True, timeout=10)
        resp.raise_for_status()
        first_bytes = resp.raw.read(1024)
        if not first_bytes:
            return False
        content_type = resp.headers.get("Content-Type", "")
        if not any(fmt in content_type for fmt in ["audio", "octet-stream"]):
            pass
    except Exception:
        return False

    return True

# ------------------------
# Video Validators
# ------------------------
def is_valid_video_url(url: str) -> bool:
    """
    Checks if the provided URL is valid and points to a supported video file.
    Supported extensions: .mp4, .mov, .avi, .mkv, .webm
    """
    url_regex = re.compile(
        r'^(https?://)'
        r'([A-Za-z0-9\-]+\.)+[A-Za-z]{2,6}'
        r'(/[^\s]*)?$'
    )
    if not url_regex.match(url):
        return False

    allowed_ext = (".mp4", ".mov", ".avi", ".mkv", ".webm")
    if not url.lower().endswith(allowed_ext):
        return False

    try:
        resp = requests.get(url, stream=True, timeout=10)
        resp.raise_for_status()
        first_bytes = resp.raw.read(1024)
        if not first_bytes:
            return False
        content_type = resp.headers.get("Content-Type", "")
        if not any(fmt in content_type for fmt in ["video", "octet-stream"]):
            pass
    except Exception:
        return False

    return True

def is_valid_video_file(filename: str) -> bool:
    """
    Checks if a local uploaded video file has a supported extension.
    """
    allowed_ext = (".mp4", ".mov", ".avi", ".mkv", ".webm")
    return filename.lower().endswith(allowed_ext)

# ------------------------
# Image Validators
# ------------------------
def is_valid_image_url(url: str) -> bool:
    """
    Checks if the provided URL is valid and points to a supported image file.
    Supported extensions: .jpg, .jpeg, .png, .bmp, .gif, .webp
    """
    url_regex = re.compile(
        r'^(https?://)'
        r'([A-Za-z0-9\-]+\.)+[A-Za-z]{2,6}'
        r'(/[^\s]*)?$'
    )
    if not url_regex.match(url):
        return False

    allowed_ext = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp")
    if not url.lower().endswith(allowed_ext):
        return False

    try:
        resp = requests.get(url, stream=True, timeout=10)
        resp.raise_for_status()
        first_bytes = resp.raw.read(1024)
        if not first_bytes:
            return False
        content_type = resp.headers.get("Content-Type", "")
        if not any(fmt in content_type for fmt in ["image", "octet-stream"]):
            pass
    except Exception:
        return False

    return True

def is_valid_image_file(filename: str) -> bool:
    """
    Checks if a local uploaded image file has a supported extension.
    """
    allowed_ext = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp")
    return filename.lower().endswith(allowed_ext)

# ------------------------
# Document Validators (NEW)
# ------------------------
def is_valid_document_url(url: str) -> bool:
    """
    Checks if the provided URL is valid and points to a supported document file.
    Supported extensions: .pdf, .docx, .txt
    """
    url_regex = re.compile(
        r'^(https?://)'
        r'([A-Za-z0-9\-]+\.)+[A-Za-z]{2,6}'
        r'(/[^\s]*)?$'
    )
    if not url_regex.match(url):
        return False

    allowed_ext = (".pdf", ".docx", ".txt")
    if not url.lower().endswith(allowed_ext):
        return False

    try:
        resp = requests.get(url, stream=True, timeout=10)
        resp.raise_for_status()
        first_bytes = resp.raw.read(1024)
        if not first_bytes:
            return False
        content_type = resp.headers.get("Content-Type", "")
        if not any(fmt in content_type for fmt in ["application", "text", "octet-stream"]):
            pass
    except Exception:
        return False

    return True

def is_valid_document_file(filename: str) -> bool:
    """
    Checks if a local uploaded document file has a supported extension.
    """
    allowed_ext = (".pdf", ".docx", ".txt")
    return filename.lower().endswith(allowed_ext)

