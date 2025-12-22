"""
Item Loader
Loads items from definitions and creates item instances.
"""

from typing import Dict, Optional
from systems.item_system import Item, Weapon, Armor, Accessory, ItemType


class ItemDatabase:
    """
    Item database with predefined items.
    In a full game, this would load from JSON files.
    """

    # Consumables
    CONSUMABLES = {
        "health_potion_small": {
            "name": "Small Health Potion",
            "description": "Restores 50 HP",
            "type": "consumable",
            "rarity": "common",
            "max_stack": 99,
            "value": 50,
            "consumable": True,
            "usable_in_battle": True,
            "effects": {"heal_hp": 50},
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb1.png"
        },
        "health_potion_medium": {
            "name": "Health Potion",
            "description": "Restores 150 HP",
            "type": "consumable",
            "rarity": "uncommon",
            "max_stack": 99,
            "value": 150,
            "consumable": True,
            "usable_in_battle": True,
            "effects": {"heal_hp": 150},
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb2.png"
        },
        "health_potion_large": {
            "name": "Large Health Potion",
            "description": "Restores 300 HP",
            "type": "consumable",
            "rarity": "rare",
            "max_stack": 99,
            "value": 300,
            "consumable": True,
            "usable_in_battle": True,
            "effects": {"heal_hp": 300},
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb3.png"
        },
        "ap_potion": {
            "name": "AP Potion",
            "description": "Restores 50 AP",
            "type": "consumable",
            "rarity": "uncommon",
            "max_stack": 99,
            "value": 100,
            "consumable": True,
            "usable_in_battle": True,
            "effects": {"restore_ap": 50},
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb10.png"
        },
        "revive_potion": {
            "name": "Phoenix Down",
            "description": "Revives fallen ally with 50% HP",
            "type": "consumable",
            "rarity": "rare",
            "max_stack": 10,
            "value": 500,
            "consumable": True,
            "usable_in_battle": True,
            "effects": {"revive": True, "revive_hp_percent": 0.5},
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb20.png"
        },
        "meat": {
            "name": "Sea King Meat",
            "description": "Restores 50% HP. Alex's favorite!",
            "type": "consumable",
            "rarity": "uncommon",
            "max_stack": 20,
            "value": 200,
            "consumable": True,
            "usable_in_battle": False,
            "usable_outside_battle": True,
            "effects": {"heal_hp_percent": 0.5},
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb50.png"
        }
    }

    # Weapons
    WEAPONS = {
        "wooden_sword": {
            "name": "Wooden Sword",
            "description": "A basic training sword",
            "type": "weapon",
            "equip_slot": "weapon",
            "rarity": "common",
            "value": 100,
            "weapon_type": "sword",
            "attack_power": 10,
            "attack_speed": 1.0,
            "level_requirement": 1,
            "stat_bonuses": {"strength": 2},
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb100.png"
        },
        "iron_sword": {
            "name": "Iron Sword",
            "description": "A reliable iron blade",
            "type": "weapon",
            "equip_slot": "weapon",
            "rarity": "uncommon",
            "value": 500,
            "weapon_type": "sword",
            "attack_power": 25,
            "attack_speed": 1.0,
            "level_requirement": 3,
            "stat_bonuses": {"strength": 5, "skill": 2},
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb101.png"
        },
        "steel_katana": {
            "name": "Steel Katana",
            "description": "A finely crafted katana",
            "type": "weapon",
            "equip_slot": "weapon",
            "rarity": "rare",
            "value": 2000,
            "weapon_type": "sword",
            "attack_power": 40,
            "attack_speed": 1.2,
            "crit_bonus": 5,
            "level_requirement": 7,
            "stat_bonuses": {"strength": 8, "skill": 5, "speed": 3},
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb102.png"
        },
        "flintlock_pistol": {
            "name": "Flintlock Pistol",
            "description": "A reliable firearm",
            "type": "weapon",
            "equip_slot": "weapon",
            "rarity": "uncommon",
            "value": 800,
            "weapon_type": "gun",
            "attack_power": 30,
            "attack_speed": 0.8,
            "range": 3,
            "level_requirement": 4,
            "stat_bonuses": {"skill": 6, "speed": 2},
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb120.png"
        },
        "combat_boots": {
            "name": "Combat Boots",
            "description": "Reinforced boots for powerful kicks",
            "type": "weapon",
            "equip_slot": "weapon",
            "rarity": "uncommon",
            "value": 600,
            "weapon_type": "boots",
            "attack_power": 22,
            "attack_speed": 1.3,
            "level_requirement": 3,
            "stat_bonuses": {"strength": 4, "speed": 6},
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb400.png"
        }
    }

    # Armor
    ARMOR = {
        "leather_vest": {
            "name": "Leather Vest",
            "description": "Basic leather protection",
            "type": "armor",
            "equip_slot": "armor",
            "rarity": "common",
            "value": 150,
            "armor_type": "light",
            "defense": 8,
            "evasion_penalty": 0,
            "level_requirement": 1,
            "stat_bonuses": {"defense": 3},
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb200.png"
        },
        "iron_breastplate": {
            "name": "Iron Breastplate",
            "description": "Sturdy iron armor",
            "type": "armor",
            "equip_slot": "armor",
            "rarity": "uncommon",
            "value": 700,
            "armor_type": "medium",
            "defense": 18,
            "evasion_penalty": -2,
            "level_requirement": 4,
            "stat_bonuses": {"defense": 7, "endurance": 3},
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb201.png"
        },
        "steel_plate": {
            "name": "Steel Plate Armor",
            "description": "Heavy steel protection",
            "type": "armor",
            "equip_slot": "armor",
            "rarity": "rare",
            "value": 2500,
            "armor_type": "heavy",
            "defense": 30,
            "evasion_penalty": -5,
            "level_requirement": 8,
            "stat_bonuses": {"defense": 12, "endurance": 8},
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb202.png"
        },
        "pirate_coat": {
            "name": "Pirate Captain's Coat",
            "description": "A stylish coat worn by captains",
            "type": "armor",
            "equip_slot": "armor",
            "rarity": "rare",
            "value": 1500,
            "armor_type": "clothing",
            "defense": 15,
            "evasion_penalty": 0,
            "level_requirement": 6,
            "stat_bonuses": {"defense": 5, "charisma": 8, "will": 4},
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb220.png"
        }
    }

    # Accessories
    ACCESSORIES = {
        "strength_ring": {
            "name": "Ring of Strength",
            "description": "Increases physical power",
            "type": "accessory",
            "equip_slot": "accessory",
            "rarity": "uncommon",
            "value": 1000,
            "level_requirement": 1,
            "stat_bonuses": {"strength": 5},
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb300.png"
        },
        "speed_boots": {
            "name": "Boots of Speed",
            "description": "Enhances movement and reflexes",
            "type": "accessory",
            "equip_slot": "accessory",
            "rarity": "rare",
            "value": 1500,
            "level_requirement": 5,
            "stat_bonuses": {"speed": 8, "skill": 3},
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb301.png"
        },
        "lucky_charm": {
            "name": "Lucky Charm",
            "description": "Increases critical hit rate",
            "type": "accessory",
            "equip_slot": "accessory",
            "rarity": "rare",
            "value": 2000,
            "level_requirement": 5,
            "stat_bonuses": {"skill": 5},
            "special_effects": ["crit_rate_+5"],
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb302.png"
        },
        "eternal_log_pose": {
            "name": "Eternal Log Pose",
            "description": "A mysterious navigation device",
            "type": "accessory",
            "equip_slot": "accessory",
            "rarity": "legendary",
            "value": 10000,
            "unique": True,
            "level_requirement": 10,
            "stat_bonuses": {"will": 10, "charisma": 5},
            "special_effects": ["no_random_encounters"],
            "icon": "Free - Raven Fantasy Icons/Free - Raven Fantasy Icons/Separated Files/32x32/fb350.png"
        }
    }


