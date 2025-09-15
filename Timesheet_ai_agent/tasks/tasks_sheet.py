from agents.screenshot_agent import ScreenshotCaptureAgent
from agents.ocr_extraction_agent import OCRExtractionAgent
from agents.verification_agent import TimesheetVerificationAgent
from agents.correction_agent import CorrectionAgent
from agents.system_update_agent import SystemUpdateAgent

def define_tasks():
    return [
        {
            "name": "Capture Screenshot",
            "agent": ScreenshotCaptureAgent(),
            "input_key": "file_path",
            "output_key": "screenshot_path"
        },
        {
            "name": "Extract Data",
            "agent": OCRExtractionAgent(),
            "input_key": "screenshot_path",
            "output_key": "extracted_df"
        },
        {
            "name": "Verify Data",
            "agent": TimesheetVerificationAgent(),
            "input_key": "extracted_df",
            "output_key": "verified_df"
        },
        {
            "name": "Correct Data",
            "agent": CorrectionAgent(),
            "input_key": "verified_df",
            "output_key": "corrected_df"
        },
        {
            "name": "Update Systems",
            "agent": SystemUpdateAgent(),
            "input_key": "corrected_df",
            "output_key": "update_status"
        }
    ]
