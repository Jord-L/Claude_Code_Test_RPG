"""
Test Script for Phase 1 Part 1
Run this to verify the basic game loop is working correctly.
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

logger = setup_logger('test_phase1_part1')

logger.info("=" * 60)
logger.info("Phase 1 Part 1 - Basic Game Loop Test")
logger.info("=" * 60)
logger.info("")
logger.debug(f"Test started at: {datetime.now()}")
logger.debug(f"Python version: {sys.version}")
logger.debug(f"Working directory: {os.getcwd()}")

# Test 1: Import checks
logger.info("Test 1: Checking imports...")
start_time = time.time()
try:
    from utils import constants
    logger.debug(f"constants module imported from: {constants.__file__}")
    logger.info("✓ constants imported")
    
    from utils import helpers
    logger.debug(f"helpers module imported from: {helpers.__file__}")
    logger.info("✓ helpers imported")
    
    from utils import resource_loader
    logger.debug(f"resource_loader module imported from: {resource_loader.__file__}")
    logger.info("✓ resource_loader imported")
    
    import game
    logger.debug(f"game module imported from: {game.__file__}")
    logger.info("✓ game imported")
    
    elapsed = time.time() - start_time
    logger.debug(f"Import test completed in {elapsed:.3f}s")
    logger.info("✓ All imports successful!\n")
except ImportError as e:
    elapsed = time.time() - start_time
    logger.error(f"Import failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ Import failed: {e}\n")
    sys.exit(1)

# Test 2: Constants check
logger.info("Test 2: Checking constants...")
logger.debug(f"Checking constants values...")
logger.info(f"  - Screen: {constants.SCREEN_WIDTH}x{constants.SCREEN_HEIGHT}")
logger.debug(f"  SCREEN_WIDTH = {constants.SCREEN_WIDTH}")
logger.debug(f"  SCREEN_HEIGHT = {constants.SCREEN_HEIGHT}")
logger.info(f"  - FPS: {constants.FPS}")
logger.debug(f"  FPS = {constants.FPS}")
logger.info(f"  - Title: {constants.GAME_TITLE}")
logger.debug(f"  GAME_TITLE = '{constants.GAME_TITLE}'")
logger.info("✓ Constants loaded correctly!\n")

# Test 3: Helper functions
logger.info("Test 3: Testing helper functions...")
start_time = time.time()
try:
    # Test clamp
    logger.debug("Testing clamp function...")
    result = helpers.clamp(150, 0, 100)
    assert result == 100, "Clamp function failed"
    logger.debug(f"clamp(150, 0, 100) = {result} (expected 100)")
    logger.info(f"  - clamp(150, 0, 100) = {result} ✓")

    # Test lerp
    logger.debug("Testing lerp function...")
    result = helpers.lerp(0, 100, 0.5)
    assert result == 50, "Lerp function failed"
    logger.debug(f"lerp(0, 100, 0.5) = {result} (expected 50)")
    logger.info(f"  - lerp(0, 100, 0.5) = {result} ✓")

    # Test distance
    logger.debug("Testing distance function...")
    result = helpers.distance((0, 0), (3, 4))
    assert abs(result - 5.0) < 0.01, "Distance function failed"
    logger.debug(f"distance((0,0), (3,4)) = {result} (expected ~5.0)")
    logger.info(f"  - distance((0,0), (3,4)) = {result} ✓")

    elapsed = time.time() - start_time
    logger.debug(f"Helper functions test completed in {elapsed:.3f}s")
    logger.info("✓ Helper functions working!\n")
except Exception as e:
    elapsed = time.time() - start_time
    logger.error(f"Helper functions test failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ Helper functions failed: {e}\n")
    sys.exit(1)

# Test 4: Resource loader
logger.info("Test 4: Testing resource loader...")
start_time = time.time()
try:
    logger.debug("Creating ResourceLoader instance...")
    loader = resource_loader.ResourceLoader()
    logger.debug(f"ResourceLoader instance ID: {id(loader)}")
    logger.info(f"  - Singleton instance created")
    logger.debug(f"Assets path: {loader.assets_path}")
    logger.info(f"  - Assets path: {loader.assets_path}")
    
    # Check if assets path exists
    if os.path.exists(loader.assets_path):
        logger.debug(f"Assets path exists: {loader.assets_path}")
    else:
        logger.warning(f"Assets path does not exist: {loader.assets_path}")
    
    elapsed = time.time() - start_time
    logger.debug(f"Resource loader test completed in {elapsed:.3f}s")
    logger.info("✓ Resource loader initialized!\n")
except Exception as e:
    elapsed = time.time() - start_time
    logger.error(f"Resource loader test failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ Resource loader failed: {e}\n")
    sys.exit(1)

# Test 5: Game initialization
logger.info("Test 5: Testing game initialization...")
start_time = time.time()
try:
    logger.debug("Initializing pygame...")
    import pygame
    pygame.init()
    logger.debug("pygame initialized successfully")
    
    logger.debug("Creating Game instance...")
    game_instance = game.Game()
    logger.debug(f"Game instance ID: {id(game_instance)}")
    logger.debug(f"Game window size: {game_instance.screen.get_size()}")
    logger.info(f"  - Game window created: {game_instance.screen.get_size()}")
    logger.debug(f"Clock instance: {game_instance.clock}")
    logger.info(f"  - Clock created: {game_instance.clock}")
    logger.debug(f"Running state: {game_instance.running}")
    logger.info(f"  - Running state: {game_instance.running}")
    
    # Clean up
    logger.debug("Cleaning up pygame...")
    pygame.quit()
    logger.debug("pygame quit successfully")
    
    elapsed = time.time() - start_time
    logger.debug(f"Game initialization test completed in {elapsed:.3f}s")
    logger.info("✓ Game initializes correctly!\n")
except Exception as e:
    elapsed = time.time() - start_time
    logger.error(f"Game initialization failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ Game initialization failed: {e}\n")
    sys.exit(1)

logger.info("=" * 60)
logger.info("All tests passed! ✓")
logger.info("=" * 60)
logger.info("")
logger.info("To run the game, execute: python src/main.py")
logger.info("Press ESC to exit the game")
logger.info("")
logger.debug(f"Test completed at: {datetime.now()}")
logger.debug(f"Log file saved to: logs/test_phase1_part1.log")