class ItemLoader:
    """Loads and creates item instances."""

    def __init__(self):
        """Initialize item loader."""
        self._item_cache: Dict[str, Item] = {}

    def load_item(self, item_id: str) -> Optional[Item]:
        """
        Load an item by ID.

        Args:
            item_id: Item identifier

        Returns:
            Item instance or None if not found
        """
        # Check cache
        if item_id in self._item_cache:
            return self._item_cache[item_id]

        # Look in all databases
        data = None

        if item_id in ItemDatabase.CONSUMABLES:
            data = ItemDatabase.CONSUMABLES[item_id]
        elif item_id in ItemDatabase.WEAPONS:
            data = ItemDatabase.WEAPONS[item_id]
        elif item_id in ItemDatabase.ARMOR:
            data = ItemDatabase.ARMOR[item_id]
        elif item_id in ItemDatabase.ACCESSORIES:
            data = ItemDatabase.ACCESSORIES[item_id]

        if not data:
            print(f"Item {item_id} not found in database")
            return None

        # Create appropriate item type
        item = self._create_item(item_id, data)

        # Cache it
        if item:
            self._item_cache[item_id] = item

        return item

    def _create_item(self, item_id: str, data: Dict) -> Optional[Item]:
        """
        Create item instance from data.

        Args:
            item_id: Item ID
            data: Item data dictionary

        Returns:
            Item instance
        """
        item_type = data.get("type", "consumable")

        if item_type == "weapon":
            return Weapon(item_id, data)
        elif item_type == "armor":
            return Armor(item_id, data)
        elif item_type == "accessory":
            return Accessory(item_id, data)
        else:
            return Item(item_id, data)

    def get_all_item_ids(self) -> list:
        """Get list of all item IDs."""
        all_items = []
        all_items.extend(ItemDatabase.CONSUMABLES.keys())
        all_items.extend(ItemDatabase.WEAPONS.keys())
        all_items.extend(ItemDatabase.ARMOR.keys())
        all_items.extend(ItemDatabase.ACCESSORIES.keys())
        return all_items

    def get_items_by_type(self, item_type: str) -> list:
        """
        Get all items of a specific type.

        Args:
            item_type: Type to filter by

        Returns:
            List of item IDs
        """
        if item_type == "consumable":
            return list(ItemDatabase.CONSUMABLES.keys())
        elif item_type == "weapon":
            return list(ItemDatabase.WEAPONS.keys())
        elif item_type == "armor":
            return list(ItemDatabase.ARMOR.keys())
        elif item_type == "accessory":
            return list(ItemDatabase.ACCESSORIES.keys())
        return []


# Global item loader instance
_item_loader = None


def get_item_loader() -> ItemLoader:
    """Get global item loader instance."""
    global _item_loader
    if _item_loader is None:
        _item_loader = ItemLoader()
    return _item_loader


def load_item(item_id: str) -> Optional[Item]:
    """
    Convenience function to load an item.

    Args:
        item_id: Item ID

    Returns:
        Item instance
    """
    return get_item_loader().load_item(item_id)
