"""
Equipment Manager
Handles character equipment slots and stat application.
"""

from typing import Dict, Optional
from systems.item_system import Equipment, Weapon, Armor, Accessory
from entities.character import Character


class EquipmentSlots:
    """Equipment slots for a single character."""

    def __init__(self, character: Character):
        """
        Initialize equipment slots.

        Args:
            character: Character who owns these slots
        """
        self.character = character

        # Equipment slots
        self.weapon: Optional[Weapon] = None
        self.armor: Optional[Armor] = None
        self.accessory: Optional[Accessory] = None

    def equip(self, equipment: Equipment) -> Optional[Equipment]:
        """
        Equip an item.

        Args:
            equipment: Equipment to equip

        Returns:
            Previously equipped item (if any)
        """
        # Check if can equip
        if not equipment.can_equip(self.character):
            print(f"{self.character.name} cannot equip {equipment.name} (level req: {equipment.level_requirement})")
            return None

        # Determine slot
        slot = equipment.equip_slot
        previous = None

        if slot == "weapon" and isinstance(equipment, Weapon):
            previous = self.weapon
            if previous:
                previous.remove_stats(self.character)

            self.weapon = equipment
            equipment.apply_stats(self.character)

        elif slot == "armor" and isinstance(equipment, Armor):
            previous = self.armor
            if previous:
                previous.remove_stats(self.character)

            self.armor = equipment
            equipment.apply_stats(self.character)

        elif slot == "accessory" and isinstance(equipment, Accessory):
            previous = self.accessory
            if previous:
                previous.remove_stats(self.character)

            self.accessory = equipment
            equipment.apply_stats(self.character)

        else:
            print(f"Unknown equipment slot: {slot}")
            return None

        # Recalculate character stats
        self._recalculate_stats()

        print(f"{self.character.name} equipped {equipment.name}")
        return previous

    def unequip(self, slot: str) -> Optional[Equipment]:
        """
        Unequip item from slot.

        Args:
            slot: Slot name (weapon, armor, accessory)

        Returns:
            Unequipped item (if any)
        """
        equipment = None

        if slot == "weapon" and self.weapon:
            equipment = self.weapon
            equipment.remove_stats(self.character)
            self.weapon = None

        elif slot == "armor" and self.armor:
            equipment = self.armor
            equipment.remove_stats(self.character)
            self.armor = None

        elif slot == "accessory" and self.accessory:
            equipment = self.accessory
            equipment.remove_stats(self.character)
            self.accessory = None

        if equipment:
            self._recalculate_stats()
            print(f"{self.character.name} unequipped {equipment.name}")

        return equipment

    def get_equipment(self, slot: str) -> Optional[Equipment]:
        """
        Get equipment in slot.

        Args:
            slot: Slot name

        Returns:
            Equipment or None
        """
        if slot == "weapon":
            return self.weapon
        elif slot == "armor":
            return self.armor
        elif slot == "accessory":
            return self.accessory
        return None

    def get_all_equipment(self) -> Dict[str, Optional[Equipment]]:
        """Get all equipped items."""
        return {
            "weapon": self.weapon,
            "armor": self.armor,
            "accessory": self.accessory
        }

    def _recalculate_stats(self):
        """Recalculate character's derived stats after equipment change."""
        # Update max HP/AP
        old_max_hp = self.character.max_hp
        old_max_ap = self.character.max_ap

        self.character.max_hp = self.character.stats.get_max_hp(self.character.level)
        self.character.max_ap = self.character.stats.get_max_ap(self.character.level)

        # Adjust current HP/AP proportionally
        if old_max_hp > 0:
            hp_percent = self.character.current_hp / old_max_hp
            self.character.current_hp = min(self.character.current_hp, int(self.character.max_hp * hp_percent))

        if old_max_ap > 0:
            ap_percent = self.character.current_ap / old_max_ap
            self.character.current_ap = min(self.character.current_ap, int(self.character.max_ap * ap_percent))

    def get_total_attack_bonus(self) -> int:
        """Get total attack bonus from equipment."""
        bonus = 0
        if self.weapon:
            bonus += getattr(self.weapon, 'attack_power', 0)
            bonus += self.weapon.get_stat_bonus('strength')
        return bonus

    def get_total_defense_bonus(self) -> int:
        """Get total defense bonus from equipment."""
        bonus = 0
        if self.armor:
            bonus += getattr(self.armor, 'defense', 0)
            bonus += self.armor.get_stat_bonus('defense')
        return bonus

    def __repr__(self) -> str:
        """String representation."""
        equipped = []
        if self.weapon:
            equipped.append(f"W:{self.weapon.name}")
        if self.armor:
            equipped.append(f"A:{self.armor.name}")
        if self.accessory:
            equipped.append(f"Acc:{self.accessory.name}")

        return f"Equipment({self.character.name}: {', '.join(equipped) if equipped else 'None'})"


