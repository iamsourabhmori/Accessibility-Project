from tools.gemini_client import gemini_generate

class TimesheetVerificationAgent:
    def __init__(self):
        pass

    def run(self, extracted_df):
        print("[TimesheetVerificationAgent] Verifying extracted data with Gemini.")
        
        # 🔧 Convert dataframe to string for prompt context
        table_text = extracted_df.to_string()
        
        prompt = f"""
        You are a timesheet verification AI agent.
        Below is the timesheet data:

        {table_text}

        Identify rows where Reported_Hours and System_Hours do not match.
        Return instructions to correct them clearly in tabular format.
        """

        correction_instructions = gemini_generate(prompt)

        # For now, print instructions. Later parse and apply corrections.
        print("Gemini correction instructions:\n", correction_instructions)

        # Dummy logic – flag hours < 7 as mismatched and correct to 8
        extracted_df['Verified'] = extracted_df['Hours'] >= 7
        return extracted_df
