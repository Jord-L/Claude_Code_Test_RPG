"""
Action Menu
Menu for selecting combat actions (Attack, Defend, Ability, Item, Run).
"""

import pygame
from typing import List, Optional, Callable
from utils.constants import *


class ActionOption:
    """Represents a single action option in the menu."""
    
    def __init__(self, action_type: str, display_name: str, enabled: bool = True, callback: Optional[Callable] = None):
        """
        Initialize action option.
        
        Args:
            action_type: Type identifier (e.g., "attack", "defend")
            display_name: Text to display
            enabled: Whether option is selectable
            callback: Function to call when selected
        """
        self.action_type = action_type
        self.display_name = display_name
        self.enabled = enabled
        self.callback = callback


class ActionMenu:
    """
    Menu for selecting combat actions.
    Supports keyboard and mouse navigation.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initialize action menu.
        
        Args:
            x: X position
            y: Y position
            width: Menu width
            height: Menu height
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.active = False  # Can receive input
        
        # Menu options
        self.options: List[ActionOption] = []
        self.selected_index = 0
        
        # Layout
        self.padding = 10
        self.option_height = 50
        self.option_spacing = 5
        
        # Colors
        self.bg_color = UI_BG_COLOR
        self.border_color = UI_BORDER_COLOR
        self.text_color = WHITE
        self.highlight_color = UI_HIGHLIGHT_COLOR
        self.disabled_color = GRAY
        
        # Fonts
        self.font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 36)
        
        # Title
        self.title = "Select Action"
        
        # Callbacks
        self.on_action_selected: Optional[Callable] = None
        self.on_cancel: Optional[Callable] = None
    
    def set_options(self, options: List[ActionOption]):
        """
        Set menu options.
        
        Args:
            options: List of action options
        """
        self.options = options
        self.selected_index = 0
        self._ensure_valid_selection()
    
    def add_option(self, option: ActionOption):
        """Add an option to the menu."""
        self.options.append(option)
    
    def clear_options(self):
        """Remove all options."""
        self.options.clear()
        self.selected_index = 0
    
    def _ensure_valid_selection(self):
        """Ensure selected index points to an enabled option."""
        if not self.options:
            self.selected_index = 0
            return
        
        # If current selection is disabled, find next enabled option
        if not self.options[self.selected_index].enabled:
            self._move_selection(1)
    
    def _move_selection(self, direction: int):
        """
        Move selection up or down.
        
        Args:
            direction: 1 for down, -1 for up
        """
        if not self.options:
            return
        
        start_index = self.selected_index
        attempts = 0
        max_attempts = len(self.options)
        
        while attempts < max_attempts:
            self.selected_index = (self.selected_index + direction) % len(self.options)
            
            if self.options[self.selected_index].enabled:
                return  # Found an enabled option
            
            attempts += 1
        
        # If we couldn't find an enabled option, revert
        self.selected_index = start_index
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle input events.
        
        Args:
            event: Pygame event
        
        Returns:
            True if event was handled
        """
        if not self.visible or not self.active:
            return False
        
        # Keyboard navigation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self._move_selection(-1)
                return True
            
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self._move_selection(1)
                return True
            
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._select_current_option()
                return True
            
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                if self.on_cancel:
                    self.on_cancel()
                return True
        
        # Mouse navigation
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            option_index = self._get_option_at_position(mouse_pos)
            if option_index is not None and self.options[option_index].enabled:
                self.selected_index = option_index
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = event.pos
                option_index = self._get_option_at_position(mouse_pos)
                if option_index is not None:
                    self.selected_index = option_index
                    self._select_current_option()
                    return True
        
        return False
    
    def _get_option_at_position(self, pos: tuple) -> Optional[int]:
        """
        Get option index at mouse position.
        
        Args:
            pos: Mouse position (x, y)
        
        Returns:
            Option index or None
        """
        if not self.rect.collidepoint(pos):
            return None
        
        # Calculate which option the mouse is over
        content_y = self.rect.y + 50  # After title
        
        for i, option in enumerate(self.options):
            option_rect = pygame.Rect(
                self.rect.x + self.padding,
                content_y + i * (self.option_height + self.option_spacing),
                self.rect.width - self.padding * 2,
                self.option_height
            )
            
            if option_rect.collidepoint(pos):
                return i
        
        return None
    
    def _select_current_option(self):
        """Execute the currently selected option."""
        if not self.options or not self.options[self.selected_index].enabled:
            return
        
        selected_option = self.options[self.selected_index]
        
        # Call option callback if it exists
        if selected_option.callback:
            selected_option.callback()
        
        # Call menu callback
        if self.on_action_selected:
            self.on_action_selected(selected_option.action_type)
    
    def update(self, dt: float):
        """
        Update menu state.
        
        Args:
            dt: Delta time in seconds
        """
        # Could add animations here
        pass
    
    def render(self, surface: pygame.Surface):
        """
        Draw the action menu.
        
        Args:
            surface: Surface to draw on
        """
        if not self.visible:
            return
        
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        
        # Draw border
        border_color = self.border_color if self.active else DARK_GRAY
        pygame.draw.rect(surface, border_color, self.rect, 3)
        
        # Draw title
        title_surface = self.title_font.render(self.title, True, self.text_color)
        title_x = self.rect.x + (self.rect.width - title_surface.get_width()) // 2
        title_y = self.rect.y + 10
        surface.blit(title_surface, (title_x, title_y))
        
        # Draw separator line
        line_y = self.rect.y + 45
        pygame.draw.line(
            surface,
            self.border_color,
            (self.rect.x + self.padding, line_y),
            (self.rect.right - self.padding, line_y),
            2
        )
        
        # Draw options
        content_y = self.rect.y + 50
        
        for i, option in enumerate(self.options):
            self._render_option(surface, option, i, content_y)
    
    def _render_option(self, surface: pygame.Surface, option: ActionOption, index: int, start_y: int):
        """
        Render a single menu option.
        
        Args:
            surface: Surface to draw on
            option: Option to render
            index: Option index
            start_y: Y position to start rendering
        """
        option_y = start_y + index * (self.option_height + self.option_spacing)
        option_rect = pygame.Rect(
            self.rect.x + self.padding,
            option_y,
            self.rect.width - self.padding * 2,
            self.option_height
        )
        
        # Determine colors
        is_selected = (index == self.selected_index)
        
        if not option.enabled:
            bg_color = DARK_GRAY
            text_color = self.disabled_color
        elif is_selected:
            bg_color = self.highlight_color
            text_color = BLACK
        else:
            bg_color = GRAY
            text_color = self.text_color
        
        # Draw option background
        pygame.draw.rect(surface, bg_color, option_rect)
        pygame.draw.rect(surface, self.border_color, option_rect, 2)
        
        # Draw selection indicator
        if is_selected and self.active:
            indicator_rect = pygame.Rect(
                option_rect.x + 5,
                option_rect.centery - 10,
                5,
                20
            )
            pygame.draw.rect(surface, RED, indicator_rect)
        
        # Draw text
        text_surface = self.font.render(option.display_name, True, text_color)
        text_x = option_rect.x + 20
        text_y = option_rect.centery - text_surface.get_height() // 2
        surface.blit(text_surface, (text_x, text_y))
        
        # Draw additional info (like AP cost) if available
        # This could be extended in the future
    
    def set_active(self, active: bool):
        """
        Set whether menu is active (can receive input).
        
        Args:
            active: Active state
        """
        self.active = active
    
    def set_visible(self, visible: bool):
        """
        Set menu visibility.
        
        Args:
            visible: Visible state
        """
        self.visible = visible
    
    def get_selected_action(self) -> Optional[str]:
        """
        Get the currently selected action type.
        
        Returns:
            Action type string or None
        """
        if self.options and 0 <= self.selected_index < len(self.options):
            return self.options[self.selected_index].action_type
        return None
