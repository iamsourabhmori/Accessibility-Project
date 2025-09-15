# test_transcriber.py
from modules.transcriber import transcribe_audio
from modules.audio_handler import convert_to_wav
from pydub import AudioSegment
from io import BytesIO
import whisper

def test_transcribe_audio():
    # Create 1-second silent audio in-memory
    sample_audio = AudioSegment.silent(duration=1000)
    mp3_bytes = BytesIO()
    sample_audio.export(mp3_bytes, format="mp3")
    mp3_bytes.seek(0)

    # Convert MP3 to WAV in-memory
    wav_bytes = convert_to_wav(mp3_bytes)

    # Load tiny Whisper model for testing
    model = whisper.load_model("tiny")

    # Mock callback to capture words
    captured_words = []
    def mock_callback(word):
        captured_words.append(word)

    # Transcribe
    result_text = transcribe_audio(wav_bytes, model, display_callback=mock_callback)

    # Assertions
    assert isinstance(result_text, str)
    assert result_text is not None
    assert isinstance(captured_words, list)
