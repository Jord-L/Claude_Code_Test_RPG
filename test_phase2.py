"""
Comprehensive Test Suite for Phase 2 Systems
Tests all major RPG systems with detailed logging.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.logger import init_logger, get_logger

# Initialize logger
logger = init_logger("Phase2_Tests", "test_logs")
logger.section("PHASE 2 COMPREHENSIVE TEST SUITE")

def test_party_system():
    """Test party management system."""
    logger.section("Testing Party System")

    try:
        from systems.party_manager import PartyManager
        from entities.player import Player
        from entities.character import Character

        logger.info("Creating test player...")
        player = Player("Test Luffy")
        player.level = 10

        logger.info("Initializing PartyManager...")
        party_manager = PartyManager(player)

        logger.info("Creating test crew members...")
        zoro = Character("Zoro", level=9)
        nami = Character("Nami", level=8)
        usopp = Character("Usopp", level=7)

        logger.info("Adding crew members to reserve...")
        party_manager.add_to_reserve(zoro)
        party_manager.add_to_reserve(nami)
        party_manager.add_to_reserve(usopp)

        logger.info(f"Reserve size: {len(party_manager.reserve_crew)}")
        logger.info(f"Active party size: {len(party_manager.get_active_party())}")

        logger.info("✓ Party System: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Party System: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_inventory_system():
    """Test inventory and equipment system."""
    logger.section("Testing Inventory & Equipment System")

    try:
        from systems.item_system import Inventory, Item
        from systems.item_loader import load_item
        from systems.equipment_manager import EquipmentManager
        from entities.player import Player

        logger.info("Creating inventory...")
        inventory = Inventory(max_slots=50)

        logger.info("Loading test items...")
        health_potion = load_item("health_potion_small")
        if health_potion:
            logger.info(f"Loaded item: {health_potion.name}")
            inventory.add_item(health_potion, 5)
            logger.info(f"Added 5x {health_potion.name}")

        sword = load_item("wooden_sword")
        if sword:
            logger.info(f"Loaded equipment: {sword.name}")
            inventory.add_item(sword, 1)

        logger.info(f"Inventory slots used: {len(inventory.slots)}/{inventory.max_slots}")

        logger.info("Testing equipment manager...")
        player = Player("Test Player")
        equipment_manager = EquipmentManager()
        equipment_manager.initialize_character_equipment(player)

        logger.info(f"Equipment slots initialized: {player.equipment_slots is not None}")

        logger.info("✓ Inventory & Equipment: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Inventory & Equipment: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_island_system():
    """Test island and travel system."""
    logger.section("Testing Island System")

    try:
        from world.island import IslandManager
        from world.island_factory import IslandFactory

        logger.info("Creating island manager...")
        island_manager = IslandManager()

        logger.info("Creating all islands...")
        islands = IslandFactory.create_all_islands()
        logger.info(f"Created {len(islands)} islands")

        for island in islands:
            logger.info(f"  - {island.name} ({island.island_id})")
            island_manager.register_island(island)

        logger.info("Setting current island to Foosha Village...")
        island_manager.set_current_island("foosha_village")

        current = island_manager.get_current_island()
        logger.info(f"Current island: {current.name if current else 'None'}")

        if current:
            logger.info(f"  Map size: {current.map.width}x{current.map.height}")
            logger.info(f"  NPCs: {len(current.npcs)}")
            logger.info(f"  Connections: {len(current.connections)}")

        logger.info("✓ Island System: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Island System: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_dialogue_system():
    """Test dialogue system."""
    logger.section("Testing Dialogue System")

    try:
        from systems.dialogue_system import create_default_dialogues, Dialogue, DialogueLine

        logger.info("Creating dialogue manager...")
        dialogue_manager = create_default_dialogues()

        logger.info(f"Registered dialogues: {len(dialogue_manager.dialogues)}")

        logger.info("Testing dialogue playback...")
        if dialogue_manager.start_dialogue("mayor_greeting"):
            logger.info("Started mayor dialogue")

            while not dialogue_manager.current_dialogue.is_finished():
                line = dialogue_manager.get_current_line()
                logger.info(f"  {line.speaker}: {line.text}")
                dialogue_manager.advance_dialogue()

        logger.info("✓ Dialogue System: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Dialogue System: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_shop_system():
    """Test shop system."""
    logger.section("Testing Shop System")

    try:
        from systems.shop_system import create_default_shops
        from systems.item_system import Inventory

        logger.info("Creating shops...")
        shops = create_default_shops()
        logger.info(f"Created {len(shops)} shops")

        for shop_id, shop in shops.items():
            logger.info(f"  - {shop.name} ({shop_id}): {len(shop.inventory)} items")

        logger.info("Testing shop purchase...")
        makino_bar = shops.get("makino_bar")
        if makino_bar:
            inventory = Inventory(50)
            result = makino_bar.buy_item("health_potion_small", 1, 10000, inventory)
            logger.info(f"Purchase result: {result.get('success', False)}")
            if result.get('success'):
                logger.info(f"  Cost: {result.get('cost')} berries")

        logger.info("✓ Shop System: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Shop System: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_quest_system():
    """Test quest system."""
    logger.section("Testing Quest System")

    try:
        from systems.quest_system import create_default_quests, QuestStatus

        logger.info("Creating quest manager...")
        quest_manager = create_default_quests()

        logger.info(f"Registered quests: {len(quest_manager.quests)}")

        for quest_id, quest in quest_manager.quests.items():
            logger.info(f"  - {quest.name} ({quest_id})")
            logger.info(f"    Objectives: {len(quest.objectives)}")
            logger.info(f"    Rewards: {quest.exp_reward} exp, {quest.berries_reward} berries")

        logger.info("Testing quest start...")
        if quest_manager.start_quest("recruit_zoro", player_level=5):
            logger.info("Successfully started recruit_zoro quest")

        logger.info("✓ Quest System: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Quest System: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_ship_system():
    """Test ship system."""
    logger.section("Testing Ship System")

    try:
        from systems.ship_system import Ship, create_ship_upgrades

        logger.info("Creating ship...")
        ship = Ship("Going Merry")

        logger.info(f"Ship: {ship.ship_name}")
        logger.info(f"  Level: {ship.ship_level}")
        logger.info(f"  Max Crew: {ship.max_crew}")
        logger.info(f"  Storage: {ship.storage}")
        logger.info(f"  Speed: {ship.speed}")

        logger.info("Testing upgrades...")
        upgrades = create_ship_upgrades()
        logger.info(f"Available upgrades: {len(upgrades)}")

        logger.info("Upgrading capacity...")
        ship.upgrade_capacity()
        logger.info(f"  New max crew: {ship.max_crew}")

        logger.info("✓ Ship System: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Ship System: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_devil_fruit_system():
    """Test extended devil fruit system."""
    logger.section("Testing Devil Fruit System")

    try:
        from systems.devil_fruit_extended import create_extended_devil_fruits

        logger.info("Creating devil fruits...")
        fruits = create_extended_devil_fruits()

        logger.info(f"Registered fruits: {len(fruits)}")

        for fruit_id, fruit in fruits.items():
            logger.info(f"  - {fruit.name} ({fruit.fruit_type})")
            logger.info(f"    Abilities: {len(fruit.abilities)}")

            for ability in fruit.abilities[:2]:  # Show first 2 abilities
                logger.info(f"      * {ability.name} (Lv.{ability.required_level}): {ability.ap_cost} AP")

        logger.info("Testing mastery gain...")
        gomu = fruits.get("gomu_gomu")
        if gomu:
            gomu.gain_mastery(150)
            logger.info(f"  Gomu mastery: Level {gomu.mastery_level}")

        logger.info("✓ Devil Fruit System: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Devil Fruit System: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_combat_advanced():
    """Test advanced combat system."""
    logger.section("Testing Advanced Combat System")

    try:
        from systems.combat_advanced import AdvancedCombatManager, StatusEffect

        logger.info("Creating combat manager...")
        combat = AdvancedCombatManager()

        logger.info("Testing combo system...")
        for i in range(5):
            combat.on_hit_landed()
        logger.info(f"  Combo count: {combat.combo.combo_count}")
        logger.info(f"  Combo bonus: {combat.combo.combo_bonus:.2f}")

        logger.info("Testing damage calculation...")
        result = combat.calculate_damage(
            100,
            {"crit_chance": 10.0, "luck": 5},
            {"defense": 20}
        )
        logger.info(f"  Damage: {result['damage']}")
        logger.info(f"  Critical: {result['is_critical']}")

        logger.info("Testing status effects...")
        combat.status_manager.apply_status("test_char", StatusEffect.POISON, 3, 10)
        has_poison = combat.status_manager.has_effect("test_char", StatusEffect.POISON)
        logger.info(f"  Has poison: {has_poison}")

        logger.info("✓ Advanced Combat: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Advanced Combat: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_haki_system():
    """Test Haki system."""
    logger.section("Testing Haki System")

    try:
        from systems.haki_system import HakiUser, HakiType

        logger.info("Creating Haki user...")
        haki_user = HakiUser()

        logger.info("Unlocking Observation Haki...")
        haki_user.unlock_haki(HakiType.OBSERVATION)

        logger.info("Unlocking Armament Haki...")
        haki_user.unlock_haki(HakiType.ARMAMENT)

        logger.info("Testing Observation Haki...")
        obs_result = haki_user.use_observation_haki()
        if obs_result.get('success'):
            logger.info(f"  Dodge bonus: +{obs_result.get('dodge_bonus')}%")

        logger.info("Testing Armament Haki...")
        arm_result = haki_user.use_armament_haki()
        if arm_result.get('success'):
            logger.info(f"  Damage bonus: +{arm_result.get('damage_bonus')}")

        logger.info("✓ Haki System: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Haki System: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_audio_system():
    """Test audio system."""
    logger.section("Testing Audio System")

    try:
        from systems.audio_system import get_audio_manager, MusicTrack, SoundEffect

        logger.info("Getting audio manager...")
        audio = get_audio_manager()

        logger.info(f"Mixer initialized: {audio.mixer_initialized}")
        logger.info(f"Music enabled: {audio.music_enabled}")
        logger.info(f"Sound enabled: {audio.sound_enabled}")

        logger.info("Testing music playback...")
        audio.play_music(MusicTrack.MAIN_THEME)
        logger.info(f"  Current track: {audio.current_track}")

        logger.info("Testing sound effect...")
        audio.play_sound(SoundEffect.LEVEL_UP)

        logger.info("✓ Audio System: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ Audio System: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def test_npc_system():
    """Test NPC system."""
    logger.section("Testing NPC System")

    try:
        from entities.npc import NPC

        logger.info("Creating test NPC...")
        npc = NPC("test_npc", "Test Villager", 10, 10)
        npc.npc_type = "shopkeeper"
        npc.shop_id = "test_shop"

        logger.info(f"NPC: {npc.name}")
        logger.info(f"  Type: {npc.npc_type}")
        logger.info(f"  Position: ({npc.tile_x}, {npc.tile_y})")

        logger.info("Testing interaction...")
        result = npc.interact()
        logger.info(f"  Action: {result.get('action')}")
        logger.info(f"  Shop ID: {result.get('shop_id')}")

        logger.info("Testing range check...")
        in_range = npc.is_in_range(npc.x + 50, npc.y + 50)
        logger.info(f"  In range: {in_range}")

        logger.info("✓ NPC System: PASSED")
        return True

    except Exception as e:
        logger.error(f"✗ NPC System: FAILED - {e}")
        logger.exception("Full traceback:")
        return False


def run_all_tests():
    """Run all Phase 2 tests."""
    logger.section("RUNNING ALL PHASE 2 TESTS")

    tests = [
        ("Party System", test_party_system),
        ("Inventory & Equipment", test_inventory_system),
        ("Island System", test_island_system),
        ("Dialogue System", test_dialogue_system),
        ("Shop System", test_shop_system),
        ("Quest System", test_quest_system),
        ("Ship System", test_ship_system),
        ("Devil Fruit System", test_devil_fruit_system),
        ("Advanced Combat", test_combat_advanced),
        ("Haki System", test_haki_system),
        ("Audio System", test_audio_system),
        ("NPC System", test_npc_system),
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
        logger.info("🎉 ALL TESTS PASSED! 🎉")
    else:
        logger.warning(f"{total_count - passed_count} tests failed")

    logger.info(f"\nLog file: {logger.get_session_log_path()}")

    return passed_count == total_count


if __name__ == "__main__":
    logger.info("Starting Phase 2 comprehensive test suite...")
    logger.info(f"Python version: {sys.version}")
    logger.separator()

    success = run_all_tests()

    sys.exit(0 if success else 1)
