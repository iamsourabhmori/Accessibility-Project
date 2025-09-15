#test_utils.py
from modules.utils import save_transcript, display_words_streamlit, download_transcript
import os

def test_save_transcript():
    text = "Hello world"

    # Save with audio_file provided
    output_file = save_transcript(text, audio_file="tests/sample.wav", output_dir="tests/outputs")
    assert os.path.exists(output_file)
    os.remove(output_file)  # cleanup

    # Save without audio_file (default name)
    output_file2 = save_transcript(text, audio_file=None, output_dir="tests/outputs")
    assert os.path.exists(output_file2)
    os.remove(output_file2)  # cleanup

def test_display_words_streamlit():
    # Mock Streamlit placeholder
    class MockPlaceholder:
        def __init__(self):
            self.text_value = ""
        def text(self, value):
            self.text_value = value

    placeholder = MockPlaceholder()
    display_words_streamlit("Hello", placeholder)
    assert placeholder.text_value == "Hello"

def test_download_transcript():
    # Only ensure callable, cannot fully test Streamlit button programmatically
    try:
        download_transcript("Sample text", filename="sample.txt")
    except Exception:
        assert False, "download_transcript raised an exception"
