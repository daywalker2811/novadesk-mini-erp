"""Markers for unfinished tasks.

Every task starts with a `todo("XXX-00")` line. Calling an unfinished task raises
`TaskNotDone`. The progress board and the tests report it as "to do" instead of
crashing, so one unfinished task never prevents the rest of the project from running.

`TaskNotDone` extends `unittest.SkipTest`: with `python -m unittest`, unfinished
tasks are reported as *skipped*, not as errors.
"""

from __future__ import annotations

import unittest
from enum import Enum
from typing import NoReturn


class TaskNotDone(unittest.SkipTest):
    """Raised by a task that has not been implemented yet."""

    def __init__(self, task_id: str) -> None:
        super().__init__(f"{task_id} is not implemented yet")
        self.task_id = task_id


def todo(task_id: str) -> NoReturn:
    """Placeholder for a task body. Replace the call with your implementation."""
    raise TaskNotDone(task_id)


def require(condition: bool, task_id: str) -> None:
    """Report `task_id` as not done when `condition` is false (used by the tests)."""
    if not condition:
        raise TaskNotDone(task_id)


def require_enum(enum_cls: type[Enum], task_id: str) -> None:
    """Report `task_id` as not done while the Enum has no member (used by the tests)."""
    require(len(enum_cls) > 0, task_id)
