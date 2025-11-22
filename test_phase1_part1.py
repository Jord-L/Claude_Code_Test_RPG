"""
Test Script for Phase 1 Part 1
Run this to verify the basic game loop is working correctly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 60)
print("Phase 1 Part 1 - Basic Game Loop Test")
print("=" * 60)
print()

# Test 1: Import checks
print("Test 1: Checking imports...")
try:
    from utils import constants
    print("✓ constants imported")
    
    from utils import helpers
    print("✓ helpers imported")
    
    from utils import resource_loader
    print("✓ resource_loader imported")
    
    import game
    print("✓ game imported")
    
    print("✓ All imports successful!\n")
except ImportError as e:
    print(f"✗ Import failed: {e}\n")
    sys.exit(1)

# Test 2: Constants check
print("Test 2: Checking constants...")
print(f"  - Screen: {constants.SCREEN_WIDTH}x{constants.SCREEN_HEIGHT}")
print(f"  - FPS: {constants.FPS}")
print(f"  - Title: {constants.GAME_TITLE}")
print("✓ Constants loaded correctly!\n")

# Test 3: Helper functions
print("Test 3: Testing helper functions...")
result = helpers.clamp(150, 0, 100)
assert result == 100, "Clamp function failed"
print(f"  - clamp(150, 0, 100) = {result} ✓")

result = helpers.lerp(0, 100, 0.5)
assert result == 50, "Lerp function failed"
print(f"  - lerp(0, 100, 0.5) = {result} ✓")

result = helpers.distance((0, 0), (3, 4))
assert abs(result - 5.0) < 0.01, "Distance function failed"
print(f"  - distance((0,0), (3,4)) = {result} ✓")

print("✓ Helper functions working!\n")

# Test 4: Resource loader
print("Test 4: Testing resource loader...")
loader = resource_loader.ResourceLoader()
print(f"  - Singleton instance created")
print(f"  - Assets path: {loader.assets_path}")
print("✓ Resource loader initialized!\n")

# Test 5: Game initialization
print("Test 5: Testing game initialization...")
try:
    import pygame
    pygame.init()
    
    game_instance = game.Game()
    print(f"  - Game window created: {game_instance.screen.get_size()}")
    print(f"  - Clock created: {game_instance.clock}")
    print(f"  - Running state: {game_instance.running}")
    
    # Clean up
    pygame.quit()
    print("✓ Game initializes correctly!\n")
except Exception as e:
    print(f"✗ Game initialization failed: {e}\n")
    sys.exit(1)

print("=" * 60)
print("All tests passed! ✓")
print("=" * 60)
print()
print("To run the game, execute: python src/main.py")
print("Press ESC to exit the game")
print()
