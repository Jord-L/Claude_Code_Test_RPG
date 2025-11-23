"""
Ship System
Manages player's pirate ship, upgrades, and crew capacity.
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class ShipUpgrade:
    """Ship upgrade."""
    upgrade_id: str
    name: str
    description: str
    cost: int
    required_level: int = 1


class Ship:
    """Player's pirate ship."""

    def __init__(self, ship_name: str = "Going Merry"):
        """Initialize ship."""
        self.ship_name = ship_name
        self.ship_level = 1

        # Stats
        self.max_crew = 10  # Base party + reserve capacity
        self.speed = 1.0  # Travel speed multiplier
        self.storage = 50  # Extra inventory slots

        # Upgrades
        self.upgrades: List[str] = []

        # Health (for ship battles in future)
        self.max_hp = 1000
        self.current_hp = 1000

    def upgrade_capacity(self):
        """Upgrade crew capacity."""
        self.max_crew += 5
        self.upgrades.append("capacity_upgrade")

    def upgrade_storage(self):
        """Upgrade storage capacity."""
        self.storage += 25
        self.upgrades.append("storage_upgrade")

    def upgrade_speed(self):
        """Upgrade ship speed."""
        self.speed += 0.2
        self.upgrades.append("speed_upgrade")

    def repair(self, amount: int):
        """Repair ship damage."""
        self.current_hp = min(self.current_hp + amount, self.max_hp)

    def get_info(self) -> Dict:
        """Get ship information."""
        return {
            "name": self.ship_name,
            "level": self.ship_level,
            "max_crew": self.max_crew,
            "speed": self.speed,
            "storage": self.storage,
            "hp": f"{self.current_hp}/{self.max_hp}",
            "upgrades": len(self.upgrades)
        }


def create_ship_upgrades() -> Dict[str, ShipUpgrade]:
    """Create available ship upgrades."""
    upgrades = {}

    upgrades["crew_quarters"] = ShipUpgrade(
        "crew_quarters",
        "Expanded Crew Quarters",
        "Increase max crew capacity by 5",
        5000,
        5
    )

    upgrades["cargo_hold"] = ShipUpgrade(
        "cargo_hold",
        "Larger Cargo Hold",
        "Increase inventory space by 25 slots",
        10000,
        10
    )

    upgrades["better_sails"] = ShipUpgrade(
        "better_sails",
        "Improved Sails",
        "Increase travel speed by 20%",
        7500,
        7
    )

    upgrades["armored_hull"] = ShipUpgrade(
        "armored_hull",
        "Armored Hull",
        "Increase ship HP by 500",
        15000,
        15
    )

    return upgrades
