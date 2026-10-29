"""Loaders for the data/crm folder (ready to use, nothing to edit)."""

import csv
from datetime import date

from erp.common.paths import DATA_DIR
from erp.crm.models import Lead

FOLDER = DATA_DIR / "crm"


def load_leads() -> list[Lead]:
    """Leads sorted by creation date."""
    with open(FOLDER / "leads.csv", newline="", encoding="utf-8") as file:
        return [
            Lead(int(r["id"]), r["contact"], r["company"], r["email"], r["stage"], float(r["expected_revenue"]),
                 int(r["probability"]), r["salesperson"], date.fromisoformat(r["created"]))
            for r in csv.DictReader(file)
        ]


def load_lead_rows() -> tuple[list[str], list[list[str]]]:
    """Raw content of leads.csv: (headers, rows), every value as a string."""
    with open(FOLDER / "leads.csv", newline="", encoding="utf-8") as file:
        headers, *rows = list(csv.reader(file))
    return headers, rows


def load_monthly_margins() -> tuple[list[str], list[int]]:
    """(months, margins) of last year, e.g. (["2025-01", ...], [-1200, ...])."""
    with open(FOLDER / "monthly_margin.csv", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    return [r["month"] for r in rows], [int(r["margin"]) for r in rows]


def load_offers() -> list[tuple[str, int]]:
    """Catalogue offers as (offer_id, price in cents), sorted by price ascending."""
    with open(FOLDER / "offers.csv", newline="", encoding="utf-8") as file:
        return [(r["offer_id"], int(r["price_cents"])) for r in csv.DictReader(file)]


def template_names() -> list[str]:
    return sorted(path.stem for path in (FOLDER / "templates").glob("*.txt"))


def load_template(name: str) -> str:
    return (FOLDER / "templates" / f"{name}.txt").read_text(encoding="utf-8")
