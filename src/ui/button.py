"""
Button Component
Reusable button widget with hover and click support.
"""

import pygame
from utils.constants import WHITE, UI_HIGHLIGHT_COLOR, GRAY, BLACK


class Button:
    """
    A clickable button UI component with hover and click states.
    Supports both keyboard and mouse interaction.
    """
    
    def __init__(self, x, y, width, height, text, callback=None, 
                 font_size=32, padding=10):
        """
        Initialize the button.
        
        Args:
            x: X position (top-left or center based on centered flag)
            y: Y position (top-left or center based on centered flag)
            width: Button width
            height: Button height
            text: Button text
            callback: Function to call when clicked
            font_size: Size of the text font
            padding: Internal padding
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.padding = padding
        
        # State
        self.hovered = False
        self.pressed = False
        self.enabled = True
        self.visible = True
        
        # Colors
        self.color_normal = GRAY
        self.color_hover = UI_HIGHLIGHT_COLOR
        self.color_pressed = (200, 150, 0)
        self.color_disabled = (80, 80, 80)
        self.text_color = WHITE
        self.text_color_disabled = (150, 150, 150)
        self.border_color = WHITE
        self.border_width = 2
        
        # Font
        self.font = pygame.font.Font(None, font_size)
        
    def handle_event(self, event):
        """
        Handle pygame events.
        
        Args:
            event: pygame.Event object
            
        Returns:
            True if button was clicked
        """
        if not self.enabled or not self.visible:
            return False
        
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.hovered:
                    self.pressed = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                was_pressed = self.pressed
                self.pressed = False
                
                # Button was clicked (pressed and released while hovered)
                if was_pressed and self.hovered:
                    if self.callback:
                        self.callback()
                    return True
        
        return False
    
    def update(self, dt):
        """
        Update button state.
        
        Args:
            dt: Delta time in seconds
        """
        # Could add animations here in the future
        pass
    
    def render(self, surface):
        """
        Draw the button.
        
        Args:
            surface: pygame.Surface to draw on
        """
        if not self.visible:
            return
        
        # Determine current color
        if not self.enabled:
            color = self.color_disabled
            text_color = self.text_color_disabled
        elif self.pressed:
            color = self.color_pressed
            text_color = self.text_color
        elif self.hovered:
            color = self.color_hover
            text_color = self.text_color
        else:
            color = self.color_normal
            text_color = self.text_color
        
        # Draw button background
        pygame.draw.rect(surface, color, self.rect)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)
        
        # Draw text (centered)
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def set_position(self, x, y):
        """Set button position."""
        self.rect.x = x
        self.rect.y = y
    
    def set_size(self, width, height):
        """Set button size."""
        self.rect.width = width
        self.rect.height = height
    
    def set_text(self, text):
        """Change button text."""
        self.text = text
    
    def set_enabled(self, enabled):
        """Enable or disable the button."""
        self.enabled = enabled
        if not enabled:
            self.hovered = False
            self.pressed = False
    
    def set_visible(self, visible):
        """Show or hide the button."""
        self.visible = visible
    
    def is_hovered(self):
        """Check if mouse is over button."""
        return self.hovered and self.enabled
    
    def is_pressed(self):
        """Check if button is currently pressed."""
        return self.pressed and self.enabled
    
    @property
    def x(self):
        """Get button X position."""
        return self.rect.x
    
    @property
    def y(self):
        """Get button Y position."""
        return self.rect.y
    
    @property
    def width(self):
        """Get button width."""
        return self.rect.width
    
    @property
    def height(self):
        """Get button height."""
        return self.rect.height


class TextButton(Button):
    """
    A text-only button without background (for links/text buttons).
    """
    
    def __init__(self, x, y, text, callback=None, font_size=32):
        """Initialize text button."""
        # Create dummy rect for positioning
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, WHITE)
        width, height = text_surface.get_size()
        
        super().__init__(x, y, width + 10, height + 10, text, callback, font_size)
        
        # Override colors for text-only style
        self.color_normal = (0, 0, 0, 0)  # Transparent
        self.border_width = 0
    
    def render(self, surface):
        """Draw text button."""
        if not self.visible:
            return
        
        # Determine text color
        if not self.enabled:
            text_color = self.text_color_disabled
        elif self.hovered:
            text_color = self.color_hover
        else:
            text_color = self.text_color
        
        # Draw text only
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
        # Draw underline when hovered
        if self.hovered:
            underline_rect = pygame.Rect(
                text_rect.left,
                text_rect.bottom,
                text_rect.width,
                2
            )
            pygame.draw.rect(surface, text_color, underline_rect)


class ImageButton(Button):
    """
    A button that displays an image instead of text.
    """
    
    def __init__(self, x, y, width, height, image, callback=None):
        """
        Initialize image button.
        
        Args:
            x: X position
            y: Y position
            width: Button width
            height: Button height
            image: pygame.Surface image to display
            callback: Function to call when clicked
        """
        super().__init__(x, y, width, height, "", callback)
        
        # Store and scale image
        self.original_image = image
        self.image = pygame.transform.scale(image, (width - 20, height - 20))
    
    def render(self, surface):
        """Draw image button."""
        if not self.visible:
            return
        
        # Determine current color
        if not self.enabled:
            color = self.color_disabled
        elif self.pressed:
            color = self.color_pressed
        elif self.hovered:
            color = self.color_hover
        else:
            color = self.color_normal
        
        # Draw button background
        pygame.draw.rect(surface, color, self.rect)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)
        
        # Draw image (centered)
        image_rect = self.image.get_rect(center=self.rect.center)
        surface.blit(self.image, image_rect)
    
    def set_image(self, image):
        """Change button image."""
        self.original_image = image
        self.image = pygame.transform.scale(
            image, 
            (self.rect.width - 20, self.rect.height - 20)
        )
