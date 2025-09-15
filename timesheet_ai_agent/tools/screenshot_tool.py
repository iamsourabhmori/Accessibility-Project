# print("-------------------------inside capture scrrendshot--------------------------------")

# import os
# import pyautogui
# from datetime import datetime

# def capture_screenshot():
#     """
#     Captures a live screenshot at runtime and saves it in the screenshots/ directory
#     with a timestamped filename.
    
#     Returns:
#         str: The filepath of the saved screenshot.
#     """
#     # Ensure screenshots directory exists
#     screenshots_dir = "screenshots"
#     os.makedirs(screenshots_dir, exist_ok=True)

#     # Generate a timestamped filename
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"timesheet_{timestamp}.png"
#     filepath = os.path.join(screenshots_dir, filename)

#     # Capture screenshot
#     screenshot = pyautogui.screenshot()
#     screenshot.save(filepath)

#     return filepath


#--------------------------------------------------------------------------------------------------------------------------------------

# from crewai import tool
# import pyautogui

# @tool("screenshot_capture_tool")
# def capture_screenshot(filename="timesheet.png"):
#     """
#     Captures a screenshot and saves it as 'timesheet.png' by default.
#     """
#     screenshot = pyautogui.screenshot()
#     screenshot.save(filename)
#     return f"Screenshot saved as {filename}"


#-----------------------------------------------------------------------------------------------
# import os
# import pyautogui
# from datetime import datetime

# def capture_screenshot():
#     """
#     Captures a live screenshot at runtime and saves it in the screenshots/ directory
#     with a timestamped filename.

#     Returns:
#         str: The filepath of the saved screenshot.
#     """
#     # Define screenshots directory
#     screenshots_dir = "screenshots"

#     # Create screenshots directory if it does not exist
#     os.makedirs(screenshots_dir, exist_ok=True)

#     # Generate a unique filename with timestamp
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"screenshot_{timestamp}.png"
#     filepath = os.path.join(screenshots_dir, filename)

#     # Capture screenshot and save
#     screenshot = pyautogui.screenshot()
#     screenshot.save(filepath)

#     return filepath


#-----------------------------------------------------------------------------------------------------------------


import os
import pyautogui
import subprocess
import time
from datetime import datetime

def capture_screenshot():
    """
    Captures a live screenshot at runtime and saves it in the screenshots/ directory
    with a timestamped filename.

    Returns:
        str: The filepath of the saved screenshot.
    """
    # Define screenshots directory
    screenshots_dir = "screenshots"

    # Create screenshots directory if it does not exist
    os.makedirs(screenshots_dir, exist_ok=True)

    # Generate a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)

    # Capture screenshot and save
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)

    return filepath


def capture_csv_screenshot(csv_path):
    """
    Opens a CSV file in LibreOffice Calc (or Excel if Windows),
    waits for it to open, takes a screenshot, and saves it.

    Args:
        csv_path (str): Path to the CSV file to open.

    Returns:
        str: The filepath of the saved screenshot.
    """
    # Open CSV file with LibreOffice Calc (adjust for Windows if needed)
    subprocess.Popen(['libreoffice', '--calc', csv_path])  # Linux LibreOffice example

    time.sleep(5)  # Wait for window to open (adjust if needed)

    # Prepare screenshots directory
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"csv_screenshot_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)

    # Take screenshot and save
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)

    return filepath
