
# modules/image_handler.py
import streamlit as st
from modules.voice_commands import handle_voice_command

from PIL import Image
from io import BytesIO
import requests
from modules.huggingface_model import load_image_caption_model
from modules.voice_commands import handle_voice_command

# ------------------------
# Image loading helper
# ------------------------
def load_image(file_or_url):
    """
    Load image from uploaded file or URL into PIL.Image.
    """
    try:
        if isinstance(file_or_url, BytesIO):
            file_or_url.seek(0)
            img = Image.open(file_or_url).convert("RGB")
        elif isinstance(file_or_url, str) and file_or_url.startswith("http"):
            resp = requests.get(file_or_url, stream=True, timeout=10)
            resp.raise_for_status()
            img = Image.open(BytesIO(resp.content)).convert("RGB")
        else:
            raise ValueError("Unsupported image input type")
        return img
    except Exception as e:
        st.error(f"⚠️ Failed to load image: {e}")
        return None

# ------------------------
# Image captioning function
# ------------------------
def generate_image_caption(image_pil):
    """
    Generate 2-3 line description/caption for the image using BLIP model.
    """
    processor, model = load_image_caption_model()

    try:
        inputs = processor(images=image_pil, return_tensors="pt")
        outputs = model.generate(**inputs, max_new_tokens=50)  # Limit token length
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        st.error(f"⚠️ Image captioning failed: {e}")
        return "Unable to generate caption"

# ------------------------
# Streamlit display helper
# ------------------------
def display_image_with_caption(file_or_url, caption=None):
    """
    Display image in Streamlit with caption below.
    """
    img = load_image(file_or_url)
    if img is not None:
        st.image(img, use_column_width=True)
        if caption:
            st.caption(f"📝 Caption: {caption}")

# ------------------------
# Voice command handler for image
# ------------------------
def process_image_voice_command(command_text):
    """
    Handle voice commands for image uploading and processing.
    """
    action = handle_voice_command(command_text)

    if action == "upload_image_file":
        uploaded_file = st.file_uploader("📤 Upload an image file", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            img = load_image(uploaded_file)
            if img:
                caption = generate_image_caption(img)
                display_image_with_caption(img, caption)

    elif action == "upload_image_url":
        url = st.text_input("🌐 Enter an image URL")
        if url:
            img = load_image(url)
            if img:
                caption = generate_image_caption(img)
                display_image_with_caption(img, caption)

    else:
        st.info("🎤 Say: 'Upload Image file' or 'Upload Image from the URL'")
