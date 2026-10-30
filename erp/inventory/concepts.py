"""INVENTORY — concept tasks (Member A).

How it works
------------
* Each task is a function (or class) containing a `todo("INV-xx")` line.
  Replace that line with your implementation.
* Read the "Discover" links: today's goal is to learn these tools on your own.
* Check your progress with `python -m erp inventory`, and run your code on the
  real data with `python -m erp demo inventory`.
* Commit after each task: git commit -m "INV-03: physical count differences".

You may add helper functions and imports. Do not rename the existing functions:
the tests use these names.
"""

from __future__ import annotations

from datetime import date
from symtable import Class

from erp.common.todo import todo
from erp.inventory.data import load_products
from erp.inventory.models import Product, StockMove

from enum import StrEnum


# Add the imports you need here (collections, itertools, functools, heapq, bisect...).


# ════════════════════════════════════════════════════════════════════════════
# INV-01 · Move types                                Concept: Enum (+ match/case)
# ════════════════════════════════════════════════════════════════════════════
# The `move_type` column of stock_moves.csv contains plain strings. A typo such as
# "delivry" would silently be ignored by `if move_type == "delivery"`. An Enum
# lists every allowed value once and fails loudly on unknown values.
#
# 1. Declare the members of MoveType. Their values must be exactly the strings
#    used in the data: RECEIPT = "receipt", DELIVERY = "delivery",
#    ADJUSTMENT = "adjustment".
# 2. Implement the `sign` property with a `match` statement:
#    RECEIPT → +1 (goods come in), DELIVERY → -1 (goods go out),
#    ADJUSTMENT → +1 (the quantity of an adjustment is already signed).
# 3. Implement signed_quantity(move): the quantity with the sign of its type.
#
#    MoveType("delivery") is MoveType.DELIVERY            → True
#    MoveType.DELIVERY.sign                               → -1
#    signed_quantity(StockMove(day, "FURN-001", "delivery", 8))   → -8
#    MoveType("delivry")                                  → ValueError
#
# 📚 Discover: https://docs.python.org/3/library/enum.html  (StrEnum, iteration over members)
#             https://docs.python.org/3/tutorial/controlflow.html#match-statements
# ⏱ ~25 min
class MoveType(StrEnum):
    """Type of a stock move."""

    RECEIPT = "receipt"
    DELIVERY = "delivery"
    ADJUSTMENT = "adjustment"

    @property
    def sign(self) -> int:
        match self:
            case MoveType.RECEIPT | MoveType.ADJUSTMENT:
                return 1
            case MoveType.DELIVERY:
                return -1


def signed_quantity(move: StockMove) -> int:
    return MoveType(move.move_type).sign * move.quantity


# ════════════════════════════════════════════════════════════════════════════
# INV-02 · Catalog index                     Concept: comprehensions & unpacking
# ════════════════════════════════════════════════════════════════════════════
# 1. index_by_sku(products): a dict {sku: product}, written as ONE dict comprehension.
# 2. categories(products): the set of categories, written as ONE set comprehension.
# 3. cheapest_first(products): a tuple (cheapest product, list of the other
#    products sorted by unit cost). Sort once, then split the result with
#    extended unpacking (`first, *rest = ...`). An empty list must raise
#    ValueError (unpacking does it for you).
#
#    categories(load_products())   → {"Seating", "Desks", "Storage", "Accessories"}
#
# 📚 Discover: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
#             (read the dict/set comprehension parts too)
#             https://peps.python.org/pep-3132/  (extended iterable unpacking)
# ⏱ ~20 min
def index_by_sku(products: list[Product]) -> dict[str, Product]:
    return {i.sku:i for i in products}


def categories(products: list[Product]) -> set[str]:
    return {i.category for i in products}


def cheapest_first(products: list[Product]) -> tuple[Product, list[Product]]:
    products.sort(key=lambda x:x.unit_cost)
    cheapest, *rest = products
    return cheapest,rest


