"""
One Piece RPG - Pre-Grand Line
Main Entry Point

This is the entry point for the game. It initializes the game and starts the main loop.
"""

import pygame
import sys
from game import Game


def main():
    """Initialize and run the game."""
    try:
        # Create game instance
        game = Game()
        
        # Run the game
        game.run()
        
    except Exception as e:
        print(f"Fatal error occurred: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        # Ensure proper cleanup
        pygame.quit()
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
