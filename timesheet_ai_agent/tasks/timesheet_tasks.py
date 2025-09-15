from crewai import Task
from tools.screenshot_tool import capture_screenshot
from tools.ocr_tool import extract_timesheet_data
from tools.timesheet_verifier import verify_timesheet
from tools.timesheet_updater import update_timesheet

# Task 1: Capture Screenshot
capture_timesheet_task = Task(
    description="Capture the timesheet screenshot from the user device.",
    tool=capture_screenshot
)

# Task 2: Extract Data
extract_timesheet_task = Task(
    description="Extract timesheet data using OCR from the screenshot.",
    tool=extract_timesheet_data
)

# Task 3: Verify Data
verify_timesheet_task = Task(
    description="Verify extracted timesheet data across systems.",
    tool=verify_timesheet
)

# Task 4: Update Data
update_timesheet_task = Task(
    description="Update timesheet data in systems if mismatched.",
    tool=update_timesheet
)
