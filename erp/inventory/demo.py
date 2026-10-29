"""Demo of the inventory tasks on the real data (python -m erp demo inventory)."""

from erp.common.todo import require_enum
from erp.inventory import algorithms as algo
from erp.inventory import concepts as c
from erp.inventory.data import load_daily_net, load_products, load_stock_moves, load_warehouse_map


def steps():
    products = load_products()
    moves = load_stock_moves()
    return [
        ("INV-01", "move types", lambda: require_enum(c.MoveType, "INV-01") or [m.value for m in c.MoveType]),
        ("INV-02", "categories", lambda: sorted(c.categories(products))),
        ("INV-02", "cheapest product", lambda: c.cheapest_first(products)[0].name),
        ("INV-03", "count differences", lambda: c.count_differences(
            ["FURN-001", "ACC-100", "FURN-021"], [7, 18, 4], c.stock_on_hand(moves))),
        ("INV-04", "Office Chair under 5", lambda: c.first_day_below(moves, "FURN-001", 5)),
        ("INV-05", "stock on hand", lambda: c.stock_on_hand(moves)),
        ("INV-05", "most active SKUs", lambda: c.most_active_skus(moves, 3)),
        ("INV-06", "locations in aisle A", lambda: c.location_codes("A", 2, 3)),
        ("INV-06", "moves per day", lambda: c.moves_per_day(moves)),
        ("INV-07", "reorder shortlist", lambda: c.reorder_shortlist(products, c.stock_on_hand(moves), 5)),
        ("INV-07", "price tiers", lambda: {p.name: c.price_tier(p.unit_cost) for p in products}),
        ("INV-08", "inventory value", lambda: c.inventory_value(products, c.stock_on_hand(moves))),
        ("INV-A1", "net movement, first and second week", lambda: algo.net_movement_between(load_daily_net(), [(0, 4), (5, 9)])),
        ("INV-A2", "moves from dock to picking spot", lambda: algo.shortest_pick_path(load_warehouse_map())),
        ("INV-B1", "packages for 23 units", lambda: algo.min_packages(23, [4, 6, 9])),
        ("INV-B2", "stock report", lambda: "\n" + c.stock_report(products, c.stock_on_hand(moves))),
    ]
