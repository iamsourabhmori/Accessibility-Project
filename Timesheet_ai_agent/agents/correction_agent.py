# class CorrectionAgent:
#     def __init__(self):
#         pass

#     def run(self, verified_df):
#         print("[CorrectionAgent] Correcting mismatched data.")
#         corrected_df = verified_df.copy()
#         corrected_df.loc[corrected_df['Hours'] < 7, 'Hours'] = 8
#         corrected_df['Corrected'] = True
#         return corrected_df

#---------------------------------------------------------------------------------------------------------------------------------------

class CorrectionAgent:
    def __init__(self):
        pass

    def run(self, verified_df, master_df):
        """
        Runs correction by verifying mismatches and applying corrections.
        """
        from tools.timesheet_verifier import verify_timesheet
        from tools.system_api import apply_corrections

        discrepancies = verify_timesheet(verified_df, master_df)
        corrected_df = apply_corrections(verified_df, discrepancies)
        return corrected_df
