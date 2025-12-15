"""
Main Menu State
The main menu screen with navigation options.
"""

import pygame
from states.state import State
from ui.button import Button
from ui.text_box import CenteredText
from utils.constants import *


class MenuState(State):
    """
    Main menu state with options for New Game, Load Game, Settings, Exit.
    """
    
    def __init__(self, game):
        """
        Initialize the menu state.
        
        Args:
            game: Game instance
        """
        super().__init__(game)
        
        # Menu options
        self.options = [
            "New Game",
            "Load Game",
            "Settings",
            "Exit"
        ]
        self.selected_index = 0
        
        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 48)
        self.subtitle_font = pygame.font.Font(None, 32)
        
        # Colors
        self.text_color = WHITE
        self.highlight_color = UI_HIGHLIGHT_COLOR
        
        # Menu positioning
        self.menu_y_start = SCREEN_HEIGHT // 2
        self.menu_spacing = 60
        
        # Animation
        self.pulse_timer = 0
        self.pulse_speed = 3.0
        
        # UI Components
        self.title_text = None
        self.subtitle_text = None
        self.buttons = []
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up UI components."""
        # Title
        self.title_text = CenteredText(
            x=SCREEN_WIDTH // 2,
            y=150,
            text="One Piece RPG",
            font_size=72,
            color=WHITE,
            centered=True
        )
        
        # Subtitle
        self.subtitle_text = CenteredText(
            x=SCREEN_WIDTH // 2,
            y=210,
            text="Pre-Grand Line",
            font_size=32,
            color=WHITE,
            centered=True
        )
        
        # Create buttons for menu options
        button_width = 300
        button_height = 50
        
        for i, option in enumerate(self.options):
            y_pos = self.menu_y_start + (i * self.menu_spacing)
            
            button = Button(
                x=SCREEN_WIDTH // 2 - button_width // 2,
                y=y_pos - button_height // 2,
                width=button_width,
                height=button_height,
                text=option,
                callback=lambda opt=option: self._select_option(opt)
            )
            self.buttons.append(button)
    
    def _select_option(self, option: str):
        """
        Handle menu option selection.
        
        Args:
            option: Selected menu option
        """
        print(f"Menu: Selected '{option}'")
        
        if option == "New Game":
            # Transition to character creation
            self.state_manager.change_state(STATE_CHAR_CREATION)

        elif option == "Load Game":
            # Transition to load game screen
            from utils.constants import STATE_LOAD_GAME
            self.state_manager.change_state(STATE_LOAD_GAME)

        elif option == "Settings":
            # Transition to settings screen
            from utils.constants import STATE_SETTINGS
            self.state_manager.change_state(STATE_SETTINGS)

        elif option == "Exit":
            # Exit the game
            import sys
            pygame.quit()
            sys.exit()
    
    def handle_event(self, event: pygame.event.Event):
        """
        Handle menu input.
        
        Args:
            event: Pygame event
        """
        # Keyboard navigation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_index = (self.selected_index - 1) % len(self.options)
                print(f"Menu: Highlighted '{self.options[self.selected_index]}'")
            
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_index = (self.selected_index + 1) % len(self.options)
                print(f"Menu: Highlighted '{self.options[self.selected_index]}'")
            
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                selected_option = self.options[self.selected_index]
                self._select_option(selected_option)
            
            elif event.key == pygame.K_ESCAPE:
                # ESC on main menu exits game
                import sys
                pygame.quit()
                sys.exit()
        
        # Handle button events (mouse)
        for i, button in enumerate(self.buttons):
            button.handle_event(event)
            
            # Update selection index based on mouse hover
            if button.is_hovered:
                self.selected_index = i
    
    def update(self, dt: float):
        """
        Update menu state.
        
        Args:
            dt: Delta time
        """
        # Update pulse animation for selected item
        self.pulse_timer += dt * self.pulse_speed
        
        # Update buttons
        for button in self.buttons:
            button.update(dt)
    
    def render(self, screen: pygame.Surface):
        """
        Render the main menu.
        
        Args:
            screen: Pygame surface to render to
        """
        # Clear screen with background
        screen.fill(BLACK)
        
        # Draw title
        self.title_text.render(screen)
        
        # Draw subtitle
        self.subtitle_text.render(screen)
        
        # Draw menu options (custom rendering for selection indicator)
        for i, option in enumerate(self.options):
            y_pos = self.menu_y_start + (i * self.menu_spacing)
            
            # Determine color (highlight selected)
            if i == self.selected_index:
                # Pulse effect for selected item
                import math
                pulse = abs(math.sin(self.pulse_timer))
                alpha = int(155 + (pulse * 100))
                
                # Draw selection indicator
                indicator = "> "
                color = self.highlight_color
            else:
                indicator = "  "
                color = self.text_color
            
            # Draw option text
            text = indicator + option
            text_surface = self.menu_font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            screen.blit(text_surface, text_rect)
        
        # Draw controls hint at bottom
        hint_text = "↑↓ Navigate  |  ENTER Select  |  ESC Exit"
        hint_surface = self.subtitle_font.render(hint_text, True, self.text_color)
        hint_rect = hint_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(hint_surface, hint_rect)
        
        # Draw version info
        version_text = "v0.1.0-alpha | Phase 1 Part 6"
        version_font = pygame.font.Font(None, 24)
        version_surface = version_font.render(version_text, True, self.text_color)
        screen.blit(version_surface, (10, SCREEN_HEIGHT - 30))
    
    def startup(self, persistent):
        """Called when state becomes active."""
        print("Main Menu loaded")
        self.selected_index = 0
        self.pulse_timer = 0
    
    def cleanup(self):
        """Called when state is removed."""
        print("Main Menu cleanup")
        return {}
