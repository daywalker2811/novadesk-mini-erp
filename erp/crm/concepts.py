"""CRM — concept tasks (Member C).

How it works
------------
* Each task is a function (or class) containing a `todo("CRM-xx")` line.
  Replace that line with your implementation.
* Read the "Discover" links: today's goal is to learn these tools on your own.
* Check your progress with `python -m erp crm`, and run your code on the
  real data with `python -m erp demo crm`.
* Commit after each task: git commit -m "CRM-03: CSV import and weighted pipeline".

You may add helper functions and imports. Do not rename the existing functions:
the tests use these names.
"""

from __future__ import annotations

from collections.abc import Iterable

from erp.common.todo import todo
from erp.crm.models import Lead

from enum import StrEnum

# Add the imports you need here (collections, itertools, functools, heapq, bisect...).

FINAL_STAGES = {"won", "lost"}


# ════════════════════════════════════════════════════════════════════════════
# CRM-01 · Lead stages                               Concept: Enum (+ match/case)
# ════════════════════════════════════════════════════════════════════════════
# The pipeline of Odoo CRM is a series of stages.
#
# 1. Declare the members of LeadStage, with exactly the values used in leads.csv:
#    NEW = "new", QUALIFIED = "qualified", PROPOSITION = "proposition",
#    WON = "won", LOST = "lost". Keep this order.
# 2. default_probability: the probability (in %) suggested for a new lead in
#    this stage, written with a `match` statement:
#    NEW 10, QUALIFIED 30, PROPOSITION 60, WON 100, LOST 0.
# 3. is_open: False for WON and LOST, True otherwise.
#
#    LeadStage("proposition").default_probability   → 60
#    LeadStage.LOST.is_open                         → False
#
# 📚 Discover: https://docs.python.org/3/library/enum.html  (StrEnum, iteration over members)
#             https://docs.python.org/3/tutorial/controlflow.html#match-statements
# ⏱ ~25 min
class LeadStage(StrEnum):
    """Stage of a lead in the sales pipeline."""

    NEW ="new"
    QUALIFIED = "qualified"
    PROPOSITION = "proposition"
    WON = "won"
    LOST = "lost"

    @property
    def default_probability(self) -> int:
        match self:
            case LeadStage.NEW:
                return 10
            case LeadStage.QUALIFIED:
                return 30
            case LeadStage.PROPOSITION:
                return 60
            case LeadStage.WON:
                return 100
            case LeadStage.LOST:
                return 0

    @property
    def is_open(self) -> bool:
        if self.default_probability == 100 or self.default_probability == 0:
            return False
        else:
            return True


# ════════════════════════════════════════════════════════════════════════════
# CRM-02 · Contacts & domains                  Concept: comprehensions & unpacking
# ════════════════════════════════════════════════════════════════════════════
# 1. split_contact_name(full_name): (first word, last word) of a contact name,
#    ignoring extra spaces. Use extended unpacking (`first, *rest = ...`). A
#    single-word name gives (name, ""). An empty or blank name must raise ValueError.
#        split_contact_name("Jean-Marc  de la Fontaine")  → ("Jean-Marc", "Fontaine")
#        split_contact_name("Cher")                       → ("Cher", "")
# 2. email_domains(leads): the set of e-mail domains (the part after "@"), in
#    lowercase, as ONE set comprehension. Ignore the leads whose e-mail does not
#    contain "@".
#        email_domains(load_leads()) contains "northwind.eu" and "helio-energy.com"
#
# 📚 Discover: https://peps.python.org/pep-3132/  (extended iterable unpacking)
#             https://docs.python.org/3/tutorial/datastructures.html#sets  (set comprehensions)
#             https://docs.python.org/3/library/stdtypes.html#str.partition
# ⏱ ~20 min
def split_contact_name(full_name: str) -> tuple[str, str]:
    todo("CRM-02")


def email_domains(leads: list[Lead]) -> set[str]:
    todo("CRM-02")


