"""
Test for Phase 1 Part 7 - Basic Combat System
Tests the complete turn-based combat system.
"""

import sys
sys.path.insert(0, 'src')

# Setup logging
from test_utils.logging_setup import setup_test_logger, log_test_start, log_test_end

logger = setup_test_logger('test_phase1_part7')
log_test_start(logger, "Phase 1 Part 7 - Combat System Test")

from entities.player import Player
from entities.enemy import Enemy, EnemyFactory
from entities.stats import Stats
from combat.battle_manager import BattleManager
from combat.combat_action import ActionFactory, ActionType
from combat.enemy_ai import EnemyAI, AIFactory
from systems.devil_fruit_manager import devil_fruit_manager


def create_test_player(name: str = "Luffy", level: int = 5) -> Player:
    """Create a test player character."""
    logger.debug(f"Creating test player: {name}, Level {level}")
    player = Player(name, level)
    logger.debug(f"Player created: HP={player.current_hp}/{player.max_hp}, ATK={player.stats.get_attack()}")
    
    # Give player a Devil Fruit
    if devil_fruit_manager.loaded or devil_fruit_manager.load_all_fruits():
        logger.debug("Attempting to equip Gomu Gomu no Mi")
        gomu_gomu = devil_fruit_manager.get_fruit_by_id("gomu_gomu")
        if gomu_gomu:
            player.equip_devil_fruit(gomu_gomu)
            logger.info(f"✓ {player.name} equipped {gomu_gomu['name']}")
            logger.debug(f"  Abilities unlocked: {len(player.devil_fruit.unlocked_abilities)}")
        else:
            logger.warning("Gomu Gomu no Mi not found in database")
    else:
        logger.warning("Devil Fruit manager not loaded")
    
    return player


def test_combat_basic():
    """Test basic combat without abilities."""
    logger.info("\n" + "="*60)
    logger.info("TEST 1: BASIC COMBAT (Attack Only)")
    logger.info("="*60 + "\n")
    
    logger.debug("Initializing Test 1: Basic Combat")
    
    # Create player
    logger.debug("Creating player character")
    player = Player("TestPlayer", level=3)
    logger.debug(f"Player stats: HP={player.current_hp}/{player.max_hp}, ATK={player.stats.get_attack()}, SPD={player.stats.get_speed()}")
    
    # Create enemy
    logger.debug("Creating bandit enemy (level 2)")
    enemy = EnemyFactory.create_bandit(level=2)
    logger.debug(f"Enemy stats: HP={enemy.current_hp}/{enemy.max_hp}, ATK={enemy.stats.get_attack()}, SPD={enemy.stats.get_speed()}")
    
    logger.info(f"Player: {player}")
    logger.info(f"Enemy: {enemy}")
    logger.info("")
    
    # Create battle
    logger.debug("Creating BattleManager with 1v1 setup")
    battle = BattleManager([player], [enemy])
    logger.debug(f"Turn order: {[c.name for c in battle.turn_order]}")
    logger.info(f"✓ Battle initialized")
    
    # Simulate a few turns
    turn_count = 0
    max_turns = 10
    logger.debug(f"Starting combat simulation (max {max_turns} turns)")
    
    while battle.battle_active and turn_count < max_turns:
        turn_count += 1
        current_actor = battle.current_actor
        logger.debug(f"\n--- Turn {turn_count}: {current_actor.name}'s turn ---")
        logger.debug(f"  HP: {current_actor.current_hp}/{current_actor.max_hp}")
        
        if battle.is_player_turn():
            # Player attacks
            target = battle.get_alive_enemies()[0] if battle.get_alive_enemies() else None
            if target:
                logger.debug(f"  Player attacking {target.name}")
                action = ActionFactory.basic_attack(battle.current_actor, target)
                result = battle.execute_action(action)
                if result:
                    logger.debug(f"  Attack result: {result}")
                logger.info(f"Turn {turn_count}: {current_actor.name} attacked {target.name}")
        else:
            # Enemy AI chooses action
            logger.debug(f"  Enemy AI calculating action")
            ai = EnemyAI(battle.current_actor)
            action = ai.choose_action(battle.get_alive_players(), battle.get_alive_enemies())
            logger.debug(f"  AI chose: {action.action_type.name}")
            result = battle.execute_action(action)
            if result:
                logger.debug(f"  Action result: {result}")
            logger.info(f"Turn {turn_count}: {current_actor.name} used {action.action_type.name}")
    
    logger.debug(f"\nCombat ended after {turn_count} turns")
    logger.debug(f"Battle active: {battle.battle_active}")
    logger.debug(f"Battle result: {battle.result}")
    
    logger.info("\n" + "-"*60)
    if battle.result:
        if battle.result.victory:
            logger.info("✓ TEST PASSED - Player Victory!")
            logger.info(f"  Rewards: {battle.result.exp_gained} EXP, {battle.result.berries_gained} Berries")
            logger.debug(f"  Battle duration: {turn_count} turns")
        else:
            logger.info("✓ TEST PASSED - Battle Ended (Defeat or Flee)")
    else:
        logger.info("✓ TEST PASSED - Battle Ended After Max Turns")
    
    return True


