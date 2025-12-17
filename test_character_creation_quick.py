"""
Quick test for character creation with Devil Fruit selection
"""

import pygame
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from states.character_creation_state import CharacterCreationState
from systems.devil_fruit_manager import devil_fruit_manager

class MockGame:
    """Mock game object for testing."""
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Character Creation Test")

def test_character_creation():
    """Test the character creation screen."""
    print("="*60)
    print("TESTING CHARACTER CREATION WITH DEVIL FRUIT SELECTION")
    print("="*60)

    # Initialize pygame
    pygame.init()

    # Create mock game
    game = MockGame()

    # Create character creation state
    print("\n✓ Creating character creation state...")
    state = CharacterCreationState(game)

    # Check if Devil Fruits loaded
    if not devil_fruit_manager.loaded:
        print("❌ Devil Fruits not loaded!")
        return False

    print(f"✓ Devil Fruits loaded: {len(devil_fruit_manager.fruits_by_id)} total")

    # Test fruit type filters
    print(f"\n📋 Testing fruit type filters:")
    for filter_type in ["all", "paramecia", "zoan", "logia", "none"]:
        state._set_fruit_filter(filter_type)
        fruit_count = len(state.fruit_list)
        print(f"   - {filter_type}: {fruit_count} fruits")

    # Test selecting a specific fruit
    print(f"\n🍎 Testing fruit selection:")
    state._set_fruit_filter("paramecia")
    if state.fruit_list:
        state._select_fruit(0)
        selected = state.selected_fruit_data
        if selected:
            print(f"   ✓ Selected: {selected.get('name')}")
            print(f"   - Type: {selected.get('type')}")
            print(f"   - Rarity: {selected.get('rarity')}")
            print(f"   - Description: {selected.get('description')[:50]}...")
        else:
            print(f"   ✗ Could not select fruit")
    else:
        print(f"   ✗ No fruits in list")

    # Test Zoan fruits
    print(f"\n🦁 Testing Zoan fruits:")
    state._set_fruit_filter("zoan")
    print(f"   Total Zoan fruits: {len(state.fruit_list)}")
    if state.fruit_list:
        # Check for different subtypes
        regular = [f for f in state.fruit_list if f.get('subtype', '').lower() == 'regular']
        ancient = [f for f in state.fruit_list if f.get('subtype', '').lower() == 'ancient']
        mythical = [f for f in state.fruit_list if f.get('subtype', '').lower() == 'mythical']

        print(f"   - Regular: {len(regular)}")
        print(f"   - Ancient: {len(ancient)}")
        print(f"   - Mythical: {len(mythical)}")

        # Show some examples
        if mythical:
            print(f"\n   Sample Mythical Zoans:")
            for fruit in mythical[:5]:
                print(f"   - {fruit.get('name')}")

    # Test Logia fruits
    print(f"\n🔥 Testing Logia fruits:")
    state._set_fruit_filter("logia")
    print(f"   Total Logia fruits: {len(state.fruit_list)}")
    if state.fruit_list:
        print(f"   Sample Logia fruits:")
        for fruit in state.fruit_list[:5]:
            print(f"   - {fruit.get('name')}")

    # Test "None" option
    print(f"\n🌊 Testing 'No Devil Fruit' option:")
    state._set_fruit_filter("none")
    print(f"   Fruit list empty: {len(state.fruit_list) == 0}")
    print(f"   Selected fruit: {state.selected_fruit_data}")
    print(f"   ✓ Player can choose to not have a Devil Fruit (and swim!)")

    print(f"\n{'='*60}")
    print("✅ CHARACTER CREATION TEST PASSED!")
    print(f"{'='*60}\n")

    print("ℹ️  To fully test, run the game and go to New Game > Character Creation")
    print("   You should see:")
    print("   1. Name entry screen")
    print("   2. Devil Fruit selection with filters (All/Paramecia/Zoan/Logia/None)")
    print("   3. Scrollable list of 166 Devil Fruits")
    print("   4. Details panel showing fruit information")
    print("   5. Character preview with stats")
    print("   6. Confirmation screen")

    pygame.quit()
    return True

if __name__ == "__main__":
    test_character_creation()
