from crewai import Agent
from tools.screenshot_tool import capture_screenshot
from tools.ocr_tool import extract_timesheet_data
from tools.timesheet_verifier import verify_timesheet
from tools.timesheet_updater import update_timesheet

timesheet_agent = Agent(
    role="Timesheet Data Verifier and Updater",
    goal="Ensure timesheet data consistency across multiple systems for consultants.",
    backstory=(
        "This agent helps consultants avoid data mismatch issues by capturing timesheet entries, "
        "verifying them across required systems, and updating them when needed."
    ),
    tools=[
        capture_screenshot,
        extract_timesheet_data,
        verify_timesheet,
        update_timesheet
    ]
)

#--------------------------------------------------------------------------------------------------------------------
# agents/timesheet_agent.py

# from crewai import Agent
# from tools.screenshot_tool import capture_screenshot
# from tools.ocr_tool import extract_timesheet_data
# from tools.timesheet_verifier import verify_timesheet
# from tools.timesheet_updater import update_timesheet

# # ================================
# # ✅ Local minimal Tool wrapper
# # ================================
# class Tool:
#     def __init__(self, name, func):
#         self.name = name
#         self.func = func

#     def run(self, *args, **kwargs):
#         return self.func(*args, **kwargs)

# # ================================
# # 🚀 Define tools as Tool objects
# # ================================
# screenshot_tool = Tool(name="Screenshot Capture", func=capture_screenshot)
# ocr_tool = Tool(name="OCR Extraction", func=extract_timesheet_data)
# verify_tool = Tool(name="Timesheet Verification", func=verify_timesheet)
# update_tool = Tool(name="Timesheet Update", func=update_timesheet)

# # ================================
# # 🤖 Agent definition
# # ================================
# timesheet_agent = Agent(
#     role="Timesheet Data Verifier and Updater",
#     goal="Ensure timesheet data consistency across multiple systems for consultants.",
#     backstory=(
#         "This agent helps consultants avoid data mismatch issues by capturing timesheet entries, "
#         "verifying them across required systems, and updating them when needed."
#     ),
#     tools=[screenshot_tool, ocr_tool, verify_tool, update_tool]
# )




#-------------------------------------------------------------------------------------------------------------------------------

# agents/timesheet_agent.py

# from crewai import Agent
# from tools.screenshot_tool import ScreenshotTool
# from tools.ocr_tool import OCRTool
# from tools.timesheet_verifier import TimesheetVerifierTool
# from tools.timesheet_updater import TimesheetUpdaterTool

# # Initialize tools as instances of CrewAI-compatible Tool classes
# screenshot_tool = ScreenshotTool()
# ocr_tool = OCRTool()
# verify_tool = TimesheetVerifierTool()
# update_tool = TimesheetUpdaterTool()

# # Agent definition with tools
# timesheet_agent = Agent(
#     role="Timesheet Data Verifier and Updater",
#     goal="Ensure timesheet data consistency across multiple systems for consultants.",
#     backstory=(
#         "This agent helps consultants avoid data mismatch issues by capturing timesheet entries, "
#         "verifying them across required systems, and updating them when needed."
#     ),
#     tools=[screenshot_tool, ocr_tool, verify_tool, update_tool]
# )
