# agents/update_agent.py

import pandas as pd
from tools.timesheet_verifier import verify_and_correct_timesheet

def run_update_agent(input_csv, output_csv):
    """
    Loads CSV, verifies & corrects it, and saves updated CSV.
    """
    df = pd.read_csv(input_csv)
    corrected_df = verify_and_correct_timesheet(df)
    corrected_df.to_csv(output_csv, index=False)
    print(f"✅ Timesheet updated and saved to {output_csv}")

# Example usage:
if __name__ == "__main__":
    run_update_agent('timesheet_mismatched.csv', 'timesheet_updated.csv')
