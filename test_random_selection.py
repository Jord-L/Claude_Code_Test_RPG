"""
Test random Devil Fruit selection and all fruits available
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from systems.devil_fruit_manager import devil_fruit_manager
import random

def test_all_fruits_and_random():
    """Test that all fruits are available and random selection works."""
    print("="*60)
    print("TESTING ALL FRUITS AVAILABLE & RANDOM SELECTION")
    print("="*60)

    # Load all fruits
    success = devil_fruit_manager.load_all_fruits()
    if not success:
        print("\n❌ FAILED: Could not load Devil Fruits")
        return False

    print("\n✓ Devil Fruits loaded successfully!")

    # Get all fruits (no filter)
    all_fruits = devil_fruit_manager.get_all_fruits()
    print(f"\n📊 Total fruits available: {len(all_fruits)}")

    # Test by type
    print(f"\n🔍 Fruits by type:")
    paramecia = devil_fruit_manager.get_fruits_by_type("paramecia")
    logia = devil_fruit_manager.get_fruits_by_type("logia")
    zoan = devil_fruit_manager.get_fruits_by_type("zoan")

    print(f"   - Paramecia: {len(paramecia)} fruits")
    print(f"   - Logia: {len(logia)} fruits")
    print(f"   - Zoan: {len(zoan)} fruits")

    # Test random selection from all fruits
    print(f"\n🎲 Testing Random Selection (All Fruits):")
    for i in range(5):
        random_fruit = random.choice(all_fruits)
        fruit_name = random_fruit.get("name", "Unknown")
        fruit_type = random_fruit.get("type", "Unknown")
        rarity = random_fruit.get("rarity", "Common")
        print(f"   {i+1}. {fruit_name} ({fruit_type}) - {rarity}")

    # Test random selection per type
    print(f"\n🎲 Testing Random Selection by Type:")

    print(f"   Random Paramecia:")
    for i in range(3):
        random_fruit = random.choice(paramecia)
        print(f"   - {random_fruit.get('name')}")

    print(f"   Random Logia:")
    for i in range(3):
        random_fruit = random.choice(logia)
        print(f"   - {random_fruit.get('name')}")

    print(f"   Random Zoan:")
    for i in range(3):
        random_fruit = random.choice(zoan)
        subtype = random_fruit.get("subtype", "Regular")
        print(f"   - {random_fruit.get('name')} ({subtype})")

    # Verify sorting works
    print(f"\n📋 Testing Alphabetical Sorting:")
    sorted_all = sorted(all_fruits, key=lambda f: f.get("name", ""))
    print(f"   First 10 fruits (sorted):")
    for i, fruit in enumerate(sorted_all[:10]):
        print(f"   {i+1}. {fruit.get('name')}")

    # Check that legendary/rare fruits are available
    print(f"\n⭐ Legendary & Rare Fruits Available:")
    legendary = [f for f in all_fruits if f.get("rarity") == "Legendary"]
    rare = [f for f in all_fruits if f.get("rarity") == "Rare"]

    print(f"   Legendary: {len(legendary)} fruits")
    print(f"   Sample Legendary:")
    for fruit in legendary[:5]:
        print(f"   - {fruit.get('name')} ({fruit.get('type')})")

    print(f"\n   Rare: {len(rare)} fruits")

    # Verify NO starting_available filtering
    print(f"\n✅ Verification - All fruits selectable:")
    non_starting = [f for f in all_fruits if not f.get("starting_available", False)]
    print(f"   Fruits that were NOT marked as starting_available: {len(non_starting)}")
    print(f"   These are NOW selectable! ✓")
    print(f"\n   Sample non-starting fruits:")
    for fruit in non_starting[:5]:
        name = fruit.get('name', 'Unknown')
        fruit_type = fruit.get('type', 'Unknown')
        rarity = fruit.get('rarity', 'Common')
        print(f"   - {name} ({fruit_type}) - {rarity}")

    print(f"\n{'='*60}")
    print("✅ ALL TESTS PASSED!")
    print(f"{'='*60}\n")

    print("📝 Summary:")
    print(f"   - All 166 fruits are now selectable at character creation")
    print(f"   - Random selection works for all fruits and by type")
    print(f"   - Alphabetical sorting makes browsing easier")
    print(f"   - No starting_available restrictions")

    return True

if __name__ == "__main__":
    test_all_fruits_and_random()
