
#-----------------------------------------------------------------------------------------------------------------------------------------

# import pytesseract
# import cv2 
# import pandas as pd

# def extract_table_from_image(image_path):
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # OCR extraction
#     text = pytesseract.image_to_string(gray)

#     # Split into lines and then into cells (by whitespace or tabs)
#     lines = text.strip().split("\n")
#     rows = [line.strip().split() for line in lines if line.strip()]

#     if not rows:
#         return pd.DataFrame()  # Return empty if no rows found

#     header = rows[0]
#     valid_data_rows = [row for row in rows[1:] if len(row) == len(header)]

#     if not valid_data_rows:
#         raise ValueError("No valid rows match header length. Check OCR output formatting.")

#     df = pd.DataFrame(valid_data_rows, columns=header)
#     return df

#-----------------------------------------------------------------------------------------------------------------------------------

import pytesseract
import cv2
import pandas as pd
import re

def extract_table_from_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform OCR
    text = pytesseract.image_to_string(gray)

    # Clean and process lines
    lines = [re.sub(r'\s+', ' ', line.strip()) for line in text.strip().split('\n') if line.strip()]

    if not lines:
        return pd.DataFrame()

    # Extract header
    header_line = lines[0]
    headers = header_line.split()

    # Handle common OCR header merge issues (like "Employee_ID" -> "Employee", "ID")
    def clean_headers(headers):
        fixed_headers = []
        skip_next = False
        for i in range(len(headers)):
            if skip_next:
                skip_next = False
                continue
            if i + 1 < len(headers) and headers[i].lower() + "_" + headers[i + 1].lower() in ['employee_id', 'system_hours', 'date_of_work']:
                fixed_headers.append(headers[i] + "_" + headers[i + 1])
                skip_next = True
            else:
                fixed_headers.append(headers[i])
        return fixed_headers

    headers = clean_headers(headers)

    # Extract rows
    rows = []
    for line in lines[1:]:
        row = line.split()
        if len(row) == len(headers):
            rows.append(row)

    # Build DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # Normalize headers to reduce mismatch risk (optional)
    df.columns = [re.sub(r'[^a-zA-Z0-9_]', '', col) for col in df.columns]

    return df
