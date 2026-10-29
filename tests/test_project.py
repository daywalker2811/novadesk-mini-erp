"""Tests of the project module (Member B). Do not edit.

Run them all:        python -m unittest tests.test_project -v
Run one task only:   python -m unittest tests.test_project -k prj03 -v
"""

import dataclasses
import functools
import types
import unittest
from datetime import date
from itertools import islice

from erp.common.todo import require, require_enum
from erp.project import algorithms as algo
from erp.project import concepts as c
from erp.project.data import load_meetings, load_tasks, load_timesheets
from erp.project.models import Task, TimesheetLine


def task(tid: str, stage: str = "new", deadline: int = 20, hours: float = 4, assignee: str | None = "alice",
         tags: tuple[str, ...] = ()) -> Task:
    return Task(tid, f"Task {tid}", stage, assignee, hours, date(2026, 3, deadline), (), tags)


def line(day: int, employee: str, hours: float, task_id: str = "T-01") -> TimesheetLine:
    return TimesheetLine(date(2026, 3, day), employee, task_id, hours)


class TestPrj01Stages(unittest.TestCase):
    def setUp(self):
        require_enum(c.Stage, "PRJ-01")

    def test_prj01_members_match_the_data(self):
        self.assertEqual([s.value for s in c.Stage], ["new", "in_progress", "review", "done", "cancelled"])
        self.assertIs(c.Stage("review"), c.Stage.REVIEW)
        with self.assertRaises(ValueError):
            c.Stage("archived")

    def test_prj01_is_closed(self):
        self.assertEqual([s.is_closed for s in c.Stage], [False, False, False, True, True])

    def test_prj01_next_stage(self):
        self.assertIs(c.Stage.NEW.next_stage(), c.Stage.IN_PROGRESS)
        self.assertIs(c.Stage.IN_PROGRESS.next_stage(), c.Stage.REVIEW)
        self.assertIs(c.Stage.REVIEW.next_stage(), c.Stage.DONE)
        for final in (c.Stage.DONE, c.Stage.CANCELLED):
            with self.assertRaises(ValueError):
                final.next_stage()


class TestPrj02Comprehensions(unittest.TestCase):
    def test_prj02_parse_timesheet_line(self):
        self.assertEqual(c.parse_timesheet_line(" 2026-03-02,alice,T-01,4.0\n"), line(2, "alice", 4.0))
        with self.assertRaises(ValueError):
            c.parse_timesheet_line("2026-03-02,alice,4.0")

    def test_prj02_open_tasks_by_id(self):
        tasks = [task("T-1", "done"), task("T-2", "new"), task("T-3", "cancelled"), task("T-4", "review")]
        self.assertEqual(c.open_tasks_by_id(tasks), {"T-2": tasks[1], "T-4": tasks[3]})

    def test_prj02_all_tags(self):
        self.assertEqual(c.all_tags(load_tasks()),
                         {"onsite", "design", "purchase", "sales", "subcontractor", "logistics", "accounting"})
        self.assertEqual(c.all_tags([]), set())


class TestPrj03LateAndOverruns(unittest.TestCase):
    def test_prj03_late_tasks(self):
        tasks = [task("T-4", deadline=10), task("T-2", deadline=12), task("T-1", "done", deadline=5),
                 task("T-3", deadline=10), task("T-5", deadline=16)]
        self.assertEqual(c.late_tasks(tasks, date(2026, 3, 16)), ["T-3", "T-4", "T-2"])
        self.assertEqual(c.late_tasks(load_tasks(), date(2026, 3, 16)), ["T-03", "T-04", "T-06"])

    def test_prj03_overruns(self):
        self.assertEqual(c.overruns(["T-1", "T-2", "T-3"], [5, 8, 2], [6.5, 7, 4]), [("T-3", 2.0), ("T-1", 1.5)])
        self.assertEqual(c.overruns([], [], []), [])
        with self.assertRaises(ValueError):
            c.overruns(["T-1"], [5, 8], [6, 7])


