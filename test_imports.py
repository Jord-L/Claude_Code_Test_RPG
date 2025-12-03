"""
Simple Import Test
Tests that all Phase 2 modules can be imported without errors.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.logger import init_logger, get_logger

# Initialize logger
logger = init_logger("Import_Tests", "test_logs")
logger.section("PHASE 2 IMPORT TEST")

def test_import(module_name, description):
    """Test importing a module."""
    try:
        logger.info(f"Importing {description}...")
        __import__(module_name)
        logger.info(f"  ✓ {module_name}")
        return True
    except Exception as e:
        logger.error(f"  ✗ {module_name}: {e}")
        logger.exception("Full error:")
        return False


def run_import_tests():
    """Run all import tests."""
    logger.info("Testing all Phase 2 module imports...\n")

    modules = [
        # Core
        ("utils.constants", "Constants"),
        ("utils.logger", "Logger"),

        # Entities
        ("entities.character", "Character"),
        ("entities.player", "Player"),
        ("entities.enemy", "Enemy"),
        ("entities.npc", "NPC"),

        # World
        ("world.tile", "Tile"),
        ("world.map", "Map"),
        ("world.camera", "Camera"),
        ("world.player_controller", "Player Controller"),
        ("world.island", "Island System"),
        ("world.island_factory", "Island Factory"),

        # Systems
        ("systems.sprite_manager", "Sprite Manager"),
        ("systems.party_manager", "Party Manager"),
        ("systems.item_system", "Item System"),
        ("systems.item_loader", "Item Loader"),
        ("systems.equipment_manager", "Equipment Manager"),
        ("systems.dialogue_system", "Dialogue System"),
        ("systems.shop_system", "Shop System"),
        ("systems.quest_system", "Quest System"),
        ("systems.ship_system", "Ship System"),
        ("systems.devil_fruit_extended", "Devil Fruit Extended"),
        ("systems.combat_advanced", "Advanced Combat"),
        ("systems.haki_system", "Haki System"),
        ("systems.audio_system", "Audio System"),

        # Combat
        ("combat.battle_manager", "Battle Manager"),
        ("combat.combat_action", "Combat Action"),
        ("combat.enemy_ai", "Enemy AI"),
        ("combat.turn_system", "Turn System"),

        # UI
        ("ui.panel", "Panel"),
        ("ui.button", "Button"),
        ("ui.party_menu", "Party Menu"),
        ("ui.inventory_menu", "Inventory Menu"),
        ("ui.equipment_menu", "Equipment Menu"),
        ("ui.travel_menu", "Travel Menu"),

        # States
        ("states.state", "Base State"),
        ("states.world_state", "World State"),
        ("states.battle_state", "Battle State"),

        # Utils
        ("utils.party_helpers", "Party Helpers"),
        ("utils.item_helpers", "Item Helpers"),
    ]

    results = []

    for module_name, description in modules:
        passed = test_import(module_name, description)
        results.append((module_name, description, passed))

    # Summary
    logger.separator()
    logger.section("IMPORT TEST SUMMARY")

    passed_count = sum(1 for _, _, passed in results if passed)
    total_count = len(results)

    failed_modules = [(name, desc) for name, desc, passed in results if not passed]

    if failed_modules:
        logger.error("FAILED IMPORTS:")
        for name, desc in failed_modules:
            logger.error(f"  ✗ {desc} ({name})")
    else:
        logger.info("✓ ALL IMPORTS SUCCESSFUL!")

    logger.separator()
    logger.info(f"RESULT: {passed_count}/{total_count} modules imported successfully")

    logger.info(f"\nLog file: {logger.get_session_log_path()}")

    return passed_count == total_count


if __name__ == "__main__":
    logger.info("Starting import tests...")
    logger.info(f"Python version: {sys.version}")
    logger.separator()

    success = run_import_tests()

    if success:
        logger.info("\n🎉 All modules can be imported successfully!")
        logger.info("You can now run the full test suite: python test_phase2.py")
    else:
        logger.error("\n❌ Some modules failed to import")
        logger.error("Fix import errors before running full tests")

    sys.exit(0 if success else 1)
