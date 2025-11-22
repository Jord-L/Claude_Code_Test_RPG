"""
Character Preview Component
Visual preview of the character being created.
"""

import pygame
from typing import Optional
from entities.character import Character
from entities.player import Player
from utils.constants import *


class CharacterPreview:
    """
    Displays a visual preview of the character.
    Shows character sprite, name, and Devil Fruit info.
    """
    
    def __init__(self, x: int, y: int, size: int = 100):
        """
        Initialize character preview.
        
        Args:
            x: Center X position
            y: Center Y position
            size: Size of the preview box
        """
        self.x = x
        self.y = y
        self.size = size
        
        # Character data
        self.character: Optional[Character] = None
        
        # Preview colors (placeholder until we have sprites)
        self.base_color = (100, 150, 200)  # Blue-ish
        self.fruit_color = None
        
        # Fonts
        self.name_font = pygame.font.Font(None, 24)
        self.fruit_font = pygame.font.Font(None, 18)
        
        # Animation
        self.bob_offset = 0
        self.bob_speed = 2.0
        self.bob_amplitude = 5
    
    def set_character(self, character: Character):
        """
        Set the character to preview.
        
        Args:
            character: Character instance
        """
        self.character = character
        
        # Set fruit-specific color if applicable
        if character.devil_fruit:
            fruit_type = character.devil_fruit.fruit_type
            
            if fruit_type == "logia":
                self.fruit_color = (255, 100, 100)  # Red for Logia
            elif fruit_type == "zoan":
                self.fruit_color = (255, 200, 100)  # Orange for Zoan
            elif fruit_type == "paramecia":
                self.fruit_color = (150, 100, 255)  # Purple for Paramecia
        else:
            self.fruit_color = None
    
    def update(self, dt: float):
        """
        Update animation.
        
        Args:
            dt: Delta time
        """
        # Simple bobbing animation
        self.bob_offset = self.bob_amplitude * pygame.math.sin(
            pygame.time.get_ticks() * 0.001 * self.bob_speed
        )
    
    def render(self, screen: pygame.Surface):
        """
        Render the character preview.
        
        Args:
            screen: Surface to render to
        """
        if not self.character:
            self._render_placeholder(screen)
            return
        
        # Calculate bob position
        preview_y = self.y + self.bob_offset
        
        # Draw character sprite (placeholder)
        self._render_character_sprite(screen, self.x, int(preview_y))
        
        # Draw character name
        self._render_name(screen)
        
        # Draw Devil Fruit indicator
        if self.character.devil_fruit:
            self._render_fruit_indicator(screen)
    
    def _render_placeholder(self, screen: pygame.Surface):
        """Render placeholder when no character is set."""
        # Draw question mark
        placeholder_rect = pygame.Rect(
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size
        )
        
        pygame.draw.rect(screen, GRAY, placeholder_rect)
        pygame.draw.rect(screen, WHITE, placeholder_rect, 2)
        
        # Draw question mark
        font = pygame.font.Font(None, 72)
        text = font.render("?", True, WHITE)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
    
    def _render_character_sprite(self, screen: pygame.Surface, x: int, y: int):
        """
        Render character sprite (currently a placeholder).
        
        Args:
            screen: Surface to render to
            x: X position
            y: Y position
        """
        # TODO: Replace with actual sprite rendering when sprites are available
        
        # Draw base character shape (circle for now)
        color = self.fruit_color if self.fruit_color else self.base_color
        
        # Body
        pygame.draw.circle(screen, color, (x, y), self.size // 2)
        pygame.draw.circle(screen, WHITE, (x, y), self.size // 2, 3)
        
        # Add some details
        # Eyes
        eye_offset = self.size // 6
        eye_size = self.size // 10
        pygame.draw.circle(screen, WHITE, (x - eye_offset, y - eye_offset), eye_size)
        pygame.draw.circle(screen, WHITE, (x + eye_offset, y - eye_offset), eye_size)
        pygame.draw.circle(screen, BLACK, (x - eye_offset, y - eye_offset), eye_size // 2)
        pygame.draw.circle(screen, BLACK, (x + eye_offset, y - eye_offset), eye_size // 2)
        
        # Smile
        smile_rect = pygame.Rect(
            x - self.size // 3,
            y,
            self.size // 1.5,
            self.size // 3
        )
        pygame.draw.arc(screen, WHITE, smile_rect, 3.14, 0, 3)
        
        # Pirate hat (simple triangle)
        hat_points = [
            (x, y - self.size // 2 - 20),
            (x - self.size // 3, y - self.size // 2),
            (x + self.size // 3, y - self.size // 2)
        ]
        pygame.draw.polygon(screen, BLACK, hat_points)
        pygame.draw.polygon(screen, WHITE, hat_points, 2)
    
    def _render_name(self, screen: pygame.Surface):
        """Render character name below the sprite."""
        if not self.character:
            return
        
        name_text = self.name_font.render(
            self.character.name,
            True,
            WHITE
        )
        name_rect = name_text.get_rect(center=(self.x, self.y + self.size // 2 + 40))
        
        # Background for better visibility
        bg_rect = name_rect.inflate(20, 10)
        pygame.draw.rect(screen, (20, 20, 40), bg_rect)
        pygame.draw.rect(screen, UI_BORDER_COLOR, bg_rect, 2)
        
        screen.blit(name_text, name_rect)
    
    def _render_fruit_indicator(self, screen: pygame.Surface):
        """Render Devil Fruit indicator."""
        if not self.character or not self.character.devil_fruit:
            return
        
        fruit = self.character.devil_fruit
        
        # Fruit icon (small circle with type indicator)
        icon_x = self.x - self.size // 2 - 20
        icon_y = self.y - self.size // 2
        icon_radius = 15
        
        # Draw fruit icon
        pygame.draw.circle(screen, self.fruit_color, (icon_x, icon_y), icon_radius)
        pygame.draw.circle(screen, WHITE, (icon_x, icon_y), icon_radius, 2)
        
        # Type letter (P/Z/L)
        type_letter = fruit.fruit_type[0].upper()
        letter_font = pygame.font.Font(None, 20)
        letter_text = letter_font.render(type_letter, True, WHITE)
        letter_rect = letter_text.get_rect(center=(icon_x, icon_y))
        screen.blit(letter_text, letter_rect)
        
        # Fruit name below preview
        fruit_name = fruit.name
        if len(fruit_name) > 20:
            fruit_name = fruit_name[:17] + "..."
        
        fruit_text = self.fruit_font.render(
            fruit_name,
            True,
            self.fruit_color
        )
        fruit_rect = fruit_text.get_rect(center=(self.x, self.y + self.size // 2 + 70))
        screen.blit(fruit_text, fruit_rect)
    
    def get_rect(self) -> pygame.Rect:
        """
        Get the bounding rectangle.
        
        Returns:
            Pygame Rect
        """
        return pygame.Rect(
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size
        )
