# crew/workflow_controller_task.py
"""
Workflow controller for the 8-step 508 Compliance pipeline.
This module orchestrates the agents in sequence and produces artifacts
(report CSVs, annotated files, audio summaries) that the Streamlit UI consumes.

Usage:
    from crew.workflow_controller_task import run_full_workflow
    result = run_full_workflow(source, source_type="url" or "file")
"""

import os
import uuid
import json
import pandas as pd
from datetime import datetime

# Agents (these should exist in agents/)
from agents.source_and_validation import SourceAndValidationAgent
from agents.compliance_scan import ComplianceScanAgent
from agents.reporting import ReportingAgent
from agents.suggestion_and_fix import SuggestionAndFixAgent
from agents.interaction import InteractionAgent

# Tools
from tools.file_ops import save_uploaded_file
from tools.parsers import parse_document, parse_webpage
from tools import speech as speech_tools  # expects text_to_speech(...) and speech_to_text(...)
# If your tools.speech uses classes, adapt below (we try to be flexible)

# Output folders
OUTPUT_ROOT = os.getenv("OUTPUT_DIR", "outputs")
print("OUTPUT_ROOT :",OUTPUT_ROOT)
REPORTS_DIR = os.path.join(OUTPUT_ROOT, "reports")
print("REPORTS_DIR :",REPORTS_DIR)

AUDIO_DIR = os.path.join(OUTPUT_ROOT, "audio")
print("AUDIO_DIR :",AUDIO_DIR)

TRANSCRIPTS_DIR = os.path.join(OUTPUT_ROOT, "transcripts")
print("TRANSCRIPTS_DIR :",TRANSCRIPTS_DIR)


os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)


def _save_df(df: pd.DataFrame, filename: str) -> str:
    path = os.path.join(REPORTS_DIR, filename)
    print("_save_df:",path)
    df.to_csv(path, index=False)
    return path


def _save_json(obj, filename: str) -> str:
    path = os.path.join(REPORTS_DIR, filename)
    print("_save_json:",path)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return path


def _make_summary_text(summary_df: pd.DataFrame, top_n=5) -> str:
    # Create a short natural-language summary of the findings
    try:
        row = summary_df.iloc[0].to_dict()
        text = (
            f"Accessibility scan completed. Total issues: {row.get('Total Issues', 'unknown')}. "
            f"Critical: {row.get('Critical',0)}, Moderate: {row.get('Moderate',0)}, Minor: {row.get('Minor',0)}. "
        )
        return text
    except Exception:
        return "Accessibility scan completed. Please check the findings report."


def _generate_audio_summary(text: str, out_name: str) -> str:
    """
    Use tools.speech.text_to_speech (or fallback) to create an mp3 summary.
    Returns path to mp3.
    """
    # Try both naming conventions: function or class
    try:
        # if tools.speech exposes text_to_speech(text)
        mp3_path = speech_tools.text_to_speech(text)
        return mp3_path
    except Exception:
        try:
            # if tools.speech exposes TextToSpeech().speak(...) that returns path
            tts = getattr(speech_tools, "TextToSpeech", None)
            if tts:
                tts_inst = tts()
                # Some implementations stream to player - here we try to save and return.
                mp3_path = tts_inst.speak(text)  # may return path or None
                return mp3_path
        except Exception:
            pass
    # fallback: write plain text file (no audio)
    fallback_path = os.path.join(AUDIO_DIR, out_name + ".txt")
    with open(fallback_path, "w", encoding="utf-8") as f:
        f.write(text)
    return fallback_path


