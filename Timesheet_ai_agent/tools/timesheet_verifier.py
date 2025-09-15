
#---------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------------------

def verify_timesheet(screenshot_df, master_df):
    discrepancies = []

    # ✅ Flexible column mapping
    def map_columns(df):
        column_map = {}
        for col in df.columns:
            col_lower = col.lower()
            if "employee" in col_lower:
                column_map["Employee"] = col
            elif "date" in col_lower:
                column_map["Date"] = col
            elif "hour" in col_lower:
                column_map["Hours"] = col
        return column_map

    # 🧠 Map both DataFrames
    screenshot_cols = map_columns(screenshot_df)
    master_cols = map_columns(master_df)

    # 🚨 Ensure required columns exist
    required = ["Employee", "Date", "Hours"]
    for r in required:
        if r not in screenshot_cols or r not in master_cols:
            raise ValueError(f"Missing required column '{r}' in one of the DataFrames.")

    # ✅ Comparison logic
    for i, row in screenshot_df.iterrows():
        emp_name = row[screenshot_cols["Employee"]]
        date = row[screenshot_cols["Date"]]
        hours = row[screenshot_cols["Hours"]]

        # Match on Employee and Date
        master_row = master_df[
            (master_df[master_cols["Employee"]] == emp_name) &
            (master_df[master_cols["Date"]] == date)
        ]

        if not master_row.empty:
            expected_hours = master_row.iloc[0][master_cols["Hours"]]
            if str(expected_hours) != str(hours):
                discrepancies.append({
                    "Employee": emp_name,
                    "Date": date,
                    "Expected": expected_hours,
                    "Found": hours
                })

    return discrepancies


#-------------------------------------------------------------------------------------------------------------------------------
# import pandas as pd

# def verify_timesheet(screenshot_df, master_df):
#     discrepancies = []

#     def map_columns(df):
#         column_map = {}
#         for col in df.columns:
#             col_lower = col.lower()
#             if "employee" in col_lower:
#                 column_map["Employee"] = col
#             elif "date" in col_lower:
#                 column_map["Date"] = col
#             elif "hour" in col_lower:
#                 column_map["Hours"] = col
#         return column_map

#     screenshot_cols = map_columns(screenshot_df)
#     master_cols = map_columns(master_df)

#     required = ["Employee", "Date", "Hours"]
#     for r in required:
#         if r not in screenshot_cols or r not in master_cols:
#             raise ValueError(f"Missing required column '{r}' in one of the DataFrames.")

#     for i, row in screenshot_df.iterrows():
#         emp_name = row[screenshot_cols["Employee"]]
#         date = row[screenshot_cols["Date"]]
#         try:
#             hours = float(row[screenshot_cols["Hours"]])
#         except:
#             hours = None

#         master_row = master_df[
#             (master_df[master_cols["Employee"]] == emp_name) &
#             (master_df[master_cols["Date"]] == date)
#         ]

#         if not master_row.empty:
#             try:
#                 expected_hours = float(master_row.iloc[0][master_cols["Hours"]])
#             except:
#                 expected_hours = None
#             if expected_hours != hours:
#                 discrepancies.append({
#                     "Employee": emp_name,
#                     "Date": date,
#                     "Expected": expected_hours,
#                     "Found": hours
#                 })

#     return discrepancies



# def verify_timesheet_multi_systems(master_df, system_dfs):
#     """
#     Compare multiple system timesheets against the master and each other.
    
#     Args:
#         master_df (pd.DataFrame): Master timesheet dataframe.
#         system_dfs (dict): Dict of {system_name: pd.DataFrame} timesheet data.
    
#     Returns:
#         List of discrepancy dicts with details.
#     """
#     discrepancies = []

#     # Normalize column names
#     master_df.columns = [col.strip().lower() for col in master_df.columns]
#     master_df.rename(columns={"employee": "name"}, inplace=True)

#     for name, df in system_dfs.items():
#         df.columns = [col.strip().lower() for col in df.columns]
#         df.rename(columns={"employee": "name"}, inplace=True)
#         system_dfs[name] = df

#     # Compare each system with master
#     for system_name, system_df in system_dfs.items():
#         merged_df = pd.merge(master_df, system_df, on=["name", "date"], suffixes=("_master", f"_{system_name}"))

#         for _, row in merged_df.iterrows():
#             master_hours = row["hours_master"]
#             system_hours = row[f"hours_{system_name}"]

#             if master_hours != system_hours:
#                 discrepancies.append({
#                     "Type": "Mismatch with Master",
#                     "System": system_name,
#                     "Name": row["name"],
#                     "Date": row["date"],
#                     "Master Hours": master_hours,
#                     "System Hours": system_hours
#                 })

#     # Cross-compare between systems
#     system_names = list(system_dfs.keys())
#     for i in range(len(system_names)):
#         for j in range(i + 1, len(system_names)):
#             sys1, sys2 = system_names[i], system_names[j]
#             df1 = system_dfs[sys1]
#             df2 = system_dfs[sys2]

#             merged = pd.merge(df1, df2, on=["name", "date"], suffixes=(f"_{sys1}", f"_{sys2}"))

#             for _, row in merged.iterrows():
#                 hours1 = row[f"hours_{sys1}"]
#                 hours2 = row[f"hours_{sys2}"]

#                 if hours1 != hours2:
#                     discrepancies.append({
#                         "Type": "Mismatch Between Systems",
#                         "System 1": sys1,
#                         "System 2": sys2,
#                         "Name": row["name"],
#                         "Date": row["date"],
#                         f"{sys1} Hours": hours1,
#                         f"{sys2} Hours": hours2
#                     })

#     return discrepancies
