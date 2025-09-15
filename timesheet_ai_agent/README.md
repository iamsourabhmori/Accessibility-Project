# Timesheet AI Agent

## Purpose
Ensures consultants' timesheet data is consistent across multiple systems by capturing, verifying, and updating entries using Crew AI workflows.

## Folder Structure
- agents/ : Timesheet agent definition
- tasks/ : Tasks for screenshot capture, OCR, verification, update
- tools/ : Tools for screenshot, OCR, verification, update
- crew.py : Assembles agent and tasks
- main.py : Runs the agent

## Run
```bash
pip install -r requirements.txt
python main.py
