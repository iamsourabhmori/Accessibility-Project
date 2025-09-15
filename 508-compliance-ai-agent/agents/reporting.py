# agents/reporting.py

import pandas as pd

class ReportingAgent:
    def __init__(self):
        pass

    def generate_findings_report(self, issues_df: pd.DataFrame) -> pd.DataFrame:
        # Summarize compliance
        total = len(issues_df)
        critical = len(issues_df[issues_df['severity'] == 'critical'])
        moderate = len(issues_df[issues_df['severity'] == 'moderate'])
        minor = len(issues_df[issues_df['severity'] == 'minor'])

        summary = {
            "Total Issues": total,
            "Critical": critical,
            "Moderate": moderate,
            "Minor": minor,
            "Percent Compliant": max(0, 100 - (total * 2))  # dummy logic
        }

        summary_df = pd.DataFrame([summary])

        # Save or return detailed report & summary separately if needed
        return summary_df

    def generate_comparison_report(self, original_df: pd.DataFrame, fixed_df: pd.DataFrame) -> pd.DataFrame:
        # Compare before/after for key fields and flag changes
        comparison = original_df.copy()
        comparison['Fixed'] = False
        for idx in fixed_df.index:
            if idx in comparison.index and not fixed_df.loc[idx].equals(comparison.loc[idx]):
                comparison.loc[idx, 'Fixed'] = True
        return comparison
