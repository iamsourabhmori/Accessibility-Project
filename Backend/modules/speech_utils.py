# modules/speech_utils.py

import webrtcvad
import soundfile as sf
import numpy as np
from io import BytesIO

def is_speech_present(wav_bytes, sample_rate=16000, frame_duration=30):
    """
    Detect if speech is present in audio or extracted audio from video.
    
    Parameters:
    - wav_bytes: BytesIO or file-like object containing WAV audio
    - sample_rate: expected sample rate for VAD
    - frame_duration: frame duration in ms

    Returns:
    - True if speech is detected, False if mostly music
    """

    try:
        # Ensure BytesIO pointer is at start
        if isinstance(wav_bytes, BytesIO):
            wav_bytes.seek(0)

        with sf.SoundFile(wav_bytes) as f:
            audio = f.read(dtype='int16')  # VAD expects int16 PCM
            sr = f.samplerate

            if sr != sample_rate:
                raise ValueError("Sample rate mismatch for VAD")

            # Convert to mono if needed
            if audio.ndim > 1:
                audio = np.mean(audio, axis=1).astype(np.int16)

            # Initialize VAD
            vad = webrtcvad.Vad(1)  # 0-3, 1 is low aggressiveness
            frame_size = int(sample_rate * frame_duration / 1000)
            speech_frames = 0
            total_frames = 0

            for start in range(0, len(audio), frame_size):
                end = start + frame_size
                if end > len(audio):
                    break
                frame = audio[start:end].tobytes()
                if vad.is_speech(frame, sample_rate):
                    speech_frames += 1
                total_frames += 1

            if total_frames == 0:
                return False

            speech_ratio = speech_frames / total_frames
            return speech_ratio > 0.1  # True if more than 10% frames have speech

    except Exception:
        # For video or audio errors, assume speech present
        return True

# ------------------------
# Video transcription note:
# ------------------------
# 1. Extract audio from video using audio_handler.extract_audio_from_video()
# 2. Pass the resulting WAV BytesIO to is_speech_present()
# 3. No additional VAD logic is needed

