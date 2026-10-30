"""PROJECT — concept tasks (Member B).

How it works
------------
* Each task is a function (or class) containing a `todo("PRJ-xx")` line.
  Replace that line with your implementation.
* Read the "Discover" links: today's goal is to learn these tools on your own.
* Check your progress with `python -m erp project`, and run your code on the
  real data with `python -m erp demo project`.
* Commit after each task: git commit -m "PRJ-03: late tasks and overruns".

You may add helper functions and imports. Do not rename the existing functions:
the tests use these names.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

from erp.common.todo import todo
from erp.project.models import Task, TimesheetLine, total_hours

from enum import StrEnum

# Add the imports you need here (collections, itertools, functools, heapq, bisect...).

CLOSED_STAGES = {"done", "cancelled"}


# ════════════════════════════════════════════════════════════════════════════
# PRJ-01 · Task stages                               Concept: Enum (+ match/case)
# ════════════════════════════════════════════════════════════════════════════
# A task moves through stages, like the kanban columns of Odoo Project.
#
# 1. Declare the members of Stage, with exactly the values used in tasks.json:
#    NEW = "new", IN_PROGRESS = "in_progress", REVIEW = "review", DONE = "done",
#    CANCELLED = "cancelled". Keep this order: it is the order of the columns.
# 2. is_closed: True for DONE and CANCELLED, False otherwise.
# 3. next_stage(): the following column, written with a `match` statement:
#    NEW → IN_PROGRESS → REVIEW → DONE. A closed task has no next stage: raise a
#    ValueError with a clear message (for example "done is a final stage").
#
#    Stage("review").next_stage()       → Stage.DONE
#    Stage.CANCELLED.is_closed          → True
#    [s.value for s in Stage][:2]       → ["new", "in_progress"]
#
# 📚 Discover: https://docs.python.org/3/library/enum.html  (StrEnum, iteration over members)
#             https://docs.python.org/3/tutorial/controlflow.html#match-statements
# ⏱ ~25 min
class Stage(StrEnum):
    """Kanban stage of a task."""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    CANCELLED = "cancelled"

    @property
    def is_closed(self) -> bool:
        return self == Stage.DONE or self == Stage.CANCELLED

    def next_stage(self) -> Stage:
        match self:
            case(Stage.NEW): 
                return self.IN_PROGRESS
            case(Stage.IN_PROGRESS): 
                return self.REVIEW
            case(Stage.REVIEW): 
                return self.DONE
            case _: 
                raise ValueError("Stage is already closed")


# ════════════════════════════════════════════════════════════════════════════
# PRJ-02 · Timesheet import & indexes          Concept: comprehensions & unpacking
# ════════════════════════════════════════════════════════════════════════════
# 1. parse_timesheet_line(line): turn "2026-03-02,alice,T-01,4.0" into a
#    TimesheetLine. Split the line and unpack the four fields in ONE assignment
#    (day, employee, task_id, hours = ...). A line with a wrong number of fields
#    must raise ValueError (unpacking does it for you). Ignore surrounding spaces.
# 2. open_tasks_by_id(tasks): {id: task} for the tasks whose stage is not in
#    CLOSED_STAGES, as ONE dict comprehension.
# 3. all_tags(tasks): the set of every tag used by any task, as ONE set
#    comprehension (a comprehension can contain two `for` clauses).
#
#    all_tags(load_tasks()) → {"onsite", "design", "purchase", "sales", "subcontractor", "logistics", "accounting"}
#
# 📚 Discover: https://docs.python.org/3/tutorial/datastructures.html#nested-list-comprehensions
#             https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences  (unpacking)
# ⏱ ~20 min
def parse_timesheet_line(line: str) -> TimesheetLine:
    todo("PRJ-02")


def open_tasks_by_id(tasks: list[Task]) -> dict[str, Task]:
    todo("PRJ-02")


def all_tags(tasks: list[Task]) -> set[str]:
    todo("PRJ-02")


# ════════════════════════════════════════════════════════════════════════════
# PRJ-03 · Late tasks & overruns               Concept: map / filter / zip / key
# ════════════════════════════════════════════════════════════════════════════
# 1. late_tasks(tasks, today): ids of the tasks that are not closed and whose
#    deadline is strictly before `today`, sorted by deadline, then by id.
#    Use filter() and sorted() with a key.
# 2. overruns(task_ids, planned, spent): three parallel lists. Return the
#    (task_id, extra_hours) of the tasks where spent > planned, with
#    extra_hours = spent - planned, the biggest overrun first. The lists must have
#    the same length (ValueError otherwise): find the right parameter of zip().
#
#    overruns(["T-1", "T-2", "T-3"], [5, 8, 2], [6.5, 7, 4])   → [("T-3", 2.0), ("T-1", 1.5)]
#
# 📚 Discover: https://docs.python.org/3/library/functions.html#zip
#             https://docs.python.org/3/library/functions.html#filter
#             https://docs.python.org/3/howto/sorting.html#key-functions
# ⏱ ~20 min
def late_tasks(tasks: list[Task], today: date) -> list[str]:
    todo("PRJ-03")


def overruns(task_ids: list[str], planned: list[float], spent: list[float]) -> list[tuple[str, float]]:
    todo("PRJ-03")


# ════════════════════════════════════════════════════════════════════════════
# PRJ-04 · Working days                                    Concept: generators
# ════════════════════════════════════════════════════════════════════════════
# 1. workdays_from(start): an INFINITE generator yielding the working days
#    (Monday to Friday) from `start` included (if it is a working day). It never
#    stops: the caller decides how many values to take.
#    date.weekday() returns 0 for Monday ... 6 for Sunday.
# 2. add_workdays(start, n): the date that is n working days after `start`
#    (start itself is not counted), for n >= 1. Take the values you need from
#    workdays_from() with itertools.islice() or next(): no list of dates.
#
#    2026-03-13 is a Friday.
#    list(islice(workdays_from(date(2026, 3, 13)), 3))  → [Mar 13, Mar 16, Mar 17]
#    add_workdays(date(2026, 3, 13), 1)                → date(2026, 3, 16)
#
# 📚 Discover: https://docs.python.org/3/howto/functional.html#generators
#             https://docs.python.org/3/library/itertools.html#itertools.islice
#             https://docs.python.org/3/library/datetime.html  (timedelta, weekday)
# ⏱ ~25 min
def workdays_from(start: date):
    todo("PRJ-04")


def add_workdays(start: date, n: int) -> date:
    todo("PRJ-04")


# ════════════════════════════════════════════════════════════════════════════
# PRJ-05 · Assignments & contributors                    Concept: collections
# ════════════════════════════════════════════════════════════════════════════
# 1. tasks_by_assignee(tasks): {assignee: [task ids]} in input order. Tasks
#    without assignee (None) go under the key "unassigned". Use a defaultdict.
# 2. top_contributors(lines, k): the k employees who logged the most hours, as
#    (employee, total hours), biggest first. Use a Counter.
#
#    top_contributors(load_timesheets(), 1)  → [("bob", 36.5)]
#
# 📚 Discover: https://docs.python.org/3/library/collections.html  (defaultdict, Counter)
# ⏱ ~20 min
def tasks_by_assignee(tasks: list[Task]) -> dict[str, list[str]]:
    todo("PRJ-05")


def top_contributors(lines: list[TimesheetLine], k: int) -> list[tuple[str, float]]:
    todo("PRJ-05")


# ════════════════════════════════════════════════════════════════════════════
# PRJ-06 · Review pairs & weekly hours                     Concept: itertools
# ════════════════════════════════════════════════════════════════════════════
# 1. review_pairs(members): every pair of team members for cross code reviews,
#    each pair once, in input order. One itertools function does it.
#        review_pairs(["alice", "bob", "carla"])
#        → [("alice", "bob"), ("alice", "carla"), ("bob", "carla")]
# 2. hours_per_week(lines): [(ISO week number, total hours)] in date order. The
#    lines are sorted by date: group consecutive lines of the same ISO week
#    (day.isocalendar().week).
#        hours_per_week(load_timesheets())  → [(10, 28.5), (11, 30.5)]
#
# 📚 Discover: https://docs.python.org/3/library/itertools.html  (combinations, groupby)
# ⏱ ~25 min
def review_pairs(members: list[str]) -> list[tuple[str, str]]:
    todo("PRJ-06")


def hours_per_week(lines: list[TimesheetLine]) -> list[tuple[int, float]]:
    todo("PRJ-06")


# ════════════════════════════════════════════════════════════════════════════
# PRJ-07 · Planning queue & workload                    Concept: heapq & bisect
# ════════════════════════════════════════════════════════════════════════════
# 1. next_tasks(tasks, k): ids of the k open tasks (stage not in CLOSED_STAGES) to
#    plan first: earliest deadline first, then smallest planned_hours, then id.
#    Do not sort everything: use heapq.
# 2. workload_label(weekly_hours): the label of a weekly workload, with the
#    breakpoints below. A value equal to a breakpoint belongs to the upper label
#    (20 → "normal"). No if/elif chain: use bisect.
#
#    WORKLOAD_BREAKPOINTS = [20, 35, 45] → "light" | "normal" | "heavy" | "overload"
#
# 📚 Discover: https://docs.python.org/3/library/heapq.html  (nsmallest)
#             https://docs.python.org/3/library/bisect.html (read the "grade" example)
# ⏱ ~25 min
WORKLOAD_BREAKPOINTS = [20, 35, 45]
WORKLOAD_LABELS = ["light", "normal", "heavy", "overload"]


def next_tasks(tasks: list[Task], k: int) -> list[str]:
    todo("PRJ-07")


def workload_label(weekly_hours: float) -> str:
    todo("PRJ-07")


# ════════════════════════════════════════════════════════════════════════════
# PRJ-08 · Reusable helpers                                 Concept: functools
# ════════════════════════════════════════════════════════════════════════════
# 1. hours_counter_for(employee): return a function that takes a list of timesheet
#    lines and returns the hours of THAT employee. Build it from total_hours()
#    (in models.py) with functools.partial: no lambda, no nested def.
#        alice_hours = hours_counter_for("alice")
#        alice_hours(load_timesheets())  → 12.0
# 2. working_days_in_month(year, month): number of Monday-to-Friday days in the
#    month. The planning screen asks for the same months again and again: make
#    sure each (year, month) is computed only once (the tests check cache_info()).
#    Tip: calendar.monthrange(year, month) gives the number of days of a month.
#        working_days_in_month(2026, 3)  → 22
#
# 📚 Discover: https://docs.python.org/3/library/functools.html  (partial, cache)
# ⏱ ~20 min
def hours_counter_for(employee: str):
    todo("PRJ-08")


def working_days_in_month(year: int, month: int) -> int:
    todo("PRJ-08")


# ════════════════════════════════════════════════════════════════════════════
# PRJ-B2 · BONUS · Milestones                       Concept: dataclass options
# ════════════════════════════════════════════════════════════════════════════
# Milestones must be sortable by deadline (then by name) and must never change
# once created. Configure the dataclass instead of writing methods:
#   * comparisons (<, >, sorted) must work: find the dataclass parameter;
#   * instances must be immutable (assigning an attribute raises
#     dataclasses.FrozenInstanceError);
#   * `task_ids` must NOT take part in comparisons, and must default to an empty
#     tuple (look at dataclasses.field()).
# The order of the fields matters: comparison uses them from top to bottom.
#
#    sorted([Milestone(date(2026, 3, 27), "Installed"), Milestone(date(2026, 3, 13), "Ordered")])[0].name
#    → "Ordered"
#
# 📚 Discover: https://docs.python.org/3/library/dataclasses.html  (order, frozen, field)
# ⏱ ~15 min
@dataclass
class Milestone:
    deadline: date
    name: str
    task_ids: tuple[str, ...] = ()
