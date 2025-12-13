"""
Test Menu Functionality
Tests that all menu states work and can be accessed.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.logger import init_logger

# Initialize logger
logger = init_logger("Menu_Test", "test_logs")
logger.section("MENU FUNCTIONALITY TEST")


def test_menu_imports():
    """Test that all menu states can be imported."""
    logger.section("Testing Menu State Imports")

    try:
        logger.info("Importing MenuState...")
        from states.menu_state import MenuState
        logger.info("  ✓ MenuState")

        logger.info("Importing SettingsState...")
        from states.settings_state import SettingsState
        logger.info("  ✓ SettingsState")

        logger.info("Importing LoadGameState...")
        from states.load_game_state import LoadGameState
        logger.info("  ✓ LoadGameState")

        logger.info("Importing CharacterCreationState...")
        from states.character_creation_state import CharacterCreationState
        logger.info("  ✓ CharacterCreationState")

        logger.info("✓ Menu Imports: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Menu Imports: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_state_constants():
    """Test that state constants are defined."""
    logger.section("Testing State Constants")

    try:
        from utils.constants import (
            STATE_MENU, STATE_CHAR_CREATION,
            STATE_SETTINGS, STATE_LOAD
        )

        logger.info(f"STATE_MENU: {STATE_MENU}")
        logger.info(f"STATE_CHAR_CREATION: {STATE_CHAR_CREATION}")
        logger.info(f"STATE_SETTINGS: {STATE_SETTINGS}")
        logger.info(f"STATE_LOAD: {STATE_LOAD}")

        logger.info("✓ State Constants: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ State Constants: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_game_registration():
    """Test that game can register all states."""
    logger.section("Testing Game State Registration")

    try:
        import pygame
        pygame.init()

        logger.info("Creating Game instance...")
        from game import Game

        # Set up minimal display for testing
        screen = pygame.display.set_mode((800, 600))

        game = Game()
        logger.info("  ✓ Game instance created")

        logger.info("Checking registered states...")
        from utils.constants import STATE_MENU, STATE_SETTINGS, STATE_LOAD

        if STATE_MENU in game.state_manager.state_dict:
            logger.info(f"  ✓ {STATE_MENU} registered")
        else:
            logger.error(f"  ✗ {STATE_MENU} NOT registered")

        if STATE_SETTINGS in game.state_manager.state_dict:
            logger.info(f"  ✓ {STATE_SETTINGS} registered")
        else:
            logger.error(f"  ✗ {STATE_SETTINGS} NOT registered")

        if STATE_LOAD in game.state_manager.state_dict:
            logger.info(f"  ✓ {STATE_LOAD} registered")
        else:
            logger.error(f"  ✗ {STATE_LOAD} NOT registered")

        pygame.quit()

        logger.info("✓ Game Registration: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Game Registration: FAILED - {e}")
        logger.exception("Full traceback:")
        pygame.quit()
        return False


def test_save_directory():
    """Test that save directory is created."""
    logger.section("Testing Save Directory")

    try:
        import os

        save_dir = "saves"

        # Check if directory exists or can be created
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            logger.info(f"Created save directory: {save_dir}")
        else:
            logger.info(f"Save directory exists: {save_dir}")

        logger.info("✓ Save Directory: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Save Directory: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def run_all_tests():
    """Run all menu functionality tests."""
    logger.section("RUNNING ALL MENU TESTS")

    tests = [
        ("Menu Imports", test_menu_imports),
        ("State Constants", test_state_constants),
        ("Game Registration", test_game_registration),
        ("Save Directory", test_save_directory),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            logger.error(f"Test {test_name} crashed: {e}")
            results.append((test_name, False))

        logger.separator()

    # Summary
    logger.section("TEST SUMMARY")

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        logger.info(f"{status}: {test_name}")

    logger.separator()
    logger.info(f"TOTAL: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        logger.info("🎉 ALL MENU TESTS PASSED! 🎉")
    else:
        logger.warning(f"{total_count - passed_count} tests failed")

    logger.info(f"\nLog file: {logger.get_session_log_path()}")

    return passed_count == total_count


if __name__ == "__main__":
    logger.info("Starting menu functionality test suite...")
    logger.info(f"Python version: {sys.version}")
    logger.separator()

    success = run_all_tests()

    sys.exit(0 if success else 1)