# ════════════════════════════════════════════════════════════════════════════
# INV-03 · Physical count differences          Concept: map / filter / zip / key
# ════════════════════════════════════════════════════════════════════════════
# Once a month, the warehouse team counts the products on the shelves. The scanner
# returns two parallel lists: the SKUs and the counted quantities.
#
# Return the list of (sku, difference) where difference = counted - theoretical,
# using theoretical.get(sku, 0) when the SKU is unknown.
# * Keep only non-zero differences.
# * Sort by absolute difference (largest first), then by SKU (alphabetical).
# * The two lists must have the same length: when they don't, a ValueError must be
#   raised. zip() can do this for you, so find the right parameter.
# * Use zip(), filter() (or map()) and sorted() with a key. No index loop.
#
#    count_differences(["A", "B", "C"], [5, 2, 7], {"A": 5, "B": 4, "C": 3})
#    → [("C", 4), ("B", -2)]
#
# 📚 Discover: https://docs.python.org/3/library/functions.html#zip
#             https://docs.python.org/3/library/functions.html#filter
#             https://docs.python.org/3/howto/sorting.html#key-functions
# ⏱ ~20 min
def count_differences(skus: list[str], counted: list[int], theoretical: dict[str, int]) -> list[tuple[str, int]]:
    todo("INV-03")


# ════════════════════════════════════════════════════════════════════════════
# INV-04 · Stock level over time                Concept: generators (needs INV-01)
# ════════════════════════════════════════════════════════════════════════════
# A warehouse may record millions of moves: we don't want to build a full list of
# stock levels in memory. A generator produces the values one at a time.
#
# 1. running_stock(moves, sku, initial=0) is a GENERATOR (it uses `yield`): for
#    each move of `sku`, in input order, it yields (day, stock level after the move).
#    Use signed_quantity() from INV-01.
# 2. first_day_below(moves, sku, threshold, initial=0): the first day on which
#    the stock level of `sku` is strictly below `threshold`, or None.
#    One line: next() on a generator expression built from running_stock().
#
#    moves: (03-02, "A", receipt, 10), (03-03, "B", receipt, 4), (03-04, "A", delivery, 7)
#    list(running_stock(moves, "A"))      → [(date(2026, 3, 2), 10), (date(2026, 3, 4), 3)]
#    first_day_below(moves, "A", 5)       → date(2026, 3, 4)
#
# 📚 Discover: https://docs.python.org/3/howto/functional.html#generators
#             https://docs.python.org/3/library/functions.html#next  (the `default` argument)
# ⏱ ~25 min
def running_stock(moves: list[StockMove], sku: str, initial: int = 0):
    todo("INV-04")


def first_day_below(moves: list[StockMove], sku: str, threshold: int, initial: int = 0) -> date | None:
    todo("INV-04")


# ════════════════════════════════════════════════════════════════════════════
# INV-05 · Stock on hand & activity                   Concept: collections
# ════════════════════════════════════════════════════════════════════════════
# 1. stock_on_hand(moves): {sku: current stock} computed from every move (all
#    stocks start at 0). Use a defaultdict or a Counter, plus signed_quantity()
#    from INV-01.
# 2. most_active_skus(moves, k): the k SKUs with the most moves, as
#    (sku, number of moves), most active first. Ties keep the order in which the
#    SKUs first appear. One Counter method does all the work.
#
#    most_active_skus(load_stock_moves(), 1)   → [("FURN-001", 7)]
#
# 📚 Discover: https://docs.python.org/3/library/collections.html  (Counter, defaultdict)
# ⏱ ~20 min
def stock_on_hand(moves: list[StockMove]) -> dict[str, int]:
    todo("INV-05")


def most_active_skus(moves: list[StockMove], k: int) -> list[tuple[str, int]]:
    todo("INV-05")


# ════════════════════════════════════════════════════════════════════════════
# INV-06 · Locations & daily activity                  Concept: itertools
# ════════════════════════════════════════════════════════════════════════════
# 1. location_codes(aisles, racks, levels): every storage location code, in order,
#    formatted "<aisle>-<rack on 2 digits>-<level>". Racks and levels start at 1.
#    No nested loops: one itertools function builds every combination.
#        location_codes("AB", 2, 2)
#        → ["A-01-1", "A-01-2", "A-02-1", "A-02-2", "B-01-1", "B-01-2", "B-02-1", "B-02-2"]
# 2. moves_per_day(moves): [(day, number of moves that day)] in date order. The
#    moves are already sorted by date: group consecutive moves of the same day.
#        moves_per_day(load_stock_moves())[:2]
#        → [(date(2026, 3, 2), 3), (date(2026, 3, 3), 2)]
#
# 📚 Discover: https://docs.python.org/3/library/itertools.html  (product, groupby)
# ⏱ ~25 min
def location_codes(aisles: str, racks: int, levels: int) -> list[str]:
    todo("INV-06")


