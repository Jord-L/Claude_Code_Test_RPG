"""
Haki System
Three types of Haki: Observation, Armament, and Conqueror's.
"""

from typing import Dict, Optional
from enum import Enum
from dataclasses import dataclass


class HakiType(Enum):
    """Types of Haki."""
    OBSERVATION = "observation"  # Kenbunshoku - Dodge/predict
    ARMAMENT = "armament"  # Busoshoku - Attack/defense boost
    CONQUERORS = "conquerors"  # Haoshoku - Stun weak enemies


@dataclass
class HakiAbility:
    """Haki ability."""
    haki_type: HakiType
    level: int = 1  # 1-10 mastery
    exp: int = 0

    def gain_exp(self, amount: int):
        """Gain Haki experience."""
        self.exp += amount
        while self.exp >= self.level * 200 and self.level < 10:
            self.exp -= self.level * 200
            self.level += 1
            print(f"{self.haki_type.value.capitalize()} Haki leveled up to {self.level}!")


class HakiUser:
    """Character with Haki abilities."""

    def __init__(self):
        """Initialize Haki user."""
        self.haki_abilities: Dict[HakiType, HakiAbility] = {}
        self.haki_unlocked = False

    def unlock_haki(self, haki_type: HakiType):
        """Unlock a type of Haki."""
        if haki_type not in self.haki_abilities:
            self.haki_abilities[haki_type] = HakiAbility(haki_type)
            self.haki_unlocked = True
            print(f"Unlocked {haki_type.value.capitalize()} Haki!")

    def has_haki(self, haki_type: HakiType) -> bool:
        """Check if has Haki type."""
        return haki_type in self.haki_abilities

    def get_haki_level(self, haki_type: HakiType) -> int:
        """Get Haki level."""
        if haki_type in self.haki_abilities:
            return self.haki_abilities[haki_type].level
        return 0

    def use_observation_haki(self) -> Dict:
        """
        Use Observation Haki.

        Returns:
            Effect results
        """
        if not self.has_haki(HakiType.OBSERVATION):
            return {"success": False}

        level = self.get_haki_level(HakiType.OBSERVATION)
        dodge_bonus = level * 5  # +5% dodge per level
        crit_avoid = level * 3  # +3% crit avoid per level

        # Gain exp
        self.haki_abilities[HakiType.OBSERVATION].gain_exp(10)

        return {
            "success": True,
            "dodge_bonus": dodge_bonus,
            "crit_avoid": crit_avoid,
            "duration": 3  # turns
        }

    def use_armament_haki(self) -> Dict:
        """
        Use Armament Haki.

        Returns:
            Effect results
        """
        if not self.has_haki(HakiType.ARMAMENT):
            return {"success": False}

        level = self.get_haki_level(HakiType.ARMAMENT)
        damage_bonus = level * 10  # +10 damage per level
        defense_bonus = level * 5  # +5 defense per level

        # Gain exp
        self.haki_abilities[HakiType.ARMAMENT].gain_exp(10)

        return {
            "success": True,
            "damage_bonus": damage_bonus,
            "defense_bonus": defense_bonus,
            "duration": 3  # turns
        }

    def use_conquerors_haki(self, enemy_level: int) -> Dict:
        """
        Use Conqueror's Haki.

        Args:
            enemy_level: Enemy level to check if can stun

        Returns:
            Effect results
        """
        if not self.has_haki(HakiType.CONQUERORS):
            return {"success": False}

        level = self.get_haki_level(HakiType.CONQUERORS)

        # Can stun enemies up to (user_level + haki_level * 2) levels below
        max_stun_level = level * 3

        # Gain exp
        self.haki_abilities[HakiType.CONQUERORS].gain_exp(15)

        if enemy_level <= max_stun_level:
            return {
                "success": True,
                "stunned": True,
                "message": "Overwhelming presence!"
            }
        else:
            return {
                "success": True,
                "stunned": False,
                "damage": level * 20,  # Deals damage even if doesn't stun
                "message": "Enemy resisted Conqueror's Haki!"
            }


def unlock_haki_for_character(character, required_level: int = 20):
    """
    Unlock Haki for a character.

    Args:
        character: Character to unlock for
        required_level: Level required (default 20)
    """
    if not hasattr(character, 'haki_user'):
        character.haki_user = HakiUser()

    if character.level >= required_level:
        # Unlock Observation first
        character.haki_user.unlock_haki(HakiType.OBSERVATION)

        # Unlock Armament at level 25
        if character.level >= 25:
            character.haki_user.unlock_haki(HakiType.ARMAMENT)

        # Conqueror's is rare - only for special characters
        if hasattr(character, 'has_conquerors') and character.has_conquerors:
            character.haki_user.unlock_haki(HakiType.CONQUERORS)
