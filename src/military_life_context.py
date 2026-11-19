
from dataclasses import dataclass


@dataclass
class MilitaryLifeContext:
    """Trusted context supplied by the authenticated application."""

    household_id: str
    access_token: str
