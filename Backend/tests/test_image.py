# test_image.py
import pytest
from io import BytesIO
from PIL import Image
from modules.image_handler import load_image, generate_image_caption, display_image_with_caption

# ------------------------
# Test constants
# ------------------------
TEST_IMAGE_URL = "https://images.unsplash.com/photo-1593642532973-d31b6557fa68"  # Example online image
TEST_IMAGE_LOCAL = BytesIO()

# Create a small blank image in memory for local testing
img = Image.new("RGB", (100, 100), color=(73, 109, 137))
img.save(TEST_IMAGE_LOCAL, format="PNG")
TEST_IMAGE_LOCAL.seek(0)


# ------------------------
# Test functions
# ------------------------

def test_load_image_from_bytesio():
    """Test loading image from BytesIO"""
    loaded_img = load_image(TEST_IMAGE_LOCAL)
    assert loaded_img is not None
    assert isinstance(loaded_img, Image.Image)
    assert loaded_img.size == (100, 100)


def test_load_image_from_url():
    """Test loading image from URL"""
    loaded_img = load_image(TEST_IMAGE_URL)
    assert loaded_img is not None
    assert isinstance(loaded_img, Image.Image)


def test_generate_image_caption():
    """Test generating caption for an image"""
    loaded_img = load_image(TEST_IMAGE_LOCAL)
    caption = generate_image_caption(loaded_img)
    assert caption is not None
    assert isinstance(caption, str)
    assert len(caption) > 0


def test_display_image_with_caption(monkeypatch):
    """Test Streamlit image display with caption (mocked)"""
    loaded_img = load_image(TEST_IMAGE_LOCAL)

    # Patch st.image and st.caption to avoid actual Streamlit UI calls
    fake_image_called = {}
    fake_caption_called = {}

    import streamlit as st

    def fake_image(img, use_column_width):
        fake_image_called["called"] = True
        fake_image_called["img"] = img

    def fake_caption(text):
        fake_caption_called["called"] = True
        fake_caption_called["text"] = text

    monkeypatch.setattr(st, "image", fake_image)
    monkeypatch.setattr(st, "caption", fake_caption)

    display_image_with_caption(TEST_IMAGE_LOCAL, caption="Test caption")

    assert fake_image_called.get("called") is True
    assert fake_caption_called.get("called") is True
    assert fake_caption_called.get("text") == "📝 Caption: Test caption"
