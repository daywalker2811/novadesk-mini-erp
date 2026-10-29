"""PROJECT — algorithm tasks (Member B).

These tasks look like the exercises of online coding tests (Coderbyte...).
For each one:
  1. Solve the examples by hand on paper first.
  2. Write a first solution that works, even a slow one.
  3. State its time complexity in the docstring, then improve it if you can.
     Interviewers always ask: "What is the complexity? Can you do better?"

PRJ-A1 and PRJ-A2 are mandatory. PRJ-B1 is a bonus.
"""

from __future__ import annotations

from erp.common.todo import todo

# Add the imports you need here.


# ════════════════════════════════════════════════════════════════════════════
# PRJ-A1 · Busy blocks in a calendar                               ⏱ ~40 min
# ════════════════════════════════════════════════════════════════════════════
# The planning screen shows when an employee is busy. Meetings are given as
# (start, end) in minutes since midnight, in ANY order, and they may overlap.
# A meeting that starts exactly when another one ends is part of the same block.
#
# Return the busy blocks: the smallest list of non-overlapping (start, end)
# periods covering every meeting, sorted by start time.
#
#    meetings = [(540, 570), (555, 600), (660, 705), (705, 750), (840, 900), (870, 885)]
#    (09:00-09:30, 09:15-10:00, 11:00-11:45, 11:45-12:30, 14:00-15:00, 14:30-14:45)
#    → [(540, 600), (660, 750), (840, 900)]
#    (09:00-10:00, 11:00-12:30, 14:00-15:00)
#
#    busy_blocks([])  → []
#
# Target: better than comparing every meeting with every other one (O(n²)).
def busy_blocks(meetings: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Complexity: ... (write it here)"""
    todo("PRJ-A1")


# ════════════════════════════════════════════════════════════════════════════
# PRJ-A2 · Execution order of tasks                                ⏱ ~60 min
# ════════════════════════════════════════════════════════════════════════════
# `dependencies` maps each task id to the ids of the tasks that must be finished
# BEFORE it can start. Every task appears as a key (with an empty list when it
# has no dependency).
#
# Return an execution order: a list containing every task once, in which each
# task comes after all of its dependencies. When several tasks are ready at the
# same time, take the smallest id first (alphabetical order), so that the answer
# is unique.
# If the dependencies form a loop (A needs B, B needs A...), no order exists:
# raise ValueError("circular dependency").
#
#    execution_order({"T-3": ["T-1", "T-2"], "T-1": [], "T-2": ["T-1"], "T-4": []})
#    → ["T-1", "T-2", "T-3", "T-4"]
#    T-1 and T-4 are ready at the start; T-1 is taken first. Then T-2 and T-4 are
#    ready: T-2 is taken. Then T-3 and T-4: T-3 is taken. Then T-4.
#
#    execution_order({"A": ["B"], "B": ["A"]})  → ValueError
#
# Hint: count, for each task, how many of its dependencies are not finished yet.
# Target: O((V + E) log V), where V is the number of tasks and E the number of
# dependencies.
def execution_order(dependencies: dict[str, list[str]]) -> list[str]:
    """Complexity: ... (write it here)"""
    todo("PRJ-A2")


# ════════════════════════════════════════════════════════════════════════════
# PRJ-B1 · BONUS · Busiest period                                  ⏱ ~40 min
# ════════════════════════════════════════════════════════════════════════════
# daily_hours[i] is the number of hours logged by the team on working day i.
# The project manager wants the k CONSECUTIVE days with the highest total.
#
# Return (index of the first day of the period, total hours of the period),
# total rounded to 2 decimals. If several periods share the best total, return
# the earliest one. Raise ValueError if k < 1 or k > len(daily_hours).
#
#    busiest_period([4, 9.5, 6, 2, 8, 7.5], 2)  → (1, 15.5)
#    busiest_period([4, 9.5, 6, 2, 8, 7.5], 3)  → (0, 19.5)
#
# Constraints: up to 100,000 days and any k. Recomputing the sum of each period
# from scratch costs O(n·k): reuse the previous total instead. Target: O(n).
def busiest_period(daily_hours: list[float], k: int) -> tuple[int, float]:
    """Complexity: ... (write it here)"""
    todo("PRJ-B1")
