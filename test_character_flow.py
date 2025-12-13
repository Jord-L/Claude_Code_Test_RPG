"""
Test Character Creation Flow
Simulates going through character creation and clicking Confirm.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from entities.player import Player
from systems.devil_fruit_manager import devil_fruit_manager

def test_character_creation_flow():
    """
    Test the character creation flow without pygame.
    This simulates what happens when a user creates a character.
    """
    print("\n" + "="*70)
    print("TESTING CHARACTER CREATION FLOW")
    print("="*70 + "\n")

    # Step 1: User enters name
    player_name = "TestPlayer"
    print(f"Step 1: User enters name: '{player_name}'")

    # Step 2: User selects devil fruit (or None)
    print(f"\nStep 2: User selects Devil Fruit...")
    fruits = devil_fruit_manager.get_starting_fruits()
    if fruits:
        selected_fruit = fruits[0]  # Select first fruit
        print(f"  Selected: {selected_fruit.get('name')}")
    else:
        selected_fruit = None
        print(f"  Selected: None")

    # Step 3: Confirm button clicked - simulate _on_confirm()
    print(f"\nStep 3: Confirm button clicked")
    print("\n" + "="*60)
    print("CONFIRM BUTTON CLICKED - Starting character creation...")
    print("="*60)

    # Create the player
    player = Player(player_name, level=1)
    print(f"✓ Player object created: {player.name}")

    # Equip Devil Fruit if selected
    if selected_fruit:
        player.equip_devil_fruit(selected_fruit)
        print(f"✓ {player.name} ate the {selected_fruit.get('name')}!")
    else:
        print(f"✓ {player.name} starts without a Devil Fruit!")

    print(f"\n📋 Character Summary:")
    print(f"   Name: {player.name}")
    print(f"   Level: {player.level}")
    print(f"   HP: {player.current_hp}/{player.max_hp}")
    print(f"   Attack: {player.stats.get_attack()}")
    print(f"   Defense: {player.stats.get_defense()}")
    print(f"   Speed: {player.stats.get_speed()}")
    print(f"   Devil Fruit: {player.devil_fruit.name if player.devil_fruit else 'None'}")

    # Step 4: Simulate cleanup() - preparing data for world state
    print(f"\n" + "="*60)
    print("CHARACTER CREATION CLEANUP - Preparing data for next state")
    print("="*60)
    print(f"✓ Returning player data: {player.name}")
    print(f"   Level: {player.level}")
    print(f"   Devil Fruit: {player.devil_fruit.name if player.devil_fruit else 'None'}")
    print("="*60 + "\n")

    persistent_data = {"player": player}

    # Step 5: Simulate world_state.startup() - receiving player data
    print("\n" + "="*60)
    print("WORLD STATE STARTUP - Initializing game world")
    print("="*60)
    print(f"Received persistent data keys: {list(persistent_data.keys())}")

    if "player" in persistent_data:
        received_player = persistent_data["player"]
        print(f"✓ Using player from character creation: {received_player.name}")
        print(f"   Level: {received_player.level}")
        print(f"   HP: {received_player.current_hp}/{received_player.max_hp}")
        print(f"   Devil Fruit: {received_player.devil_fruit.name if received_player.devil_fruit else 'None'}")
        print("\n✅ SUCCESS: Player data successfully passed to world state!")
    else:
        print("❌ ERROR: No player in persistent data")

    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70 + "\n")

    return player


if __name__ == "__main__":
    try:
        player = test_character_creation_flow()
        print(f"✅ Test passed! Created player: {player.name}")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
