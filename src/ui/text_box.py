"""
Text Box Component
Widget for displaying text with word wrapping and formatting.
"""

import pygame
from utils.constants import WHITE, BLACK, UI_BG_COLOR, UI_BORDER_COLOR


class TextBox:
    """
    A text display widget with word wrapping and scrolling support.
    """
    
    def __init__(self, x, y, width, height, text="", font_size=24, padding=10):
        """
        Initialize the text box.
        
        Args:
            x: X position
            y: Y position
            width: Box width
            height: Box height
            text: Initial text content
            font_size: Size of the text font
            padding: Internal padding
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.padding = padding
        
        # State
        self.visible = True
        self.scrollable = False
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Colors
        self.bg_color = UI_BG_COLOR
        self.text_color = WHITE
        self.border_color = UI_BORDER_COLOR
        self.border_width = 2
        
        # Font
        self.font = pygame.font.Font(None, font_size)
        self.line_height = self.font.get_height() + 4
        
        # Text rendering
        self.wrapped_lines = []
        self._wrap_text()
    
    def _wrap_text(self):
        """Wrap text to fit within the box width."""
        self.wrapped_lines = []
        
        if not self.text:
            return
        
        words = self.text.split(' ')
        current_line = []
        max_width = self.rect.width - (self.padding * 2)
        
        for word in words:
            # Check for manual line breaks
            if '\n' in word:
                parts = word.split('\n')
                for i, part in enumerate(parts):
                    if i > 0:
                        # Add current line and start new one
                        if current_line:
                            self.wrapped_lines.append(' '.join(current_line))
                            current_line = []
                    if part:
                        current_line.append(part)
                continue
            
            # Try adding word to current line
            test_line = current_line + [word]
            test_text = ' '.join(test_line)
            test_surface = self.font.render(test_text, True, self.text_color)
            
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                # Word doesn't fit, start new line
                if current_line:
                    self.wrapped_lines.append(' '.join(current_line))
                current_line = [word]
        
        # Add remaining line
        if current_line:
            self.wrapped_lines.append(' '.join(current_line))
        
        # Calculate max scroll
        total_height = len(self.wrapped_lines) * self.line_height
        visible_height = self.rect.height - (self.padding * 2)
        self.max_scroll = max(0, total_height - visible_height)
        self.scrollable = self.max_scroll > 0
    
    def handle_event(self, event):
        """
        Handle pygame events (scrolling).
        
        Args:
            event: pygame.Event object
        """
        if not self.visible or not self.scrollable:
            return
        
        if event.type == pygame.MOUSEWHEEL:
            # Check if mouse is over text box
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                # Scroll (negative y = scroll up)
                self.scroll_offset -= event.y * self.line_height
                self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
    
    def update(self, dt):
        """Update text box state."""
        pass
    
    def render(self, surface):
        """
        Draw the text box.
        
        Args:
            surface: pygame.Surface to draw on
        """
        if not self.visible:
            return
        
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)
        
        # Create clipping rect for text (so it doesn't overflow)
        clip_rect = pygame.Rect(
            self.rect.x + self.padding,
            self.rect.y + self.padding,
            self.rect.width - (self.padding * 2),
            self.rect.height - (self.padding * 2)
        )
        
        # Save original clip
        original_clip = surface.get_clip()
        surface.set_clip(clip_rect)
        
        # Draw text lines
        y_offset = self.rect.y + self.padding - self.scroll_offset
        
        for line in self.wrapped_lines:
            # Only draw if visible
            if y_offset + self.line_height >= self.rect.y and y_offset < self.rect.y + self.rect.height:
                text_surface = self.font.render(line, True, self.text_color)
                surface.blit(text_surface, (self.rect.x + self.padding, y_offset))
            
            y_offset += self.line_height
        
        # Restore original clip
        surface.set_clip(original_clip)
        
        # Draw scroll indicator if scrollable
        if self.scrollable:
            self._draw_scroll_indicator(surface)
    
    def _draw_scroll_indicator(self, surface):
        """Draw a scroll indicator on the right side."""
        indicator_width = 8
        indicator_x = self.rect.right - indicator_width - 5
        
        # Calculate indicator height and position
        visible_ratio = (self.rect.height - self.padding * 2) / (len(self.wrapped_lines) * self.line_height)
        indicator_height = max(20, int((self.rect.height - self.padding * 2) * visible_ratio))
        
        scroll_ratio = self.scroll_offset / self.max_scroll if self.max_scroll > 0 else 0
        indicator_y = self.rect.y + self.padding + int((self.rect.height - self.padding * 2 - indicator_height) * scroll_ratio)
        
        # Draw indicator
        indicator_rect = pygame.Rect(indicator_x, indicator_y, indicator_width, indicator_height)
        pygame.draw.rect(surface, self.border_color, indicator_rect)
    
    def set_text(self, text):
        """
        Change the text content.
        
        Args:
            text: New text string
        """
        self.text = text
        self.scroll_offset = 0
        self._wrap_text()
    
    def append_text(self, text):
        """
        Append text to existing content.
        
        Args:
            text: Text to append
        """
        self.text += text
        self._wrap_text()
    
    def clear(self):
        """Clear all text."""
        self.text = ""
        self.wrapped_lines = []
        self.scroll_offset = 0
        self.max_scroll = 0
    
    def set_position(self, x, y):
        """Set text box position."""
        self.rect.x = x
        self.rect.y = y
    
    def set_size(self, width, height):
        """Set text box size and re-wrap text."""
        self.rect.width = width
        self.rect.height = height
        self._wrap_text()
    
    def set_visible(self, visible):
        """Show or hide the text box."""
        self.visible = visible
    
    def scroll_to_top(self):
        """Scroll to the top of the text."""
        self.scroll_offset = 0
    
    def scroll_to_bottom(self):
        """Scroll to the bottom of the text."""
        self.scroll_offset = self.max_scroll


class Label(TextBox):
    """
    A simple text label (non-scrollable, auto-sized text box).
    """
    
    def __init__(self, x, y, text="", font_size=24, color=WHITE):
        """
        Initialize the label.
        
        Args:
            x: X position
            y: Y position
            text: Label text
            font_size: Text size
            color: Text color
        """
        # Create font to measure text
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        width, height = text_surface.get_size()
        
        super().__init__(x, y, width + 10, height + 10, text, font_size, padding=5)
        
        # Override colors for label style
        self.bg_color = (0, 0, 0, 0)  # Transparent
        self.border_width = 0
        self.text_color = color
        self.scrollable = False
    
    def render(self, surface):
        """Draw label (just text, no background)."""
        if not self.visible:
            return
        
        # Draw text only
        if self.wrapped_lines:
            text_surface = self.font.render(self.wrapped_lines[0], True, self.text_color)
            surface.blit(text_surface, (self.rect.x + self.padding, self.rect.y + self.padding))


class MultilineLabel(Label):
    """
    A multi-line label that auto-sizes to fit all text.
    """
    
    def __init__(self, x, y, text="", font_size=24, color=WHITE, max_width=None):
        """
        Initialize multi-line label.
        
        Args:
            x: X position
            y: Y position
            text: Label text
            font_size: Text size
            color: Text color
            max_width: Maximum width before wrapping (None = no wrap)
        """
        self.max_width = max_width
        super().__init__(x, y, text, font_size, color)
    
    def _wrap_text(self):
        """Override to respect max_width."""
        if self.max_width:
            # Temporarily set width for wrapping
            old_width = self.rect.width
            self.rect.width = self.max_width
            super()._wrap_text()
            
            # Resize to fit content
            height = len(self.wrapped_lines) * self.line_height + (self.padding * 2)
            self.rect.height = height
        else:
            # No max width - split by newlines only
            self.wrapped_lines = self.text.split('\n') if self.text else []
    
    def render(self, surface):
        """Draw multi-line label."""
        if not self.visible:
            return
        
        y_offset = self.rect.y + self.padding
        for line in self.wrapped_lines:
            text_surface = self.font.render(line, True, self.text_color)
            surface.blit(text_surface, (self.rect.x + self.padding, y_offset))
            y_offset += self.line_height


class CenteredText:
    """
    Simple centered text renderer for menus and UI.
    """
    
    def __init__(self, x, y, text="", font_size=24, color=WHITE, centered=True):
        """
        Initialize centered text.
        
        Args:
            x: X position (center if centered=True)
            y: Y position
            text: Text to display
            font_size: Size of font
            color: Text color
            centered: If True, x is center point; if False, x is left edge
        """
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size
        self.color = color
        self.centered = centered
        self.visible = True
        
        self.font = pygame.font.Font(None, font_size)
        self._update_surface()
    
    def _update_surface(self):
        """Update the rendered text surface."""
        self.surface = self.font.render(self.text, True, self.color)
        if self.centered:
            self.rect = self.surface.get_rect(center=(self.x, self.y))
        else:
            self.rect = self.surface.get_rect(topleft=(self.x, self.y))
    
    def set_text(self, text):
        """Change the text."""
        self.text = text
        self._update_surface()
    
    def set_color(self, color):
        """Change the text color."""
        self.color = color
        self._update_surface()
    
    def render(self, surface):
        """Draw the text."""
        if self.visible:
            surface.blit(self.surface, self.rect)
