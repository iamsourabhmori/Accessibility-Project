# from crewai_tools import tool

# @tool("timesheet_verification_tool")
# def verify_timesheet(data, systems=[]):
#     """
#     Verifies timesheet data against multiple systems.
#     Returns a list of mismatches or confirmation.
#     """
#     # Placeholder: Implement API calls / web automation to check data in systems
#     results = {}
#     for system in systems:
#         results[system] = f"Verified in {system}"  # Simulated response
#     return results


#----------------------------------------------------------------------------------------------------------------------

# tools/timesheet_verifier.py

import pandas as pd

def verify_and_correct_timesheet(df):
    """
    Compares Reported_Hours and System_Hours columns,
    fixes mismatches by replacing with System_Hours,
    and adds a Final_Hours column.
    """
    df['Final_Hours'] = df.apply(
        lambda row: row['System_Hours'] if row['Reported_Hours'] != row['System_Hours'] else row['Reported_Hours'],
        axis=1
    )
    return df
