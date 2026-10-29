"""Progress board: runs the tests of each module and prints one line per task.

Every task runs in its own process, with a time limit. A crash or an infinite loop
only affects its own task, and a syntax error only affects its own module: the
other members' work always keeps running.
"""

from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from erp.common.paths import PROJECT_ROOT
from erp.common.runner import RESULT_MARKER

TIMEOUT_SECONDS = 20   # per task


@dataclass(frozen=True)
class Module:
    key: str
    member: str
    icon: str
    package: str
    test_module: str


MODULES = [
    Module("inventory", "Member A", "📦", "erp.inventory", "tests.test_inventory"),
    Module("project", "Member B", "🗂 ", "erp.project", "tests.test_project"),
    Module("crm", "Member C", "🤝", "erp.crm", "tests.test_crm"),
]


def status(result: dict) -> tuple[str, str]:
    passed, failures, errors = result["passed"], result["failures"], result["errors"]
    todo, blocked_by = result["todo"], result["blocked_by"]
    total = passed + len(failures) + len(errors) + todo + len(blocked_by)
    if errors:
        return "💥", f"error: {errors[0]}"
    if failures:
        return "❌", f"{passed}/{total} checks pass, first failure: {failures[0]}"
    if todo and passed:
        return "🟡", f"in progress ({passed}/{total} checks pass)"
    if todo or not total:
        return "⏳", "to do"
    if blocked_by:
        return "🔒", "waiting for " + ", ".join(sorted(blocked_by))
    return "✅", "done"


EMPTY = {"passed": 0, "failures": [], "errors": [], "todo": 0, "blocked_by": []}


def _run_task(test_module: str, task_id: str) -> dict:
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    try:
        completed = subprocess.run(
            [sys.executable, "-m", "erp.common.runner", test_module, task_id],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=TIMEOUT_SECONDS, cwd=PROJECT_ROOT, env=env,
        )
    except subprocess.TimeoutExpired:
        return {"timeout": True}
    for line in reversed(completed.stdout.splitlines()):
        if line.startswith(RESULT_MARKER):
            return json.loads(line[len(RESULT_MARKER):])
    last_error = (completed.stderr.strip().splitlines() or ["unknown error"])[-1]
    return {"load_error": last_error}


def run_module(module: Module) -> tuple[int, int]:
    """Print the board of one module. Return (done, total)."""
    titles: dict[str, str] = importlib.import_module(module.package).TASKS
    print(f"\n{module.icon} {module.key.upper()} ({module.member})")
    with ThreadPoolExecutor(max_workers=6) as pool:
        summaries = dict(zip(titles, pool.map(lambda tid: _run_task(module.test_module, tid), titles)))

    load_errors = [s["load_error"] for s in summaries.values() if "load_error" in s]
    if load_errors and len(load_errors) == len(summaries):
        print(f"   💥 cannot load the module: {load_errors[0]}")
        print(f"      details: python -m unittest {module.test_module} -v")
        return 0, len(titles)

    done = 0
    for task_id, title in titles.items():
        summary = summaries[task_id]
        if summary.get("timeout"):
            icon, detail = "⌛", f"stopped after {TIMEOUT_SECONDS} s: infinite loop or very slow algorithm?"
        elif "load_error" in summary:
            icon, detail = "💥", summary["load_error"]
        else:
            icon, detail = status(summary["result"] or EMPTY)
        done += icon == "✅"
        print(f"   {icon} {task_id:<7}{title:<34} {detail}")
    example = next(iter(titles)).lower().replace("-", "")
    if done < len(titles):
        print(f"   → {done}/{len(titles)} tasks done   ·   details: python -m unittest {module.test_module} -k {example} -v")
    else:
        print(f"   → {done}/{len(titles)} tasks done   🎉")
    return done, len(titles)


def run(keys: list[str] | None = None) -> None:
    selected = [m for m in MODULES if not keys or m.key in keys]
    if not selected:
        print("Unknown module. Choose among: " + ", ".join(m.key for m in MODULES))
        return
    print("NovaDesk mini-ERP — progress board")
    print("✅ done  🟡 in progress  ⏳ to do  🔒 waiting for another task  ❌ wrong result  💥 crash  ⌛ too slow")
    totals = [run_module(m) for m in selected]
    done = sum(d for d, _ in totals)
    total = sum(t for _, t in totals)
    print(f"\nTeam total: {done}/{total} tasks done")
