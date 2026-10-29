"""Loaders for the data/project folder (ready to use, nothing to edit)."""

import csv
import json
from datetime import date

from erp.common.paths import DATA_DIR
from erp.project.models import Task, TimesheetLine

FOLDER = DATA_DIR / "project"


def load_tasks() -> list[Task]:
    raw = json.loads((FOLDER / "tasks.json").read_text(encoding="utf-8"))
    return [
        Task(t["id"], t["name"], t["stage"], t["assignee"], float(t["planned_hours"]),
             date.fromisoformat(t["deadline"]), tuple(t["depends_on"]), tuple(t["tags"]))
        for t in raw
    ]


def load_timesheet_lines() -> list[str]:
    """Raw lines of timesheets.csv, header excluded, e.g. "2026-03-02,alice,T-01,4.0"."""
    lines = (FOLDER / "timesheets.csv").read_text(encoding="utf-8").splitlines()
    return lines[1:]


def load_timesheets() -> list[TimesheetLine]:
    """Timesheet lines sorted by date."""
    with open(FOLDER / "timesheets.csv", newline="", encoding="utf-8") as file:
        return [
            TimesheetLine(date.fromisoformat(r["date"]), r["employee"], r["task_id"], float(r["hours"]))
            for r in csv.DictReader(file)
        ]


def to_minutes(hhmm: str) -> int:
    """'09:30' → 570 (minutes since midnight)."""
    hours, minutes = hhmm.split(":")
    return int(hours) * 60 + int(minutes)


def to_hhmm(minutes: int) -> str:
    """570 → '09:30'."""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def load_meetings(employee: str) -> list[tuple[int, int]]:
    """Meetings of one employee as (start, end) in minutes since midnight, in file order."""
    with open(FOLDER / "meetings.csv", newline="", encoding="utf-8") as file:
        return [(to_minutes(r["start"]), to_minutes(r["end"])) for r in csv.DictReader(file) if r["employee"] == employee]