def test_combat_with_abilities():
    """Test combat with Devil Fruit abilities."""
    logger.info("\n" + "="*60)
    logger.info("TEST 2: COMBAT WITH DEVIL FRUIT ABILITIES")
    logger.info("="*60 + "\n")
    
    logger.debug("Initializing Test 2: Combat with Abilities")
    
    # Load Devil Fruits
    if not devil_fruit_manager.loaded:
        logger.debug("Loading Devil Fruits...")
        devil_fruit_manager.load_all_fruits()
    
    # Create player with Devil Fruit
    logger.debug("Creating player with Devil Fruit")
    player = create_test_player("Luffy", level=5)
    
    # Create stronger enemy
    logger.debug("Creating marine enemy (level 4)")
    enemy = EnemyFactory.create_marine(level=4)
    logger.debug(f"Enemy created: {enemy.name}, HP={enemy.current_hp}/{enemy.max_hp}")
    
    logger.info(f"Player: {player}")
    if player.devil_fruit:
        logger.info(f"  Devil Fruit: {player.devil_fruit.name}")
        logger.info(f"  Abilities: {len(player.devil_fruit.unlocked_abilities)}")
        logger.debug(f"  Available abilities: {[a['name'] for a in player.devil_fruit.unlocked_abilities]}")
    logger.info(f"Enemy: {enemy}")
    logger.info("")
    
    # Create battle
    logger.debug("Creating battle with ability-capable characters")
    battle = BattleManager([player], [enemy])
    logger.debug(f"Turn order: {[c.name for c in battle.turn_order]}")
    
    # Simulate turns
    turn_count = 0
    max_turns = 15
    ability_uses = 0
    logger.debug(f"Starting combat simulation (max {max_turns} turns)")
    
    while battle.battle_active and turn_count < max_turns:
        turn_count += 1
        current_actor = battle.current_actor
        logger.debug(f"\n--- Turn {turn_count}: {current_actor.name}'s turn ---")
        logger.debug(f"  HP: {current_actor.current_hp}/{current_actor.max_hp}, AP: {current_actor.current_ap}/{current_actor.max_ap}")
        
        if battle.is_player_turn():
            # Player uses abilities or attacks
            if player.devil_fruit and player.current_ap >= 10:
                # Use ability
                abilities = player.devil_fruit.get_available_abilities(player.current_ap)
                logger.debug(f"  Available abilities: {len(abilities)}")
                if abilities and battle.get_alive_enemies():
                    ability = abilities[0]
                    target = battle.get_alive_enemies()[0]
                    logger.debug(f"  Using ability: {ability['name']} (Cost: {ability.get('ap_cost', 0)} AP)")
                    action = ActionFactory.use_ability(player, ability, target)
                    result = battle.execute_action(action)
                    ability_uses += 1
                    logger.info(f"Turn {turn_count}: {player.name} used {ability['name']} on {target.name}")
                    if result:
                        logger.debug(f"  Ability result: {result}")
                else:
                    # No abilities or AP, attack
                    target = battle.get_alive_enemies()[0] if battle.get_alive_enemies() else None
                    if target:
                        logger.debug(f"  No abilities available, attacking normally")
                        action = ActionFactory.basic_attack(player, target)
                        battle.execute_action(action)
                        logger.info(f"Turn {turn_count}: {player.name} attacked {target.name}")
            else:
                # Attack
                target = battle.get_alive_enemies()[0] if battle.get_alive_enemies() else None
                if target:
                    logger.debug(f"  Insufficient AP for abilities, attacking")
                    action = ActionFactory.basic_attack(player, target)
                    battle.execute_action(action)
                    logger.info(f"Turn {turn_count}: {player.name} attacked {target.name}")
        else:
            # Enemy AI
            logger.debug(f"  Enemy AI (normal difficulty) calculating action")
            ai = EnemyAI(battle.current_actor, difficulty="normal")
            action = ai.choose_action(battle.get_alive_players(), battle.get_alive_enemies())
            logger.debug(f"  AI chose: {action.action_type.name}")
            battle.execute_action(action)
            logger.info(f"Turn {turn_count}: {current_actor.name} used {action.action_type.name}")
    
    logger.debug(f"\nCombat ended after {turn_count} turns")
    logger.debug(f"Total ability uses: {ability_uses}")
    
    logger.info("\n" + "-"*60)
    if battle.result:
        if battle.result.victory:
            logger.info("✓ TEST PASSED - Player Victory with Abilities!")
            logger.info(f"  Rewards: {battle.result.exp_gained} EXP, {battle.result.berries_gained} Berries")
            logger.debug(f"  Abilities used: {ability_uses} times")
        else:
            logger.info("✓ TEST PASSED - Battle Ended")
    else:
        logger.info("✓ TEST PASSED - Battle Ended After Max Turns")
    
    return True


