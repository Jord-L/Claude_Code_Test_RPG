"""
Test Script for Phase 1 Part 2
Run this to verify the state management system is working correctly.
"""

import sys
import os
import logging
import time
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Setup logging
def setup_logger(test_name):
    """Setup logger for this test file."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger.handlers = []
    
    # File handler
    log_file = os.path.join(log_dir, f"{test_name}.log")
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger('test_phase1_part2')

logger.info("=" * 60)
logger.info("Phase 1 Part 2 - State Management System Test")
logger.info("=" * 60)
logger.info("")
logger.debug(f"Test started at: {datetime.now()}")

# Test 1: Import checks
logger.info("Test 1: Checking new imports...")
start_time = time.time()
try:
    from states.state import State
    logger.debug(f"State class imported from: {State.__module__}")
    logger.info("✓ State base class imported")
    
    from states.state_manager import StateManager
    logger.debug(f"StateManager class imported from: {StateManager.__module__}")
    logger.info("✓ StateManager imported")
    
    from states.menu_state import MenuState
    logger.debug(f"MenuState class imported from: {MenuState.__module__}")
    logger.info("✓ MenuState imported")
    
    elapsed = time.time() - start_time
    logger.debug(f"Import test completed in {elapsed:.3f}s")
    logger.info("✓ All state imports successful!\n")
except ImportError as e:
    elapsed = time.time() - start_time
    logger.error(f"Import failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ Import failed: {e}\n")
    sys.exit(1)

# Test 2: State class structure
logger.info("Test 2: Testing State base class...")
start_time = time.time()
try:
    # Check if State is abstract
    from abc import ABC
    logger.debug("Checking if State is abstract base class...")
    assert issubclass(State, ABC), "State should inherit from ABC"
    logger.debug(f"State MRO: {[c.__name__ for c in State.__mro__]}")
    logger.info("✓ State is abstract base class")
    
    # Check required methods exist
    required_methods = ['startup', 'cleanup', 'handle_event', 'update', 'render']
    logger.debug(f"Checking for required methods: {required_methods}")
    for method in required_methods:
        assert hasattr(State, method), f"State missing method: {method}"
        logger.debug(f"  Found method: {method}")
    logger.info(f"✓ State has all required methods: {required_methods}")
    
    elapsed = time.time() - start_time
    logger.debug(f"State structure test completed in {elapsed:.3f}s")
    logger.info("✓ State base class structure correct!\n")
except AssertionError as e:
    elapsed = time.time() - start_time
    logger.error(f"State structure test failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ State structure test failed: {e}\n")
    sys.exit(1)

# Test 3: StateManager functionality
logger.info("Test 3: Testing StateManager...")
start_time = time.time()
try:
    import pygame
    pygame.init()
    logger.debug("pygame initialized for StateManager test")
    
    # Create a mock game object
    class MockGame:
        def __init__(self):
            self.screen = pygame.display.set_mode((800, 600))
            self.running = True
            logger.debug("MockGame created with 800x600 screen")
    
    mock_game = MockGame()
    logger.debug(f"MockGame instance ID: {id(mock_game)}")
    
    manager = StateManager(mock_game)
    logger.debug(f"StateManager instance ID: {id(manager)}")
    logger.info("✓ StateManager created")
    
    # Test state registration
    logger.debug("Registering 'menu' state...")
    manager.register_state("menu", MenuState)
    logger.debug(f"State dict keys: {list(manager.state_dict.keys())}")
    assert "menu" in manager.state_dict, "State not registered"
    logger.info("✓ State registration works")
    
    # Test state stack is empty initially
    initial_stack_len = len(manager.state_stack)
    logger.debug(f"Initial state stack length: {initial_stack_len}")
    assert initial_stack_len == 0, "State stack should be empty"
    logger.info("✓ State stack initially empty")
    
    # Test changing to a state
    logger.debug("Changing to 'menu' state...")
    manager.change_state("menu")
    new_stack_len = len(manager.state_stack)
    logger.debug(f"State stack length after change: {new_stack_len}")
    assert new_stack_len == 1, "State not added to stack"
    logger.info("✓ State change works")
    
    # Test getting current state
    logger.debug("Getting current state...")
    current = manager.get_current_state()
    logger.debug(f"Current state: {current}, type: {type(current).__name__}")
    assert current is not None, "Current state is None"
    assert isinstance(current, MenuState), "Current state wrong type"
    logger.info("✓ Get current state works")
    
    # Test state name
    logger.debug("Getting state name...")
    name = manager.get_state_name()
    logger.debug(f"State name: {name}")
    assert name == "MenuState", f"State name wrong: {name}"
    logger.info("✓ State name retrieval works")
    
    # Cleanup
    logger.debug("Clearing state stack...")
    manager.clear_stack()
    final_stack_len = len(manager.state_stack)
    logger.debug(f"Final state stack length: {final_stack_len}")
    assert final_stack_len == 0, "Stack not cleared"
    logger.info("✓ Stack clearing works")
    
    pygame.quit()
    logger.debug("pygame quit")
    
    elapsed = time.time() - start_time
    logger.debug(f"StateManager test completed in {elapsed:.3f}s")
    logger.info("✓ StateManager functionality verified!\n")
    
except Exception as e:
    elapsed = time.time() - start_time
    logger.error(f"StateManager test failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ StateManager test failed: {e}\n")
    pygame.quit()
    sys.exit(1)

# Test 4: MenuState functionality
logger.info("Test 4: Testing MenuState...")
start_time = time.time()
try:
    import pygame
    pygame.init()
    logger.debug("pygame initialized for MenuState test")
    
    class MockGame:
        def __init__(self):
            self.screen = pygame.display.set_mode((800, 600))
            self.running = True
    
    mock_game = MockGame()
    menu = MenuState(mock_game)
    logger.debug(f"MenuState instance ID: {id(menu)}")
    logger.info("✓ MenuState created")
    
    # Test startup
    logger.debug("Calling MenuState.startup()...")
    menu.startup({})
    logger.debug(f"Selected index after startup: {menu.selected_index}")
    assert menu.selected_index == 0, "Initial selection wrong"
    logger.info("✓ MenuState startup works")
    
    # Test options exist
    options_count = len(menu.options)
    logger.debug(f"Menu options count: {options_count}")
    logger.debug(f"Menu options: {menu.options}")
    assert options_count == 4, "Wrong number of menu options"
    expected_options = ["New Game", "Load Game", "Settings", "Exit"]
    assert menu.options == expected_options, "Menu options incorrect"
    logger.info(f"✓ Menu options correct: {menu.options}")
    
    # Test update
    logger.debug("Testing MenuState.update()...")
    menu.update(0.016)  # Simulate one frame
    logger.debug("MenuState update completed without error")
    logger.info("✓ MenuState update works")
    
    # Test render (just check it doesn't crash)
    logger.debug("Testing MenuState.render()...")
    surface = pygame.Surface((800, 600))
    menu.render(surface)
    logger.debug("MenuState render completed without error")
    logger.info("✓ MenuState render works")
    
    # Test cleanup
    logger.debug("Testing MenuState.cleanup()...")
    data = menu.cleanup()
    logger.debug(f"Cleanup returned: {type(data).__name__}")
    assert isinstance(data, dict), "Cleanup should return dict"
    logger.info("✓ MenuState cleanup works")
    
    pygame.quit()
    logger.debug("pygame quit")
    
    elapsed = time.time() - start_time
    logger.debug(f"MenuState test completed in {elapsed:.3f}s")
    logger.info("✓ MenuState functionality verified!\n")
    
except Exception as e:
    elapsed = time.time() - start_time
    logger.error(f"MenuState test failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ MenuState test failed: {e}\n")
    pygame.quit()
    sys.exit(1)

# Test 5: Integration test
logger.info("Test 5: Testing Game integration...")
start_time = time.time()
try:
    import pygame
    pygame.init()
    logger.debug("pygame initialized for integration test")
    
    import game
    logger.debug("Creating Game instance...")
    game_instance = game.Game()
    logger.debug(f"Game instance ID: {id(game_instance)}")
    logger.info("✓ Game initializes with state system")
    
    # Check state manager exists
    logger.debug("Checking for state_manager attribute...")
    assert hasattr(game_instance, 'state_manager'), "Game missing state_manager"
    logger.debug(f"state_manager ID: {id(game_instance.state_manager)}")
    logger.info("✓ Game has state_manager")
    
    # Check state is registered and active
    logger.debug("Checking if initial state is active...")
    current_state = game_instance.state_manager.get_current_state()
    logger.debug(f"Current state: {current_state}")
    assert current_state is not None, "No active state"
    logger.info("✓ Initial state is active")
    
    # Check it's the menu state
    logger.debug("Checking initial state type...")
    state_name = game_instance.state_manager.get_state_name()
    logger.debug(f"State name: {state_name}")
    assert state_name == "MenuState", "Initial state should be MenuState"
    logger.info("✓ Initial state is MenuState")
    
    # Cleanup
    pygame.quit()
    logger.debug("pygame quit")
    
    elapsed = time.time() - start_time
    logger.debug(f"Integration test completed in {elapsed:.3f}s")
    logger.info("✓ Game integration verified!\n")
    
except Exception as e:
    elapsed = time.time() - start_time
    logger.error(f"Game integration test failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ Game integration test failed: {e}\n")
    pygame.quit()
    sys.exit(1)

logger.info("=" * 60)
logger.info("All tests passed! ✓")
logger.info("=" * 60)
logger.info("")
logger.info("To run the game with new menu, execute: python src/main.py")
logger.info("")
logger.info("New controls:")
logger.info("  ↑/↓ or W/S - Navigate menu")
logger.info("  ENTER/SPACE - Select option")
logger.info("  ESC - Exit from main menu")
logger.info("  F3 - Toggle FPS display")
logger.info("")
logger.debug(f"Test completed at: {datetime.now()}")
logger.debug(f"Log file saved to: logs/test_phase1_part2.log")
