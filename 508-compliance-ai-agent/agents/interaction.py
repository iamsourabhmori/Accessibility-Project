# agents/interaction.py

class InteractionAgent:
    def __init__(self):
        pass

    def prompt_next_steps(self):
        prompt_text = (
            "Would you like to:\n"
            "1. Run another 508 compliance check on a new source?\n"
            "2. Recheck specific areas like multimedia content?\n"
            "3. Export fixed files, reports, or summaries?\n"
            "Please respond by voice or keyboard."
        )
        return prompt_text

    def process_user_response(self, response: str):
        response = response.lower()
        if "another" in response or "new" in response:
            return "run_new_check"
        elif "recheck" in response or "multimedia" in response:
            return "recheck_area"
        elif "export" in response:
            return "export_files"
        else:
            return "exit"