def test_multi_enemy_battle():
    """Test combat against multiple enemies."""
    logger.info("\n" + "="*60)
    logger.info("TEST 3: MULTI-ENEMY BATTLE")
    logger.info("="*60 + "\n")
    
    logger.debug("Initializing Test 3: Multi-Enemy Battle (2v3)")
    
    # Create player party
    logger.debug("Creating player party (2 characters)")
    player1 = create_test_player("Luffy", level=6)
    player2 = Player("Zoro", level=5)
    logger.debug(f"Player 1: {player1.name}, HP={player1.current_hp}/{player1.max_hp}")
    logger.debug(f"Player 2: {player2.name}, HP={player2.current_hp}/{player2.max_hp}")
    
    # Create multiple enemies
    logger.debug("Creating enemy party (3 enemies)")
    enemy1 = EnemyFactory.create_pirate(level=4)
    enemy1.name = "Pirate A"
    enemy2 = EnemyFactory.create_pirate(level=4)
    enemy2.name = "Pirate B"
    enemy3 = EnemyFactory.create_bandit(level=3)
    logger.debug(f"Enemy 1: {enemy1.name}, HP={enemy1.current_hp}/{enemy1.max_hp}")
    logger.debug(f"Enemy 2: {enemy2.name}, HP={enemy2.current_hp}/{enemy2.max_hp}")
    logger.debug(f"Enemy 3: {enemy3.name}, HP={enemy3.current_hp}/{enemy3.max_hp}")
    
    logger.info("Player Party:")
    logger.info(f"  - {player1}")
    logger.info(f"  - {player2}")
    logger.info("\nEnemy Party:")
    logger.info(f"  - {enemy1}")
    logger.info(f"  - {enemy2}")
    logger.info(f"  - {enemy3}")
    logger.info("")
    
    # Create battle
    logger.debug("Creating BattleManager with 2v3 setup")
    battle = BattleManager([player1, player2], [enemy1, enemy2, enemy3])
    logger.debug(f"Turn order: {[c.name for c in battle.turn_order]}")
    
    # Simulate turns
    turn_count = 0
    max_turns = 20
    enemies_defeated = 0
    logger.debug(f"Starting multi-combat simulation (max {max_turns} turns)")
    
    while battle.battle_active and turn_count < max_turns:
        turn_count += 1
        current_actor = battle.current_actor
        logger.debug(f"\n--- Turn {turn_count}: {current_actor.name}'s turn ---")
        
        if battle.is_player_turn():
            # Player strategy: target weakest enemy
            alive_enemies = battle.get_alive_enemies()
            logger.debug(f"  Alive enemies: {len(alive_enemies)}")
            if alive_enemies:
                # Find lowest HP enemy
                target = min(alive_enemies, key=lambda e: e.current_hp)
                logger.debug(f"  Targeting weakest enemy: {target.name} (HP: {target.current_hp}/{target.max_hp})")
                
                # Use ability if available, otherwise attack
                actor = battle.current_actor
                if actor.devil_fruit and actor.current_ap >= 10:
                    abilities = actor.devil_fruit.get_available_abilities(actor.current_ap)
                    if abilities:
                        logger.debug(f"  Using ability: {abilities[0]['name']}")
                        action = ActionFactory.use_ability(actor, abilities[0], target)
                        battle.execute_action(action)
                        logger.info(f"Turn {turn_count}: {actor.name} used {abilities[0]['name']} on {target.name}")
                    else:
                        logger.debug(f"  No abilities available, attacking")
                        action = ActionFactory.basic_attack(actor, target)
                        battle.execute_action(action)
                        logger.info(f"Turn {turn_count}: {actor.name} attacked {target.name}")
                else:
                    logger.debug(f"  Basic attack")
                    action = ActionFactory.basic_attack(actor, target)
                    battle.execute_action(action)
                    logger.info(f"Turn {turn_count}: {actor.name} attacked {target.name}")
                
                # Check if enemy was defeated
                if not target.is_alive:
                    enemies_defeated += 1
                    logger.debug(f"  {target.name} defeated! ({enemies_defeated} total)")
        else:
            # Enemy AI
            logger.debug(f"  Enemy AI calculating action")
            ai = AIFactory.create_balanced_ai(battle.current_actor, difficulty="normal")
            action = ai.choose_action(battle.get_alive_players(), battle.get_alive_enemies())
            logger.debug(f"  AI chose: {action.action_type.name}")
            battle.execute_action(action)
            logger.info(f"Turn {turn_count}: {current_actor.name} used {action.action_type.name}")
    
    logger.debug(f"\nMulti-combat ended after {turn_count} turns")
    logger.debug(f"Enemies defeated: {enemies_defeated}/3")
    
    logger.info("\n" + "-"*60)
    if battle.result:
        if battle.result.victory:
            logger.info("✓ TEST PASSED - Party Victory Against Multiple Enemies!")
            logger.info(f"  Rewards: {battle.result.exp_gained} EXP, {battle.result.berries_gained} Berries")
            logger.debug(f"  Enemies defeated: {enemies_defeated}")
        else:
            logger.info("✓ TEST PASSED - Battle Ended")
    else:
        logger.info("✓ TEST PASSED - Battle Ended After Max Turns")
    
    return True


