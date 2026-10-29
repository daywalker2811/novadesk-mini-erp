"""Tests of the inventory module (Member A). Do not edit.

Run them all:        python -m unittest tests.test_inventory -v
Run one task only:   python -m unittest tests.test_inventory -k inv03 -v
"""

import types
import unittest
from datetime import date

from erp.common.todo import require, require_enum
from erp.inventory import algorithms as algo
from erp.inventory import concepts as c
from erp.inventory.data import load_products, load_stock_moves, load_warehouse_map
from erp.inventory.models import Product, StockMove


def move(day: int, sku: str, move_type: str, quantity: int) -> StockMove:
    return StockMove(date(2026, 3, day), sku, move_type, quantity)


MOVES = [move(2, "A", "receipt", 10), move(3, "B", "receipt", 4), move(4, "A", "delivery", 7),
         move(5, "A", "adjustment", -1), move(6, "B", "delivery", 4), move(9, "A", "receipt", 6)]


def product(sku: str, cost: float = 10.0, reorder_point: int = 5, category: str = "Desks") -> Product:
    return Product(sku, f"Product {sku}", category, cost, reorder_point)


class TestInv01MoveTypes(unittest.TestCase):
    def setUp(self):
        require_enum(c.MoveType, "INV-01")

    def test_inv01_members_match_the_data(self):
        self.assertEqual([m.value for m in c.MoveType], ["receipt", "delivery", "adjustment"])
        self.assertIs(c.MoveType("delivery"), c.MoveType.DELIVERY)
        self.assertEqual(c.MoveType.RECEIPT, "receipt")  # a StrEnum compares equal to its value

    def test_inv01_unknown_value_is_rejected(self):
        with self.assertRaises(ValueError):
            c.MoveType("delivry")

    def test_inv01_sign(self):
        self.assertEqual(c.MoveType.RECEIPT.sign, 1)
        self.assertEqual(c.MoveType.DELIVERY.sign, -1)
        self.assertEqual(c.MoveType.ADJUSTMENT.sign, 1)

    def test_inv01_signed_quantity(self):
        self.assertEqual(c.signed_quantity(move(2, "A", "receipt", 10)), 10)
        self.assertEqual(c.signed_quantity(move(2, "A", "delivery", 8)), -8)
        self.assertEqual(c.signed_quantity(move(2, "A", "adjustment", -1)), -1)


class TestInv02CatalogIndex(unittest.TestCase):
    def test_inv02_index_by_sku(self):
        products = [product("A"), product("B")]
        self.assertEqual(c.index_by_sku(products), {"A": products[0], "B": products[1]})

    def test_inv02_categories(self):
        self.assertEqual(c.categories(load_products()), {"Seating", "Desks", "Storage", "Accessories"})

    def test_inv02_cheapest_first(self):
        a, b, d = product("A", 30.0), product("B", 10.0), product("D", 20.0)
        self.assertEqual(c.cheapest_first([a, b, d]), (b, [d, a]))
        self.assertEqual(c.cheapest_first([a]), (a, []))
        with self.assertRaises(ValueError):
            c.cheapest_first([])


class TestInv03CountDifferences(unittest.TestCase):
    def test_inv03_example(self):
        self.assertEqual(c.count_differences(["A", "B", "C"], [5, 2, 7], {"A": 5, "B": 4, "C": 3}),
                         [("C", 4), ("B", -2)])

    def test_inv03_unknown_sku_and_ties(self):
        result = c.count_differences(["Z", "B", "A"], [3, 1, 2], {"A": 5, "B": 4})
        self.assertEqual(result, [("A", -3), ("B", -3), ("Z", 3)])

    def test_inv03_lengths_must_match(self):
        with self.assertRaises(ValueError):
            c.count_differences(["A", "B"], [1], {})


class TestInv04RunningStock(unittest.TestCase):
    def setUp(self):
        require_enum(c.MoveType, "INV-01")

    def test_inv04_is_a_generator(self):
        self.assertIsInstance(c.running_stock(MOVES, "A"), types.GeneratorType)

    def test_inv04_running_stock(self):
        self.assertEqual(list(c.running_stock(MOVES, "A")),
                         [(date(2026, 3, 2), 10), (date(2026, 3, 4), 3), (date(2026, 3, 5), 2), (date(2026, 3, 9), 8)])
        self.assertEqual(list(c.running_stock(MOVES, "B", initial=1)), [(date(2026, 3, 3), 5), (date(2026, 3, 6), 1)])
        self.assertEqual(list(c.running_stock(MOVES, "Z")), [])

    def test_inv04_first_day_below(self):
        self.assertEqual(c.first_day_below(MOVES, "A", 5), date(2026, 3, 4))
        self.assertIsNone(c.first_day_below(MOVES, "A", 2))
        self.assertEqual(c.first_day_below(load_stock_moves(), "FURN-001", 5), date(2026, 3, 9))


class TestInv05Collections(unittest.TestCase):
    def test_inv05_stock_on_hand(self):
        require_enum(c.MoveType, "INV-01")
        self.assertEqual(dict(c.stock_on_hand(MOVES)), {"A": 8, "B": 0})
        stock = c.stock_on_hand(load_stock_moves())
        self.assertEqual(stock["FURN-001"], 8)
        self.assertEqual(stock["ACC-101"], 18)

    def test_inv05_most_active_skus(self):
        self.assertEqual(c.most_active_skus(MOVES, 1), [("A", 4)])
        self.assertEqual(c.most_active_skus(MOVES, 5), [("A", 4), ("B", 2)])
        self.assertEqual(c.most_active_skus(load_stock_moves(), 1), [("FURN-001", 7)])


