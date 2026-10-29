"""Inventory data models (ready to use, nothing to edit)."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Product:
    sku: str              # unique reference, e.g. "FURN-001"
    name: str
    category: str         # Seating, Desks, Storage, Accessories
    unit_cost: float      # in euros
    reorder_point: int    # minimum stock before reordering (safety stock)


@dataclass(frozen=True)
class StockMove:
    day: date
    sku: str
    move_type: str        # "receipt", "delivery" or "adjustment"
    quantity: int         # always positive, except for adjustments (signed)