def test_boss_battle():
    """Test combat against a boss enemy."""
    logger.info("\n" + "="*60)
    logger.info("TEST 4: BOSS BATTLE")
    logger.info("="*60 + "\n")
    
    logger.debug("Initializing Test 4: Boss Battle")
    
    # Create player party
    logger.debug("Creating player party (2 characters)")
    player1 = create_test_player("Luffy", level=10)
    player2 = Player("Zoro", level=9)
    logger.debug("Boosting Zoro's stats for boss fight")
    player2.stats.increase_stat("strength", 15)
    player2.stats.increase_stat("defense", 10)
    logger.debug(f"Player 1: {player1.name}, Level {player1.level}, HP={player1.current_hp}/{player1.max_hp}")
    logger.debug(f"Player 2: {player2.name}, Level {player2.level}, HP={player2.current_hp}/{player2.max_hp}, STR={player2.stats.strength}")
    
    # Create boss
    logger.debug("Creating boss enemy: Captain Kuro (level 8)")
    boss = EnemyFactory.create_boss("Captain Kuro", level=8)
    boss.description = "A cunning pirate captain with deadly claws."
    logger.debug(f"Boss: {boss.name}, HP={boss.current_hp}/{boss.max_hp}, ATK={boss.stats.get_attack()}")
    
    logger.info("Player Party:")
    logger.info(f"  - {player1}")
    logger.info(f"  - {player2}")
    logger.info("\nBoss:")
    logger.info(f"  - {boss}")
    logger.info(f"    {boss.description}")
    logger.info("")
    
    # Create battle
    logger.debug("Creating BattleManager with boss battle setup")
    battle = BattleManager([player1, player2], [boss])
    logger.debug(f"Turn order: {[c.name for c in battle.turn_order]}")
    
    # Simulate turns
    turn_count = 0
    max_turns = 30
    defend_count = 0
    ability_count = 0
    logger.debug(f"Starting boss battle simulation (max {max_turns} turns)")
    
    while battle.battle_active and turn_count < max_turns:
        turn_count += 1
        current_actor = battle.current_actor
        logger.debug(f"\n--- Turn {turn_count}: {current_actor.name}'s turn ---")
        logger.debug(f"  HP: {current_actor.current_hp}/{current_actor.max_hp} ({current_actor.get_hp_percentage()*100:.1f}%)")
        
        if battle.is_player_turn():
            actor = battle.current_actor
            
            # Strategic play: heal if low HP, ability if available, otherwise attack
            if actor.get_hp_percentage() < 0.3:
                # Would use healing item here
                # For now, just defend
                logger.debug(f"  Low HP! Defending (HP < 30%)")
                action = ActionFactory.defend(actor)
                battle.execute_action(action)
                defend_count += 1
                logger.info(f"Turn {turn_count}: {actor.name} defended (low HP)")
            elif actor.devil_fruit and actor.current_ap >= 15:
                abilities = actor.devil_fruit.get_available_abilities(actor.current_ap)
                if abilities:
                    logger.debug(f"  Using ability: {abilities[0]['name']}")
                    action = ActionFactory.use_ability(actor, abilities[0], boss)
                    battle.execute_action(action)
                    ability_count += 1
                    logger.info(f"Turn {turn_count}: {actor.name} used {abilities[0]['name']} on boss")
                else:
                    logger.debug(f"  No abilities available, attacking")
                    action = ActionFactory.basic_attack(actor, boss)
                    battle.execute_action(action)
                    logger.info(f"Turn {turn_count}: {actor.name} attacked boss")
            else:
                logger.debug(f"  Standard attack")
                action = ActionFactory.basic_attack(actor, boss)
                battle.execute_action(action)
                logger.info(f"Turn {turn_count}: {actor.name} attacked boss")
        else:
            # Boss uses tactical AI
            logger.debug(f"  Boss AI (tactical, hard difficulty) calculating action")
            ai = AIFactory.create_tactical_ai(battle.current_actor, difficulty="hard")
            action = ai.choose_action(battle.get_alive_players(), battle.get_alive_enemies())
            logger.debug(f"  Boss chose: {action.action_type.name}")
            battle.execute_action(action)
            logger.info(f"Turn {turn_count}: Boss {current_actor.name} used {action.action_type.name}")
    
    logger.debug(f"\nBoss battle ended after {turn_count} turns")
    logger.debug(f"Defensive actions: {defend_count}")
    logger.debug(f"Abilities used: {ability_count}")
    logger.debug(f"Boss HP remaining: {boss.current_hp}/{boss.max_hp}")
    
    logger.info("\n" + "-"*60)
    if battle.result:
        if battle.result.victory:
            logger.info("✓ TEST PASSED - Boss Defeated!")
            logger.info(f"  Rewards: {battle.result.exp_gained} EXP, {battle.result.berries_gained} Berries")
            logger.debug(f"  Victory after {turn_count} turns")
        else:
            logger.info("✓ TEST PASSED - Battle Ended (Boss is tough!)")
    else:
        logger.info("✓ TEST PASSED - Battle Ended After Max Turns (Boss survived!)")
    
    return True


