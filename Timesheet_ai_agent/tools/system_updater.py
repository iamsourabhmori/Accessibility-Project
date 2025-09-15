


# def update_timesheet_via_api(corrected_df, api_credentials):
#     print("Corrected DF columns:", corrected_df.columns.tolist())

#     """
#     Pushes the corrected timesheet entries to an external platform via API.
#     """
#     # Example logic (you'll replace with actual API endpoints and fields)
#     import requests
#     for _, row in corrected_df.iterrows():
#         payload = {
#             "employee_id": row["EmployeeID"],
#             "date": row["Date"],
#             "hours": row["Hours"],
#             "project": row["Project"]
#         }
#         response = requests.post("https://external-system.example.com/api/timesheets",
#                                  headers={"Authorization": f"Bearer {api_credentials['token']}"},
#                                  json=payload)
#         print(f"Pushed for {row['EmployeeID']}: {response.status_code}")





# def update_timesheet_via_ui_automation(corrected_df):
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
