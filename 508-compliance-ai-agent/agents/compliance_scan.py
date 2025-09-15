# # agents/compliance_scan.py

# from tools.parsers import parse_document, parse_webpage
# from tools.accessibility import (
#     check_alt_text, check_color_contrast, check_keyboard_accessibility,
#     check_semantic_structure, check_multimedia_accessibility
# )
# import pandas as pd

# class ComplianceScanAgent:
#     def __init__(self):
#         pass

#     def run(self, source, source_type):
#         """
#         source_type: "url", "pdf", "docx", "html"
#         """
#         if source_type == "url" or source_type == "html":
#             content = parse_webpage(source)  # returns parsed HTML content
#         else:
#             content = parse_document(source)  # returns text & metadata from PDF/DOCX

#         # Run accessibility checks
#         issues = []
#         issues += check_alt_text(content)
#         issues += check_color_contrast(content)
#         issues += check_keyboard_accessibility(content)
#         issues += check_semantic_structure(content)
#         issues += check_multimedia_accessibility(content)

#         # Convert issues to DataFrame for reporting
#         df_issues = pd.DataFrame(issues)
#         return df_issues

#     def highlight_issues(self, source, issues_df):
#         """
#         Produce annotated source highlighting issues.
#         Returns annotated file path or HTML snippet depending on source.
#         """
#         # This is a placeholder for highlight implementation
#         # Actual implementation depends on source type and output format
#         annotated = f"Annotated version of {source} with {len(issues_df)} issues highlighted."
#         return annotated

#-----------------------------------------------------------------------------------------------------------------------------

# agents/compliance_scan.py

import pandas as pd
from tools.parsers import parse_document, parse_webpage
from tools.accessibility import (
    check_alt_text, check_color_contrast, check_keyboard_accessibility,
    check_semantic_structure, check_multimedia_accessibility
)

class ComplianceScanAgent:
    def run(self, source, source_type):
        """
        source_type: "url", "pdf", "docx", "html"
        """
        if source_type == "url":
            content = parse_webpage(source)
        else:
            content = parse_document(source)

        # Run accessibility checks
        issues = []
        issues.extend(check_alt_text(content))
        issues.extend(check_color_contrast(content))
        issues.extend(check_keyboard_accessibility(content))
        issues.extend(check_semantic_structure(content))
        issues.extend(check_multimedia_accessibility(content))

        return pd.DataFrame(issues, columns=["element", "message", "wcag_criteria"])

    def highlight_issues(self, content, issues_df):
        """Annotate HTML with highlights."""
        annotated_html = content
        for _, issue in issues_df.iterrows():
            element = issue.get("element", "")
            message = issue.get("message", "")
            if element and element in annotated_html:
                annotated_html = annotated_html.replace(
                    element,
                    f'<span style="background-color: yellow;" title="{message}">{element}</span>'
                )
        return annotated_html
