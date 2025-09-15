# tests/test_video_handler.py

import pytest
from io import BytesIO
from modules import video_handler
import os

# Helper: generate a small dummy video for testing
def create_dummy_video_bytes(duration_sec=1, fps=24, resolution=(320, 240)):
    from moviepy.editor import ColorClip
    import tempfile

    clip = ColorClip(size=resolution, color=(255, 0, 0), duration=duration_sec)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        clip.write_videofile(tmp_file.name, fps=fps, codec="libx264", audio=False, verbose=False, logger=None)
        tmp_file.seek(0)
        video_bytes = BytesIO(tmp_file.read())
    clip.close()
    os.remove(tmp_file.name)
    return video_bytes

def test_load_video_file():
    video_bytes = create_dummy_video_bytes()
    path = video_handler.save_uploaded_video(video_bytes, filename="test.mp4")
    assert os.path.exists(path)
    os.remove(path)

def test_is_supported_video_format():
    assert video_handler.is_supported_video_format("movie.mp4")
    assert video_handler.is_supported_video_format("clip.MOV")
    assert not video_handler.is_supported_video_format("audio.mp3")
    assert not video_handler.is_supported_video_format("document.pdf")

def test_get_video_info():
    video_bytes = create_dummy_video_bytes(duration_sec=2)
    info = video_handler.get_video_info(video_bytes)
    assert info["duration"] >= 1.9  # allow slight discrepancy
    assert info["fps"] == 24
    assert info["resolution"] == [320, 240] or info["resolution"] == (320, 240)

def test_is_video_length_supported():
    video_bytes = create_dummy_video_bytes(duration_sec=5)
    assert video_handler.is_video_length_supported(video_bytes, max_duration_sec=10)
    assert not video_handler.is_video_length_supported(video_bytes, max_duration_sec=2)

def test_check_video_audio_presence():
    from moviepy.editor import ColorClip, AudioClip
    import numpy as np
    import tempfile

    # Video with no audio
    video_bytes = create_dummy_video_bytes(duration_sec=1)
    assert not video_handler.check_video_audio_presence(video_bytes)

    # Video with dummy audio
    duration = 1
    fps = 24
    resolution = (320, 240)
    clip = ColorClip(size=resolution, color=(0, 255, 0), duration=duration)
    # Create silent audio
    audio = AudioClip(lambda t: np.zeros_like(t), duration=duration, fps=44100)
    clip = clip.set_audio(audio)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        clip.write_videofile(tmp_file.name, fps=fps, codec="libx264", audio_codec="aac", verbose=False, logger=None)
        tmp_file.seek(0)
        video_bytes_with_audio = BytesIO(tmp_file.read())
    clip.close()
    os.remove(tmp_file.name)
    assert video_handler.check_video_audio_presence(video_bytes_with_audio)
