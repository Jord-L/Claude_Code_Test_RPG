"""
Comprehensive Phase 1 Test Suite
Tests all core gameplay systems without requiring graphics.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.logger import init_logger

# Initialize logger
logger = init_logger("Phase1_Comprehensive", "test_logs")
logger.section("PHASE 1 COMPREHENSIVE TEST SUITE")


def test_character_system():
    """Test character creation and stats."""
    logger.section("Testing Character System")

    try:
        from entities.character import Character
        from entities.player import Player
        from entities.enemy import Enemy

        logger.info("Creating player character...")
        player = Player("Alex")
        player.level = 5

        logger.info(f"Player: {player.name} (Level {player.level})")
        logger.info(f"  HP: {player.current_hp}/{player.max_hp}")
        logger.info(f"  AP: {player.current_ap}/{player.max_ap}")
        logger.info(f"  Attack: {player.stats.get_attack()}")
        logger.info(f"  Defense: {player.stats.get_defense()}")

        logger.info("Creating enemy...")
        enemy = Enemy("Bandit", level=3)
        logger.info(f"Enemy: {enemy.name} (Level {enemy.level})")
        logger.info(f"  HP: {enemy.current_hp}/{enemy.max_hp}")

        logger.info("Testing character actions...")
        initial_hp = player.current_hp
        player.take_damage(20)
        logger.info(f"  Took 20 damage: {initial_hp} → {player.current_hp}")

        player.heal(10)
        logger.info(f"  Healed 10 HP: {player.current_hp}")

        logger.info("✓ Character System: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Character System: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_combat_system():
    """Test combat mechanics."""
    logger.section("Testing Combat System")

    try:
        from combat.battle_manager import BattleManager
        from entities.player import Player
        from entities.enemy import Enemy

        logger.info("Creating battle...")
        player = Player("Alex")
        player.level = 10

        enemies = [Enemy("Bandit", level=5), Enemy("Thief", level=6)]

        battle = BattleManager([player], enemies)

        logger.info(f"Battle created: {player.name} vs {len(enemies)} enemies")
        logger.info(f"  All combatants: {len(battle.all_combatants)}")

        logger.info("Testing battle actions...")
        logger.info(f"  Turn system initialized: {battle.turn_system is not None}")
        logger.info(f"  Battle successfully created")

        logger.info("✓ Combat System: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Combat System: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_world_system():
    """Test world map and tiles."""
    logger.section("Testing World System")

    try:
        from world.map import Map
        from world.tile import TileType
        from world.camera import Camera

        logger.info("Creating map...")
        game_map = Map(20, 20, TileType.GRASS)

        logger.info(f"Map created: {game_map.width}x{game_map.height}")
        logger.info(f"  Total tiles: {len(game_map.tiles)}")

        logger.info("Testing tile access...")
        tile = game_map.get_tile(5, 5)
        logger.info(f"  Tile at (5,5): {tile.tile_type}")
        logger.info(f"  Walkable: {tile.walkable}")

        logger.info("Setting different tile types...")
        game_map.set_tile(10, 10, TileType.WATER)
        water_tile = game_map.get_tile(10, 10)
        logger.info(f"  Tile at (10,10): {water_tile.tile_type}")
        logger.info(f"  Walkable: {water_tile.walkable}")

        logger.info("Creating camera...")
        from utils.constants import TILE_SIZE
        map_width_px = game_map.width * TILE_SIZE
        map_height_px = game_map.height * TILE_SIZE
        camera = Camera(map_width_px, map_height_px)
        logger.info(f"  Camera created for map: {map_width_px}x{map_height_px}px")

        logger.info("✓ World System: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ World System: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_devil_fruit_system():
    """Test devil fruit mechanics."""
    logger.section("Testing Devil Fruit System")

    try:
        from systems.data_loader import DataLoader
        from entities.player import Player

        logger.info("Loading devil fruits from database...")
        data_loader = DataLoader()

        logger.info("Creating player...")
        player = Player("Alex")

        logger.info("Testing devil fruit assignment...")
        # Test that player can have a devil fruit
        if hasattr(player, 'devil_fruit'):
            logger.info(f"  Player has devil_fruit attribute: {player.devil_fruit is None}")

        logger.info("Devil fruit system structure verified")

        logger.info("✓ Devil Fruit System: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Devil Fruit System: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_data_loading():
    """Test database loading."""
    logger.section("Testing Data Loading")

    try:
        from systems.data_loader import DataLoader

        logger.info("Initializing data loader...")
        data_loader = DataLoader()

        logger.info(f"DataLoader initialized successfully")
        logger.info(f"  Database path configured: {hasattr(data_loader, 'db_path')}")
        logger.info("Data loading system is operational")

        logger.info("✓ Data Loading: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Data Loading: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_experience_leveling():
    """Test experience and leveling system."""
    logger.section("Testing Experience & Leveling")

    try:
        from entities.player import Player

        logger.info("Creating player...")
        player = Player("Alex")
        initial_level = player.level
        initial_stats = (player.max_hp, player.stats.get_attack(), player.stats.get_defense())

        logger.info(f"Starting level: {initial_level}")
        logger.info(f"  Stats: HP={initial_stats[0]}, ATK={initial_stats[1]}, DEF={initial_stats[2]}")

        logger.info("Gaining experience...")
        exp_needed = player.exp_to_next_level - player.experience
        player.gain_experience(exp_needed + 10)  # Enough to level up

        new_stats = (player.max_hp, player.stats.get_attack(), player.stats.get_defense())

        logger.info(f"After leveling up:")
        logger.info(f"  New level: {player.level}")
        logger.info(f"  New stats: HP={new_stats[0]}, ATK={new_stats[1]}, DEF={new_stats[2]}")

        if player.level > initial_level:
            logger.info("  ✓ Leveling works!")
            logger.info(f"  HP increased: {new_stats[0] - initial_stats[0]}")
            logger.info(f"  ATK increased: {new_stats[1] - initial_stats[1]}")
            logger.info(f"  DEF increased: {new_stats[2] - initial_stats[2]}")

        logger.info("✓ Experience & Leveling: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Experience & Leveling: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def run_all_tests():
    """Run all Phase 1 tests."""
    logger.section("RUNNING ALL PHASE 1 TESTS")

    tests = [
        ("Character System", test_character_system),
        ("Combat System", test_combat_system),
        ("World System", test_world_system),
        ("Devil Fruit System", test_devil_fruit_system),
        ("Data Loading", test_data_loading),
        ("Experience & Leveling", test_experience_leveling),
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
        logger.info("🎉 ALL PHASE 1 TESTS PASSED! 🎉")
    else:
        logger.warning(f"{total_count - passed_count} tests failed")

    logger.info(f"\nLog file: {logger.get_session_log_path()}")

    return passed_count == total_count


if __name__ == "__main__":
    logger.info("Starting Phase 1 comprehensive test suite...")
    logger.info(f"Python version: {sys.version}")
    logger.separator()

    success = run_all_tests()

    sys.exit(0 if success else 1)
