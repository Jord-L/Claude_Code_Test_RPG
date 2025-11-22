"""
Panel Component
Container widget for grouping UI elements.
"""

import pygame
from utils.constants import UI_BG_COLOR, UI_BORDER_COLOR, WHITE


class Panel:
    """
    A container panel that can hold multiple UI elements.
    """
    
    def __init__(self, x, y, width, height, title="", padding=10):
        """
        Initialize the panel.
        
        Args:
            x: X position
            y: Y position
            width: Panel width
            height: Panel height
            title: Optional title text
            padding: Internal padding
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.padding = padding
        
        # State
        self.visible = True
        self.children = []  # List of child UI elements
        
        # Colors
        self.bg_color = UI_BG_COLOR
        self.border_color = UI_BORDER_COLOR
        self.title_color = WHITE
        self.border_width = 2
        
        # Title font
        self.title_font = pygame.font.Font(None, 32)
        self.title_height = 40 if title else 0
        
        # Content area (inside padding and below title)
        self.content_rect = pygame.Rect(
            x + padding,
            y + padding + self.title_height,
            width - (padding * 2),
            height - (padding * 2) - self.title_height
        )
    
    def add_child(self, child):
        """
        Add a UI element as a child of this panel.
        
        Args:
            child: UI element with handle_event, update, and render methods
        """
        self.children.append(child)
    
    def remove_child(self, child):
        """
        Remove a child UI element.
        
        Args:
            child: UI element to remove
        """
        if child in self.children:
            self.children.remove(child)
    
    def clear_children(self):
        """Remove all child elements."""
        self.children.clear()
    
    def handle_event(self, event):
        """
        Handle pygame events and pass to children.
        
        Args:
            event: pygame.Event object
        """
        if not self.visible:
            return
        
        # Pass event to all children
        for child in self.children:
            if hasattr(child, 'handle_event'):
                child.handle_event(event)
    
    def update(self, dt):
        """
        Update panel and all children.
        
        Args:
            dt: Delta time in seconds
        """
        if not self.visible:
            return
        
        # Update all children
        for child in self.children:
            if hasattr(child, 'update'):
                child.update(dt)
    
    def render(self, surface):
        """
        Draw the panel and all children.
        
        Args:
            surface: pygame.Surface to draw on
        """
        if not self.visible:
            return
        
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)
        
        # Draw title if present
        if self.title:
            title_surface = self.title_font.render(self.title, True, self.title_color)
            title_x = self.rect.x + (self.rect.width - title_surface.get_width()) // 2
            title_y = self.rect.y + 10
            surface.blit(title_surface, (title_x, title_y))
            
            # Draw separator line below title
            line_y = self.rect.y + self.title_height
            pygame.draw.line(
                surface,
                self.border_color,
                (self.rect.x + self.padding, line_y),
                (self.rect.right - self.padding, line_y),
                1
            )
        
        # Render all children
        for child in self.children:
            if hasattr(child, 'render'):
                child.render(surface)
    
    def set_position(self, x, y):
        """
        Set panel position and update children.
        
        Args:
            x: New X position
            y: New Y position
        """
        # Calculate offset
        dx = x - self.rect.x
        dy = y - self.rect.y
        
        # Update panel rect
        self.rect.x = x
        self.rect.y = y
        
        # Update content rect
        self.content_rect.x = x + self.padding
        self.content_rect.y = y + self.padding + self.title_height
        
        # Move all children by the same offset
        for child in self.children:
            if hasattr(child, 'rect'):
                child.rect.x += dx
                child.rect.y += dy
    
    def set_size(self, width, height):
        """
        Set panel size.
        
        Args:
            width: New width
            height: New height
        """
        self.rect.width = width
        self.rect.height = height
        
        # Update content rect
        self.content_rect.width = width - (self.padding * 2)
        self.content_rect.height = height - (self.padding * 2) - self.title_height
    
    def set_visible(self, visible):
        """Show or hide the panel."""
        self.visible = visible
    
    def set_title(self, title):
        """Change panel title."""
        self.title = title
        self.title_height = 40 if title else 0
        self.content_rect.y = self.rect.y + self.padding + self.title_height


class ScrollablePanel(Panel):
    """
    A panel with vertical scrolling support.
    """
    
    def __init__(self, x, y, width, height, title="", padding=10):
        """Initialize scrollable panel."""
        super().__init__(x, y, width, height, title, padding)
        
        # Scrolling
        self.scroll_offset = 0
        self.max_scroll = 0
        self.content_height = 0
        self._update_scroll_bounds()
    
    def _update_scroll_bounds(self):
        """Calculate scroll boundaries based on children."""
        if not self.children:
            self.content_height = 0
            self.max_scroll = 0
            return
        
        # Find lowest child position
        max_y = 0
        for child in self.children:
            if hasattr(child, 'rect'):
                child_bottom = child.rect.y + child.rect.height
                max_y = max(max_y, child_bottom)
        
        self.content_height = max_y - self.content_rect.y
        self.max_scroll = max(0, self.content_height - self.content_rect.height)
    
    def handle_event(self, event):
        """Handle scrolling events."""
        if not self.visible:
            return
        
        # Handle scroll wheel
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                # Scroll
                self.scroll_offset -= event.y * 20
                self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
                
                # Update child positions
                self._apply_scroll()
        
        # Pass to children
        super().handle_event(event)
    
    def _apply_scroll(self):
        """Apply scroll offset to children."""
        for child in self.children:
            if hasattr(child, 'rect') and hasattr(child, '_base_y'):
                child.rect.y = child._base_y - self.scroll_offset
    
    def add_child(self, child):
        """Add child and store base position."""
        super().add_child(child)
        
        # Store base Y position for scrolling
        if hasattr(child, 'rect'):
            child._base_y = child.rect.y
        
        self._update_scroll_bounds()
    
    def render(self, surface):
        """Render with clipping for scroll area."""
        if not self.visible:
            return
        
        # Draw background and border
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)
        
        # Draw title
        if self.title:
            title_surface = self.title_font.render(self.title, True, self.title_color)
            title_x = self.rect.x + (self.rect.width - title_surface.get_width()) // 2
            title_y = self.rect.y + 10
            surface.blit(title_surface, (title_x, title_y))
            
            line_y = self.rect.y + self.title_height
            pygame.draw.line(
                surface,
                self.border_color,
                (self.rect.x + self.padding, line_y),
                (self.rect.right - self.padding, line_y),
                1
            )
        
        # Set clipping for content area
        original_clip = surface.get_clip()
        surface.set_clip(self.content_rect)
        
        # Render children
        for child in self.children:
            if hasattr(child, 'render'):
                child.render(surface)
        
        # Restore clip
        surface.set_clip(original_clip)
        
        # Draw scroll indicator
        if self.max_scroll > 0:
            self._draw_scroll_indicator(surface)
    
    def _draw_scroll_indicator(self, surface):
        """Draw scroll indicator."""
        indicator_width = 8
        indicator_x = self.rect.right - indicator_width - 5
        
        # Calculate indicator size and position
        visible_ratio = self.content_rect.height / self.content_height
        indicator_height = max(20, int(self.content_rect.height * visible_ratio))
        
        scroll_ratio = self.scroll_offset / self.max_scroll if self.max_scroll > 0 else 0
        indicator_y = self.content_rect.y + int((self.content_rect.height - indicator_height) * scroll_ratio)
        
        # Draw indicator
        indicator_rect = pygame.Rect(indicator_x, indicator_y, indicator_width, indicator_height)
        pygame.draw.rect(surface, self.border_color, indicator_rect)


class ModalPanel(Panel):
    """
    A panel that appears centered on screen with a semi-transparent overlay.
    """
    
    def __init__(self, width, height, title="", padding=10):
        """
        Initialize modal panel (will be centered on screen).
        
        Args:
            width: Panel width
            height: Panel height
            title: Panel title
            padding: Internal padding
        """
        # Position will be set when screen size is known
        super().__init__(0, 0, width, height, title, padding)
        
        # Overlay
        self.overlay_color = (0, 0, 0, 180)  # Semi-transparent black
        self.overlay_surface = None
    
    def center_on_screen(self, screen_width, screen_height):
        """Center the modal on the screen."""
        x = (screen_width - self.rect.width) // 2
        y = (screen_height - self.rect.height) // 2
        self.set_position(x, y)
    
    def render(self, surface):
        """Render modal with overlay."""
        if not self.visible:
            return
        
        # Create overlay surface if needed
        if self.overlay_surface is None or self.overlay_surface.get_size() != surface.get_size():
            self.overlay_surface = pygame.Surface(surface.get_size())
            self.overlay_surface.set_alpha(180)
            self.overlay_surface.fill((0, 0, 0))
        
        # Draw overlay
        surface.blit(self.overlay_surface, (0, 0))
        
        # Draw panel on top
        super().render(surface)
