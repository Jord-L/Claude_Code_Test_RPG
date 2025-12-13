"""
Game Class
Main game class that handles the game loop, state management, and core systems.
"""

import pygame
from utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE,
    BLACK, WHITE, STATE_MENU, STATE_CHAR_CREATION
)
from utils.logger import get_logger
from states.state_manager import StateManager
from states.menu_state import MenuState
from states.character_creation_state import CharacterCreationState
from states.world_state import WorldState
from states.battle_state import BattleState


class Game:
    """Main game class that manages the game loop and states."""
    
    def __init__(self):
        """Initialize the game."""
        self.logger = get_logger()
        self.logger.debug("Initializing Game class...")
        
        # Initialize Pygame
        self.logger.debug("Initializing Pygame...")
        pygame.init()
        
        # Create the game window
        self.logger.debug(f"Creating game window ({SCREEN_WIDTH}x{SCREEN_HEIGHT})...")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.logger.info(f"Game window created: {GAME_TITLE}")
        self.logger.info(f"Resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        
        # Clock for FPS control
        self.clock = pygame.time.Clock()
        self.logger.debug(f"Target FPS: {FPS}")
        
        # Game state
        self.running = True
        self.dt = 0  # Delta time
        self.show_fps = True  # Toggle FPS display
        
        # Initialize state manager
        self.logger.debug("Initializing state manager...")
        self.state_manager = StateManager(self)
        
        # Register all states
        self.logger.debug("Registering game states...")
        self._register_states()
        
        # Start with main menu
        self.logger.info("Starting with main menu state...")
        self.state_manager.change_state(STATE_MENU)
        
        self.logger.info("Game initialization complete")
    
    def _register_states(self):
        """Register all game states with the state manager."""
        self.logger.debug(f"Registering state: {STATE_MENU} -> MenuState")
        self.state_manager.register_state(STATE_MENU, MenuState)
        
        self.logger.debug(f"Registering state: {STATE_CHAR_CREATION} -> CharacterCreationState")
        self.state_manager.register_state(STATE_CHAR_CREATION, CharacterCreationState)
        
        self.logger.debug(f"Registering state: world -> WorldState")
        self.state_manager.register_state("world", WorldState)
        
        self.logger.debug(f"Registering state: battle -> BattleState")
        self.state_manager.register_state("battle", BattleState)
    
    def handle_events(self):
        """Handle all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.logger.info("Quit event received")
                self.running = False
            
            # Global key handlers
            if event.type == pygame.KEYDOWN:
                # F3 toggles FPS display
                if event.key == pygame.K_F3:
                    self.show_fps = not self.show_fps
                    self.logger.debug(f"FPS display: {'ON' if self.show_fps else 'OFF'}")
                
                # F12 for quick debug info dump
                if event.key == pygame.K_F12:
                    self._log_debug_info()
            
            # Pass events to current state
            try:
                self.state_manager.handle_event(event)
            except Exception as e:
                self.logger.error(f"Error handling event in state: {e}")
                self.logger.exception("Full traceback:")
    
    def update(self):
        """Update game logic."""
        try:
            # Update current state
            self.state_manager.update(self.dt)
        except Exception as e:
            self.logger.error(f"Error updating state: {e}")
            self.logger.exception("Full traceback:")
    
    def render(self):
        """Render the game."""
        try:
            # Clear screen
            self.screen.fill(BLACK)
            
            # Render current state
            self.state_manager.render(self.screen)
            
            # Draw FPS counter if enabled
            if self.show_fps:
                self._draw_fps()
            
            # Draw state name (debug info)
            self._draw_debug_info()
            
            # Update display
            pygame.display.flip()
        except Exception as e:
            self.logger.error(f"Error rendering: {e}")
            self.logger.exception("Full traceback:")
    
    def _draw_fps(self):
        """Draw FPS counter in top-right corner."""
        fps = int(self.clock.get_fps())
        font = pygame.font.Font(None, 28)
        
        # Choose color based on FPS
        if fps >= 58:
            color = (0, 255, 0)  # Green - good
        elif fps >= 45:
            color = (255, 255, 0)  # Yellow - acceptable
        else:
            color = (255, 0, 0)  # Red - poor
        
        fps_text = font.render(f"FPS: {fps}", True, color)
        self.screen.blit(fps_text, (SCREEN_WIDTH - 100, 10))
    
    def _draw_debug_info(self):
        """Draw debug information in top-left corner."""
        font = pygame.font.Font(None, 24)
        state_name = self.state_manager.get_state_name()
        debug_text = font.render(f"State: {state_name}", True, WHITE)
        self.screen.blit(debug_text, (10, 10))
    
    def _log_debug_info(self):
        """Log detailed debug information (F12 key)."""
        self.logger.separator("-")
        self.logger.info("DEBUG INFO DUMP (F12)")
        self.logger.info(f"Running: {self.running}")
        self.logger.info(f"Delta Time: {self.dt:.4f}s")
        self.logger.info(f"FPS: {int(self.clock.get_fps())}")
        self.logger.info(f"Current State: {self.state_manager.get_state_name()}")
        self.logger.info(f"State Stack Depth: {len(self.state_manager.state_stack)}")
        self.logger.separator("-")
    
    def run(self):
        """Main game loop."""
        self.logger.info("Entering main game loop")
        self.logger.debug("Game controls: F3=Toggle FPS, F12=Debug Info, ESC=Exit")
        
        frame_count = 0
        
        try:
            while self.running:
                frame_count += 1
                
                # Handle events
                self.handle_events()
                
                # Update game logic
                self.update()
                
                # Render
                self.render()
                
                # Control FPS and calculate delta time
                self.dt = self.clock.tick(FPS) / 1000.0  # Convert to seconds
                
                # Log every 1800 frames (30 seconds at 60 FPS)
                if frame_count % 1800 == 0:
                    self.logger.debug(f"Running: {frame_count} frames, {frame_count // 60} seconds, FPS: {int(self.clock.get_fps())}")
        
        except Exception as e:
            self.logger.critical("Exception in main game loop!")
            self.logger.exception(f"Error: {e}")
            raise
        
        finally:
            self.logger.info(f"Game loop ended after {frame_count} frames")
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources before exit."""
        self.logger.info("Starting cleanup...")
        
        try:
            self.state_manager.clear_stack()
            self.logger.debug("State manager cleared")
        except Exception as e:
            self.logger.error(f"Error clearing state manager: {e}")
        
        self.logger.info("Cleanup complete")
