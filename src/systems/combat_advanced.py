"""
Advanced Combat System
Enhanced combat mechanics: combos, critical hits, status effects.
"""

from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
import random


class StatusEffect(Enum):
    """Status effects."""
    POISON = "poison"
    BURN = "burn"
    FREEZE = "freeze"
    STUN = "stun"
    BLEED = "bleed"
    BUFF_ATK = "buff_attack"
    BUFF_DEF = "buff_defense"
    BUFF_SPD = "buff_speed"


@dataclass
class ActiveStatus:
    """Active status effect on character."""
    effect: StatusEffect
    duration: int  # Turns remaining
    potency: int  # Effect strength


class ComboSystem:
    """Combo attack system."""

    def __init__(self):
        """Initialize combo system."""
        self.combo_count = 0
        self.max_combo = 99
        self.combo_bonus = 0.0

    def add_hit(self):
        """Add hit to combo."""
        self.combo_count = min(self.combo_count + 1, self.max_combo)
        self.combo_bonus = min(self.combo_count * 0.05, 2.0)  # Max 200% bonus

    def reset(self):
        """Reset combo."""
        self.combo_count = 0
        self.combo_bonus = 0.0

    def get_damage_multiplier(self) -> float:
        """Get damage multiplier from combo."""
        return 1.0 + self.combo_bonus


class CriticalHitSystem:
    """Critical hit calculation."""

    @staticmethod
    def roll_critical(base_crit_chance: float, luck: int = 0) -> bool:
        """
        Roll for critical hit.

        Args:
            base_crit_chance: Base crit % (0-100)
            luck: Luck stat bonus

        Returns:
            True if critical hit
        """
        crit_chance = base_crit_chance + (luck * 0.5)
        crit_chance = min(crit_chance, 95.0)  # Max 95% crit
        return random.random() * 100 < crit_chance

    @staticmethod
    def calculate_crit_damage(base_damage: int, crit_multiplier: float = 1.5) -> int:
        """Calculate critical hit damage."""
        return int(base_damage * crit_multiplier)


class StatusEffectManager:
    """Manages status effects on characters."""

    def __init__(self):
        """Initialize status manager."""
        self.active_effects: Dict[str, List[ActiveStatus]] = {}  # character_id -> effects

    def apply_status(self, character_id: str, effect: StatusEffect, duration: int, potency: int):
        """Apply status effect to character."""
        if character_id not in self.active_effects:
            self.active_effects[character_id] = []

        # Check if effect already exists
        for active in self.active_effects[character_id]:
            if active.effect == effect:
                # Refresh duration and update potency
                active.duration = max(active.duration, duration)
                active.potency = max(active.potency, potency)
                return

        # Add new effect
        self.active_effects[character_id].append(
            ActiveStatus(effect, duration, potency)
        )

    def process_turn(self, character_id: str, character) -> Dict:
        """
        Process status effects for character's turn.

        Returns:
            Effect results
        """
        if character_id not in self.active_effects:
            return {}

        results = {
            "damage_taken": 0,
            "healing_received": 0,
            "messages": []
        }

        effects_to_remove = []

        for status in self.active_effects[character_id]:
            # Process effect
            if status.effect == StatusEffect.POISON:
                damage = status.potency
                character.take_damage(damage)
                results["damage_taken"] += damage
                results["messages"].append(f"Poisoned! Lost {damage} HP")

            elif status.effect == StatusEffect.BURN:
                damage = status.potency * 2
                character.take_damage(damage)
                results["damage_taken"] += damage
                results["messages"].append(f"Burning! Lost {damage} HP")

            elif status.effect == StatusEffect.BLEED:
                damage = status.potency
                character.take_damage(damage)
                results["damage_taken"] += damage
                results["messages"].append(f"Bleeding! Lost {damage} HP")

            # Decrease duration
            status.duration -= 1
            if status.duration <= 0:
                effects_to_remove.append(status)

        # Remove expired effects
        for status in effects_to_remove:
            self.active_effects[character_id].remove(status)
            results["messages"].append(f"{status.effect.value} wore off")

        return results

    def has_effect(self, character_id: str, effect: StatusEffect) -> bool:
        """Check if character has status effect."""
        if character_id not in self.active_effects:
            return False
        return any(s.effect == effect for s in self.active_effects[character_id])

    def clear_effects(self, character_id: str):
        """Remove all effects from character."""
        if character_id in self.active_effects:
            self.active_effects[character_id].clear()


class AdvancedCombatManager:
    """Manages advanced combat features."""

    def __init__(self):
        """Initialize advanced combat."""
        self.combo = ComboSystem()
        self.status_manager = StatusEffectManager()

    def calculate_damage(self, base_damage: int, attacker_stats: Dict, defender_stats: Dict) -> Dict:
        """
        Calculate damage with advanced mechanics.

        Returns:
            Damage calculation results
        """
        damage = base_damage

        # Apply combo bonus
        damage = int(damage * self.combo.get_damage_multiplier())

        # Roll for critical
        crit_chance = attacker_stats.get("crit_chance", 5.0)
        is_crit = CriticalHitSystem.roll_critical(crit_chance, attacker_stats.get("luck", 0))

        if is_crit:
            damage = CriticalHitSystem.calculate_crit_damage(damage)

        # Apply defense
        defense = defender_stats.get("defense", 0)
        damage = max(1, damage - defense)

        return {
            "damage": damage,
            "is_critical": is_crit,
            "combo_count": self.combo.combo_count,
            "combo_bonus": self.combo.combo_bonus
        }

    def on_hit_landed(self):
        """Call when attack lands."""
        self.combo.add_hit()

    def on_combo_broken(self):
        """Call when combo is broken (miss, defend, etc)."""
        self.combo.reset()