class TestPrj04Generators(unittest.TestCase):
    def test_prj04_workdays_from_is_an_infinite_generator(self):
        days = c.workdays_from(date(2026, 3, 13))
        self.assertIsInstance(days, types.GeneratorType)
        self.assertEqual(list(islice(days, 3)), [date(2026, 3, 13), date(2026, 3, 16), date(2026, 3, 17)])
        self.assertEqual(next(c.workdays_from(date(2026, 3, 14))), date(2026, 3, 16))  # Saturday → Monday
        self.assertEqual(len(list(islice(c.workdays_from(date(2026, 1, 1)), 1000))), 1000)

    def test_prj04_add_workdays(self):
        self.assertEqual(c.add_workdays(date(2026, 3, 13), 1), date(2026, 3, 16))
        self.assertEqual(c.add_workdays(date(2026, 3, 16), 5), date(2026, 3, 23))
        self.assertEqual(c.add_workdays(date(2026, 3, 14), 10), date(2026, 3, 27))


class TestPrj05Collections(unittest.TestCase):
    def test_prj05_tasks_by_assignee(self):
        tasks = [task("T-1", assignee="bob"), task("T-2", assignee=None), task("T-3", assignee="bob")]
        self.assertEqual(dict(c.tasks_by_assignee(tasks)), {"bob": ["T-1", "T-3"], "unassigned": ["T-2"]})
        real = c.tasks_by_assignee(load_tasks())
        self.assertEqual(real["unassigned"], ["T-08", "T-12"])

    def test_prj05_top_contributors(self):
        lines = [line(2, "a", 3), line(2, "b", 5), line(3, "a", 4), line(3, "c", 1)]
        self.assertEqual(c.top_contributors(lines, 2), [("a", 7), ("b", 5)])
        self.assertEqual(c.top_contributors(load_timesheets(), 1), [("bob", 36.5)])


class TestPrj06Itertools(unittest.TestCase):
    def test_prj06_review_pairs(self):
        self.assertEqual(c.review_pairs(["alice", "bob", "carla"]),
                         [("alice", "bob"), ("alice", "carla"), ("bob", "carla")])
        self.assertEqual(len(c.review_pairs(["a", "b", "c", "d", "e"])), 10)
        self.assertEqual(c.review_pairs(["solo"]), [])

    def test_prj06_hours_per_week(self):
        lines = [line(6, "a", 2), line(9, "a", 3), line(13, "b", 4), line(16, "a", 1.5)]
        self.assertEqual(c.hours_per_week(lines), [(10, 2), (11, 7), (12, 1.5)])
        self.assertEqual(c.hours_per_week(load_timesheets()), [(10, 28.5), (11, 30.5)])


class TestPrj07HeapBisect(unittest.TestCase):
    def test_prj07_next_tasks(self):
        tasks = [task("T-1", deadline=20, hours=8), task("T-2", "done", deadline=1),
                 task("T-3", deadline=18, hours=5), task("T-4", deadline=20, hours=2), task("T-5", deadline=20, hours=2)]
        self.assertEqual(c.next_tasks(tasks, 3), ["T-3", "T-4", "T-5"])
        self.assertEqual(c.next_tasks(tasks, 10), ["T-3", "T-4", "T-5", "T-1"])

    def test_prj07_workload_label(self):
        self.assertEqual([c.workload_label(h) for h in (0, 19.5, 20, 34.9, 35, 45, 60)],
                         ["light", "light", "normal", "normal", "heavy", "overload", "overload"])


class TestPrj08Functools(unittest.TestCase):
    def test_prj08_hours_counter_for(self):
        alice_hours = c.hours_counter_for("alice")
        self.assertIsInstance(alice_hours, functools.partial, "build the function with functools.partial")
        self.assertEqual(alice_hours(load_timesheets()), 12.0)
        self.assertEqual(c.hours_counter_for("zoe")(load_timesheets()), 0)

    def test_prj08_working_days_in_month_is_cached(self):
        self.assertEqual(c.working_days_in_month(2026, 3), 22)
        self.assertTrue(hasattr(c.working_days_in_month, "cache_info"),
                        "working_days_in_month must be decorated with a functools cache decorator")
        c.working_days_in_month.cache_clear()
        self.assertEqual(c.working_days_in_month(2026, 2), 20)
        self.assertEqual(c.working_days_in_month(2026, 2), 20)
        self.assertEqual(c.working_days_in_month(2026, 5), 21)
        info = c.working_days_in_month.cache_info()
        self.assertEqual((info.hits, info.misses), (1, 2))


