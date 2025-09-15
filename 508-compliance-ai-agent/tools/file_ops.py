# tools/file_ops.py

import os

UPLOAD_DIR = "data/uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(uploaded_file) -> str:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path