def moves_per_day(moves: list[StockMove]) -> list[tuple[date, int]]:
    todo("INV-06")


# ════════════════════════════════════════════════════════════════════════════
# INV-07 · Reorder shortlist & price tiers               Concept: heapq & bisect
# ════════════════════════════════════════════════════════════════════════════
# 1. reorder_shortlist(products, on_hand, k): the SKUs of the k products with the
#    largest shortage, largest first. shortage = reorder_point - on_hand.get(sku, 0).
#    Only products with a shortage > 0 are candidates. Ties keep the catalog order.
#    Do not sort the whole catalog: use heapq.
# 2. price_tier(unit_cost): the tier of a price with the breakpoints below. A price
#    equal to a breakpoint belongs to the upper tier (50.0 → "standard").
#    No if/elif chain: use bisect.
#
#    PRICE_BREAKPOINTS = [50, 150, 400]  →  "budget" | "standard" | "premium" | "luxury"
#    price_tier(19.9) → "budget"    price_tier(150) → "premium"    price_tier(540) → "luxury"
#
# 📚 Discover: https://docs.python.org/3/library/heapq.html  (nlargest, nsmallest)
#             https://docs.python.org/3/library/bisect.html (read the "grade" example)
# ⏱ ~25 min
PRICE_BREAKPOINTS = [50, 150, 400]
PRICE_TIERS = ["budget", "standard", "premium", "luxury"]


def reorder_shortlist(products: list[Product], on_hand: dict[str, int], k: int) -> list[str]:
    todo("INV-07")


def price_tier(unit_cost: float) -> str:
    todo("INV-07")


# ════════════════════════════════════════════════════════════════════════════
# INV-08 · Product lookup & valuation                    Concept: functools
# ════════════════════════════════════════════════════════════════════════════
# 1. find_product(sku): the Product with this SKU (loaded with load_products()),
#    or None. Reading the CSV file on every call is wasteful: decorate the
#    function so that each SKU is computed only once. The tests check
#    find_product.cache_info().
# 2. inventory_value(products, on_hand): total value of the stock,
#    sum of unit_cost × on_hand.get(sku, 0), rounded to 2 decimals.
#    Use functools.reduce (yes, sum() would work: the goal is to discover reduce).
#
#    inventory_value([Product("A", "x", "c", 10.0, 1), Product("B", "y", "c", 2.5, 1)], {"A": 3, "B": 2})
#    → 35.0
#
# 📚 Discover: https://docs.python.org/3/library/functools.html  (cache, reduce)
# ⏱ ~20 min
def find_product(sku: str) -> Product | None:
    todo("INV-08")


def inventory_value(products: list[Product], on_hand: dict[str, int]) -> float:
    todo("INV-08")


# ════════════════════════════════════════════════════════════════════════════
# INV-B2 · BONUS · Stock report                    Concept: f-string format spec
# ════════════════════════════════════════════════════════════════════════════
# Return the stock report as one string, one line per product (catalog order),
# lines separated by "\n", no trailing newline. Each line is:
#   * the SKU left-aligned on 10 characters,
#   * the name left-aligned on 18 characters,
#   * the quantity on hand right-aligned on 5 characters, then " u",
#   * the stock value (unit_cost × quantity) right-aligned on 12 characters, with a
#     thousands separator and 2 decimals, then " €".
# Everything must be done with format specs inside f-strings (no ljust/rjust).
#
#    "FURN-011  Standing Desk         2 u    1,080.00 €"
#
# 📚 Discover: https://docs.python.org/3/library/string.html#format-specification-mini-language
# ⏱ ~15 min
def stock_report(products: list[Product], on_hand: dict[str, int]) -> str:
    todo("INV-B2")
