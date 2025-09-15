# app/config.py

import os

# Load environment variables or defaults
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CREWAI_API_KEY = os.getenv("CREWAI_API_KEY", "")
TTS_API_KEY = os.getenv("TTS_API_KEY", "")
ASR_API_KEY = os.getenv("ASR_API_KEY", "")

# Other config
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "data/")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "outputs/")
