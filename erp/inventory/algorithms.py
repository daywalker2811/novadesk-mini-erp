"""INVENTORY — algorithm tasks (Member A).

These tasks look like the exercises of online coding tests (Coderbyte...).
For each one:
  1. Solve the examples by hand on paper first.
  2. Write a first solution that works, even a slow one.
  3. State its time complexity in the docstring, then improve it if you can.
     Interviewers always ask: "What is the complexity? Can you do better?"

INV-A1 and INV-A2 are mandatory. INV-B1 is a bonus.
"""

from __future__ import annotations

from erp.common.todo import todo

# Add the imports you need here.


# ════════════════════════════════════════════════════════════════════════════
# INV-A1 · Net movement between two days                          ⏱ ~40 min
# ════════════════════════════════════════════════════════════════════════════
# The stock controller works with the list `daily_net`: daily_net[i] is the net
# number of units that entered (positive) or left (negative) the warehouse on
# working day i.
#
# She asks many questions such as "what was the net movement from day 3 to day 7?".
# Each query is a pair (start, end) of day indexes, both INCLUDED, with
# 0 <= start <= end < len(daily_net). Return the answers in the order of the queries.
#
#    daily_net = [5, -2, 7, 0, -4, 3]
#    queries   = [(0, 2), (1, 4), (3, 3), (0, 5)]
#    → [10, 1, 0, 9]
#
# Constraints: up to 100,000 days and 100,000 queries. Summing each range
# separately is far too slow at that scale: find a way to answer every query in
# constant time after a single preparation pass over the days.
# Target: O(n + q).
def net_movement_between(daily_net: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """Complexity: ... (write it here)"""
    todo("INV-A1")


# ════════════════════════════════════════════════════════════════════════════
# INV-A2 · Picking route in the warehouse                          ⏱ ~60 min
# ════════════════════════════════════════════════════════════════════════════
# The warehouse map is a list of strings of the same length:
#   '#' a rack or a wall (impossible to cross)
#   '.' an aisle
#   'D' the loading dock (start, exactly one)
#   'P' the picking spot (goal, exactly one)
# The picker moves one cell at a time: up, down, left or right (no diagonals).
#
# Return the MINIMUM number of moves to go from 'D' to 'P', or -1 if 'P' cannot
# be reached.
#
#    ["D.#",
#     ".##",      → 4   (down, down, right, right)
#     "..P"]
#
#    ["D#P"]      → -1
#
# The real map is in data/inventory/warehouse_map.txt (see load_warehouse_map()).
# Hint: think about exploring the cells in order of their distance from the dock.
# Target: every cell is visited at most once.
def shortest_pick_path(grid: list[str]) -> int:
    """Complexity: ... (write it here)"""
    todo("INV-A2")


# ════════════════════════════════════════════════════════════════════════════
# INV-B1 · BONUS · Shipping packages                              ⏱ ~45 min
# ════════════════════════════════════════════════════════════════════════════
# Products are shipped in packages of fixed sizes, for example [4, 6, 9] units.
# Every package must be full, and you can use as many packages of each size as
# you want.
#
# Return the MINIMUM number of packages needed to ship exactly `quantity` units,
# or -1 if it is impossible.
#
#    min_packages(12, [4, 6, 9])  → 2     (6 + 6; 4 + 4 + 4 needs 3 packages)
#    min_packages(17, [4, 6, 9])  → 3     (4 + 4 + 9)
#    min_packages(5,  [4, 6, 9])  → -1
#    min_packages(0,  [4, 6, 9])  → 0
#
# Warning: always taking the biggest package first does NOT always work.
# Try min_packages(12, [1, 6, 9]) by hand: the answer is 2.
# Hint: the best answer for `quantity` can be built from the best answers for
# smaller quantities.
def min_packages(quantity: int, sizes: list[int]) -> int:
    """Complexity: ... (write it here)"""
    todo("INV-B1")
