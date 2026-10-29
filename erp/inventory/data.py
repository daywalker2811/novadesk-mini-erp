"""Loaders for the data/inventory folder (ready to use, nothing to edit)."""

import csv
from datetime import date

from erp.common.paths import DATA_DIR
from erp.inventory.models import Product, StockMove

FOLDER = DATA_DIR / "inventory"


def load_products() -> list[Product]:
    with open(FOLDER / "products.csv", newline="", encoding="utf-8") as file:
        return [
            Product(row["sku"], row["name"], row["category"], float(row["unit_cost"]), int(row["reorder_point"]))
            for row in csv.DictReader(file)
        ]


def load_stock_moves() -> list[StockMove]:
    """Stock moves sorted by date."""
    with open(FOLDER / "stock_moves.csv", newline="", encoding="utf-8") as file:
        return [
            StockMove(date.fromisoformat(row["date"]), row["sku"], row["move_type"], int(row["quantity"]))
            for row in csv.DictReader(file)
        ]


def load_daily_net() -> list[int]:
    """Net number of units moved per working day (receipts - deliveries ± adjustments)."""
    with open(FOLDER / "daily_net.csv", newline="", encoding="utf-8") as file:
        return [int(row["net_units"]) for row in csv.DictReader(file)]


def load_warehouse_map() -> list[str]:
    """Warehouse map, one string per row: '#' rack or wall, '.' aisle, 'D' dock, 'P' picking spot."""
    return (FOLDER / "warehouse_map.txt").read_text(encoding="utf-8").splitlines()
