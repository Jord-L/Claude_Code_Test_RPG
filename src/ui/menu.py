"""
Menu Component
Generic menu system for creating navigable option lists.
"""

import pygame
from utils.constants import WHITE, UI_HIGHLIGHT_COLOR, GRAY


class Menu:
    """
    A generic vertical menu with keyboard and mouse navigation.
    """
    
    def __init__(self, x, y, options, font_size=36, spacing=50):
        """
        Initialize the menu.
        
        Args:
            x: X position (center of menu)
            y: Y position (top of first option)
            options: List of menu option strings
            font_size: Size of option text
            spacing: Vertical spacing between options
        """
        self.x = x
        self.y = y
        self.options = options
        self.spacing = spacing
        self.selected_index = 0
        
        # State
        self.visible = True
        self.enabled = True
        
        # Colors
        self.text_color = WHITE
        self.selected_color = UI_HIGHLIGHT_COLOR
        self.disabled_color = GRAY
        
        # Font
        self.font = pygame.font.Font(None, font_size)
        
        # Selection indicator
        self.show_indicator = True
        self.indicator_text = "> "
        
        # Animation
        self.pulse_timer = 0
        self.pulse_speed = 3.0
        
        # Build option rects for mouse interaction
        self._build_option_rects()
    
    def _build_option_rects(self):
        """Create rectangles for each option for mouse detection."""
        self.option_rects = []
        
        for i, option in enumerate(self.options):
            text = self.indicator_text + option if self.show_indicator else option
            text_surface = self.font.render(text, True, self.text_color)
            
            y_pos = self.y + (i * self.spacing)
            rect = text_surface.get_rect(center=(self.x, y_pos))
            
            # Add some padding for easier clicking
            rect.inflate_ip(20, 10)
            
            self.option_rects.append(rect)
    
    def handle_event(self, event):
        """
        Handle input events.
        
        Args:
            event: pygame.Event object
            
        Returns:
            Selected option index if confirmed, None otherwise
        """
        if not self.visible or not self.enabled:
            return None
        
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.move_selection(-1)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.move_selection(1)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.selected_index
        
        elif event.type == pygame.MOUSEMOTION:
            # Check which option is hovered
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    self.selected_index = i
                    break
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check if clicked on an option
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected_index = i
                        return i
        
        return None
    
    def update(self, dt):
        """
        Update menu state.
        
        Args:
            dt: Delta time in seconds
        """
        if not self.visible:
            return
        
        # Update pulse animation
        self.pulse_timer += dt * self.pulse_speed
    
    def render(self, surface):
        """
        Draw the menu.
        
        Args:
            surface: pygame.Surface to draw on
        """
        if not self.visible:
            return
        
        for i, option in enumerate(self.options):
            y_pos = self.y + (i * self.spacing)
            
            # Determine if this option is selected
            is_selected = (i == self.selected_index)
            
            # Choose color
            if not self.enabled:
                color = self.disabled_color
            elif is_selected:
                # Pulse effect
                pulse = abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 60).x)
                alpha = int(155 + (pulse * 100))
                color = self.selected_color
            else:
                color = self.text_color
            
            # Add indicator to selected option
            text = self.indicator_text + option if (is_selected and self.show_indicator) else "  " + option
            
            # Render text
            text_surface = self.font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self.x, y_pos))
            surface.blit(text_surface, text_rect)
    
    def move_selection(self, direction):
        """
        Move selection up or down.
        
        Args:
            direction: -1 for up, 1 for down
        """
        self.selected_index = (self.selected_index + direction) % len(self.options)
    
    def set_selected(self, index):
        """Set the selected option by index."""
        if 0 <= index < len(self.options):
            self.selected_index = index
    
    def get_selected(self):
        """Get the currently selected option index."""
        return self.selected_index
    
    def get_selected_text(self):
        """Get the text of the currently selected option."""
        return self.options[self.selected_index]
    
    def set_options(self, options):
        """Change the menu options."""
        self.options = options
        self.selected_index = 0
        self._build_option_rects()
    
    def set_enabled(self, enabled):
        """Enable or disable the menu."""
        self.enabled = enabled
    
    def set_visible(self, visible):
        """Show or hide the menu."""
        self.visible = visible


