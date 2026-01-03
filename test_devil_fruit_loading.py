"""
Test Devil Fruit loading system
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from systems.devil_fruit_manager import devil_fruit_manager

def test_loading():
    """Test loading all Devil Fruits."""
    print("="*60)
    print("TESTING DEVIL FRUIT LOADING")
    print("="*60)

    # Load all fruits
    success = devil_fruit_manager.load_all_fruits()

    if not success:
        print("\n❌ FAILED: Could not load Devil Fruits")
        return False

    print("\n✓ Devil Fruits loaded successfully!")

    # Get statistics
    stats = devil_fruit_manager.get_fruit_stats()
    print(f"\n📊 Devil Fruits Statistics:")
    print(f"   Total Fruits: {stats['total']}")
    print(f"   - Paramecia: {stats['paramecia']}")
    print(f"   - Logia: {stats['logia']}")
    print(f"   - Zoan Total: {stats['zoan_total']}")
    print(f"     - Regular: {stats['zoan_regular']}")
    print(f"     - Ancient: {stats['zoan_ancient']}")
    print(f"     - Mythical: {stats['zoan_mythical']}")
    print(f"   Starting Available: {stats['starting_available']}")

    # Check expected counts
    expected = {
        'total': 166,
        'paramecia': 100,
        'logia': 12,
        'zoan_total': 54,
        'zoan_regular': 30,
        'zoan_ancient': 13,
        'zoan_mythical': 11
    }

    print(f"\n🔍 Validation:")
    all_match = True
    for key, expected_value in expected.items():
        actual_value = stats[key]
        match = "✓" if actual_value == expected_value else "✗"
        if actual_value != expected_value:
            all_match = False
        print(f"   {match} {key}: {actual_value} (expected {expected_value})")

    # Test some specific fruits
    print(f"\n🍎 Testing specific fruits:")

    test_fruits = [
        ("gomu_gomu", "Gomu Gomu no Mi", "paramecia"),
        ("mera_mera", "Mera Mera no Mi", "logia"),
        ("neko_neko_leopard", "Neko Neko no Mi, Model: Leopard", "zoan"),
        ("tori_tori_phoenix", "Tori Tori no Mi, Model: Phoenix", "zoan"),
        ("hito_hito_nika", "Hito Hito no Mi, Model: Nika", "zoan")
    ]

    for fruit_id, expected_name, fruit_type in test_fruits:
        fruit = devil_fruit_manager.get_fruit_by_id(fruit_id)
        if fruit:
            actual_name = fruit.get("name", "Unknown")
            actual_type = fruit.get("type", "Unknown")
            match_name = "✓" if actual_name == expected_name else "✗"
            match_type = "✓" if actual_type == fruit_type else "✗"
            print(f"   {match_name} {fruit_id}: {actual_name}")
            print(f"   {match_type} Type: {actual_type}")
        else:
            print(f"   ✗ {fruit_id}: NOT FOUND")
            all_match = False

    # Test starting fruits
    print(f"\n🎮 Starting Fruits:")
    starting = devil_fruit_manager.get_starting_fruits()
    print(f"   Total starting fruits: {len(starting)}")
    print(f"   Sample starting fruits:")
    for fruit in starting[:10]:
        name = fruit.get("name", "Unknown")
        fruit_type = fruit.get("type", "Unknown")
        print(f"   - {name} ({fruit_type})")

    print(f"\n{'='*60}")
    if all_match:
        print("✅ ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED - Check output above")
    print(f"{'='*60}\n")

    return all_match

if __name__ == "__main__":
    test_loading()
