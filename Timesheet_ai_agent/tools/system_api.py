
#------------------------------------------------------------------------------------------------------------------

# def apply_corrections(df, discrepancies):
#     for d in discrepancies:
#         df.loc[df["Employee_ID"] == d["Employee_ID"], "Hours"] = d["Expected"]
#     return df
#-------------------------------------------------------------------------------------------------------------------
def apply_corrections(df, discrepancies):
    df_corrected = df.copy()

    def find_col(cols, keyword):
        for c in cols:
            if keyword.lower() in c.lower():
                return c
        return None

    emp_col = find_col(df_corrected.columns, "employee")
    date_col = find_col(df_corrected.columns, "date")
    hours_col = find_col(df_corrected.columns, "hour")

    if "Correction" not in df_corrected.columns:
        df_corrected["Correction"] = ""

    for d in discrepancies:
        emp = d["Employee"]
        date = d["Date"]
        expected_hours = d["Expected"]

        mask = (df_corrected[emp_col] == emp) & (df_corrected[date_col] == date)
        if any(mask):
            idx = df_corrected.index[mask][0]
            old_hours = df_corrected.at[idx, hours_col]
            if old_hours != expected_hours:
                df_corrected.at[idx, hours_col] = expected_hours
                df_corrected.at[idx, "Correction"] = "corrected 🔴"
        else:
            # Add new row if missing (optional)
            new_row = {emp_col: emp, date_col: date, hours_col: expected_hours, "Correction": "added 🟡"}
            df_corrected = df_corrected.append(new_row, ignore_index=True)

    return df_corrected




# def update_timesheet_via_ui_automation(corrected_df):
#     """
#     Use UI automation to simulate user entry in the external system.
#     """
#     import pyautogui
#     import time

#     for _, row in corrected_df.iterrows():
#         time.sleep(2)  # Wait for focus
#         pyautogui.write(str(row['EmployeeID']))
#         pyautogui.press('tab')
#         pyautogui.write(row['Date'])
#         pyautogui.press('tab')
#         pyautogui.write(str(row['Hours']))
#         pyautogui.press('tab')
#         pyautogui.write(row['Project'])
#         pyautogui.press('enter')
#         time.sleep(1)
