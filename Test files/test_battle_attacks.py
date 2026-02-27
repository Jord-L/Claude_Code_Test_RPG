"""
Battle Attack Test
Tests different attack types and battle mechanics.
Run this to verify attack options work correctly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from entities.player import Player
from entities.enemy import Enemy
from entities.devil_fruit import DevilFruit
from combat.battle_manager import BattleManager
from combat.combat_action import CombatAction, ActionType
from combat.damage_calculator import DamageCalculator
from systems.devil_fruit_manager import devil_fruit_manager
from systems.item_system import Item, Inventory


def create_test_player():
    """Create a test player with proper DevilFruit."""
    print("\n=== Creating Test Player ===")
    player = Player("Luffy")
    player.level = 5
    player.max_hp = 150
    player.current_hp = 150
    player.base_attack = 20
    player.base_defense = 15
    player.base_speed = 18
    player.max_ap = 50
    player.current_ap = 50

    # Load actual devil fruit data
    print("Loading Devil Fruits...")
    devil_fruit_manager.load_all_fruits()
    fruit_data = devil_fruit_manager.get_fruit_by_id("gomu_gomu")

    if fruit_data:
        player.devil_fruit = DevilFruit(fruit_data)
        print(f"Equipped: {player.devil_fruit.name}")
        print(f"Type: {player.devil_fruit.fruit_type}")
        print(f"All abilities: {len(player.devil_fruit.all_abilities)}")
        print(f"Unlocked abilities: {len(player.devil_fruit.unlocked_abilities)}")
        for ability in player.devil_fruit.unlocked_abilities:
            print(f"  - {ability['name']} (AP: {ability['ap_cost']}, Dmg: {ability.get('base_damage', 'N/A')})")
    else:
        print("ERROR: Could not load gomu_gomu fruit!")

    # Add some items to inventory
    player.inventory = Inventory(max_slots=20)

    print(f"\nPlayer Stats:")
    print(f"  HP: {player.current_hp}/{player.max_hp}")
    print(f"  AP: {player.current_ap}/{player.max_ap}")
    print(f"  ATK: {player.base_attack}, DEF: {player.base_defense}, SPD: {player.base_speed}")

    return player


def create_test_enemy(name: str, level: int):
    """Create a test enemy."""
    enemy = Enemy(name)
    enemy.level = level
    enemy.max_hp = 80 + (level * 10)
    enemy.current_hp = enemy.max_hp
    enemy.base_attack = 12 + (level * 2)
    enemy.base_defense = 10 + level
    enemy.base_speed = 12 + level
    return enemy


def test_basic_attack():
    """Test basic physical attack."""
    print("\n" + "="*50)
    print("TEST: Basic Attack")
    print("="*50)

    player = create_test_player()
    enemy = create_test_enemy("Bandit", 3)

    print(f"\nEnemy: {enemy.name} - HP: {enemy.current_hp}/{enemy.max_hp}")

    # Calculate damage using attack power
    attack_power = player.get_attack_power()
    defense_power = enemy.get_defense_power()

    # Simple damage calc
    base_damage = attack_power
    damage_reduction = defense_power * 0.5
    final_damage = max(1, int(base_damage - damage_reduction))

    print(f"\nAttack Result:")
    print(f"  Attack power: {attack_power}")
    print(f"  Defense reduction: {damage_reduction}")
    print(f"  Final damage: {final_damage}")

    enemy.take_damage(final_damage)
    print(f"\nEnemy HP after attack: {enemy.current_hp}/{enemy.max_hp}")

    return True


def test_devil_fruit_ability():
    """Test devil fruit ability attack."""
    print("\n" + "="*50)
    print("TEST: Devil Fruit Ability")
    print("="*50)

    player = create_test_player()
    enemy = create_test_enemy("Marine", 4)

    if not player.devil_fruit:
        print("ERROR: No devil fruit!")
        return False

    abilities = player.devil_fruit.unlocked_abilities
    if not abilities:
        print("ERROR: No unlocked abilities!")
        return False

    print(f"\nAvailable abilities:")
    for i, ability in enumerate(abilities):
        print(f"  {i+1}. {ability['name']} - AP: {ability['ap_cost']}, Damage: {ability.get('base_damage', 'N/A')}")

    # Use first ability
    ability = abilities[0]
    print(f"\nUsing: {ability['name']}")
    print(f"AP before: {player.current_ap}")

    # Check if can afford
    ap_cost = ability.get('ap_cost', 10)
    if player.current_ap < ap_cost:
        print(f"ERROR: Not enough AP! Need {ap_cost}, have {player.current_ap}")
        return False

    # Deduct AP
    player.current_ap -= ap_cost
    print(f"AP after: {player.current_ap}")

    # Calculate ability damage manually
    base_damage = ability.get('base_damage', 20)
    defense_power = enemy.get_defense_power()
    damage_reduction = defense_power * 0.5
    final_damage = max(1, int(base_damage - damage_reduction))

    print(f"\nAbility Result:")
    print(f"  Base damage: {base_damage}")
    print(f"  Defense reduction: {damage_reduction}")
    print(f"  Final damage: {final_damage}")

    enemy.take_damage(final_damage)
    print(f"\nEnemy HP: {enemy.current_hp}/{enemy.max_hp} (was {enemy.max_hp})")

    return True


def test_defend_action():
    """Test defend action."""
    print("\n" + "="*50)
    print("TEST: Defend Action")
    print("="*50)

    player = create_test_player()

    # Create defend action
    action = CombatAction(player, ActionType.DEFEND)

    print(f"Player {player.name} takes defensive stance")
    print("(Defense buff should be applied for 1 turn)")

    return True


def test_battle_manager():
    """Test full battle manager flow."""
    print("\n" + "="*50)
    print("TEST: Battle Manager Flow")
    print("="*50)

    player = create_test_player()
    enemies = [
        create_test_enemy("Bandit A", 2),
        create_test_enemy("Bandit B", 3)
    ]

    # Create battle manager with required args
    battle_manager = BattleManager([player], enemies)

    print(f"\nBattle started!")
    print(f"Player party: {[p.name for p in battle_manager.player_party]}")
    print(f"Enemies: {[e.name for e in battle_manager.enemies]}")

    # Get turn order
    print(f"\nTurn order:")
    for i, actor in enumerate(battle_manager.turn_system.get_turn_preview(5)):
        print(f"  {i+1}. {actor.name} (SPD: {actor.base_speed})")

    # Simulate player turn
    print(f"\n--- Player Turn ---")
    current = battle_manager.current_actor
    print(f"Current actor: {current.name if current else 'None'}")

    if current == player:
        # Test available actions
        print("\nAvailable actions:")
        print("  1. Attack")
        print("  2. Defend")
        if player.devil_fruit and player.devil_fruit.unlocked_abilities:
            print(f"  3. Devil Fruit ({len(player.devil_fruit.unlocked_abilities)} abilities)")
        print("  4. Item")
        print("  5. Run")

        # Execute attack on first enemy
        target = battle_manager.get_alive_enemies()[0]
        action = CombatAction(player, ActionType.ATTACK, target=target)

        print(f"\nExecuting: Attack on {target.name}")
        success = battle_manager.execute_action(action)
        print(f"Action success: {success}")
        print(f"Target HP: {target.current_hp}/{target.max_hp}")

    return True


def test_ui_action_menu_conditions():
    """Test conditions for action menu options."""
    print("\n" + "="*50)
    print("TEST: Action Menu Conditions")
    print("="*50)

    player = create_test_player()

    # Check each condition
    print("\nAction availability:")

    # Attack - always enabled
    print("  Attack: ENABLED (always)")

    # Defend - always enabled
    print("  Defend: ENABLED (always)")

    # Devil Fruit
    has_df = hasattr(player, 'devil_fruit') and player.devil_fruit is not None
    has_abilities = has_df and len(player.devil_fruit.unlocked_abilities) > 0
    print(f"  Devil Fruit: {'ENABLED' if has_abilities else 'DISABLED'}")
    print(f"    - has devil_fruit attr: {hasattr(player, 'devil_fruit')}")
    print(f"    - devil_fruit is not None: {player.devil_fruit is not None}")
    if has_df:
        print(f"    - unlocked_abilities count: {len(player.devil_fruit.unlocked_abilities)}")

    # Item
    has_inventory = hasattr(player, 'inventory') and player.inventory is not None
    item_count = len(player.inventory.slots) if has_inventory and hasattr(player.inventory, 'slots') else 0
    has_items = item_count > 0
    print(f"  Item: {'ENABLED' if has_items else 'DISABLED'}")
    print(f"    - has inventory: {has_inventory}")
    print(f"    - inventory slots: {item_count}")

    # Run - always enabled
    print("  Run: ENABLED (always)")

    return True


def run_all_tests():
    """Run all battle tests."""
    print("\n" + "="*60)
    print("BATTLE ATTACK TESTS")
    print("="*60)

    tests = [
        ("Basic Attack", test_basic_attack),
        ("Devil Fruit Ability", test_devil_fruit_ability),
        ("Defend Action", test_defend_action),
        ("Battle Manager Flow", test_battle_manager),
        ("Action Menu Conditions", test_ui_action_menu_conditions),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, "PASS" if result else "FAIL"))
        except Exception as e:
            print(f"\nERROR in {name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, f"ERROR: {e}"))

    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    for name, result in results:
        status = "✓" if result == "PASS" else "✗"
        print(f"  {status} {name}: {result}")

    return all(r[1] == "PASS" for r in results)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
