# agents/wcag_rules.py
"""
WCAG rules + simple validators.
- Default: WCAG 2.2 Level AA subset (baseline).
- You can replace/extend RULES at runtime with your own JSON.
No paid APIs used.
"""

from bs4 import BeautifulSoup
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

@dataclass
class Issue:
    element: str
    type: str
    description: str
    severity: str
    wcag_ref: str
    location: Optional[str] = None  # CSS selector, line, url, etc.

def _collect_img_alt_issues(soup: BeautifulSoup) -> List[Issue]:
    issues = []
    for img in soup.find_all("img"):
        alt = (img.get("alt") or "").strip()
        if alt == "":
            issues.append(Issue(
                element="img",
                type="Non-text content without alt",
                description="Image is missing meaningful alt text.",
                severity="Critical",
                wcag_ref="1.1.1 Non-text Content",
                location=str(img)[:120]
            ))
    return issues

def _collect_link_text_issues(soup: BeautifulSoup) -> List[Issue]:
    issues = []
    for a in soup.find_all("a"):
        txt = (a.get_text() or "").strip()
        if txt == "" or txt.lower() in {"click here", "more", "read more"}:
            issues.append(Issue(
                element="a",
                type="Ambiguous link text",
                description="Link text should be descriptive of the destination.",
                severity="Moderate",
                wcag_ref="2.4.4 Link Purpose (In Context)",
                location=str(a)[:120]
            ))
    return issues

def _collect_heading_order_issues(soup: BeautifulSoup) -> List[Issue]:
    issues = []
    headings = [(h.name, h) for h in soup.find_all(re.compile(r"^h[1-6]$"))]
    last_level = 0
    for name, node in headings:
        level = int(name[1])
        if last_level and (level - last_level) > 1:
            issues.append(Issue(
                element=name,
                type="Heading level skipped",
                description=f"Heading jumps from h{last_level} to h{level}.",
                severity="Minor",
                wcag_ref="1.3.1 Info and Relationships",
                location=str(node)[:120]
            ))
        last_level = level
    return issues

def _collect_form_label_issues(soup: BeautifulSoup) -> List[Issue]:
    issues = []
    inputs = soup.find_all(["input", "select", "textarea"])
    for inp in inputs:
        # has label via <label for=""> OR aria-label/aria-labelledby
        id_ = inp.get("id")
        has_label = False
        if id_ and soup.find("label", attrs={"for": id_}):
            has_label = True
        if inp.get("aria-label") or inp.get("aria-labelledby"):
            has_label = True
        if not has_label and inp.get("type") not in {"hidden", "submit", "button"}:
            issues.append(Issue(
                element=inp.name,
                type="Form control without label",
                description="Form fields require a programmatic label.",
                severity="Critical",
                wcag_ref="3.3.2 Labels or Instructions",
                location=str(inp)[:120]
            ))
    return issues

def _collect_title_lang_issues(soup: BeautifulSoup) -> List[Issue]:
    issues = []
    # <title>
    title = soup.find("title")
    if not title or not (title.get_text() or "").strip():
        issues.append(Issue(
            element="title",
            type="Missing page title",
            description="Provide a meaningful page title.",
            severity="Moderate",
            wcag_ref="2.4.2 Page Titled",
            location="<title>"
        ))
    # lang attribute
    html = soup.find("html")
    if not html or not html.get("lang"):
        issues.append(Issue(
            element="html",
            type="Missing language attribute",
            description="Set the primary language on <html lang='...'>.",
            severity="Minor",
            wcag_ref="3.1.1 Language of Page",
            location="<html>"
        ))
    return issues

# Placeholder (offline) contrast check – heuristic only (no color parsing)
def _collect_contrast_placeholders(soup: BeautifulSoup) -> List[Issue]:
    # Real contrast needs computed CSS colors; here we flag inline styles missing color/background where text is very light words.
    issues = []
    for node in soup.find_all(text=True):
        text = (node or "").strip()
        if not text or len(text) < 3:
            continue
        parent = node.parent
        style = (parent.get("style") or "").lower()
        # crude heuristic: if style sets color to a light gray and no background is set
        if "color:#ccc" in style or "color: #ccc" in style:
            if "background" not in style:
                issues.append(Issue(
                    element=parent.name or "text",
                    type="Possible low contrast text",
                    description="Text may have insufficient contrast (heuristic).",
                    severity="Moderate",
                    wcag_ref="1.4.3 Contrast (Minimum)",
                    location=str(parent)[:120]
                ))
    return issues

DEFAULT_HTML_CHECKS = [
    _collect_img_alt_issues,
    _collect_link_text_issues,
    _collect_heading_order_issues,
    _collect_form_label_issues,
    _collect_title_lang_issues,
    _collect_contrast_placeholders,
]

def run_wcag_checks_on_html(html: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    issues: List[Issue] = []
    for fn in DEFAULT_HTML_CHECKS:
        try:
            issues.extend(fn(soup))
        except Exception:
            # Never crash the scan on a single rule failure
            continue
    return [asdict(i) for i in issues]

# Stubs for other formats (implement as needed)
def run_wcag_checks_on_text(text: str) -> List[Dict[str, Any]]:
    # Example: flag ASCII art tables without headers, etc. Keep simple.
    issues: List[Issue] = []
    if "click here" in text.lower():
        issues.append(Issue(
            element="text",
            type="Ambiguous link text",
            description="Avoid phrases like 'click here'; use descriptive text.",
            severity="Minor",
            wcag_ref="2.4.4 Link Purpose (In Context)"
        ))
    return [asdict(i) for i in issues]
