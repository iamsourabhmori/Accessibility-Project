import pandas as pd

class OCRExtractionAgent:
    def __init__(self):
        pass

    def run(self, screenshot_path):
        print(f"[OCRExtractionAgent] Extracting data from {screenshot_path}")
        # 🔧 Dummy DataFrame for scaffold
        data = {
            'Employee': ['John', 'Sarah'],
            'Hours': [8, 6]
        }
        return pd.DataFrame(data)