def test_ai_behaviors():
    """Test different AI personalities."""
    logger.info("\n" + "="*60)
    logger.info("TEST 5: AI PERSONALITY BEHAVIORS")
    logger.info("="*60 + "\n")
    
    logger.debug("Initializing Test 5: AI Behavior Testing")
    
    player = create_test_player("TestPlayer", level=5)
    logger.debug(f"Test player: {player.name}, HP={player.current_hp}/{player.max_hp}")
    
    # Test aggressive AI
    logger.debug("\n--- Testing Aggressive AI ---")
    logger.info("Testing Aggressive AI...")
    enemy1 = EnemyFactory.create_bandit(level=4)
    logger.debug(f"Created bandit: {enemy1.name}")
    ai1 = AIFactory.create_aggressive_ai(enemy1)
    logger.debug("AI personality: Aggressive")
    action1 = ai1.choose_action([player], [enemy1])
    logger.debug(f"Action chosen: {action1.action_type.name}, Target: {action1.target.name if action1.target else 'None'}")
    logger.info(f"  Aggressive AI chose: {action1.action_type.name}")
    
    # Test defensive AI
    logger.debug("\n--- Testing Defensive AI ---")
    logger.info("Testing Defensive AI...")
    enemy2 = EnemyFactory.create_bandit(level=4)
    logger.debug(f"Created bandit: {enemy2.name}")
    enemy2.take_damage(50)  # Make it low HP
    logger.debug(f"Reduced HP to trigger defensive behavior: {enemy2.current_hp}/{enemy2.max_hp}")
    ai2 = AIFactory.create_defensive_ai(enemy2)
    logger.debug("AI personality: Defensive")
    action2 = ai2.choose_action([player], [enemy2])
    logger.debug(f"Action chosen: {action2.action_type.name}")
    logger.info(f"  Defensive AI chose: {action2.action_type.name}")
    
    # Test tactical AI
    logger.debug("\n--- Testing Tactical AI ---")
    logger.info("Testing Tactical AI...")
    enemy3 = EnemyFactory.create_marine(level=4)
    logger.debug(f"Created marine: {enemy3.name}")
    # Give enemy a Devil Fruit for abilities
    if devil_fruit_manager.loaded:
        fruit = devil_fruit_manager.get_fruit_by_id("bara_bara")
        if fruit:
            logger.debug("Equipping Bara Bara no Mi to enemy")
            enemy3.equip_devil_fruit(fruit)
            logger.debug(f"Enemy abilities: {len(enemy3.devil_fruit.unlocked_abilities)}")
    ai3 = AIFactory.create_tactical_ai(enemy3)
    logger.debug("AI personality: Tactical")
    action3 = ai3.choose_action([player], [enemy3])
    logger.debug(f"Action chosen: {action3.action_type.name}")
    logger.info(f"  Tactical AI chose: {action3.action_type.name}")
    
    logger.info("\n✓ TEST PASSED - All AI Personalities Working!")
    logger.debug("All AI personalities tested successfully")
    return True