class TestInv06Itertools(unittest.TestCase):
    def test_inv06_location_codes(self):
        self.assertEqual(c.location_codes("AB", 2, 2),
                         ["A-01-1", "A-01-2", "A-02-1", "A-02-2", "B-01-1", "B-01-2", "B-02-1", "B-02-2"])
        self.assertEqual(len(c.location_codes("ABC", 12, 4)), 144)
        self.assertEqual(c.location_codes("C", 12, 4)[-1], "C-12-4")

    def test_inv06_moves_per_day(self):
        self.assertEqual(c.moves_per_day(MOVES)[:2], [(date(2026, 3, 2), 1), (date(2026, 3, 3), 1)])
        real = c.moves_per_day(load_stock_moves())
        self.assertEqual(real[:2], [(date(2026, 3, 2), 3), (date(2026, 3, 3), 2)])
        self.assertEqual(sum(n for _, n in real), 30)
        self.assertEqual(c.moves_per_day([]), [])


class TestInv07HeapBisect(unittest.TestCase):
    def test_inv07_reorder_shortlist(self):
        products = [product("A", reorder_point=10), product("B", reorder_point=4),
                    product("C", reorder_point=8), product("D", reorder_point=6)]
        on_hand = {"A": 2, "B": 9, "C": 3, "D": 1}  # shortages: A 8, B -5, C 5, D 5
        self.assertEqual(c.reorder_shortlist(products, on_hand, 2), ["A", "C"])
        self.assertEqual(c.reorder_shortlist(products, on_hand, 10), ["A", "C", "D"])
        self.assertEqual(c.reorder_shortlist(products, {}, 1), ["A"])

    def test_inv07_price_tier(self):
        self.assertEqual(c.price_tier(19.9), "budget")
        self.assertEqual(c.price_tier(50), "standard")
        self.assertEqual(c.price_tier(149.99), "standard")
        self.assertEqual(c.price_tier(150), "premium")
        self.assertEqual(c.price_tier(540), "luxury")


class TestInv08Functools(unittest.TestCase):
    def test_inv08_find_product_is_cached(self):
        c.find_product("FURN-011")  # reports "to do" while the task is not started
        self.assertTrue(hasattr(c.find_product, "cache_info"),
                        "find_product must be decorated with a functools cache decorator")
        c.find_product.cache_clear()
        self.assertEqual(c.find_product("FURN-011").name, "Standing Desk")
        self.assertEqual(c.find_product("FURN-011").name, "Standing Desk")
        self.assertIsNone(c.find_product("NOPE"))
        info = c.find_product.cache_info()
        self.assertEqual((info.hits, info.misses), (1, 2))

    def test_inv08_inventory_value(self):
        products = [Product("A", "x", "c", 10.0, 1), Product("B", "y", "c", 2.5, 1), Product("C", "z", "c", 99.0, 1)]
        self.assertEqual(c.inventory_value(products, {"A": 3, "B": 2}), 35.0)
        self.assertEqual(c.inventory_value([], {}), 0)


class TestInvA1NetMovement(unittest.TestCase):
    def test_inva1_example(self):
        self.assertEqual(algo.net_movement_between([5, -2, 7, 0, -4, 3], [(0, 2), (1, 4), (3, 3), (0, 5)]),
                         [10, 1, 0, 9])

    def test_inva1_edge_cases(self):
        self.assertEqual(algo.net_movement_between([4], [(0, 0)]), [4])
        self.assertEqual(algo.net_movement_between([1, 2, 3], []), [])

    def test_inva1_large_input(self):
        days = [(i % 7) - 3 for i in range(20_000)]
        queries = [(i, 19_999) for i in range(0, 20_000, 10)]
        result = algo.net_movement_between(days, queries)
        self.assertEqual(result[0], sum(days))
        self.assertEqual(result[-1], sum(days[19_990:]))


class TestInvA2PickingRoute(unittest.TestCase):
    def test_inva2_examples(self):
        self.assertEqual(algo.shortest_pick_path(["D.#", ".##", "..P"]), 4)
        self.assertEqual(algo.shortest_pick_path(["D#P"]), -1)
        self.assertEqual(algo.shortest_pick_path(["DP"]), 1)

    def test_inva2_takes_the_shortest_of_several_routes(self):
        grid = ["D....",
                ".###.",
                ".....",
                "###.P"]
        self.assertEqual(algo.shortest_pick_path(grid), 7)

    def test_inva2_real_warehouse(self):
        self.assertEqual(algo.shortest_pick_path(load_warehouse_map()), 14)


class TestInvB1Packages(unittest.TestCase):
    def test_invb1_examples(self):
        self.assertEqual(algo.min_packages(12, [4, 6, 9]), 2)
        self.assertEqual(algo.min_packages(17, [4, 6, 9]), 3)
        self.assertEqual(algo.min_packages(5, [4, 6, 9]), -1)
        self.assertEqual(algo.min_packages(0, [4, 6, 9]), 0)

    def test_invb1_biggest_first_is_not_enough(self):
        self.assertEqual(algo.min_packages(12, [1, 6, 9]), 2)
        self.assertEqual(algo.min_packages(30, [1, 10, 25]), 3)


class TestInvB2StockReport(unittest.TestCase):
    def test_invb2_format(self):
        products = [Product("FURN-011", "Standing Desk", "Desks", 540.0, 3),
                    Product("ACC-102", "Cable Tray", "Accessories", 19.9, 25)]
        expected = ("FURN-011  Standing Desk         2 u    1,080.00 €\n"
                    "ACC-102   Cable Tray           22 u      437.80 €")
        self.assertEqual(c.stock_report(products, {"FURN-011": 2, "ACC-102": 22}), expected)


if __name__ == "__main__":
    unittest.main()
