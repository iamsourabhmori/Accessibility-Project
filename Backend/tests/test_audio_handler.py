#test_audio_handler.py

from modules.audio_handler import convert_to_wav
from pydub import AudioSegment
from io import BytesIO

def test_convert_to_wav():
    # Create 1-second silent MP3 in-memory
    sample_audio = AudioSegment.silent(duration=1000)
    mp3_bytes = BytesIO()
    sample_audio.export(mp3_bytes, format="mp3")
    mp3_bytes.seek(0)

    # Convert to WAV in-memory
    wav_bytes = convert_to_wav(mp3_bytes)

    # Check output is BytesIO
    assert isinstance(wav_bytes, BytesIO)

    # Verify WAV can be loaded
    wav_audio = AudioSegment.from_file(wav_bytes)
    assert wav_audio.frame_rate == sample_audio.frame_rate
    assert wav_audio.channels == sample_audio.channels
