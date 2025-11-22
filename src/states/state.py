"""
Base State Class
Abstract base class for all game states (menu, gameplay, battle, etc.)
"""

from abc import ABC, abstractmethod
import pygame


class State(ABC):
    """
    Abstract base class for game states.
    All game states (menu, world, battle, etc.) should inherit from this.
    """
    
    def __init__(self, game):
        """
        Initialize the state.
        
        Args:
            game: Reference to the main Game instance
        """
        self.game = game
        self.screen = game.screen
        self.state_manager = game.state_manager  # Easy access to state manager
        self.next_state = None
        self.done = False
        self.quit = False
        self.previous = None
    
    @abstractmethod
    def startup(self, persistent):
        """
        Called when state becomes active.
        Use this to initialize or reset state variables.
        
        Args:
            persistent: Dictionary of persistent data from previous state
        """
        pass
    
    @abstractmethod
    def cleanup(self):
        """
        Called when leaving the state.
        Use this to save data or clean up resources.
        
        Returns:
            Dictionary of data to pass to next state
        """
        pass
    
    @abstractmethod
    def handle_event(self, event):
        """
        Handle a single pygame event.
        
        Args:
            event: pygame.Event object
        """
        pass
    
    @abstractmethod
    def update(self, dt):
        """
        Update state logic.
        
        Args:
            dt: Delta time in seconds since last frame
        """
        pass
    
    @abstractmethod
    def render(self, surface):
        """
        Render the state to the screen.
        
        Args:
            surface: pygame.Surface to draw on
        """
        pass
    
    def flip_state(self):
        """Mark this state as done and prepare for next state."""
        self.done = True
    
    def reset_state(self):
        """Reset the state flags."""
        self.done = False
        self.quit = False
        self.next_state = None
