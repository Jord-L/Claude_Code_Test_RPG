"""
Stats System
Manages character statistics and calculations.
"""

from typing import Dict, Optional
from utils.constants import (
    BASE_HP, BASE_ATTACK, BASE_DEFENSE, BASE_SPEED, BASE_DF_POWER
)


class Stats:
    """
    Manages character statistics.
    Handles base stats, modifiers, and calculated values.
    """
    
    def __init__(self, 
                 str_val: int = 10,
                 def_val: int = 10,
                 agi_val: int = 10,
                 int_val: int = 10,
                 will_val: int = 10,
                 cha_val: int = 10,
                 lck_val: int = 10):
        """
        Initialize character stats.
        
        Args:
            str_val: Strength (affects physical attack)
            def_val: Defense (affects damage reduction)
            agi_val: Agility (affects speed and evasion)
            int_val: Intelligence (affects special abilities)
            will_val: Willpower (affects resistances and AP)
            cha_val: Charisma (affects prices and interactions)
            lck_val: Luck (affects critical chance and loot)
        """
        # Primary stats
        self.strength = str_val
        self.defense = def_val
        self.agility = agi_val
        self.intelligence = int_val
        self.willpower = will_val
        self.charisma = cha_val
        self.luck = lck_val
        
        # Stat modifiers (from equipment, buffs, etc.)
        self.modifiers: Dict[str, int] = {
            "strength": 0,
            "defense": 0,
            "agility": 0,
            "intelligence": 0,
            "willpower": 0,
            "charisma": 0,
            "luck": 0,
            "max_hp": 0,
            "max_ap": 0,
            "attack": 0,
            "critical_chance": 0,
            "critical_damage": 0,
            "evasion": 0
        }
        
        # Percentage modifiers (multiplicative)
        self.percent_modifiers: Dict[str, float] = {
            "max_hp": 0.0,
            "max_ap": 0.0,
            "attack": 0.0,
            "defense": 0.0,
            "speed": 0.0
        }
    
    # Primary stat accessors with modifiers
    
    def get_strength(self) -> int:
        """Get total strength (base + modifiers)."""
        return self.strength + self.modifiers["strength"]
    
    def get_defense(self) -> int:
        """Get total defense (base + modifiers)."""
        return self.defense + self.modifiers["defense"]
    
    def get_agility(self) -> int:
        """Get total agility (base + modifiers)."""
        return self.agility + self.modifiers["agility"]
    
    def get_intelligence(self) -> int:
        """Get total intelligence (base + modifiers)."""
        return self.intelligence + self.modifiers["intelligence"]
    
    def get_willpower(self) -> int:
        """Get total willpower (base + modifiers)."""
        return self.willpower + self.modifiers["willpower"]
    
    def get_charisma(self) -> int:
        """Get total charisma (base + modifiers)."""
        return self.charisma + self.modifiers["charisma"]
    
    def get_luck(self) -> int:
        """Get total luck (base + modifiers)."""
        return self.luck + self.modifiers["luck"]
    
    # Derived stats (calculated from primary stats)
    
    def get_max_hp(self, level: int = 1) -> int:
        """
        Calculate maximum HP.
        
        Args:
            level: Character level
        
        Returns:
            Maximum HP
        """
        base = BASE_HP + (level * 10) + (self.get_strength() * 2)
        with_flat = base + self.modifiers["max_hp"]
        with_percent = int(with_flat * (1 + self.percent_modifiers["max_hp"]))
        return max(1, with_percent)
    
    def get_max_ap(self, level: int = 1) -> int:
        """
        Calculate maximum AP (Ability Points).
        
        Args:
            level: Character level
        
        Returns:
            Maximum AP
        """
        base = 50 + (level * 5) + (self.get_willpower() * 1)
        with_flat = base + self.modifiers["max_ap"]
        with_percent = int(with_flat * (1 + self.percent_modifiers["max_ap"]))
        return max(1, with_percent)
    
    def get_attack(self) -> int:
        """
        Calculate attack power.
        
        Returns:
            Attack value
        """
        base = BASE_ATTACK + (self.get_strength() * 2)
        with_flat = base + self.modifiers["attack"]
        with_percent = int(with_flat * (1 + self.percent_modifiers["attack"]))
        return max(1, with_percent)
    
    def get_defense_value(self) -> int:
        """
        Calculate defense value.
        
        Returns:
            Defense value
        """
        base = BASE_DEFENSE + (self.get_defense() * 2)
        with_percent = int(base * (1 + self.percent_modifiers["defense"]))
        return max(0, with_percent)
    
    def get_speed(self) -> int:
        """
        Calculate speed (determines turn order).
        
        Returns:
            Speed value
        """
        base = BASE_SPEED + (self.get_agility() * 2)
        with_percent = int(base * (1 + self.percent_modifiers["speed"]))
        return max(1, with_percent)
    
    def get_critical_chance(self) -> float:
        """
        Calculate critical hit chance (%).
        
        Returns:
            Critical chance as percentage (0-100)
        """
        base = 5.0 + (self.get_luck() * 0.5)
        with_modifier = base + self.modifiers["critical_chance"]
        return min(100.0, max(0.0, with_modifier))
    
    def get_critical_damage(self) -> float:
        """
        Calculate critical damage multiplier.
        
        Returns:
            Critical damage multiplier (e.g., 1.5 = 150%)
        """
        base = 1.5 + (self.get_luck() * 0.01)
        with_modifier = base + (self.modifiers["critical_damage"] / 100.0)
        return max(1.0, with_modifier)
    
    def get_evasion(self) -> float:
        """
        Calculate evasion chance (%).
        
        Returns:
            Evasion chance as percentage (0-100)
        """
        base = 5.0 + (self.get_agility() * 0.5)
        with_modifier = base + self.modifiers["evasion"]
        return min(100.0, max(0.0, with_modifier))
    
    # Modifier management
    
    def add_modifier(self, stat: str, value: int):
        """
        Add a flat modifier to a stat.
        
        Args:
            stat: Stat name
            value: Value to add (can be negative)
        """
        if stat in self.modifiers:
            self.modifiers[stat] += value
    
    def add_percent_modifier(self, stat: str, percent: float):
        """
        Add a percentage modifier to a stat.
        
        Args:
            stat: Stat name
            percent: Percentage to add (e.g., 0.1 = 10%)
        """
        if stat in self.percent_modifiers:
            self.percent_modifiers[stat] += percent
    
    def remove_modifier(self, stat: str, value: int):
        """
        Remove a flat modifier from a stat.
        
        Args:
            stat: Stat name
            value: Value to remove
        """
        if stat in self.modifiers:
            self.modifiers[stat] -= value
    
    def remove_percent_modifier(self, stat: str, percent: float):
        """
        Remove a percentage modifier from a stat.
        
        Args:
            stat: Stat name
            percent: Percentage to remove
        """
        if stat in self.percent_modifiers:
            self.percent_modifiers[stat] -= percent
    
    def clear_modifiers(self):
        """Clear all modifiers."""
        for key in self.modifiers:
            self.modifiers[key] = 0
        for key in self.percent_modifiers:
            self.percent_modifiers[key] = 0.0
    
    # Stat increases (leveling up)
    
    def increase_stat(self, stat: str, amount: int = 1):
        """
        Permanently increase a base stat.
        
        Args:
            stat: Stat name (lowercase)
            amount: Amount to increase
        """
        stat = stat.lower()
        if stat == "strength":
            self.strength += amount
        elif stat == "defense":
            self.defense += amount
        elif stat == "agility":
            self.agility += amount
        elif stat == "intelligence":
            self.intelligence += amount
        elif stat == "willpower":
            self.willpower += amount
        elif stat == "charisma":
            self.charisma += amount
        elif stat == "luck":
            self.luck += amount
    
    # Utility methods
    
    def get_all_stats(self) -> Dict[str, int]:
        """
        Get all primary stats.
        
        Returns:
            Dictionary of stat names to values
        """
        return {
            "strength": self.get_strength(),
            "defense": self.get_defense(),
            "agility": self.get_agility(),
            "intelligence": self.get_intelligence(),
            "willpower": self.get_willpower(),
            "charisma": self.get_charisma(),
            "luck": self.get_luck()
        }
    
    def get_derived_stats(self, level: int = 1) -> Dict[str, any]:
        """
        Get all derived stats.
        
        Args:
            level: Character level for calculations
        
        Returns:
            Dictionary of derived stat names to values
        """
        return {
            "max_hp": self.get_max_hp(level),
            "max_ap": self.get_max_ap(level),
            "attack": self.get_attack(),
            "defense": self.get_defense_value(),
            "speed": self.get_speed(),
            "critical_chance": self.get_critical_chance(),
            "critical_damage": self.get_critical_damage(),
            "evasion": self.get_evasion()
        }
    
    def to_dict(self) -> Dict:
        """
        Convert stats to dictionary for saving.
        
        Returns:
            Dictionary representation
        """
        return {
            "primary": {
                "strength": self.strength,
                "defense": self.defense,
                "agility": self.agility,
                "intelligence": self.intelligence,
                "willpower": self.willpower,
                "charisma": self.charisma,
                "luck": self.luck
            },
            "modifiers": self.modifiers.copy(),
            "percent_modifiers": self.percent_modifiers.copy()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Stats':
        """
        Create Stats from dictionary.
        
        Args:
            data: Dictionary with stat data
        
        Returns:
            Stats instance
        """
        primary = data.get("primary", {})
        stats = cls(
            str_val=primary.get("strength", 10),
            def_val=primary.get("defense", 10),
            agi_val=primary.get("agility", 10),
            int_val=primary.get("intelligence", 10),
            will_val=primary.get("willpower", 10),
            cha_val=primary.get("charisma", 10),
            lck_val=primary.get("luck", 10)
        )
        
        # Restore modifiers
        if "modifiers" in data:
            stats.modifiers = data["modifiers"].copy()
        if "percent_modifiers" in data:
            stats.percent_modifiers = data["percent_modifiers"].copy()
        
        return stats
