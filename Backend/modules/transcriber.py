# transcriber.py

import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import soundfile as sf
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import io

# ------------------------
# Audio/Video (Wav2Vec2)
# ------------------------
processor = None
model = None

def load_wav2vec2_model():
    """
    Load the Hugging Face Wav2Vec2 model and processor.
    Works for both audio and video (audio extracted from video).
    """
    global processor, model
    if processor is None or model is None:
        processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
        model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    return processor, model

def transcribe_audio(audio_bytes, display_callback=None, source_type="audio"):
    """
    Transcribe audio (BytesIO) to text using Wav2Vec2.
    
    Parameters:
        audio_bytes: BytesIO object containing audio data (from file or extracted from video)
        display_callback: Optional function(word) to display words in real-time
        source_type: "audio" or "video" - used for clarity/logs
        
    Returns:
        transcript (str)
    """
    processor, model = load_wav2vec2_model()

    # Read audio from BytesIO
    audio_bytes.seek(0)
    speech, rate = sf.read(audio_bytes)
    if len(speech.shape) > 1:
        speech = speech.mean(axis=1)  # Convert to mono

    # Process entire audio
    inputs = processor(speech, sampling_rate=rate, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits

    pred_ids = torch.argmax(logits, dim=-1)
    transcript = processor.batch_decode(pred_ids)[0]

    # Optional: call display callback for each word
    if display_callback:
        for word in transcript.split():
            display_callback(word)

    # -------------------
    # Video-specific note (for clarity)
    # Compatible with audio extracted from video.
    # -------------------

    return transcript.strip()


# ------------------------
# Image (BLIP captioning)
# ------------------------
caption_processor = None
caption_model = None

def load_image_caption_model():
    """
    Load the BLIP image captioning model.
    """
    global caption_processor, caption_model
    if caption_processor is None or caption_model is None:
        caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return caption_processor, caption_model

def transcribe_image(image_bytes):
    """
    Generate a caption/description for an image.
    
    Parameters:
        image_bytes: BytesIO or raw bytes of the image
    
    Returns:
        caption (str)
    """
    processor, model = load_image_caption_model()

    if isinstance(image_bytes, (bytes, bytearray)):
        image_bytes = io.BytesIO(image_bytes)
    image = Image.open(image_bytes).convert("RGB")

    inputs = processor(image, return_tensors="pt")
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=30)

    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption.strip()