# ════════════════════════════════════════════════════════════════════════════
# CRM-03 · CSV import & weighted pipeline      Concept: map / filter / zip / key
# ════════════════════════════════════════════════════════════════════════════
# 1. row_to_dict(headers, row): like the Odoo import wizard, turn a CSV row into
#    {header: value}, with surrounding spaces removed from every value
#    (use map with str.strip). Headers and row must have the same length,
#    otherwise ValueError: find the right parameter of zip().
#        row_to_dict(["id", "company"], [" 7", "Helio Energy "])  → {"id": "7", "company": "Helio Energy"}
# 2. weighted_pipeline(leads): for every lead whose stage is not in FINAL_STAGES,
#    (company, expected_revenue × probability / 100), with the weighted amount
#    rounded to 2 decimals. Sort by weighted amount (largest first), then by
#    company (alphabetical). Use filter(), map() and sorted() with a key.
#
# 📚 Discover: https://docs.python.org/3/library/functions.html#zip
#             https://docs.python.org/3/library/functions.html#map
#             https://docs.python.org/3/howto/sorting.html#key-functions
# ⏱ ~20 min
def row_to_dict(headers: list[str], row: list[str]) -> dict[str, str]:
    todo("CRM-03")


def weighted_pipeline(leads: list[Lead]) -> list[tuple[str, float]]:
    todo("CRM-03")


# ════════════════════════════════════════════════════════════════════════════
# CRM-04 · Lead streams                                    Concept: generators
# ════════════════════════════════════════════════════════════════════════════
# Leads arrive from several sources (web form, trade show, imports). We process
# them as streams, without building intermediate lists.
#
# 1. valid_leads(leads) is a GENERATOR (it uses `yield`) that yields only the
#    leads with a usable e-mail: exactly one "@", something before it, and a "."
#    somewhere after it. "tom@atelierpeeters", "" and "claire@@wavre.be" are rejected.
# 2. all_leads(*sources) is a GENERATOR that yields every lead of the first
#    source, then of the second one, etc. Use `yield from`.
#
#    list(all_leads([lead1], [], [lead2, lead3]))  → [lead1, lead2, lead3]
#
# 📚 Discover: https://docs.python.org/3/howto/functional.html#generators
#             https://docs.python.org/3/whatsnew/3.3.html#pep-380  (yield from)
# ⏱ ~20 min
def valid_leads(leads: Iterable[Lead]):
    todo("CRM-04")


def all_leads(*sources: Iterable[Lead]):
    todo("CRM-04")


# ════════════════════════════════════════════════════════════════════════════
# CRM-05 · Team activity & duplicates                      Concept: collections
# ════════════════════════════════════════════════════════════════════════════
# 1. leads_per_salesperson(leads): [(salesperson, number of leads)], most leads
#    first, ties in order of first appearance. Use a Counter.
# 2. companies_with_multiple_leads(leads): {company: [lead ids]} for the companies
#    (exact name) that have at least two leads, ids in input order. Group the
#    ids with a defaultdict, then keep the groups of size >= 2.
#        companies_with_multiple_leads(load_leads())
#        → {"Brightside Dental": [2, 7, 14], "Northwind Logistics": [4, 9]}
#    (Notice "Lumen Consulting" and "Lumen Consulting SA": task CRM-08 deals with them.)
#
# 📚 Discover: https://docs.python.org/3/library/collections.html  (Counter, defaultdict)
# ⏱ ~20 min
def leads_per_salesperson(leads: list[Lead]) -> list[tuple[str, int]]:
    todo("CRM-05")


def companies_with_multiple_leads(leads: list[Lead]) -> dict[str, list[int]]:
    todo("CRM-05")


