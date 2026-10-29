"""Project data models (ready to use, nothing to edit)."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Task:
    id: str                       # "T-01"
    name: str
    stage: str                    # "new", "in_progress", "review", "done" or "cancelled"
    assignee: str | None          # None when nobody is assigned yet
    planned_hours: float
    deadline: date
    depends_on: tuple[str, ...]   # ids of the tasks that must be finished first
    tags: tuple[str, ...]


@dataclass(frozen=True)
class TimesheetLine:
    day: date
    employee: str
    task_id: str
    hours: float


def total_hours(lines: list[TimesheetLine], employee: str) -> float:
    """Total hours logged by one employee (used by task PRJ-08)."""
    return sum(line.hours for line in lines if line.employee == employee)
