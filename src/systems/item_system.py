"""
Item and Equipment System
Handles all items, equipment, and their properties.
"""

from typing import Dict, Optional, List
from enum import Enum


class ItemType(Enum):
    """Item type enumeration."""
    CONSUMABLE = "consumable"
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"
    KEY_ITEM = "key_item"
    MATERIAL = "material"


class ItemRarity(Enum):
    """Item rarity levels."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class WeaponType(Enum):
    """Weapon categories."""
    SWORD = "sword"
    DUAL_SWORDS = "dual_swords"
    GUN = "gun"
    RIFLE = "rifle"
    STAFF = "staff"
    FIST = "fist"
    BOOTS = "boots"
    POLEARM = "polearm"
    BOW = "bow"


class ArmorType(Enum):
    """Armor categories."""
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"
    CLOTHING = "clothing"


class Item:
    """
    Base item class for all items in the game.
    """

    def __init__(self, item_id: str, data: Dict):
        """
        Initialize item from data dictionary.

        Args:
            item_id: Unique item identifier
            data: Item data from database
        """
        self.id = item_id
        self.name = data.get("name", "Unknown Item")
        self.description = data.get("description", "")
        self.item_type = ItemType(data.get("type", "consumable"))
        self.rarity = ItemRarity(data.get("rarity", "common"))

        # Stack properties
        self.max_stack = data.get("max_stack", 1)
        self.stackable = self.max_stack > 1

        # Value
        self.value = data.get("value", 0)  # Berries
        self.sell_value = data.get("sell_value", self.value // 2)

        # Usage
        self.consumable = data.get("consumable", False)
        self.usable_in_battle = data.get("usable_in_battle", False)
        self.usable_outside_battle = data.get("usable_outside_battle", True)

        # Effects (for consumables)
        self.effects = data.get("effects", {})

        # Icon/sprite
        self.icon = data.get("icon", None)

    def can_use(self, in_battle: bool = False) -> bool:
        """
        Check if item can be used in current context.

        Args:
            in_battle: Whether currently in battle

        Returns:
            True if usable
        """
        if in_battle:
            return self.usable_in_battle
        return self.usable_outside_battle

    def use(self, target) -> Dict:
        """
        Use the item on a target.

        Args:
            target: Character to use item on

        Returns:
            Dictionary of effects applied
        """
        if not self.consumable:
            return {}

        results = {}

        # HP restoration
        if "heal_hp" in self.effects:
            heal_amount = self.effects["heal_hp"]
            old_hp = target.current_hp
            target.heal(heal_amount)
            results["hp_healed"] = target.current_hp - old_hp

        # HP percentage restoration
        if "heal_hp_percent" in self.effects:
            percent = self.effects["heal_hp_percent"]
            heal_amount = int(target.max_hp * percent)
            old_hp = target.current_hp
            target.heal(heal_amount)
            results["hp_healed"] = target.current_hp - old_hp

        # AP restoration
        if "restore_ap" in self.effects:
            restore_amount = self.effects["restore_ap"]
            old_ap = target.current_ap
            target.restore_ap(restore_amount)
            results["ap_restored"] = target.current_ap - old_ap

        # Status cure
        if "cure_status" in self.effects:
            statuses = self.effects["cure_status"]
            results["status_cured"] = statuses

        # Revive
        if "revive" in self.effects and not target.is_alive:
            target.revive()
            hp_percent = self.effects.get("revive_hp_percent", 0.5)
            target.current_hp = int(target.max_hp * hp_percent)
            results["revived"] = True

        return results

    def get_color(self) -> tuple:
        """Get color based on rarity."""
        colors = {
            ItemRarity.COMMON: (200, 200, 200),      # Light gray
            ItemRarity.UNCOMMON: (100, 255, 100),    # Green
            ItemRarity.RARE: (100, 150, 255),        # Blue
            ItemRarity.EPIC: (200, 100, 255),        # Purple
            ItemRarity.LEGENDARY: (255, 200, 50)     # Gold
        }
        return colors.get(self.rarity, (255, 255, 255))

    def __repr__(self) -> str:
        """String representation."""
        return f"Item({self.name}, {self.item_type.value})"


class Equipment(Item):
    """
    Base equipment class for items that can be equipped.
    """

    def __init__(self, item_id: str, data: Dict):
        """
        Initialize equipment.

        Args:
            item_id: Unique item identifier
            data: Equipment data from database
        """
        super().__init__(item_id, data)

        # Equipment specific
        self.equip_slot = data.get("equip_slot", "weapon")
        self.level_requirement = data.get("level_requirement", 1)

        # Stat bonuses
        self.stat_bonuses = data.get("stat_bonuses", {})

        # Special effects
        self.special_effects = data.get("special_effects", [])
        self.passive_abilities = data.get("passive_abilities", [])

    def get_stat_bonus(self, stat_name: str) -> int:
        """
        Get bonus for a specific stat.

        Args:
            stat_name: Name of stat

        Returns:
            Bonus value
        """
        return self.stat_bonuses.get(stat_name, 0)

    def can_equip(self, character) -> bool:
        """
        Check if character can equip this.

        Args:
            character: Character attempting to equip

        Returns:
            True if can equip
        """
        return character.level >= self.level_requirement

    def apply_stats(self, character):
        """
        Apply stat bonuses to character.

        Args:
            character: Character to apply to
        """
        for stat_name, bonus in self.stat_bonuses.items():
            character.stats.add_modifier(stat_name, bonus)

    def remove_stats(self, character):
        """
        Remove stat bonuses from character.

        Args:
            character: Character to remove from
        """
        for stat_name, bonus in self.stat_bonuses.items():
            character.stats.remove_modifier(stat_name, bonus)


class Weapon(Equipment):
    """Weapon equipment."""

    def __init__(self, item_id: str, data: Dict):
        """Initialize weapon."""
        super().__init__(item_id, data)
        self.weapon_type = WeaponType(data.get("weapon_type", "sword"))
        self.attack_power = data.get("attack_power", 10)
        self.attack_speed = data.get("attack_speed", 1.0)
        self.crit_bonus = data.get("crit_bonus", 0)
        self.range = data.get("range", 1)  # 1 = melee, >1 = ranged


class Armor(Equipment):
    """Armor equipment."""

    def __init__(self, item_id: str, data: Dict):
        """Initialize armor."""
        super().__init__(item_id, data)
        self.armor_type = ArmorType(data.get("armor_type", "light"))
        self.defense = data.get("defense", 5)
        self.evasion_penalty = data.get("evasion_penalty", 0)
        self.elemental_resistances = data.get("elemental_resistances", {})


class Accessory(Equipment):
    """Accessory equipment."""

    def __init__(self, item_id: str, data: Dict):
        """Initialize accessory."""
        super().__init__(item_id, data)
        self.unique = data.get("unique", False)  # Can only equip one


class InventorySlot:
    """Single inventory slot with item and quantity."""

    def __init__(self, item: Item, quantity: int = 1):
        """
        Initialize inventory slot.

        Args:
            item: Item in this slot
            quantity: Number of items
        """
        self.item = item
        self.quantity = quantity

    def add(self, amount: int) -> int:
        """
        Add items to stack.

        Args:
            amount: Amount to add

        Returns:
            Amount that couldn't be added (overflow)
        """
        new_quantity = self.quantity + amount

        if new_quantity <= self.item.max_stack:
            self.quantity = new_quantity
            return 0
        else:
            overflow = new_quantity - self.item.max_stack
            self.quantity = self.item.max_stack
            return overflow

    def remove(self, amount: int) -> int:
        """
        Remove items from stack.

        Args:
            amount: Amount to remove

        Returns:
            Amount actually removed
        """
        if amount >= self.quantity:
            removed = self.quantity
            self.quantity = 0
            return removed
        else:
            self.quantity -= amount
            return amount

    def is_empty(self) -> bool:
        """Check if slot is empty."""
        return self.quantity <= 0

    def is_full(self) -> bool:
        """Check if slot is at max stack."""
        return self.quantity >= self.item.max_stack

    def __repr__(self) -> str:
        """String representation."""
        return f"InventorySlot({self.item.name} x{self.quantity})"


class Inventory:
    """
    Inventory management system.
    Handles item storage with stacking and limits.
    """

    def __init__(self, max_slots: int = 50):
        """
        Initialize inventory.

        Args:
            max_slots: Maximum number of slots
        """
        self.max_slots = max_slots
        self.slots: List[Optional[InventorySlot]] = []

    def add_item(self, item: Item, quantity: int = 1) -> bool:
        """
        Add item to inventory.

        Args:
            item: Item to add
            quantity: Amount to add

        Returns:
            True if fully added
        """
        remaining = quantity

        # Try to stack with existing
        if item.stackable:
            for slot in self.slots:
                if slot and slot.item.id == item.id and not slot.is_full():
                    overflow = slot.add(remaining)
                    remaining = overflow
                    if remaining == 0:
                        return True

        # Create new slots for remaining
        while remaining > 0:
            if len(self.slots) >= self.max_slots:
                return False  # Inventory full

            stack_size = min(remaining, item.max_stack)
            self.slots.append(InventorySlot(item, stack_size))
            remaining -= stack_size

        return True

    def remove_item(self, item_id: str, quantity: int = 1) -> int:
        """
        Remove item from inventory.

        Args:
            item_id: ID of item to remove
            quantity: Amount to remove

        Returns:
            Amount actually removed
        """
        removed = 0
        slots_to_remove = []

        for i, slot in enumerate(self.slots):
            if slot and slot.item.id == item_id:
                amount = min(quantity - removed, slot.quantity)
                slot.remove(amount)
                removed += amount

                if slot.is_empty():
                    slots_to_remove.append(i)

                if removed >= quantity:
                    break

        # Remove empty slots
        for i in reversed(slots_to_remove):
            self.slots.pop(i)

        return removed

    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        """
        Check if inventory has item.

        Args:
            item_id: Item to check
            quantity: Required amount

        Returns:
            True if has enough
        """
        total = 0
        for slot in self.slots:
            if slot and slot.item.id == item_id:
                total += slot.quantity
                if total >= quantity:
                    return True
        return False

    def get_item_count(self, item_id: str) -> int:
        """Get total count of an item."""
        total = 0
        for slot in self.slots:
            if slot and slot.item.id == item_id:
                total += slot.quantity
        return total

    def get_item(self, item_id: str) -> Optional[Item]:
        """Get item instance by ID."""
        for slot in self.slots:
            if slot and slot.item.id == item_id:
                return slot.item
        return None

    def get_all_items(self) -> List[InventorySlot]:
        """Get all non-empty slots."""
        return [slot for slot in self.slots if slot and not slot.is_empty()]

    def sort_by_type(self):
        """Sort inventory by item type."""
        self.slots.sort(key=lambda s: (s.item.item_type.value if s else "z"))

    def sort_by_rarity(self):
        """Sort inventory by rarity."""
        rarity_order = {
            ItemRarity.COMMON: 0,
            ItemRarity.UNCOMMON: 1,
            ItemRarity.RARE: 2,
            ItemRarity.EPIC: 3,
            ItemRarity.LEGENDARY: 4
        }
        self.slots.sort(key=lambda s: (rarity_order.get(s.item.rarity, -1) if s else -1), reverse=True)

    def is_full(self) -> bool:
        """Check if inventory is full."""
        return len(self.slots) >= self.max_slots

    def get_free_slots(self) -> int:
        """Get number of free slots."""
        return self.max_slots - len(self.slots)

    def __repr__(self) -> str:
        """String representation."""
        return f"Inventory({len(self.slots)}/{self.max_slots} slots)"
