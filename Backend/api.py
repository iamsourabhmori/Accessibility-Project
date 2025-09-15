
# api.py
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import io
import uuid
import requests
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# Project modules
from modules.huggingface_model import load_wav2vec2_model
from modules.audio_handler import resample_audio_to_16k
from modules.speech_utils import is_speech_present
from modules.video_utils import extract_audio_from_video, is_valid_video_file, is_valid_video_url
from modules.voice_commands import parse_voice_command  # NEW: voice command parser

# ------------------------
# FastAPI app setup
# ------------------------
app = FastAPI(
    title="Audio, Video, Image & Voice Command Transcriber API",
    version="3.0.0",
    description="Wav2Vec2-based audio/video transcriber with music detection, BLIP-based image captioning, and voice command execution."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Load HF models once
processor, model = load_wav2vec2_model()
TARGET_SR = 16000
tasks = {}  # Store background transcription tasks

# Image captioning model (BLIP)
caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# ------------------------
# Payload models
# ------------------------
class URLPayload(BaseModel):
    url: HttpUrl
    type: str = "audio"  # audio, video, or image

# ------------------------
# Helper functions
# ------------------------
def _transcribe_wav_bytes(wav_bytes: bytes) -> str:
    """Run inference on 16kHz WAV bytes and return transcript."""
    import soundfile as sf
    with sf.SoundFile(io.BytesIO(wav_bytes)) as f:
        audio = f.read(dtype="float32")
        sr = f.samplerate

    if sr != TARGET_SR:
        raise HTTPException(status_code=400, detail=f"WAV samplerate must be {TARGET_SR}. Got {sr}.")

    inputs = processor(audio, sampling_rate=sr, return_tensors="pt").input_values
    with torch.no_grad():
        logits = model(inputs).logits
    pred_ids = torch.argmax(logits, dim=-1)
    text = processor.batch_decode(pred_ids)[0]

    return text.strip()


def run_transcription_task(task_id: str, wav_bytes: bytes):
    """Background task to handle transcription with music-only detection."""
    try:
        # Check if audio contains speech
        if not is_speech_present(io.BytesIO(wav_bytes)):
            tasks[task_id]["transcript"] = "⚠️ This file contains only music. No speech detected."
        else:
            transcript = _transcribe_wav_bytes(wav_bytes)
            tasks[task_id]["transcript"] = transcript

        tasks[task_id]["status"] = "completed"
        tasks[task_id]["progress"] = 100
    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["progress"] = 0
        tasks[task_id]["error"] = str(e)

def _generate_caption(image: Image.Image) -> str:
    """Generate caption using BLIP model."""
    inputs = caption_processor(image, return_tensors="pt")
    with torch.no_grad():
        out = caption_model.generate(**inputs, max_new_tokens=30)
    return caption_processor.decode(out[0], skip_special_tokens=True)

# ------------------------
# Health check
# ------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ------------------------
# File upload endpoint (Audio/Video)
# ------------------------
@app.post("/transcribe/file")
async def transcribe_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = None, type: str = "audio"):
    raw = await file.read()
    wav_io = None

    if type == "audio":
        wav_io = resample_audio_to_16k(io.BytesIO(raw))
        if wav_io is None:
            raise HTTPException(status_code=400, detail="Failed to decode audio")
    elif type == "video":
        if not is_valid_video_file(file.filename):
            raise HTTPException(status_code=400, detail="Unsupported video file format")
        wav_io = extract_audio_from_video(io.BytesIO(raw))
        if wav_io is None:
            raise HTTPException(status_code=400, detail="Failed to extract audio from video")

    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "processing", "progress": 0, "transcript": None}

    background_tasks.add_task(run_transcription_task, task_id, wav_io.getvalue())
    return {"task_id": task_id}

# ------------------------
# URL-based transcription (Audio/Video)
# ------------------------
@app.post("/transcribe/url")
def transcribe_url(payload: URLPayload, background_tasks: BackgroundTasks = None):
    try:
        resp = requests.get(payload.url, stream=True, timeout=15)
        resp.raise_for_status()
        wav_io = None

        if payload.type == "audio":
            wav_io = resample_audio_to_16k(io.BytesIO(resp.content))
            if wav_io is None:
                raise HTTPException(status_code=400, detail="Failed to decode audio")
        elif payload.type == "video":
            if not is_valid_video_url(payload.url):
                raise HTTPException(status_code=400, detail="Unsupported video URL or format")
            wav_io = extract_audio_from_video(io.BytesIO(resp.content))
            if wav_io is None:
                raise HTTPException(status_code=400, detail="Failed to extract audio from video")

        task_id = str(uuid.uuid4())
        tasks[task_id] = {"status": "processing", "progress": 0, "transcript": None}

        background_tasks.add_task(run_transcription_task, task_id, wav_io.getvalue())
        return {"task_id": task_id}

    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Network error fetching URL: {e}")

# ------------------------
# Image Captioning (File Upload)
# ------------------------
@app.post("/transcribe/image")
async def transcribe_image(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        caption = _generate_caption(image)
        return {"caption": caption}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image transcription failed: {e}")

# ------------------------
# Image Captioning (URL)
# ------------------------
@app.post("/transcribe/image/url")
def transcribe_image_url(payload: URLPayload):
    try:
        resp = requests.get(payload.url, stream=True, timeout=15)
        resp.raise_for_status()
        image = Image.open(io.BytesIO(resp.content)).convert("RGB")
        caption = _generate_caption(image)
        return {"caption": caption}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image transcription failed: {e}")

# ------------------------
# Voice Command Endpoint
# ------------------------
@app.post("/voice/command")
async def voice_command(file: UploadFile = File(...)):
    """Accept an audio file, transcribe it, and return parsed voice command."""
    try:
        raw = await file.read()
        wav_io = resample_audio_to_16k(io.BytesIO(raw))
        if wav_io is None:
            raise HTTPException(status_code=400, detail="Failed to decode audio")

        transcript = _transcribe_wav_bytes(wav_io.getvalue())
        command = parse_voice_command(transcript)

        return {
            "transcript": transcript,
            "command": command
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Voice command processing failed: {e}")

# ------------------------
# Task status endpoint
# ------------------------
@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