class TestPrjA1BusyBlocks(unittest.TestCase):
    def test_prja1_example(self):
        meetings = [(540, 570), (555, 600), (660, 705), (705, 750), (840, 900), (870, 885)]
        self.assertEqual(algo.busy_blocks(meetings), [(540, 600), (660, 750), (840, 900)])

    def test_prja1_unsorted_and_edge_cases(self):
        self.assertEqual(algo.busy_blocks([]), [])
        self.assertEqual(algo.busy_blocks([(600, 660)]), [(600, 660)])
        self.assertEqual(algo.busy_blocks([(700, 720), (480, 500), (490, 710)]), [(480, 720)])
        self.assertEqual(algo.busy_blocks([(780, 840), (480, 540)]), [(480, 540), (780, 840)])

    def test_prja1_real_data(self):
        self.assertEqual(algo.busy_blocks(load_meetings("alice")), [(540, 600), (660, 750), (840, 900)])


class TestPrjA2ExecutionOrder(unittest.TestCase):
    def test_prja2_example(self):
        self.assertEqual(algo.execution_order({"T-3": ["T-1", "T-2"], "T-1": [], "T-2": ["T-1"], "T-4": []}),
                         ["T-1", "T-2", "T-3", "T-4"])

    def test_prja2_real_project(self):
        order = algo.execution_order({t.id: list(t.depends_on) for t in load_tasks()})
        self.assertEqual(order, ["T-01", "T-02", "T-03", "T-04", "T-05", "T-06", "T-07",
                                 "T-08", "T-09", "T-10", "T-11", "T-12"])

    def test_prja2_smallest_ready_task_first(self):
        self.assertEqual(algo.execution_order({"B": [], "A": ["C"], "C": []}), ["B", "C", "A"])

    def test_prja2_cycle(self):
        with self.assertRaises(ValueError):
            algo.execution_order({"A": ["B"], "B": ["A"]})
        with self.assertRaises(ValueError):
            algo.execution_order({"A": [], "B": ["A", "D"], "C": ["B"], "D": ["C"]})


class TestPrjB1BusiestPeriod(unittest.TestCase):
    def test_prjb1_examples(self):
        self.assertEqual(algo.busiest_period([4, 9.5, 6, 2, 8, 7.5], 2), (1, 15.5))
        self.assertEqual(algo.busiest_period([4, 9.5, 6, 2, 8, 7.5], 3), (0, 19.5))
        self.assertEqual(algo.busiest_period([5], 1), (0, 5))

    def test_prjb1_invalid_k(self):
        for k in (0, 7):
            with self.assertRaises(ValueError):
                algo.busiest_period([4, 9.5, 6, 2, 8, 7.5], k)

    def test_prjb1_large_input(self):
        days = [1.0] * 20_000
        days[14_000] = 1000.0
        self.assertEqual(algo.busiest_period(days, 10_000), (4_001, 10_999.0))


class TestPrjB2Milestones(unittest.TestCase):
    def setUp(self):
        params = c.Milestone.__dataclass_params__
        require(params.order or params.frozen, "PRJ-B2")

    def test_prjb2_sortable(self):
        installed = c.Milestone(date(2026, 3, 27), "Installed", ("T-08",))
        ordered = c.Milestone(date(2026, 3, 13), "Ordered")
        audit = c.Milestone(date(2026, 3, 27), "Audit", ("T-01", "T-02"))
        self.assertEqual([m.name for m in sorted([installed, ordered, audit])], ["Ordered", "Audit", "Installed"])
        self.assertLess(ordered, installed)

    def test_prjb2_task_ids_ignored_in_comparisons(self):
        self.assertEqual(c.Milestone(date(2026, 3, 27), "X", ("T-1",)), c.Milestone(date(2026, 3, 27), "X", ("T-2",)))
        self.assertEqual(c.Milestone(date(2026, 3, 27), "X").task_ids, ())

    def test_prjb2_frozen(self):
        with self.assertRaises(dataclasses.FrozenInstanceError):
            c.Milestone(date(2026, 3, 27), "X").name = "Y"


if __name__ == "__main__":
    unittest.main()