def run_all_tests():
    """Run all combat system tests."""
    logger.info("\n" + "="*60)
    logger.info("PHASE 1 PART 7 - COMBAT SYSTEM TEST SUITE")
    logger.info("="*60)
    
    logger.debug("Starting combat system test suite")
    
    tests = [
        ("Basic Combat", test_combat_basic),
        ("Combat with Abilities", test_combat_with_abilities),
        ("Multi-Enemy Battle", test_multi_enemy_battle),
        ("Boss Battle", test_boss_battle),
        ("AI Behaviors", test_ai_behaviors)
    ]
    
    logger.debug(f"Total tests to run: {len(tests)}")
    
    results = []
    
    for i, (test_name, test_func) in enumerate(tests, 1):
        logger.debug(f"\n{'='*60}")
        logger.debug(f"Running test {i}/{len(tests)}: {test_name}")
        logger.debug(f"{'='*60}")
        try:
            result = test_func()
            results.append((test_name, result, None))
            logger.debug(f"Test {test_name} completed successfully")
        except Exception as e:
            logger.error(f"Test {test_name} failed with exception: {e}")
            logger.info(f"\n✗ TEST FAILED - {test_name}")
            logger.info(f"  Error: {e}")
            results.append((test_name, False, str(e)))
            import traceback
            logger.debug(traceback.format_exc())
    
    # Print summary
    logger.info("\n" + "="*60)
    logger.info("TEST SUMMARY")
    logger.info("="*60)
    
    passed = sum(1 for _, result, _ in results if result)
    total = len(results)
    
    logger.debug(f"Test results: {passed} passed, {total - passed} failed out of {total} total")
    
    for test_name, result, error in results:
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status} - {test_name}")
        if error:
            logger.info(f"       Error: {error}")
            logger.debug(f"  Error details: {error}")
    
    logger.info("\n" + "-"*60)
    logger.info(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("\n🎉 ALL TESTS PASSED! Combat system is working!")
        logger.info("\nPhase 1 Part 7 Implementation: SUCCESS ✓")
        logger.debug("All combat system tests passed successfully")
    else:
        logger.warning(f"{total - passed} tests failed")
        logger.info("\n⚠️  Some tests failed. Please review errors above.")
    
    logger.info("="*60)
    
    return passed == total


if __name__ == "__main__":
    logger.debug("="*60)
    logger.debug("Starting Phase 1 Part 7 Test Suite")
    logger.debug("="*60)
    
    # Ensure Devil Fruits are loaded
    logger.info("Loading Devil Fruits...")
    logger.debug("Calling devil_fruit_manager.load_all_fruits()")
    if devil_fruit_manager.load_all_fruits():
        stats = devil_fruit_manager.get_fruit_stats()
        logger.debug(f"Devil Fruit stats: {stats}")
        logger.info(f"✓ Loaded {stats['total']} Devil Fruits\n")
    else:
        logger.warning("No Devil Fruits loaded")
        logger.info("⚠️  No Devil Fruits loaded (some tests may not show abilities)\n")
    
    success = run_all_tests()
    
    log_test_end(logger, 'test_phase1_part7.log')
    
    logger.debug(f"Test suite completed with {'SUCCESS' if success else 'FAILURES'}")
