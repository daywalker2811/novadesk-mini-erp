"""Demo of the project tasks on the real data (python -m erp demo project)."""

from datetime import date

from erp.common.todo import require, require_enum
from erp.project import algorithms as algo
from erp.project import concepts as c
from erp.project.data import load_meetings, load_tasks, load_timesheet_lines, load_timesheets, to_hhmm

TODAY = date(2026, 3, 16)


def _blocks(employee: str) -> list[str]:
    return [f"{to_hhmm(start)}-{to_hhmm(end)}" for start, end in algo.busy_blocks(load_meetings(employee))]


def steps():
    tasks = load_tasks()
    lines = load_timesheets()
    return [
        ("PRJ-01", "next stage of each column",
         lambda: require_enum(c.Stage, "PRJ-01") or {s.value: (None if s.is_closed else s.next_stage().value) for s in c.Stage}),
        ("PRJ-02", "first parsed timesheet line", lambda: c.parse_timesheet_line(load_timesheet_lines()[0])),
        ("PRJ-02", "open tasks", lambda: sorted(c.open_tasks_by_id(tasks))),
        ("PRJ-02", "tags", lambda: sorted(c.all_tags(tasks))),
        ("PRJ-03", f"late tasks on {TODAY}", lambda: c.late_tasks(tasks, TODAY)),
        ("PRJ-04", "10 working days after Mar 16", lambda: c.add_workdays(TODAY, 10)),
        ("PRJ-05", "tasks by assignee", lambda: c.tasks_by_assignee(tasks)),
        ("PRJ-05", "top contributors", lambda: c.top_contributors(lines, 3)),
        ("PRJ-06", "review pairs", lambda: c.review_pairs(["alice", "bob", "carla", "dan"])),
        ("PRJ-06", "hours per ISO week", lambda: c.hours_per_week(lines)),
        ("PRJ-07", "plan next", lambda: c.next_tasks(tasks, 3)),
        ("PRJ-07", "workload of each week", lambda: [c.workload_label(h) for _, h in c.hours_per_week(lines)]),
        ("PRJ-08", "alice's hours", lambda: c.hours_counter_for("alice")(lines)),
        ("PRJ-08", "working days in April 2026", lambda: c.working_days_in_month(2026, 4)),
        ("PRJ-A1", "alice's busy blocks", lambda: _blocks("alice")),
        ("PRJ-A2", "execution order", lambda: algo.execution_order({t.id: list(t.depends_on) for t in tasks})),
        ("PRJ-B1", "busiest 3 days", lambda: algo.busiest_period([4.0, 9.0, 8.5, 8.0, 3.0, 16.5, 14.0, 9.5, 4.0, 3.0], 3)),
        ("PRJ-B2", "milestones in order",
         lambda: require(c.Milestone.__dataclass_params__.order, "PRJ-B2") or [m.name for m in sorted([c.Milestone(date(2026, 3, 27), "Installed"), c.Milestone(date(2026, 3, 13), "Ordered")])]),
    ]
