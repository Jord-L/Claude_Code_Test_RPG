"""
Extended Devil Fruit System
Expanded Devil Fruit abilities and progression.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class DevilFruitAbility:
    """Devil Fruit special ability."""
    ability_id: str
    name: str
    description: str
    ap_cost: int
    damage: int = 0
    healing: int = 0
    buff_type: Optional[str] = None
    buff_amount: int = 0
    required_level: int = 1


class DevilFruit:
    """Extended Devil Fruit with multiple abilities."""

    def __init__(self, fruit_id: str, name: str, fruit_type: str):
        """
        Initialize Devil Fruit.

        Args:
            fruit_id: Unique fruit ID
            name: Fruit name
            fruit_type: paramecia, zoan, or logia
        """
        self.fruit_id = fruit_id
        self.name = name
        self.fruit_type = fruit_type
        self.abilities: List[DevilFruitAbility] = []
        self.mastery_level = 1
        self.mastery_exp = 0

    def add_ability(self, ability: DevilFruitAbility):
        """Add ability to fruit."""
        self.abilities.append(ability)

    def get_available_abilities(self, character_level: int) -> List[DevilFruitAbility]:
        """Get abilities available at current level."""
        return [ab for ab in self.abilities if ab.required_level <= character_level]

    def gain_mastery(self, exp: int):
        """Gain mastery experience."""
        self.mastery_exp += exp
        while self.mastery_exp >= self.mastery_level * 100:
            self.mastery_exp -= self.mastery_level * 100
            self.mastery_level += 1
            print(f"Devil Fruit mastery increased to {self.mastery_level}!")


def create_extended_devil_fruits() -> Dict[str, DevilFruit]:
    """Create extended Devil Fruit database."""
    fruits = {}

    # Gomu Gomu no Mi (Rubber)
    gomu_gomu = DevilFruit("gomu_gomu", "Gomu Gomu no Mi", "paramecia")

    gomu_gomu.add_ability(DevilFruitAbility(
        "gomu_pistol",
        "Gomu Gomu no Pistol",
        "Stretch arm to punch enemy",
        10,
        damage=50,
        required_level=1
    ))

    gomu_gomu.add_ability(DevilFruitAbility(
        "gomu_bazooka",
        "Gomu Gomu no Bazooka",
        "Two-handed powerful strike",
        25,
        damage=120,
        required_level=5
    ))

    gomu_gomu.add_ability(DevilFruitAbility(
        "gomu_gatling",
        "Gomu Gomu no Gatling",
        "Rapid-fire punches",
        40,
        damage=200,
        required_level=10
    ))

    gomu_gomu.add_ability(DevilFruitAbility(
        "gear_second",
        "Gear Second",
        "Increase speed and power",
        50,
        buff_type="speed",
        buff_amount=30,
        required_level=15
    ))

    fruits["gomu_gomu"] = gomu_gomu

    # Mera Mera no Mi (Fire)
    mera_mera = DevilFruit("mera_mera", "Mera Mera no Mi", "logia")

    mera_mera.add_ability(DevilFruitAbility(
        "fire_fist",
        "Fire Fist",
        "Launch flaming punch",
        15,
        damage=60,
        required_level=1
    ))

    mera_mera.add_ability(DevilFruitAbility(
        "fire_pillar",
        "Flame Pillar",
        "Create pillar of flames",
        35,
        damage=150,
        required_level=8
    ))

    fruits["mera_mera"] = mera_mera

    # Hie Hie no Mi (Ice)
    hie_hie = DevilFruit("hie_hie", "Hie Hie no Mi", "logia")

    hie_hie.add_ability(DevilFruitAbility(
        "ice_saber",
        "Ice Saber",
        "Create ice weapon",
        20,
        damage=70,
        required_level=1
    ))

    hie_hie.add_ability(DevilFruitAbility(
        "ice_age",
        "Ice Age",
        "Freeze everything around",
        50,
        damage=180,
        required_level=12
    ))

    fruits["hie_hie"] = hie_hie

    # Ope Ope no Mi (Operation)
    ope_ope = DevilFruit("ope_ope", "Ope Ope no Mi", "paramecia")

    ope_ope.add_ability(DevilFruitAbility(
        "room",
        "Room",
        "Create operation space",
        30,
        damage=80,
        required_level=1
    ))

    ope_ope.add_ability(DevilFruitAbility(
        "shambles",
        "Shambles",
        "Swap positions",
        40,
        damage=100,
        required_level=10
    ))

    fruits["ope_ope"] = ope_ope

    return fruits
