"""CRM — algorithm tasks (Member C).

These tasks look like the exercises of online coding tests (Coderbyte...).
For each one:
  1. Solve the examples by hand on paper first.
  2. Write a first solution that works, even a slow one.
  3. State its time complexity in the docstring, then improve it if you can.
     Interviewers always ask: "What is the complexity? Can you do better?"

CRM-A1 and CRM-A2 are mandatory. CRM-B1 is a bonus.
"""

from __future__ import annotations

from erp.common.todo import todo
from erp.crm.templates import template_tokens

# Add the imports you need here.


# ════════════════════════════════════════════════════════════════════════════
# CRM-A1 · Mail template checker                                   ⏱ ~45 min
# ════════════════════════════════════════════════════════════════════════════
# Salespeople write their own mail templates. A broken template crashes the
# mass mailing, so we check them before saving. template_tokens(template)
# (already written, see erp/crm/templates.py) gives you the tags in order:
#   "{{" / "}}"                → opening / closing of an expression
#   "if", "else", "endif"      → a condition
#   "for", "endfor"            → a loop
#
# A template is valid when:
#   * every "{{" is closed by "}}" before any other tag appears (no tag inside an
#     expression), and there is no "}}" without a "{{";
#   * every "if" is closed by an "endif" and every "for" by an "endfor";
#   * blocks are properly nested: a block opened inside another one must be
#     closed first;
#   * "else" only appears directly inside an "if" block (the innermost open
#     block must be an "if");
#   * any other keyword makes the template invalid.
#
#    "Hi {{ name }}{% if vip %}!{% endif %}"                          → True
#    "{% for x in xs %}{% if x %}{{ x }}{% endfor %}{% endif %}"      → False (crossed blocks)
#    "{% for x in xs %}{% else %}{% endfor %}"                        → False (else in a for)
#    "Hello {{ name }"                                                → False
#
# Three templates are in data/crm/templates/ (see load_template()).
# Target: a single pass over the tokens.
def is_valid_template(template: str) -> bool:
    """Complexity: ... (write it here)"""
    todo("CRM-A1")


# ════════════════════════════════════════════════════════════════════════════
# CRM-A2 · Best period of the year                                 ⏱ ~45 min
# ════════════════════════════════════════════════════════════════════════════
# margins[i] is the net margin (in euros, possibly negative) of month i.
# Management wants the CONSECUTIVE months with the highest total margin.
#
# Return (index of the first month, index of the last month, total margin).
# The period contains at least one month: if every month is negative, return the
# least bad month. The data guarantee that the best period is unique.
# Raise ValueError for an empty list.
#
#    best_period([-200, 500, -100, 400, -900, 300])   → (1, 3, 800)
#    best_period([-5, -2, -7])                        → (1, 1, -2)
#
# Constraints: up to 1,000,000 values. Trying every
# (start, end) pair is O(n²) or worse: find a single pass. Hint: when the total
# of the period you are building becomes negative, is it still worth keeping?
# Target: O(n).
def best_period(margins: list[int]) -> tuple[int, int, int]:
    """Complexity: ... (write it here)"""
    todo("CRM-A2")


# ════════════════════════════════════════════════════════════════════════════
# CRM-B1 · BONUS · Offers matching a budget                        ⏱ ~30 min
# ════════════════════════════════════════════════════════════════════════════
# A client announces a budget. The salesperson wants two DIFFERENT offers whose
# prices add up exactly to it.
# `offers` is a list of (offer_id, price in cents) SORTED by price ascending.
# Return the ids of the two offers (cheaper one first), or None if no pair
# matches. The data guarantee that at most one pair matches.
#
#    offers = [("A", 300), ("B", 500), ("C", 700), ("D", 1100)]
#    matching_offers(offers, 1200)  → ("B", "C")
#    matching_offers(offers, 1400)  → ("A", "D")
#    matching_offers(offers, 1100)  → None    (D alone is not a pair)
#    matching_offers(offers, 50)    → None
#
# Constraints: up to 1,000,000 offers. Testing every pair is O(n²). The list is
# sorted: use it. Target: O(n) time and O(1) extra memory.
def matching_offers(offers: list[tuple[str, int]], budget: int) -> tuple[str, str] | None:
    """Complexity: ... (write it here)"""
    todo("CRM-B1")
