from crewai import Crew
from agents.timesheet_agent import timesheet_agent
from tasks.timesheet_tasks import (
    capture_timesheet_task,
    extract_timesheet_task,
    verify_timesheet_task,
    update_timesheet_task
)

timesheet_crew = Crew(
    agents=[timesheet_agent],
    tasks=[
        capture_timesheet_task,
        extract_timesheet_task,
        verify_timesheet_task,
        update_timesheet_task
    ]
)
