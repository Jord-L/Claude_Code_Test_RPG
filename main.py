"""
One Piece RPG - Pre-Grand Line
Main Entry Point with Logging

A 2D turn-based RPG set in the One Piece universe
"""

import sys
import os
import logging

# Add src directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(project_root, 'src')
sys.path.insert(0, src_dir)

# Initialize logging FIRST (before any other imports)
from utils.logger import init_logger, get_logger

# Initialize logger with INFO level for console, DEBUG for file
logger = init_logger(
    name="OnePieceRPG",
    log_dir=os.path.join(project_root, "logs"),
    console_level=logging.INFO,
    file_level=logging.DEBUG
)

# Now import game
from game import Game


def main():
    """Main entry point"""
    logger.section("ONE PIECE RPG - PRE-GRAND LINE")
    logger.info("Version: 0.1.0-alpha (Phase 1 Development)")
    logger.info(f"Python: {sys.version.split()[0]}")
    logger.info(f"Project root: {project_root}")
    logger.separator()
    
    # Log session information
    logger.info(f"Session log: {logger.get_session_log_path()}")
    logger.info(f"General log: {logger.get_general_log_path()}")
    logger.separator()
    
    try:
        logger.info("Initializing game...")
        game = Game()
        logger.info("Game initialized successfully")
        
        logger.info("Starting game loop...")
        logger.info("Press ESC in the game window to exit")
        logger.separator()
        
        game.run()
        
        logger.info("Game loop ended normally")
        
    except KeyboardInterrupt:
        logger.warning("Game interrupted by user (Ctrl+C)")
        
    except Exception as e:
        logger.critical("=" * 70)
        logger.critical("FATAL ERROR OCCURRED")
        logger.critical("=" * 70)
        logger.exception(f"Error: {e}")
        logger.critical("=" * 70)
        logger.critical("Check the log file for full details")
        logger.critical(f"Log file: {logger.get_session_log_path()}")
        logger.critical("=" * 70)
        
        # Keep console open so user can see error
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    finally:
        # Ensure pygame cleanup
        try:
            import pygame
            pygame.quit()
            logger.info("Pygame cleaned up successfully")
        except:
            pass
        
        logger.separator()
        logger.info("Application shutdown complete")
        logger.info(f"Full session log saved to: {logger.get_session_log_path()}")
        logger.separator()


if __name__ == "__main__":
    main()
