
#-------------------------------------------------------------------------------------------------------------------------------------------

import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

def capture_csv_as_image(csv_path, output_dir="uploads"):
    # ✅ Step 1: Load and clean CSV
    try:
        df = pd.read_csv(csv_path, encoding="utf-8", on_bad_lines='skip')
    except Exception as e:
        raise ValueError(f"Error reading CSV: {e}")

    df.dropna(how='all', inplace=True)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.dropna(how='any')
    df = df[~(df == '').any(axis=1)]

    if df.empty:
        raise ValueError("CSV has no valid data rows after cleaning.")

    # ✅ Step 2: Set font
    try:
        font = ImageFont.load_default()
    except Exception as e:
        raise RuntimeError("Font loading failed.") from e

    padding = 10
    row_height = 25
    col_widths = []

    # ✅ Step 3: Calculate column widths
    for col in df.columns:
        max_len = max(df[col].astype(str).apply(len).max(), len(col))
        col_widths.append((max_len + 2) * 8)  # Adjust width per character

    table_width = sum(col_widths) + padding * 2
    table_height = (len(df) + 1) * row_height + padding * 2

    image = Image.new("RGB", (table_width, table_height), "white")
    draw = ImageDraw.Draw(image)

    # ✅ Step 4: Draw headers
    x = padding
    y = padding
    for i, col in enumerate(df.columns):
        draw.rectangle([x, y, x + col_widths[i], y + row_height], outline="black")
        draw.text((x + 5, y + 5), col, fill="black", font=font)
        x += col_widths[i]

    # ✅ Step 5: Draw rows
    for row_idx, row in df.iterrows():
        x = padding
        y += row_height
        for i, col in enumerate(df.columns):
            cell_value = str(row[col])
            draw.rectangle([x, y, x + col_widths[i], y + row_height], outline="gray")
            draw.text((x + 5, y + 5), cell_value, fill="black", font=font)
            x += col_widths[i]

    # ✅ Step 6: Save image
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = os.path.join(output_dir, f"csv_screenshot_{timestamp}.png")
    image.save(image_path)

    return image_path

# Optional: Return cleaned DataFrame for further use
def load_clean_csv(csv_path):
    df = pd.read_csv(csv_path, encoding="utf-8", on_bad_lines='skip')
    df.dropna(how='all', inplace=True)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.dropna(how='any')
    df = df[~(df == '').any(axis=1)]
    return df


#------------------------------------------------------------------------------------------------------------------------------------------------