class HorizontalMenu(Menu):
    """
    A horizontal menu (options arranged left to right).
    """
    
    def __init__(self, x, y, options, font_size=36, spacing=100):
        """
        Initialize horizontal menu.
        
        Args:
            x: X position (left edge)
            y: Y position (center of menu)
            options: List of menu option strings
            font_size: Size of option text
            spacing: Horizontal spacing between options
        """
        super().__init__(x, y, options, font_size, spacing)
    
    def _build_option_rects(self):
        """Build rects for horizontal layout."""
        self.option_rects = []
        
        for i, option in enumerate(self.options):
            text_surface = self.font.render(option, True, self.text_color)
            
            x_pos = self.x + (i * self.spacing)
            rect = text_surface.get_rect(center=(x_pos, self.y))
            rect.inflate_ip(20, 10)
            
            self.option_rects.append(rect)
    
    def handle_event(self, event):
        """Handle input with left/right keys."""
        if not self.visible or not self.enabled:
            return None
        
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.move_selection(-1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.move_selection(1)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.selected_index
        
        # Still handle mouse normally
        elif event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    self.selected_index = i
                    break
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected_index = i
                        return i
        
        return None
    
    def render(self, surface):
        """Draw horizontal menu."""
        if not self.visible:
            return
        
        for i, option in enumerate(self.options):
            x_pos = self.x + (i * self.spacing)
            
            is_selected = (i == self.selected_index)
            
            # Choose color
            if not self.enabled:
                color = self.disabled_color
            elif is_selected:
                pulse = abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 60).x)
                color = self.selected_color
            else:
                color = self.text_color
            
            # Render text
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(x_pos, self.y))
            surface.blit(text_surface, text_rect)
            
            # Draw underline for selected
            if is_selected and self.show_indicator:
                underline_width = text_rect.width
                underline_rect = pygame.Rect(
                    text_rect.left,
                    text_rect.bottom + 5,
                    underline_width,
                    3
                )
                pygame.draw.rect(surface, color, underline_rect)


class GridMenu(Menu):
    """
    A menu with options arranged in a grid.
    """
    
    def __init__(self, x, y, options, columns=3, font_size=32, 
                 cell_width=150, cell_height=60):
        """
        Initialize grid menu.
        
        Args:
            x: X position (left edge)
            y: Y position (top edge)
            options: List of menu option strings
            columns: Number of columns in grid
            font_size: Size of option text
            cell_width: Width of each grid cell
            cell_height: Height of each grid cell
        """
        self.columns = columns
        self.cell_width = cell_width
        self.cell_height = cell_height
        
        super().__init__(x, y, options, font_size, cell_height)
    
    def _build_option_rects(self):
        """Build rects for grid layout."""
        self.option_rects = []
        
        for i, option in enumerate(self.options):
            row = i // self.columns
            col = i % self.columns
            
            x_pos = self.x + (col * self.cell_width) + (self.cell_width // 2)
            y_pos = self.y + (row * self.cell_height) + (self.cell_height // 2)
            
            rect = pygame.Rect(
                self.x + (col * self.cell_width),
                self.y + (row * self.cell_height),
                self.cell_width,
                self.cell_height
            )
            
            self.option_rects.append(rect)
    
    def handle_event(self, event):
        """Handle input with arrow keys for grid navigation."""
        if not self.visible or not self.enabled:
            return None
        
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self._move_selection_grid(-1, 0)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self._move_selection_grid(1, 0)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self._move_selection_grid(0, -1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self._move_selection_grid(0, 1)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.selected_index
        
        # Mouse handling
        elif event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    self.selected_index = i
                    break
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected_index = i
                        return i
        
        return None
    
    def _move_selection_grid(self, row_delta, col_delta):
        """Move selection in grid."""
        current_row = self.selected_index // self.columns
        current_col = self.selected_index % self.columns
        
        new_row = current_row + row_delta
        new_col = current_col + col_delta
        
        # Calculate new index
        new_index = (new_row * self.columns) + new_col
        
        # Wrap around
        if new_index < 0:
            new_index = len(self.options) - 1
        elif new_index >= len(self.options):
            new_index = 0
        
        self.selected_index = new_index
    
    def render(self, surface):
        """Draw grid menu."""
        if not self.visible:
            return
        
        for i, option in enumerate(self.options):
            row = i // self.columns
            col = i % self.columns
            
            x_pos = self.x + (col * self.cell_width) + (self.cell_width // 2)
            y_pos = self.y + (row * self.cell_height) + (self.cell_height // 2)
            
            is_selected = (i == self.selected_index)
            
            # Draw cell background if selected
            if is_selected:
                cell_rect = self.option_rects[i]
                pulse = abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 60).x)
                alpha = int(50 + (pulse * 50))
                bg_surface = pygame.Surface((cell_rect.width, cell_rect.height))
                bg_surface.set_alpha(alpha)
                bg_surface.fill(self.selected_color)
                surface.blit(bg_surface, cell_rect)
            
            # Choose color
            if not self.enabled:
                color = self.disabled_color
            elif is_selected:
                color = self.selected_color
            else:
                color = self.text_color
            
            # Render text
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(x_pos, y_pos))
            surface.blit(text_surface, text_rect)
