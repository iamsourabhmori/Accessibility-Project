# tools/file_screenshot_tool.py

import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from docx import Document

def capture_file_screenshot(file_path):
    """
    Reads CSV, TXT, or DOCX files, renders their content as an image,
    and saves it in screenshots/ with timestamp.
    """
    # Ensure screenshots directory exists
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"file_screenshot_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)

    # Determine file type
    ext = os.path.splitext(file_path)[1].lower()

    content = ""
    if ext == ".csv":
        df = pd.read_csv(file_path)
        content = df.to_string()
    elif ext == ".txt":
        with open(file_path, 'r') as f:
            content = f.read()
    elif ext == ".docx":
        doc = Document(file_path)
        content = "\n".join([para.text for para in doc.paragraphs])
    else:
        raise Exception("Unsupported file type for screenshot rendering")

    # Render text content as image
    img = Image.new("RGB", (1000, 1000), color="white")
    draw = ImageDraw.Draw(img)

    # Load default font
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()

    # Draw text (wrap if needed)
    draw.multiline_text((10,10), content, fill="black", font=font)

    img.save(filepath)
    return filepath