# ════════════════════════════════════════════════════════════════════════════
# CRM-06 · Round robin & monthly leads                       Concept: itertools
# ════════════════════════════════════════════════════════════════════════════
# 1. assign_round_robin(lead_ids, salespeople): Odoo CRM can assign new leads to
#    salespeople in turn. Return {lead_id: salesperson}: the first lead goes to
#    the first salesperson, the second to the second one... and back to the first
#    one after the last. Use itertools.cycle with zip(). An empty team must raise
#    ValueError (try zip + cycle with an empty team: what would you get silently?).
#        assign_round_robin([21, 22, 23], ["lea", "karim"])  → {21: "lea", 22: "karim", 23: "lea"}
# 2. leads_per_month(leads): [("YYYY-MM", number of leads)] in date order. The
#    leads are sorted by creation date: group consecutive leads of the same month.
#        leads_per_month(load_leads())  → [("2026-01", 3), ("2026-02", 5), ("2026-03", 6)]
#
# 📚 Discover: https://docs.python.org/3/library/itertools.html  (cycle, groupby)
# ⏱ ~25 min
def assign_round_robin(lead_ids: list[int], salespeople: list[str]) -> dict[int, str]:
    todo("CRM-06")


def leads_per_month(leads: list[Lead]) -> list[tuple[str, int]]:
    todo("CRM-06")


# ════════════════════════════════════════════════════════════════════════════
# CRM-07 · Top opportunities & temperature              Concept: heapq & bisect
# ════════════════════════════════════════════════════════════════════════════
# 1. top_opportunities(leads, k): ids of the k leads with the highest
#    expected_revenue among the leads whose stage is not in FINAL_STAGES,
#    highest first. Do not sort everything: use heapq.
# 2. temperature(score): the label of a lead score from 0 to 100, with the
#    breakpoints below. A score equal to a breakpoint belongs to the upper label
#    (40 → "warm"). No if/elif chain: use bisect.
#
#    SCORE_BREAKPOINTS = [40, 70]  →  "cold" | "warm" | "hot"
#
# 📚 Discover: https://docs.python.org/3/library/heapq.html  (nlargest)
#             https://docs.python.org/3/library/bisect.html (read the "grade" example)
# ⏱ ~20 min
SCORE_BREAKPOINTS = [40, 70]
TEMPERATURES = ["cold", "warm", "hot"]


def top_opportunities(leads: list[Lead], k: int) -> list[int]:
    todo("CRM-07")


def temperature(score: int) -> str:
    todo("CRM-07")


# ════════════════════════════════════════════════════════════════════════════
# CRM-08 · Company keys & won revenue                       Concept: functools
# ════════════════════════════════════════════════════════════════════════════
# 1. company_key(name): a normalised key to detect duplicate companies:
#    lowercase, remove "." and ",", drop the words that are legal forms
#    (LEGAL_FORMS), and join the remaining words with single spaces.
#        company_key("Lumen Consulting SA")   → "lumen consulting"
#        company_key("Studio Kaleido B.V.")   → "studio kaleido"
#    The same company names come back thousands of times during an import: make
#    sure each name is computed only once (the tests check cache_info()).
# 2. total_won(leads): sum of expected_revenue of the "won" leads, using
#    functools.reduce (sum() would work: the goal is to discover reduce).
#        total_won(load_leads())  → 26900.0
#
# 📚 Discover: https://docs.python.org/3/library/functools.html  (cache, reduce)
# ⏱ ~20 min
LEGAL_FORMS = {"sa", "srl", "sprl", "bv", "nv", "ltd", "inc", "gmbh"}


def company_key(name: str) -> str:
    todo("CRM-08")


def total_won(leads: list[Lead]) -> float:
    todo("CRM-08")


# ════════════════════════════════════════════════════════════════════════════
# CRM-B2 · BONUS · Import session                Concept: generator-based context manager
# ════════════════════════════════════════════════════════════════════════════
# An import must be all-or-nothing. Write import_session(journal) as a context
# manager, using the @contextlib.contextmanager decorator on a generator:
#   * on entry, append "begin" to the journal;
#   * if the block ends normally, append "commit";
#   * if the block raises an exception, append "rollback" and let the exception
#     propagate (do not swallow it).
#
#    journal = []
#    with import_session(journal):
#        journal.append("row 1")
#    journal  → ["begin", "row 1", "commit"]
#
# 📚 Discover: https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager
# ⏱ ~15 min
def import_session(journal: list[str]):
    todo("CRM-B2")
