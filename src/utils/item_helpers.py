"""
Item Helper Functions
Utility functions for initializing and managing items.
"""

from systems.item_system import Inventory
from systems.item_loader import load_item


def add_starter_items(inventory: Inventory) -> None:
    """
    Add starter items to inventory for testing/demo purposes.

    Args:
        inventory: Inventory to add items to
    """
    # Consumables for survival
    health_potion_small = load_item("health_potion_small")
    if health_potion_small:
        inventory.add_item(health_potion_small, 5)
        print(f"Added 5x {health_potion_small.name}")

    health_potion_medium = load_item("health_potion_medium")
    if health_potion_medium:
        inventory.add_item(health_potion_medium, 3)
        print(f"Added 3x {health_potion_medium.name}")

    ap_potion = load_item("ap_potion")
    if ap_potion:
        inventory.add_item(ap_potion, 3)
        print(f"Added 3x {ap_potion.name}")

    meat = load_item("meat")
    if meat:
        inventory.add_item(meat, 2)
        print(f"Added 2x {meat.name}")

    # One revive potion for emergencies
    revive_potion = load_item("revive_potion")
    if revive_potion:
        inventory.add_item(revive_potion, 1)
        print(f"Added 1x {revive_potion.name}")

    # Basic equipment for party members
    wooden_sword = load_item("wooden_sword")
    if wooden_sword:
        inventory.add_item(wooden_sword, 2)
        print(f"Added 2x {wooden_sword.name}")

    leather_vest = load_item("leather_vest")
    if leather_vest:
        inventory.add_item(leather_vest, 2)
        print(f"Added 2x {leather_vest.name}")

    # One rare item to make it exciting
    steel_katana = load_item("steel_katana")
    if steel_katana:
        inventory.add_item(steel_katana, 1)
        print(f"Added 1x {steel_katana.name}")

    print(f"Starter items added! Total slots used: {len(inventory.slots)}/{inventory.max_slots}")


def give_item_reward(inventory: Inventory, item_id: str, quantity: int = 1) -> bool:
    """
    Give item as a reward (from quest, battle, etc.).

    Args:
        inventory: Inventory to add to
        item_id: Item ID to give
        quantity: Amount to give

    Returns:
        True if successfully added
    """
    item = load_item(item_id)
    if not item:
        print(f"Item {item_id} not found!")
        return False

    success = inventory.add_item(item, quantity)
    if success:
        print(f"Received {quantity}x {item.name}!")
    else:
        print(f"Inventory full! Could not receive {item.name}")

    return success


def sell_items(inventory: Inventory, item_id: str, quantity: int = 1) -> int:
    """
    Sell items from inventory and return berries earned.

    Args:
        inventory: Inventory to sell from
        item_id: Item ID to sell
        quantity: Amount to sell

    Returns:
        Berries earned
    """
    # Get item to check sell value
    item = inventory.get_item(item_id)
    if not item:
        print(f"Don't have {item_id} to sell!")
        return 0

    # Check if have enough
    if not inventory.has_item(item_id, quantity):
        print(f"Don't have {quantity}x {item.name}!")
        return 0

    # Remove items
    removed = inventory.remove_item(item_id, quantity)

    # Calculate berries
    berries = removed * item.sell_value

    print(f"Sold {removed}x {item.name} for {berries} Berries!")
    return berries


def get_inventory_summary(inventory: Inventory) -> str:
    """
    Get a text summary of the inventory.

    Args:
        inventory: Inventory to summarize

    Returns:
        Formatted summary string
    """
    lines = [
        "=== INVENTORY ===",
        f"Slots: {len(inventory.slots)}/{inventory.max_slots}",
        ""
    ]

    if len(inventory.slots) == 0:
        lines.append("Empty")
    else:
        # Group by type
        consumables = []
        weapons = []
        armor = []
        accessories = []

        for slot in inventory.get_all_items():
            item = slot.item
            qty_str = f"x{slot.quantity}" if slot.quantity > 1 else ""
            item_str = f"  - {item.name} {qty_str} ({item.rarity.value})"

            if item.item_type.value == "consumable":
                consumables.append(item_str)
            elif item.item_type.value == "weapon":
                weapons.append(item_str)
            elif item.item_type.value == "armor":
                armor.append(item_str)
            elif item.item_type.value == "accessory":
                accessories.append(item_str)

        if consumables:
            lines.append("Consumables:")
            lines.extend(consumables)
            lines.append("")

        if weapons:
            lines.append("Weapons:")
            lines.extend(weapons)
            lines.append("")

        if armor:
            lines.append("Armor:")
            lines.extend(armor)
            lines.append("")

        if accessories:
            lines.append("Accessories:")
            lines.extend(accessories)

    return "\n".join(lines)