def run_full_workflow(source, source_type="url", user_id: str = "anon"):
    """
    Run the full Step1..Step8 workflow synchronously.
    :param source: URL string or local file path (already saved). If an uploaded file object was passed,
                   call save_uploaded_file() before invoking this function or pass the path returned.
    :param source_type: 'url' or 'file' ; if 'file' the `source` should be a file path.
    :param user_id: optional user id used for traceability
    :returns: dict with artifact paths and summary metadata
    """
    run_id = str(uuid.uuid4())[:8]
    started_at = datetime.utcnow().isoformat() + "Z"
    metadata = {
        "run_id": run_id,
        "user_id": user_id,
        "started_at": started_at,
        "source": source,
        "source_type": source_type,
    }

    # Initialize agents
    src_agent = SourceAndValidationAgent()
    scan_agent = ComplianceScanAgent()
    report_agent = ReportingAgent()
    suggest_agent = SuggestionAndFixAgent()
    interact_agent = InteractionAgent()

    artifacts = {}

    try:
        # --- Step 1: Source validation & ingestion ---
        metadata["step1_started"] = datetime.utcnow().isoformat() + "Z"
        if source_type == "url":
            valid = src_agent.validate_url(source)
            if not valid:
                raise ValueError("Invalid URL provided")
            ingested_ref = source  # for webpages we use URL as content ref
        else:
            # assume source is a file-like object (path or uploaded object)
            if hasattr(source, "read"):
                # maybe a file-like upload; save it
                file_path = save_uploaded_file(source)
                ingested_ref = file_path
            else:
                ingested_ref = source  # path already
            # additional validation
            if not src_agent.validate_file(ingested_ref if isinstance(ingested_ref, str) else getattr(ingested_ref, "name", "")):
                raise ValueError("Unsupported file type for scanning")
        metadata["step1_completed"] = datetime.utcnow().isoformat() + "Z"
        artifacts["ingested_ref"] = ingested_ref

        # --- Step 2: Compliance scan ---
        metadata["step2_started"] = datetime.utcnow().isoformat() + "Z"
        if source_type == "url":
            parsed = parse_webpage(ingested_ref)
            issues_df = scan_agent.run(ingested_ref, "url")
        else:
            parsed = parse_document(ingested_ref)
            issues_df = scan_agent.run(ingested_ref, "file")
        # ensure DataFrame shape
        if issues_df is None:
            issues_df = pd.DataFrame(columns=["element", "type", "description", "severity"])
        artifacts["issues_df_path"] = _save_df(issues_df, f"{run_id}_issues.csv")
        metadata["step2_completed"] = datetime.utcnow().isoformat() + "Z"

        # --- Step 3: Generate findings report ---
        metadata["step3_started"] = datetime.utcnow().isoformat() + "Z"
        summary_df = report_agent.generate_findings_report(issues_df)
        artifacts["findings_report_path"] = _save_df(summary_df, f"{run_id}_findings_summary.csv")
        metadata["step3_completed"] = datetime.utcnow().isoformat() + "Z"

        # --- Step 4: Highlight problem areas (annotated source) ---
        metadata["step4_started"] = datetime.utcnow().isoformat() + "Z"
        annotated = scan_agent.highlight_issues(ingested_ref, issues_df)
        # save annotated representation (if HTML or text, save to reports)
        annotated_name = f"{run_id}_annotated.txt"
        annotated_path = os.path.join(REPORTS_DIR, annotated_name)
        try:
            if isinstance(annotated, str):
                with open(annotated_path, "w", encoding="utf-8") as f:
                    f.write(annotated)
            else:
                # if agent returns a path
                annotated_path = str(annotated)
        except Exception:
            annotated_path = None
        artifacts["annotated_path"] = annotated_path
        metadata["step4_completed"] = datetime.utcnow().isoformat() + "Z"

        # --- Step 5: Generate suggestions for issues ---
        metadata["step5_started"] = datetime.utcnow().isoformat() + "Z"
        suggestions_df = suggest_agent.generate_suggestions(issues_df)
        artifacts["suggestions_path"] = _save_df(suggestions_df, f"{run_id}_suggestions.csv")
        metadata["step5_completed"] = datetime.utcnow().isoformat() + "Z"

        # --- Step 6: Optionally apply fixes ---
        metadata["step6_started"] = datetime.utcnow().isoformat() + "Z"
        # For automatic mode we attempt to apply fixes programmatically.
        fixed_source = suggest_agent.apply_fixes(ingested_ref, suggestions_df)
        # Save fixed representation (path or string)
        fixed_name = f"{run_id}_fixed.txt"
        fixed_path = os.path.join(REPORTS_DIR, fixed_name)
        try:
            if isinstance(fixed_source, str):
                # If apply_fixes returned a string representation, save it
                with open(fixed_path, "w", encoding="utf-8") as f:
                    f.write(fixed_source)
            else:
                fixed_path = str(fixed_source)
        except Exception:
            fixed_path = None
        artifacts["fixed_path"] = fixed_path
        metadata["step6_completed"] = datetime.utcnow().isoformat() + "Z"

        # --- Step 7: Re-run metrics / comparison ---
        metadata["step7_started"] = datetime.utcnow().isoformat() + "Z"
        # For tabular data: generate comparison report (here using issues_df as placeholder)
        comparison_df = report_agent.generate_comparison_report(issues_df, issues_df)  # replace with real original/fixed frames
        artifacts["comparison_path"] = _save_df(comparison_df, f"{run_id}_comparison.csv")
        metadata["step7_completed"] = datetime.utcnow().isoformat() + "Z"

        # --- Step 8: Prepare next steps prompt and audio summary ---
        metadata["step8_started"] = datetime.utcnow().isoformat() + "Z"
        summary_text = _make_summary_text(summary_df)
        # Add an actionable line
        summary_text += " You can say, 'run another check', 'export reports', or 'exit'."
        # create audio summary
        audio_basename = f"{run_id}_summary"
        audio_path = _generate_audio_summary(summary_text, audio_basename)
        artifacts["audio_summary_path"] = audio_path

        # save manifest
        manifest = {
            "metadata": metadata,
            "artifacts": artifacts
        }
        manifest_path = _save_json(manifest, f"{run_id}_manifest.json")
        artifacts["manifest_path"] = manifest_path

        metadata["completed_at"] = datetime.utcnow().isoformat() + "Z"
        return {"status": "success", "metadata": metadata, "artifacts": artifacts}

    except Exception as e:
        metadata["error"] = str(e)
        metadata["failed_at"] = datetime.utcnow().isoformat() + "Z"
        return {"status": "failed", "metadata": metadata, "error": str(e)}
