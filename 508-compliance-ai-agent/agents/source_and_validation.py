# agents/source_and_validation.py

import validators
import os
from tools.parsers import is_supported_file
from tools.file_ops import save_uploaded_file

class SourceAndValidationAgent:
    def __init__(self):
        pass

    def validate_url(self, url: str) -> bool:
        return validators.url(url)

    def validate_file(self, filename: str) -> bool:
        return is_supported_file(filename)

    def save_and_validate_file(self, file) -> (bool, str):
        # file is expected to be a file-like object from upload
        filename = file.name
        if not self.validate_file(filename):
            return False, "Unsupported file type"
        filepath = save_uploaded_file(file)
        return True, filepath

    def run(self, source):
        # source can be URL string or uploaded file object
        if isinstance(source, str):
            if self.validate_url(source):
                return True, source
            else:
                return False, "Invalid URL"
        else:
            return self.save_and_validate_file(source)

    def explain_508_compliance(self) -> str:
        return (
            "Section 508 requires federal agencies to make their electronic and information technology "
            "accessible to people with disabilities. This includes providing text alternatives, ensuring "
            "keyboard accessibility, sufficient color contrast, and using semantic markup aligned with WCAG."
        )
