"""Runs the tests of ONE task and prints a JSON summary (used by the board).

The board starts this script in a separate process for every task, with a time
limit: an infinite loop or a very slow algorithm only affects its own task.

    python -m erp.common.runner tests.test_inventory INV-03
"""

from __future__ import annotations

import importlib
import json
import re
import sys
import traceback
import unittest

RESULT_MARKER = "@@BOARD-RESULT@@"
TEST_NAME = re.compile(r"^test_([a-z]{3})(\d{2}|[ab]\d)_")


def task_id(test: unittest.TestCase) -> str:
    match = TEST_NAME.match(getattr(test, "_testMethodName", ""))
    if not match:
        return "?"
    prefix, number = match.groups()
    return f"{prefix.upper()}-{number.upper()}"


def short(err: tuple, limit: int = 110) -> str:
    text = traceback.format_exception_only(err[0], err[1])[-1].strip().replace("\n", " ")
    return text if len(text) <= limit else text[: limit - 1] + "…"


class Collector(unittest.TestResult):
    def __init__(self) -> None:
        super().__init__()
        self.tasks: dict[str, dict] = {}

    def _get(self, test: unittest.TestCase) -> dict:
        return self.tasks.setdefault(
            task_id(test), {"passed": 0, "failures": [], "errors": [], "todo": 0, "blocked_by": []})

    def addSuccess(self, test):  # noqa: N802 (unittest API)
        self._get(test)["passed"] += 1

    def addFailure(self, test, err):  # noqa: N802
        self._get(test)["failures"].append(short(err))

    def addError(self, test, err):  # noqa: N802
        self._get(test)["errors"].append(short(err))

    def addSkip(self, test, reason):  # noqa: N802
        result = self._get(test)
        owner = reason.split(" ", 1)[0]
        if owner == task_id(test):
            result["todo"] += 1
        elif owner not in result["blocked_by"]:
            result["blocked_by"].append(owner)

    def addSubTest(self, test, subtest, err):  # noqa: N802
        if err is not None:
            key = "failures" if issubclass(err[0], test.failureException) else "errors"
            self._get(test)[key].append(short(err))


def _flatten(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from _flatten(item)
        else:
            yield item


def main(test_module: str, wanted_task: str) -> None:
    try:
        module = importlib.import_module(test_module)
    except Exception as exc:  # a syntax error in the member's file, for example
        summary = {"load_error": f"{type(exc).__name__}: {exc}"}
    else:
        tests = [t for t in _flatten(unittest.defaultTestLoader.loadTestsFromModule(module)) if task_id(t) == wanted_task]
        collector = Collector()
        unittest.TestSuite(tests).run(collector)
        summary = {"result": collector.tasks.get(wanted_task)}
    print(RESULT_MARKER + json.dumps(summary))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
