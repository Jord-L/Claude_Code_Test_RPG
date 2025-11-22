"""
State Manager
Manages game states using a stack-based system for smooth transitions.
"""

import pygame
from utils.logger import get_logger


class StateManager:
    """
    Manages game states using a stack.
    Allows for push/pop operations for nested states (like pause menus).
    """
    
    def __init__(self, game):
        """
        Initialize the state manager.
        
        Args:
            game: Reference to main Game instance
        """
        self.game = game
        self.state_dict = {}  # Dictionary of state_name: StateClass
        self.state_stack = []  # Stack of active states
        self.persistent = {}  # Data that persists between states
        self.logger = get_logger()
        
        self.logger.debug("StateManager initialized")
    
    def register_state(self, state_name, state_class):
        """
        Register a state class with a name.
        
        Args:
            state_name: String identifier for the state
            state_class: Class (not instance) of the state
        """
        self.state_dict[state_name] = state_class
        self.logger.debug(f"Registered state: {state_name} -> {state_class.__name__}")
    
    def push_state(self, state_name, **kwargs):
        """
        Push a new state onto the stack.
        The new state becomes active, but previous state remains in memory.
        Useful for overlays like pause menus.
        
        Args:
            state_name: Name of the state to push
            **kwargs: Additional arguments to pass to state startup
        """
        if state_name not in self.state_dict:
            self.logger.error(f"Attempted to push unregistered state: {state_name}")
            raise ValueError(f"State '{state_name}' not registered")
        
        # Pause current state if exists
        if self.state_stack:
            current = self.state_stack[-1]
            self.logger.debug(f"Pausing state: {current.__class__.__name__}")
        
        try:
            # Create and initialize new state
            self.logger.debug(f"Creating state instance: {state_name}")
            new_state = self.state_dict[state_name](self.game)
            
            startup_data = {**self.persistent, **kwargs}
            self.logger.debug(f"Starting up state with data: {list(startup_data.keys())}")
            new_state.startup(startup_data)
            
            # Push to stack
            self.state_stack.append(new_state)
            self.logger.info(f"Pushed state: {state_name} (Stack depth: {len(self.state_stack)})")
            
        except Exception as e:
            self.logger.error(f"Failed to push state '{state_name}': {e}")
            self.logger.exception("Full traceback:")
            raise
    
    def pop_state(self):
        """
        Remove the current state from the stack.
        Returns to the previous state.
        """
        if not self.state_stack:
            self.logger.warning("Attempted to pop from empty state stack")
            return
        
        # Cleanup current state
        current = self.state_stack.pop()
        state_name = current.__class__.__name__
        self.logger.info(f"Popping state: {state_name}")
        
        try:
            # Get persistent data from state
            self.persistent = current.cleanup()
            if self.persistent is None:
                self.persistent = {}
            self.logger.debug(f"State cleanup returned: {list(self.persistent.keys())}")
            
        except Exception as e:
            self.logger.error(f"Error during state cleanup: {e}")
            self.logger.exception("Full traceback:")
            self.persistent = {}
        
        # Resume previous state if exists
        if self.state_stack:
            previous = self.state_stack[-1]
            previous_name = previous.__class__.__name__
            self.logger.info(f"Resuming state: {previous_name}")
            
            try:
                previous.startup(self.persistent)
            except Exception as e:
                self.logger.error(f"Error resuming state '{previous_name}': {e}")
                self.logger.exception("Full traceback:")
        else:
            self.logger.debug("State stack is now empty")
    
    def change_state(self, state_name, **kwargs):
        """
        Replace the current state with a new one.
        Cleans up current state completely.
        
        Args:
            state_name: Name of the new state
            **kwargs: Additional arguments to pass to state startup
        """
        if state_name not in self.state_dict:
            self.logger.error(f"Attempted to change to unregistered state: {state_name}")
            raise ValueError(f"State '{state_name}' not registered")
        
        # Store old state in case new state creation fails
        old_state = None
        
        # Cleanup current state if exists
        if self.state_stack:
            old_state = self.state_stack.pop()
            current_name = old_state.__class__.__name__
            self.logger.info(f"Changing from state: {current_name}")
            
            try:
                self.persistent = old_state.cleanup()
                if self.persistent is None:
                    self.persistent = {}
            except Exception as e:
                self.logger.error(f"Error during state cleanup: {e}")
                self.logger.exception("Full traceback:")
                self.persistent = {}
        
        try:
            # Create and initialize new state
            self.logger.debug(f"Creating state instance: {state_name}")
            new_state = self.state_dict[state_name](self.game)
            
            startup_data = {**self.persistent, **kwargs}
            self.logger.debug(f"Starting up state with data: {list(startup_data.keys())}")
            new_state.startup(startup_data)
            
            # Push to stack
            self.state_stack.append(new_state)
            self.logger.info(f"Changed to state: {state_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to change to state '{state_name}': {e}")
            self.logger.exception("Full traceback:")
            
            # Restore old state if new state creation failed
            if old_state:
                self.logger.warning("Restoring previous state due to failure")
                self.state_stack.append(old_state)
                try:
                    old_state.startup(self.persistent)
                except Exception as restore_error:
                    self.logger.critical(f"Failed to restore previous state: {restore_error}")
            
            raise
    
    def handle_event(self, event):
        """
        Pass event to the current active state.
        
        Args:
            event: pygame.Event object
        """
        if self.state_stack:
            try:
                self.state_stack[-1].handle_event(event)
            except Exception as e:
                # Get state name safely
                state_name = self.state_stack[-1].__class__.__name__ if self.state_stack else "Unknown"
                self.logger.error(f"Error in {state_name}.handle_event(): {e}")
                self.logger.exception("Full traceback:")
    
    def update(self, dt):
        """
        Update the current active state.
        
        Args:
            dt: Delta time in seconds
        """
        if not self.state_stack:
            return
        
        current = self.state_stack[-1]
        
        try:
            current.update(dt)
        except Exception as e:
            state_name = current.__class__.__name__
            self.logger.error(f"Error in {state_name}.update(): {e}")
            self.logger.exception("Full traceback:")
        
        # Check if state wants to transition
        if current.quit:
            self.logger.info(f"State requested quit: {current.__class__.__name__}")
            self.game.running = False
        elif current.done:
            if current.next_state:
                self.logger.debug(f"State requesting transition to: {current.next_state}")
                self.change_state(current.next_state)
            else:
                self.logger.debug("State is done, popping...")
                self.pop_state()
    
    def render(self, surface):
        """
        Render the current active state.
        
        Args:
            surface: pygame.Surface to draw on
        """
        if self.state_stack:
            try:
                self.state_stack[-1].render(surface)
            except Exception as e:
                state_name = self.state_stack[-1].__class__.__name__
                self.logger.error(f"Error in {state_name}.render(): {e}")
                self.logger.exception("Full traceback:")
    
    def get_current_state(self):
        """
        Get the current active state.
        
        Returns:
            Current State object or None
        """
        return self.state_stack[-1] if self.state_stack else None
    
    def get_state_name(self):
        """
        Get the name of the current state.
        
        Returns:
            String name of current state or "None"
        """
        if self.state_stack:
            return self.state_stack[-1].__class__.__name__
        return "None"
    
    def clear_stack(self):
        """Clear all states from the stack."""
        self.logger.info("Clearing state stack...")
        
        while self.state_stack:
            try:
                self.pop_state()
            except Exception as e:
                self.logger.error(f"Error popping state during clear: {e}")
        
        self.logger.info("State stack cleared")
