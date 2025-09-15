# agents/timesheet_agent.py

from tools.gemini_client import gemini_generate, gemini_chat

class TimesheetAgent:
    def __init__(self):
        pass

    def summarize_timesheet(self, extracted_df):
        """
        Uses gemini_generate to summarize the extracted timesheet data.
        """
        prompt = f"Summarize this timesheet data:\n{extracted_df.to_string(index=False)}"
        summary = gemini_generate(prompt)
        return summary

    def explain_verification(self, verified_df):
        """
        Uses gemini_chat for an interactive explanation of verification.
        """
        prompt = f"Explain the verification results in detail:\n{verified_df.to_string(index=False)}"
        explanation = gemini_chat(prompt)
        return explanation
