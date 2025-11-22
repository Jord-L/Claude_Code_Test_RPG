"""
Diagnostic Test Script
Tests if the game can start properly and identifies issues.
"""

import sys
import os

print("=" * 60)
print("DIAGNOSTIC TEST - One Piece RPG")
print("=" * 60)
print()

# Test 1: Check Python version
print("Test 1: Checking Python version...")
print(f"  Python version: {sys.version}")
print(f"  Python executable: {sys.executable}")
if sys.version_info < (3, 8):
    print("  ⚠️ WARNING: Python 3.8+ recommended")
else:
    print("  ✓ Python version OK")
print()

# Test 2: Check if pygame is installed
print("Test 2: Checking pygame installation...")
try:
    import pygame
    print(f"  ✓ pygame {pygame.version.ver} found")
except ImportError as e:
    print(f"  ✗ pygame not found: {e}")
    print("  Run: pip install pygame")
    input("\nPress Enter to exit...")
    sys.exit(1)
print()

# Test 3: Check if src directory is in path
print("Test 3: Checking project structure...")
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
print(f"  Project root: {project_root}")
print(f"  Src directory: {src_path}")
if os.path.exists(src_path):
    print("  ✓ src directory found")
else:
    print("  ✗ src directory not found!")
print()

# Test 4: Try to import game modules
print("Test 4: Testing imports...")
sys.path.insert(0, project_root)
try:
    from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE
    print(f"  ✓ Constants imported")
    print(f"    - Title: {GAME_TITLE}")
    print(f"    - Resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print(f"    - FPS: {FPS}")
except Exception as e:
    print(f"  ✗ Failed to import constants: {e}")
    import traceback
    traceback.print_exc()

try:
    from src.game import Game
    print(f"  ✓ Game class imported")
except Exception as e:
    print(f"  ✗ Failed to import Game class: {e}")
    import traceback
    traceback.print_exc()
print()

# Test 5: Try to initialize pygame
print("Test 5: Testing pygame initialization...")
try:
    pygame.init()
    print("  ✓ pygame initialized")
    
    # Try to create a test window
    print("  Creating test window...")
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test Window")
    print("  ✓ Window created successfully")
    
    # Show window for 2 seconds
    print("  Displaying window for 2 seconds...")
    clock = pygame.time.Clock()
    for i in range(2):
        screen.fill((0, 100, 0))  # Green screen
        font = pygame.font.Font(None, 48)
        text = font.render(f"Test Window - {2-i}s", True, (255, 255, 255))
        screen.blit(text, (200, 275))
        pygame.display.flip()
        
        # Process events to prevent "not responding"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        
        clock.tick(1)  # 1 FPS for this test
    
    pygame.quit()
    print("  ✓ pygame test successful")
    
except Exception as e:
    print(f"  ✗ pygame initialization failed: {e}")
    import traceback
    traceback.print_exc()
print()

# Test 6: Try to actually create Game instance
print("Test 6: Testing Game class instantiation...")
try:
    from src.game import Game
    print("  Creating Game instance...")
    game = Game()
    print("  ✓ Game instance created successfully!")
    print("  Game is ready to run.")
    
    # Clean up
    pygame.quit()
    
except Exception as e:
    print(f"  ✗ Failed to create Game instance: {e}")
    import traceback
    traceback.print_exc()
print()

print("=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
print()
print("If all tests passed, try running: python main.py")
print("If tests failed, check the error messages above.")
print()
input("Press Enter to exit...")
