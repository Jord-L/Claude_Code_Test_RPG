"""
One Piece RPG - Pre-Grand Line
Main Entry Point - VERBOSE DEBUG VERSION

A 2D turn-based RPG set in the One Piece universe
"""

import sys
import os

print("\n" + "=" * 70)
print(" ONE PIECE RPG - PRE-GRAND LINE - DEBUG MODE")
print("=" * 70)
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print()

# Add src directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(project_root, 'src')
print(f"Project root: {project_root}")
print(f"Src directory: {src_dir}")
sys.path.insert(0, src_dir)
print(f"Python path updated: {sys.path[0]}")
print()

# Test imports
print("Testing imports...")
try:
    print("  - Importing pygame...")
    import pygame
    print(f"    ✓ pygame {pygame.version.ver}")
    
    print("  - Importing constants...")
    from utils.constants import GAME_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS
    print(f"    ✓ Constants loaded")
    
    print("  - Importing Game class...")
    from game import Game
    print(f"    ✓ Game class imported")
    
except Exception as e:
    print(f"\n❌ IMPORT ERROR: {e}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to exit...")
    sys.exit(1)

print("\n" + "-" * 70)
print(" STARTING GAME")
print("-" * 70)
print()


def main():
    """Main entry point"""
    print("Initializing game...")
    
    try:
        # Create game instance
        print("Creating Game instance...")
        game = Game()
        print("✓ Game instance created")
        
        print("\nStarting game loop...")
        print("(Press ESC in the game window to exit, or close the window)")
        print()
        
        # Run game
        game.run()
        
        print("\nGame ended normally.")
        
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user (Ctrl+C)")
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    finally:
        # Ensure pygame cleanup
        try:
            pygame.quit()
            print("Pygame cleaned up")
        except:
            pass


if __name__ == "__main__":
    main()
    
    # Keep console window open
    print("\n" + "=" * 70)
    input("Press Enter to close this window...")
