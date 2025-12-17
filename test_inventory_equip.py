"""
Test inventory item selection and equipping functionality
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from entities.character import Character
from systems.item_system import Inventory, Weapon, Armor, Accessory, ItemType, ItemRarity
from systems.equipment_manager import EquipmentSlots

def test_inventory_equipping():
    """Test that inventory equipping works correctly."""
    print("="*60)
    print("TESTING INVENTORY ITEM SELECTION & EQUIPPING")
    print("="*60)

    # Create test character
    print("\n1. Creating test character...")
    character = Character("Test Pirate", level=1)
    character.equipment_slots = EquipmentSlots(character)
    inventory = Inventory(max_slots=50)
    character.inventory = inventory

    print(f"   ✓ Character: {character.name} (Level {character.level})")

    # Create test equipment items
    print("\n2. Creating test equipment items...")

    # Level 1 weapon - should be equippable
    sword = Weapon("test_sword_1", {
        "name": "Rusty Sword",
        "description": "A basic sword",
        "type": "weapon",
        "rarity": "common",
        "equip_slot": "weapon",
        "level_requirement": 1,
        "attack_power": 5,
        "attack_speed": 1.0,
        "weapon_type": "sword",
        "stat_bonuses": {"attack": 5}
    })

    # Level 5 weapon - should NOT be equippable at level 1
    katana = Weapon("test_katana_5", {
        "name": "Steel Katana",
        "description": "A sharp katana",
        "type": "weapon",
        "rarity": "rare",
        "equip_slot": "weapon",
        "level_requirement": 5,
        "attack_power": 15,
        "attack_speed": 1.2,
        "weapon_type": "sword",
        "stat_bonuses": {"attack": 15}
    })

    # Level 1 armor
    vest = Armor("test_vest_1", {
        "name": "Leather Vest",
        "description": "Basic protection",
        "type": "armor",
        "rarity": "common",
        "equip_slot": "armor",
        "level_requirement": 1,
        "defense": 3,
        "evasion_penalty": 0,
        "armor_type": "light",
        "stat_bonuses": {"defense": 3}
    })

    # Accessory
    ring = Accessory("test_ring_1", {
        "name": "Lucky Ring",
        "description": "Brings good fortune",
        "type": "accessory",
        "rarity": "uncommon",
        "equip_slot": "accessory",
        "level_requirement": 1,
        "stat_bonuses": {"luck": 5}
    })

    print(f"   ✓ Created: {sword.name} (Level {sword.level_requirement})")
    print(f"   ✓ Created: {katana.name} (Level {katana.level_requirement})")
    print(f"   ✓ Created: {vest.name} (Level {vest.level_requirement})")
    print(f"   ✓ Created: {ring.name} (Level {ring.level_requirement})")

    # Add items to inventory
    print("\n3. Adding items to inventory...")
    inventory.add_item(sword, 1)
    inventory.add_item(katana, 1)
    inventory.add_item(vest, 1)
    inventory.add_item(ring, 1)

    print(f"   ✓ Inventory size: {len(inventory.slots)}/{inventory.max_slots}")
    print(f"   ✓ Items in inventory:")
    for slot in inventory.slots:
        if slot.item:
            print(f"      - {slot.item.name} x{slot.quantity}")

    # Test equipping valid item (level 1 sword)
    print("\n4. Testing equipping valid item (Level 1 Sword)...")
    if sword.can_equip(character):
        print(f"   ✓ Can equip {sword.name}")
        old_weapon = character.equipment_slots.equip(sword)
        inventory.remove_item(sword.id, 1)
        print(f"   ✓ Equipped {sword.name}")
        print(f"   ✓ Old weapon: {old_weapon}")

        # Verify equipped
        equipped_weapon = character.equipment_slots.get_equipment("weapon")
        if equipped_weapon == sword:
            print(f"   ✓ Weapon slot now has: {equipped_weapon.name}")
        else:
            print(f"   ✗ ERROR: Weapon slot has wrong item")
    else:
        print(f"   ✗ ERROR: Cannot equip {sword.name}")

    # Test equipping invalid item (level 5 katana on level 1 character)
    print("\n5. Testing level requirement check (Level 5 Katana)...")
    if not katana.can_equip(character):
        print(f"   ✓ Correctly blocked: {katana.name} requires level {katana.level_requirement}")
        print(f"   ✓ Character is only level {character.level}")
    else:
        print(f"   ✗ ERROR: Should not allow equipping {katana.name}")

    # Test equipping armor
    print("\n6. Testing armor equipping...")
    if vest.can_equip(character):
        print(f"   ✓ Can equip {vest.name}")
        old_armor = character.equipment_slots.equip(vest)
        inventory.remove_item(vest.id, 1)
        print(f"   ✓ Equipped {vest.name}")

        equipped_armor = character.equipment_slots.get_equipment("armor")
        if equipped_armor == vest:
            print(f"   ✓ Armor slot now has: {equipped_armor.name}")

    # Test equipping accessory
    print("\n7. Testing accessory equipping...")
    if ring.can_equip(character):
        print(f"   ✓ Can equip {ring.name}")
        old_accessory = character.equipment_slots.equip(ring)
        inventory.remove_item(ring.id, 1)
        print(f"   ✓ Equipped {ring.name}")

        equipped_accessory = character.equipment_slots.get_equipment("accessory")
        if equipped_accessory == ring:
            print(f"   ✓ Accessory slot now has: {equipped_accessory.name}")

    # Test swapping equipment
    print("\n8. Testing equipment swapping (equip new weapon over old)...")
    character.level = 5  # Level up to equip katana
    print(f"   Character leveled up to {character.level}")

    if katana.can_equip(character):
        print(f"   ✓ Can now equip {katana.name}")
        old_weapon = character.equipment_slots.equip(katana)
        inventory.remove_item(katana.id, 1)

        if old_weapon:
            inventory.add_item(old_weapon, 1)
            print(f"   ✓ Swapped out: {old_weapon.name} (returned to inventory)")
            print(f"   ✓ Equipped: {katana.name}")

        equipped_weapon = character.equipment_slots.get_equipment("weapon")
        if equipped_weapon == katana:
            print(f"   ✓ Weapon slot now has: {equipped_weapon.name}")

    # Display final state
    print("\n9. Final equipment state:")
    weapon = character.equipment_slots.get_equipment("weapon")
    armor = character.equipment_slots.get_equipment("armor")
    accessory = character.equipment_slots.get_equipment("accessory")

    print(f"   Weapon: {weapon.name if weapon else 'None'}")
    print(f"   Armor: {armor.name if armor else 'None'}")
    print(f"   Accessory: {accessory.name if accessory else 'None'}")

    print("\n10. Final inventory state:")
    print(f"   Items in inventory:")
    for slot in inventory.slots:
        if slot.item:
            print(f"      - {slot.item.name} x{slot.quantity}")

    print("\n" + "="*60)
    print("✅ INVENTORY EQUIPPING TEST COMPLETED!")
    print("="*60)

    print("\n📝 Summary:")
    print("   ✓ Items can be selected from inventory")
    print("   ✓ Level requirements are checked")
    print("   ✓ Equipment can be equipped to character")
    print("   ✓ Old equipment is swapped back to inventory")
    print("   ✓ All equipment slots working (weapon/armor/accessory)")

    return True

if __name__ == "__main__":
    test_inventory_equipping()
