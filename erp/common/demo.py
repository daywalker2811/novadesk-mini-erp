"""Runs each finished task on the real data of the data/ folder."""

from __future__ import annotations

import importlib
import reprlib

from erp.common.board import MODULES
from erp.common.todo import TaskNotDone

_repr = reprlib.Repr()
_repr.maxlist = 8
_repr.maxdict = 8
_repr.maxstring = 90
_repr.maxother = 90


def run(keys: list[str] | None = None) -> None:
    for module in MODULES:
        if keys and module.key not in keys:
            continue
        print(f"\n{module.icon} {module.key.upper()} — demo on the real data")
        try:
            demo = importlib.import_module(f"{module.package}.demo")
            steps = demo.steps()
        except Exception as exc:
            print(f"   💥 cannot load the module: {type(exc).__name__}: {exc}")
            continue
        for task_id, label, action in steps:
            try:
                value = action()
            except TaskNotDone as exc:
                print(f"   ⏳ {task_id:<7}{label}: waiting for {exc.task_id}")
            except Exception as exc:
                print(f"   💥 {task_id:<7}{label}: {type(exc).__name__}: {exc}")
            else:
                text = value if isinstance(value, str) and "\n" in value else _repr.repr(value)
                print(f"   ✅ {task_id:<7}{label}: {text}")
