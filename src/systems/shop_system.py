"""
Shop System
Allows buying and selling items at shops.
"""

from typing import List, Dict, Tuple, Optional
from systems.item_system import Item, Inventory
from systems.item_loader import load_item


class Shop:
    """Shop that buys and sells items."""

    def __init__(self, shop_id: str, name: str):
        """Initialize shop."""
        self.shop_id = shop_id
        self.name = name
        self.inventory: List[Tuple[str, int]] = []  # [(item_id, stock)]
        self.buy_rate = 1.0  # Price multiplier for buying
        self.sell_rate = 0.5  # Price multiplier for selling

    def add_item(self, item_id: str, stock: int = 99):
        """Add item to shop inventory."""
        self.inventory.append((item_id, stock))

    def get_items(self) -> List[Item]:
        """Get list of items for sale."""
        items = []
        for item_id, stock in self.inventory:
            item = load_item(item_id)
            if item:
                items.append(item)
        return items

    def buy_item(self, item_id: str, quantity: int, player_berries: int, player_inventory: Inventory) -> Dict:
        """
        Player buys item from shop.

        Returns:
            Result dictionary with success status and message
        """
        item = load_item(item_id)
        if not item:
            return {"success": False, "message": "Item not found"}

        cost = int(item.value * self.buy_rate * quantity)

        if player_berries < cost:
            return {"success": False, "message": "Not enough berries!"}

        if player_inventory.add_item(item, quantity):
            return {
                "success": True,
                "cost": cost,
                "item": item,
                "quantity": quantity
            }
        else:
            return {"success": False, "message": "Inventory full!"}

    def sell_item(self, item_id: str, quantity: int, player_inventory: Inventory) -> Dict:
        """
        Player sells item to shop.

        Returns:
            Result dictionary with success status and earnings
        """
        # Get item from player inventory
        item = player_inventory.get_item(item_id)
        if not item:
            return {"success": False, "message": "You don't have that item"}

        if not player_inventory.has_item(item_id, quantity):
            return {"success": False, "message": "Not enough items"}

        # Calculate sell price
        earnings = int(item.sell_value * self.sell_rate * quantity)

        # Remove from inventory
        removed = player_inventory.remove_item(item_id, quantity)

        return {
            "success": True,
            "earnings": earnings,
            "item": item,
            "quantity": removed
        }


def create_default_shops() -> Dict[str, Shop]:
    """Create default game shops."""
    shops = {}

    # Mira's Bar (Foosha Village)
    makino_bar = Shop("makino_bar", "Mira's Bar")
    makino_bar.add_item("health_potion_small", 99)
    makino_bar.add_item("health_potion_medium", 50)
    makino_bar.add_item("meat", 20)
    shops["makino_bar"] = makino_bar

    # Shell Town Weapons
    shell_weapons = Shop("shell_weapons", "Weapons Dealer")
    shell_weapons.add_item("wooden_sword", 10)
    shell_weapons.add_item("iron_sword", 5)
    shell_weapons.add_item("pistol", 3)
    shops["shell_weapons"] = shell_weapons

    # Loguetown Weapons
    loguetown_weapons = Shop("loguetown_weapons", "Ippon-Matsu's Weapons")
    loguetown_weapons.add_item("steel_katana", 3)
    loguetown_weapons.add_item("iron_sword", 10)
    loguetown_weapons.add_item("combat_boots", 5)
    shops["loguetown_weapons"] = loguetown_weapons

    # Loguetown Armor
    loguetown_armor = Shop("loguetown_armor", "Armor Shop")
    loguetown_armor.add_item("iron_breastplate", 5)
    loguetown_armor.add_item("steel_plate", 2)
    loguetown_armor.add_item("pirate_coat", 3)
    loguetown_armor.add_item("leather_vest", 10)
    shops["loguetown_armor"] = loguetown_armor

    # Baratie Food
    baratie_food = Shop("baratie_food", "Baratie Restaurant")
    baratie_food.add_item("meat", 99)
    baratie_food.add_item("health_potion_large", 20)
    baratie_food.add_item("ap_potion", 15)
    shops["baratie_food"] = baratie_food

    return shops
