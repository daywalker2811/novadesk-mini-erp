"""CRM data models (ready to use, nothing to edit)."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Lead:
    id: int
    contact: str              # "Jean Dupont"
    company: str
    email: str                # may be empty or invalid: it comes from a web form
    stage: str                # "new", "qualified", "proposition", "won" or "lost"
    expected_revenue: float   # in euros
    probability: int          # 0 to 100
    salesperson: str
    created: date
