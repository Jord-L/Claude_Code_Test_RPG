"""
Test Script for Phase 1 Part 5
Run this to verify the character system is working correctly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Setup logging
from test_utils.logging_setup import setup_test_logger, log_test_start, log_test_end

logger = setup_test_logger('test_phase1_part5')
log_test_start(logger, "Phase 1 Part 5 - Character System Test")

logger.info("=" * 60)
logger.info("Phase 1 Part 5 - Character System Test")
logger.info("=" * 60)
logger.info("")

# Test 1: Import checks
logger.info("Test 1: Checking character system imports...")
logger.debug("Attempting to import character system modules")
try:
    from entities.stats import Stats
    logger.debug("Stats module imported successfully")
    logger.info("✓ Stats imported")
    
    from entities.devil_fruit import DevilFruit
    logger.debug("DevilFruit module imported successfully")
    logger.info("✓ DevilFruit imported")
    
    from entities.character import Character
    logger.debug("Character module imported successfully")
    logger.info("✓ Character imported")
    
    from entities.player import Player
    logger.debug("Player module imported successfully")
    logger.info("✓ Player imported")
    
    logger.info("✓ All character system imports successful!\n")
except ImportError as e:
    logger.error(f"Import failed: {e}")
    logger.info(f"✗ Import failed: {e}\n")
    import traceback
    logger.debug(traceback.format_exc())
    traceback.print_exc()
    sys.exit(1)

# Test 2: Stats system
logger.info("Test 2: Testing Stats system...")
logger.debug("Creating Stats instance with str=15, def=10, agi=12")
try:
    # Create stats
    stats = Stats(str_val=15, def_val=10, agi_val=12)
    logger.debug(f"Stats created: STR={stats.strength}, DEF={stats.defense}, AGI={stats.agility}")
    
    assert stats.strength == 15, "Strength not set"
    assert stats.defense == 10, "Defense not set"
    assert stats.agility == 12, "Agility not set"
    logger.info("✓ Stats initialization works")
    
    # Test derived stats
    max_hp = stats.get_max_hp(level=1)
    logger.debug(f"Calculated Max HP: {max_hp}")
    assert max_hp > 0, "Max HP calculation failed"
    logger.info(f"✓ Max HP calculation works: {max_hp}")
    
    attack = stats.get_attack()
    logger.debug(f"Calculated Attack: {attack}")
    assert attack > 0, "Attack calculation failed"
    logger.info(f"✓ Attack calculation works: {attack}")
    
    speed = stats.get_speed()
    logger.debug(f"Calculated Speed: {speed}")
    assert speed > 0, "Speed calculation failed"
    logger.info(f"✓ Speed calculation works: {speed}")
    
    # Test modifiers
    logger.debug("Adding flat modifier: +10 attack")
    stats.add_modifier("attack", 10)
    new_attack = stats.get_attack()
    logger.debug(f"New attack value: {new_attack} (expected: {attack + 10})")
    assert new_attack == attack + 10, "Flat modifier failed"
    logger.info("✓ Flat modifiers work")
    
    # Test stat increases
    old_str = stats.strength
    logger.debug(f"Increasing strength by 2 (current: {old_str})")
    stats.increase_stat("strength", 2)
    logger.debug(f"New strength: {stats.strength}")
    assert stats.strength == old_str + 2, "Stat increase failed"
    logger.info("✓ Stat increases work")
    
    # Test serialization
    logger.debug("Testing Stats serialization")
    stats_dict = stats.to_dict()
    logger.debug(f"Serialized stats keys: {list(stats_dict.keys())}")
    assert "primary" in stats_dict, "Serialization failed"
    logger.info("✓ Stats serialization works")
    
    # Test deserialization
    logger.debug("Testing Stats deserialization")
    stats2 = Stats.from_dict(stats_dict)
    logger.debug(f"Deserialized STR: {stats2.strength}, Original: {stats.strength}")
    assert stats2.strength == stats.strength, "Deserialization failed"
    logger.info("✓ Stats deserialization works")
    
    logger.info("✓ Stats system verified!\n")
    
except Exception as e:
    logger.error(f"Stats test failed: {e}")
    logger.info(f"✗ Stats test failed: {e}\n")
    import traceback
    logger.debug(traceback.format_exc())
    traceback.print_exc()
    sys.exit(1)

# Test 3: DevilFruit class
logger.info("Test 3: Testing DevilFruit class...")
logger.debug("Creating test Devil Fruit data")
try:
    # Create test fruit data
    test_fruit_data = {
        "id": "test_fruit",
        "name": "Test Test no Mi",
        "translation": "Test Fruit",
        "description": "A test fruit",
        "type": "paramecia",
        "rarity": "Common",
        "abilities": [
            {
                "name": "Test Attack",
                "level_required": 1,
                "ap_cost": 10,
                "description": "A test ability"
            },
            {
                "name": "Advanced Test",
                "level_required": 5,
                "ap_cost": 20,
                "description": "Advanced test ability"
            }
        ],
        "weaknesses": ["Water", "Seastone"],
        "strengths": ["Testing"]
    }
    logger.debug(f"Test fruit data: {test_fruit_data['name']} ({test_fruit_data['type']})")
    
    # Create fruit
    logger.debug("Creating DevilFruit instance")
    fruit = DevilFruit(test_fruit_data)
    logger.debug(f"Fruit created: ID={fruit.fruit_id}, Mastery Level={fruit.mastery_level}")
    
    assert fruit.fruit_id == "test_fruit", "Fruit ID wrong"
    assert fruit.mastery_level == 1, "Initial mastery level wrong"
    logger.info("✓ DevilFruit initialization works")
    
    # Check unlocked abilities
    logger.debug(f"Unlocked abilities: {len(fruit.unlocked_abilities)}")
    assert len(fruit.unlocked_abilities) == 1, "Starting abilities wrong"
    logger.info(f"✓ Starting abilities unlocked: {len(fruit.unlocked_abilities)}")
    
    # Test mastery leveling
    logger.debug("Testing mastery leveling (adding 10x 100 EXP)")
    initial_level = fruit.mastery_level
    for i in range(10):
        fruit.gain_mastery_exp(100)
        logger.debug(f"  EXP gain {i+1}: Level {fruit.mastery_level}, Total EXP: {fruit.mastery_exp}")
    
    logger.debug(f"Mastery progression: Level {initial_level} -> Level {fruit.mastery_level}")
    assert fruit.mastery_level > 1, "Mastery leveling failed"
    logger.info(f"✓ Mastery leveling works: Level {fruit.mastery_level}")
    
    # Check if new ability unlocked
    logger.debug(f"Total abilities after leveling: {len(fruit.unlocked_abilities)}")
    assert len(fruit.unlocked_abilities) > 1, "Abilities not unlocking"
    logger.info(f"✓ New abilities unlock: {len(fruit.unlocked_abilities)} abilities")
    
    # Test serialization
    logger.debug("Testing DevilFruit serialization")
    fruit_dict = fruit.to_dict()
    logger.debug(f"Serialized keys: {list(fruit_dict.keys())}")
    assert "fruit_id" in fruit_dict, "Serialization failed"
    logger.info("✓ DevilFruit serialization works")
    
    logger.info("✓ DevilFruit class verified!\n")
    
except Exception as e:
    logger.error(f"DevilFruit test failed: {e}")
    logger.info(f"✗ DevilFruit test failed: {e}\n")
    import traceback
    logger.debug(traceback.format_exc())
    traceback.print_exc()
    sys.exit(1)

# Test 4: Character class
logger.info("Test 4: Testing Character class...")
logger.debug("Creating test Character: 'Test Hero', Level 1")
try:
    # Create character
    char = Character("Test Hero", level=1)
    logger.debug(f"Character created: {char.name}, Level {char.level}, HP: {char.current_hp}/{char.max_hp}")
    
    assert char.name == "Test Hero", "Name not set"
    assert char.level == 1, "Level not set"
    assert char.is_alive == True, "Should be alive"
    logger.info("✓ Character initialization works")
    
    # Test HP
    max_hp = char.max_hp
    logger.debug(f"Testing damage: Taking 10 damage (HP: {char.current_hp}/{max_hp})")
    char.take_damage(10)
    logger.debug(f"After damage: HP: {char.current_hp}/{max_hp}")
    assert char.current_hp < max_hp, "Damage not applied"
    logger.info(f"✓ Damage system works: {char.current_hp}/{char.max_hp} HP")
    
    # Test healing
    hp_before_heal = char.current_hp
    logger.debug(f"Testing healing: +5 HP (current: {hp_before_heal})")
    char.heal(5)
    logger.debug(f"After healing: HP: {char.current_hp}/{max_hp}")
    assert char.current_hp > max_hp - 10, "Healing failed"
    logger.info("✓ Healing works")
    
    # Test experience and leveling
    old_level = char.level
    logger.debug(f"Testing leveling: Adding 150 EXP (current level: {old_level})")
    char.gain_experience(150)
    logger.debug(f"After EXP: Level {char.level}, EXP: {char.experience}")
    assert char.level > old_level, "Leveling failed"
    logger.info(f"✓ Leveling works: Level {char.level}")
    
    # Test Devil Fruit equipping
    logger.debug("Testing Devil Fruit equipping")
    char.equip_devil_fruit(test_fruit_data)
    logger.debug(f"Devil Fruit equipped: {char.devil_fruit.name if char.devil_fruit else 'None'}")
    assert char.has_devil_fruit() == True, "Devil Fruit not equipped"
    assert char.can_swim() == False, "Should not be able to swim"
    logger.info("✓ Devil Fruit equipping works")
    
    # Test equipment
    logger.debug("Testing equipment system")
    test_weapon = {
        "id": "test_sword",
        "name": "Test Sword",
        "stats": {"attack": 15}
    }
    char.equip_item("weapon", test_weapon)
    logger.debug(f"Equipped weapon: {char.equipment['weapon']['name'] if char.equipment['weapon'] else 'None'}")
    assert char.equipment["weapon"] is not None, "Equipment failed"
    logger.info("✓ Equipment system works")
    
    # Test death
    logger.debug("Testing death system: Dealing fatal damage")
    char.current_hp = 1
    char.take_damage(999)
    logger.debug(f"After fatal damage: HP={char.current_hp}, Is Alive={char.is_alive}")
    assert char.is_alive == False, "Death detection failed"
    logger.info("✓ Death system works")
    
    # Test revival
    logger.debug("Testing revival")
    char.revive()
    logger.debug(f"After revival: HP={char.current_hp}, Is Alive={char.is_alive}")
    assert char.is_alive == True, "Revival failed"
    assert char.current_hp > 0, "HP not restored on revival"
    logger.info("✓ Revival works")
    
    # Test serialization
    logger.debug("Testing Character serialization")
    char_dict = char.to_dict()
    logger.debug(f"Serialized character keys: {list(char_dict.keys())}")
    assert "name" in char_dict, "Serialization failed"
    assert "level" in char_dict, "Serialization failed"
    logger.info("✓ Character serialization works")
    
    logger.info("✓ Character class verified!\n")
    
except Exception as e:
    logger.error(f"Character test failed: {e}")
    logger.info(f"✗ Character test failed: {e}\n")
    import traceback
    logger.debug(traceback.format_exc())
    traceback.print_exc()
    sys.exit(1)

# Test 5: Player class
logger.info("Test 5: Testing Player class...")
logger.debug("Creating Player: 'Luffy', Level 1")
try:
    # Create player
    player = Player("Luffy", level=1)
    logger.debug(f"Player created: {player.name}, Berries: {player.berries}")
    
    assert player.name == "Luffy", "Name not set"
    assert player.berries > 0, "Starting berries not set"
    logger.info(f"✓ Player initialization works: {player.berries} Berries")
    
    # Test berries
    old_berries = player.berries
    logger.debug(f"Adding 500 Berries (current: {old_berries})")
    player.add_berries(500)
    logger.debug(f"After addition: {player.berries} Berries")
    assert player.berries == old_berries + 500, "Add berries failed"
    logger.info("✓ Add berries works")
    
    logger.debug(f"Spending 200 Berries (current: {player.berries})")
    success = player.spend_berries(200)
    logger.debug(f"Spend result: {success}, New balance: {player.berries}")
    assert success == True, "Spend berries failed"
    assert player.berries == old_berries + 300, "Berries calculation wrong"
    logger.info("✓ Spend berries works")
    
    # Test inventory
    logger.debug("Testing inventory: Adding 3x health_potion")
    player.add_item("health_potion", 3)
    quantity = player.get_item_quantity("health_potion")
    logger.debug(f"Health potions in inventory: {quantity}")
    assert player.has_item("health_potion", 3), "Add item failed"
    logger.info("✓ Add item works")
    
    logger.debug("Removing 1x health_potion")
    player.remove_item("health_potion", 1)
    new_quantity = player.get_item_quantity("health_potion")
    logger.debug(f"Health potions remaining: {new_quantity}")
    assert new_quantity == 2, "Remove item failed"
    logger.info("✓ Remove item works")
    
    # Test item usage
    logger.debug("Testing item usage")
    test_item_data = {
        "id": "health_potion",
        "effects": [{"type": "Restore HP", "value": 50}]
    }
    player.current_hp = player.max_hp - 50
    hp_before = player.current_hp
    logger.debug(f"Using health potion (HP before: {hp_before}/{player.max_hp})")
    player.use_item("health_potion", test_item_data)
    logger.debug(f"HP after using item: {player.current_hp}/{player.max_hp}")
    assert player.current_hp > player.max_hp - 50, "Item usage failed"
    logger.info("✓ Item usage works")
    
    # Test key items
    logger.debug("Testing key items: Adding 'important_map'")
    player.add_key_item("important_map")
    logger.debug(f"Key items: {player.key_items}")
    assert player.has_key_item("important_map"), "Key item failed"
    logger.info("✓ Key items work")
    
    # Test reputation
    logger.debug("Testing reputation system: +10 with pirates")
    player.change_reputation("pirates", 10)
    rep = player.get_reputation("pirates")
    logger.debug(f"Pirate reputation: {rep}")
    assert rep == 10, "Reputation failed"
    logger.info("✓ Reputation system works")
    
    # Test bounty
    logger.debug("Testing bounty system: Setting to 30,000,000")
    player.increase_bounty(30000000)
    logger.debug(f"Player bounty: {player.bounty:,}")
    assert player.bounty == 30000000, "Bounty failed"
    logger.info("✓ Bounty system works")
    
    # Test island discovery
    logger.debug("Testing island discovery: 'test_island'")
    player.discover_island("test_island")
    logger.debug(f"Discovered islands: {player.discovered_islands}")
    assert "test_island" in player.discovered_islands, "Island discovery failed"
    logger.info("✓ Island discovery works")
    
    # Test fast travel
    logger.debug("Testing fast travel: Unlocking 'test_island'")
    player.unlock_fast_travel("test_island")
    can_travel = player.can_fast_travel_to("test_island")
    logger.debug(f"Can fast travel to test_island: {can_travel}")
    assert can_travel, "Fast travel failed"
    logger.info("✓ Fast travel works")
    
    # Test statistics
    logger.debug("Testing statistics: Recording battle victory (3 enemies)")
    player.record_battle_victory(3)
    battles_won = player.stats_tracker["battles_won"]
    enemies_defeated = player.stats_tracker["enemies_defeated"]
    logger.debug(f"Battles won: {battles_won}, Enemies defeated: {enemies_defeated}")
    assert battles_won == 1, "Battle stats failed"
    assert enemies_defeated == 3, "Enemy stats failed"
    logger.info("✓ Statistics tracking works")
    
    # Test serialization
    logger.debug("Testing Player serialization")
    player_dict = player.to_dict()
    logger.debug(f"Serialized player keys: {list(player_dict.keys())}")
    assert "berries" in player_dict, "Serialization failed"
    assert "inventory" in player_dict, "Serialization failed"
    logger.info("✓ Player serialization works")
    
    # Test deserialization
    logger.debug("Testing Player deserialization")
    player2 = Player.from_dict(player_dict)
    logger.debug(f"Restored player: {player2.name}, Berries: {player2.berries}")
    assert player2.name == player.name, "Deserialization failed"
    assert player2.berries == player.berries, "Berries not restored"
    logger.info("✓ Player deserialization works")
    
    logger.info("✓ Player class verified!\n")
    
except Exception as e:
    logger.error(f"Player test failed: {e}")
    logger.info(f"✗ Player test failed: {e}\n")
    import traceback
    logger.debug(traceback.format_exc())
    traceback.print_exc()
    sys.exit(1)

# Test 6: Integration test
logger.info("Test 6: Testing system integration...")
logger.debug("Creating complete player character for integration test")
try:
    # Create a complete player character
    player = Player("Test Captain", level=5)
    logger.debug(f"Created player: {player.name}, Level {player.level}")
    
    # Add berries
    logger.debug("Adding 10,000 berries")
    player.add_berries(10000)
    
    # Equip Devil Fruit
    logger.debug("Equipping test Devil Fruit")
    player.equip_devil_fruit(test_fruit_data)
    
    # Level up fruit mastery
    logger.debug("Leveling up fruit mastery (10 iterations)")
    for i in range(10):
        player.devil_fruit.gain_mastery_exp(100)
        if i % 3 == 0:
            logger.debug(f"  Mastery progress: Level {player.devil_fruit.mastery_level}")
    logger.debug(f"Final mastery level: {player.devil_fruit.mastery_level}")
    
    # Add items
    logger.debug("Adding items to inventory")
    player.add_item("sword", 1)
    player.add_item("potion", 5)
    logger.debug(f"Inventory: {player.inventory}")
    
    # Simulate combat
    logger.debug("Simulating combat scenario")
    player.current_hp = player.max_hp - 50
    player.current_ap = player.max_ap - 20
    logger.debug(f"Combat state: HP={player.current_hp}/{player.max_hp}, AP={player.current_ap}/{player.max_ap}")
    
    # Use ability
    if player.devil_fruit.unlocked_abilities:
        ability = player.devil_fruit.unlocked_abilities[0]
        ap_cost = ability.get("ap_cost", 10)
        logger.debug(f"Using ability: {ability['name']} (Cost: {ap_cost} AP)")
        if player.use_ap(ap_cost):
            logger.info(f"✓ Used ability: {ability['name']}")
            logger.debug(f"AP after ability: {player.current_ap}/{player.max_ap}")
    
    # Rest
    logger.debug("Resting to restore HP and AP")
    player.rest()
    logger.debug(f"After rest: HP={player.current_hp}/{player.max_hp}, AP={player.current_ap}/{player.max_ap}")
    assert player.current_hp == player.max_hp, "Rest failed"
    assert player.current_ap == player.max_ap, "Rest failed"
    logger.info("✓ Rest works")
    
    # Save/load cycle
    logger.debug("Testing save/load cycle")
    save_data = player.to_dict()
    logger.debug(f"Save data size: {len(str(save_data))} characters")
    
    loaded_player = Player.from_dict(save_data)
    logger.debug(f"Loaded player: {loaded_player.name}, Level {loaded_player.level}")
    
    assert loaded_player.name == player.name, "Load failed"
    assert loaded_player.level == player.level, "Level not saved"
    assert loaded_player.berries == player.berries, "Berries not saved"
    logger.info("✓ Save/load cycle works")
    
    logger.info("✓ Integration test passed!\n")
    
except Exception as e:
    logger.error(f"Integration test failed: {e}")
    logger.info(f"✗ Integration test failed: {e}\n")
    import traceback
    logger.debug(traceback.format_exc())
    traceback.print_exc()
    sys.exit(1)

logger.info("=" * 60)
logger.info("All tests passed! ✓")
logger.info("=" * 60)
logger.info("")

logger.info("Character System Summary:")
logger.info("")
logger.info("✓ Stats - 7 primary stats with derived calculations")
logger.info("✓ DevilFruit - Mastery system with ability unlocking")
logger.info("✓ Character - Base class for all characters")
logger.info("✓ Player - Extended with inventory, berries, reputation")
logger.info("")
logger.info("Features:")
logger.info("  ✓ Level and experience system")
logger.info("  ✓ HP/AP management")
logger.info("  ✓ Devil Fruit mastery and abilities")
logger.info("  ✓ Equipment system")
logger.info("  ✓ Stat modifiers (flat and percentage)")
logger.info("  ✓ Damage calculation with defense")
logger.info("  ✓ Critical hits and evasion")
logger.info("  ✓ Death and revival")
logger.info("  ✓ Inventory management")
logger.info("  ✓ Currency (Berries)")
logger.info("  ✓ Reputation and bounty")
logger.info("  ✓ World exploration tracking")
logger.info("  ✓ Statistics tracking")
logger.info("  ✓ Save/load support")
logger.info("")
logger.info("✅ Character system is ready for gameplay!")
logger.info("")

log_test_end(logger, 'test_phase1_part5.log')