class EquipmentManager:
    """
    Global equipment manager.
    Manages equipment for all characters.
    """

    def __init__(self):
        """Initialize equipment manager."""
        self.character_equipment: Dict[str, EquipmentSlots] = {}

    def get_or_create_slots(self, character: Character) -> EquipmentSlots:
        """
        Get equipment slots for character, creating if needed.

        Args:
            character: Character to get slots for

        Returns:
            EquipmentSlots for character
        """
        char_id = character.name  # Use name as ID for now

        if char_id not in self.character_equipment:
            self.character_equipment[char_id] = EquipmentSlots(character)

        return self.character_equipment[char_id]

    def equip_item(self, character: Character, equipment: Equipment) -> Optional[Equipment]:
        """
        Equip item to character.

        Args:
            character: Character to equip to
            equipment: Equipment to equip

        Returns:
            Previously equipped item (if any)
        """
        slots = self.get_or_create_slots(character)
        return slots.equip(equipment)

    def unequip_item(self, character: Character, slot: str) -> Optional[Equipment]:
        """
        Unequip item from character.

        Args:
            character: Character to unequip from
            slot: Slot to unequip

        Returns:
            Unequipped item (if any)
        """
        slots = self.get_or_create_slots(character)
        return slots.unequip(slot)

    def get_equipment(self, character: Character, slot: str) -> Optional[Equipment]:
        """
        Get equipment in slot for character.

        Args:
            character: Character to check
            slot: Slot to check

        Returns:
            Equipment or None
        """
        if character.name not in self.character_equipment:
            return None

        slots = self.character_equipment[character.name]
        return slots.get_equipment(slot)

    def get_all_equipment(self, character: Character) -> Dict[str, Optional[Equipment]]:
        """
        Get all equipment for character.

        Args:
            character: Character to check

        Returns:
            Dictionary of slot -> equipment
        """
        slots = self.get_or_create_slots(character)
        return slots.get_all_equipment()

    def is_equipped(self, character: Character, equipment: Equipment) -> bool:
        """
        Check if equipment is currently equipped by character.

        Args:
            character: Character to check
            equipment: Equipment to check

        Returns:
            True if equipped
        """
        all_equipment = self.get_all_equipment(character)
        return equipment in all_equipment.values()

    def get_equipment_summary(self, character: Character) -> str:
        """
        Get text summary of character's equipment.

        Args:
            character: Character to summarize

        Returns:
            Formatted summary string
        """
        slots = self.get_or_create_slots(character)
        lines = [
            f"=== {character.name}'s Equipment ===",
            f"Weapon: {slots.weapon.name if slots.weapon else 'None'}",
            f"Armor: {slots.armor.name if slots.armor else 'None'}",
            f"Accessory: {slots.accessory.name if slots.accessory else 'None'}",
            ""
        ]

        # Show stat bonuses
        if slots.weapon or slots.armor or slots.accessory:
            lines.append("Stat Bonuses:")
            atk_bonus = slots.get_total_attack_bonus()
            def_bonus = slots.get_total_defense_bonus()

            if atk_bonus > 0:
                lines.append(f"  Attack: +{atk_bonus}")
            if def_bonus > 0:
                lines.append(f"  Defense: +{def_bonus}")

        return "\n".join(lines)
