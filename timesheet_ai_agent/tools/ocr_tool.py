# from crewai_tools import tool
# import pytesseract
# from PIL import Image

# @tool("ocr_extraction_tool")
# def extract_timesheet_data(image_path):
#     """
#     Extracts text data from a screenshot image.
#     """
#     img = Image.open(image_path)
#     text = pytesseract.image_to_string(img)
#     return text

#---------------------------------------------------------------------------------------------

# tools/ocr_tool.py

import pytesseract
from PIL import Image

def extract_table_from_screenshot(image_path):
    """
    Uses pytesseract to extract text from screenshot.
    Returns raw extracted text.
    """
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text
