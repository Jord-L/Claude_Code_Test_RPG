"""
Character Class
Base class for all characters (player, enemies, NPCs, crew members).
"""

from typing import Dict, List, Optional, TYPE_CHECKING
from entities.stats import Stats
from entities.devil_fruit import DevilFruit

if TYPE_CHECKING:
    from systems.equipment_manager import EquipmentSlots


class Character:
    """
    Base class for all characters in the game.
    Handles stats, HP/AP, equipment, and Devil Fruits.
    """
    
    def __init__(self, name: str, level: int = 1):
        """
        Initialize a character.
        
        Args:
            name: Character name
            level: Starting level
        """
        self.name = name
        self.level = level
        self.experience = 0
        self.exp_to_next_level = 100
        
        # Stats
        self.stats = Stats()
        
        # HP and AP
        self.max_hp = self.stats.get_max_hp(self.level)
        self.current_hp = self.max_hp
        self.max_ap = self.stats.get_max_ap(self.level)
        self.current_ap = self.max_ap
        
        # Devil Fruit
        self.devil_fruit: Optional[DevilFruit] = None
        
        # Equipment (old dict format - deprecated, kept for compatibility)
        self.equipment = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }

        # New equipment system (initialized by EquipmentManager)
        self.equipment_slots: Optional['EquipmentSlots'] = None
        
        # Status effects
        self.status_effects = []
        
        # Combat state
        self.is_alive = True
        self.can_act = True
        
    # Level system
    
    def gain_experience(self, amount: int) -> bool:
        """
        Gain experience points.
        
        Args:
            amount: Experience to gain
        
        Returns:
            True if leveled up
        """
        self.experience += amount
        
        leveled_up = False
        while self.experience >= self.exp_to_next_level:
            leveled_up = True
            self.level_up()
        
        return leveled_up
    
    def level_up(self):
        """Level up the character."""
        self.level += 1
        self.experience -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        
        # Increase stats (can be overridden by subclasses)
        self._apply_level_up_bonuses()
        
        # Recalculate max HP/AP
        old_max_hp = self.max_hp
        old_max_ap = self.max_ap
        
        self.max_hp = self.stats.get_max_hp(self.level)
        self.max_ap = self.stats.get_max_ap(self.level)
        
        # Restore HP/AP by the increased amount
        hp_increase = self.max_hp - old_max_hp
        ap_increase = self.max_ap - old_max_ap
        
        self.current_hp = min(self.current_hp + hp_increase, self.max_hp)
        self.current_ap = min(self.current_ap + ap_increase, self.max_ap)
        
        print(f"{self.name} leveled up to level {self.level}!")
    
    def _apply_level_up_bonuses(self):
        """Apply stat increases on level up (can be overridden)."""
        # Base implementation: increase all stats by 1
        self.stats.increase_stat("strength", 1)
        self.stats.increase_stat("defense", 1)
        self.stats.increase_stat("agility", 1)
        self.stats.increase_stat("willpower", 1)
    
    # HP and AP management
    
    def take_damage(self, amount: int) -> int:
        """
        Take damage.
        
        Args:
            amount: Damage amount (before defense)
        
        Returns:
            Actual damage taken
        """
        # Calculate damage reduction from defense
        defense = self.stats.get_defense_value()
        damage_reduction = defense * 0.5  # 50% effectiveness
        actual_damage = max(1, int(amount - damage_reduction))
        
        # Check for intangibility (Logia)
        if self.devil_fruit and self.devil_fruit.has_intangibility():
            # TODO: Check if attack can hit Logia users (Haki, natural counter)
            # For now, Logia users take no damage from physical attacks
            actual_damage = 0
        
        self.current_hp = max(0, self.current_hp - actual_damage)
        
        if self.current_hp <= 0:
            self.is_alive = False
            self.on_death()
        
        return actual_damage
    
    def heal(self, amount: int) -> int:
        """
        Heal HP.
        
        Args:
            amount: Amount to heal
        
        Returns:
            Actual amount healed
        """
        old_hp = self.current_hp
        self.current_hp = min(self.current_hp + amount, self.max_hp)
        return self.current_hp - old_hp
    
    def restore_ap(self, amount: int) -> int:
        """
        Restore AP.
        
        Args:
            amount: Amount to restore
        
        Returns:
            Actual amount restored
        """
        old_ap = self.current_ap
        self.current_ap = min(self.current_ap + amount, self.max_ap)
        return self.current_ap - old_ap
    
    def use_ap(self, amount: int) -> bool:
        """
        Use AP for an ability.
        
        Args:
            amount: AP cost
        
        Returns:
            True if had enough AP
        """
        if self.current_ap >= amount:
            self.current_ap -= amount
            return True
        return False
    
    def is_at_full_hp(self) -> bool:
        """Check if at full HP."""
        return self.current_hp >= self.max_hp
    
    def is_at_full_ap(self) -> bool:
        """Check if at full AP."""
        return self.current_ap >= self.max_ap
    
    def get_hp_percentage(self) -> float:
        """Get HP as percentage (0.0 to 1.0)."""
        return self.current_hp / self.max_hp if self.max_hp > 0 else 0.0
    
    def get_ap_percentage(self) -> float:
        """Get AP as percentage (0.0 to 1.0)."""
        return self.current_ap / self.max_ap if self.max_ap > 0 else 0.0
    
    # Devil Fruit
    
    def equip_devil_fruit(self, fruit_data: Dict):
        """
        Equip a Devil Fruit.
        
        Args:
            fruit_data: Devil Fruit data from database
        """
        if self.devil_fruit:
            print("Already has a Devil Fruit!")
            return
        
        self.devil_fruit = DevilFruit(fruit_data)
        self._apply_devil_fruit_bonuses()
        print(f"{self.name} ate the {self.devil_fruit.name}!")
    
    def _apply_devil_fruit_bonuses(self):
        """Apply stat bonuses from Devil Fruit."""
        if not self.devil_fruit:
            return
        
        # Apply flat modifiers
        modifiers = self.devil_fruit.get_stat_modifiers()
        for stat, value in modifiers.items():
            self.stats.add_modifier(stat, value)
        
        # Apply percentage modifiers
        percent_mods = self.devil_fruit.get_percent_modifiers()
        for stat, value in percent_mods.items():
            self.stats.add_percent_modifier(stat, value)
        
        # Recalculate max HP/AP
        self.max_hp = self.stats.get_max_hp(self.level)
        self.max_ap = self.stats.get_max_ap(self.level)
    
    def has_devil_fruit(self) -> bool:
        """Check if character has a Devil Fruit."""
        return self.devil_fruit is not None
    
    def can_swim(self) -> bool:
        """Check if character can swim."""
        return not self.has_devil_fruit()
    
    # Equipment
    
    def equip_item(self, slot: str, item_data: Dict):
        """
        Equip an item.
        
        Args:
            slot: Equipment slot ("weapon", "armor", "accessory")
            item_data: Item data
        """
        if slot not in self.equipment:
            return
        
        # Unequip current item in slot
        if self.equipment[slot]:
            self.unequip_item(slot)
        
        # Equip new item
        self.equipment[slot] = item_data
        self._apply_equipment_bonuses(item_data)
        
        print(f"{self.name} equipped {item_data.get('name', 'Unknown Item')}!")
    
    def unequip_item(self, slot: str) -> Optional[Dict]:
        """
        Unequip an item.
        
        Args:
            slot: Equipment slot
        
        Returns:
            Unequipped item data or None
        """
        if slot not in self.equipment:
            return None
        
        item = self.equipment[slot]
        if item:
            self._remove_equipment_bonuses(item)
            self.equipment[slot] = None
            print(f"{self.name} unequipped {item.get('name', 'Unknown Item')}!")
        
        return item
    
    def _apply_equipment_bonuses(self, item_data: Dict):
        """Apply stat bonuses from equipment."""
        stats = item_data.get("stats", {})
        for stat, value in stats.items():
            self.stats.add_modifier(stat, value)
    
    def _remove_equipment_bonuses(self, item_data: Dict):
        """Remove stat bonuses from equipment."""
        stats = item_data.get("stats", {})
        for stat, value in stats.items():
            self.stats.remove_modifier(stat, value)
    
    # Combat
    
    def get_attack_power(self) -> int:
        """Get total attack power."""
        return self.stats.get_attack()
    
    def get_defense_power(self) -> int:
        """Get total defense power."""
        return self.stats.get_defense_value()
    
    def get_speed(self) -> int:
        """Get speed (for turn order)."""
        return self.stats.get_speed()
    
    def calculate_damage(self, target: 'Character', base_damage: int) -> int:
        """
        Calculate damage dealt to a target.
        
        Args:
            target: Target character
            base_damage: Base damage amount
        
        Returns:
            Final damage amount
        """
        # Check for critical hit
        crit_chance = self.stats.get_critical_chance()
        import random
        is_critical = random.random() * 100 < crit_chance
        
        if is_critical:
            crit_multiplier = self.stats.get_critical_damage()
            base_damage = int(base_damage * crit_multiplier)
            print("Critical hit!")
        
        return base_damage
    
    def can_dodge(self) -> bool:
        """Check if attack is dodged."""
        evasion = self.stats.get_evasion()
        import random
        return random.random() * 100 < evasion
    
    # Status management
    
    def on_death(self):
        """Called when character HP reaches 0."""
        self.is_alive = False
        self.can_act = False
        print(f"{self.name} has been defeated!")
    
    def revive(self, hp_percent: float = 0.5):
        """
        Revive the character.
        
        Args:
            hp_percent: HP percentage to revive with (0.0 to 1.0)
        """
        self.is_alive = True
        self.can_act = True
        self.current_hp = int(self.max_hp * hp_percent)
        print(f"{self.name} has been revived!")
    
    def rest(self):
        """Fully restore HP and AP."""
        self.current_hp = self.max_hp
        self.current_ap = self.max_ap
        self.status_effects.clear()
    
    # Utility
    
    def get_level_progress(self) -> float:
        """Get progress to next level (0.0 to 1.0)."""
        return self.experience / self.exp_to_next_level
    
    def to_dict(self) -> Dict:
        """
        Convert character to dictionary for saving.
        
        Returns:
            Dictionary representation
        """
        data = {
            "name": self.name,
            "level": self.level,
            "experience": self.experience,
            "exp_to_next_level": self.exp_to_next_level,
            "current_hp": self.current_hp,
            "current_ap": self.current_ap,
            "stats": self.stats.to_dict(),
            "is_alive": self.is_alive
        }
        
        if self.devil_fruit:
            data["devil_fruit"] = self.devil_fruit.to_dict()
        
        # Add equipment
        data["equipment"] = {}
        for slot, item in self.equipment.items():
            if item:
                data["equipment"][slot] = item.get("id")
        
        return data
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.name} (Lv. {self.level}) - HP: {self.current_hp}/{self.max_hp}"
    
    def __repr__(self) -> str:
        """Debug representation."""
        return f"Character(name={self.name}, level={self.level}, hp={self.current_hp}/{self.max_hp})"
