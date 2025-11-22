"""
Camera System
Camera that follows the player and handles viewport.
"""

import pygame
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


class Camera:
    """
    Camera system for 2D world exploration.
    Centers on player and handles map boundaries.
    """
    
    def __init__(self, map_width: int, map_height: int):
        """
        Initialize camera.
        
        Args:
            map_width: Map width in pixels
            map_height: Map height in pixels
        """
        self.x = 0
        self.y = 0
        self.map_width = map_width
        self.map_height = map_height
        
        # Camera movement smoothing
        self.smoothing = 0.1  # 0 = instant, 1 = no smoothing
        self.target_x = 0
        self.target_y = 0
        
        # Shake effect (for impacts, explosions, etc.)
        self.shake_amount = 0
        self.shake_duration = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0
    
    def center_on(self, world_x: int, world_y: int):
        """
        Center camera on a world position.
        
        Args:
            world_x: World X coordinate
            world_y: World Y coordinate
        """
        # Calculate centered position
        self.target_x = world_x - SCREEN_WIDTH // 2
        self.target_y = world_y - SCREEN_HEIGHT // 2
        
        # Clamp to map bounds
        self.target_x = max(0, min(self.target_x, self.map_width - SCREEN_WIDTH))
        self.target_y = max(0, min(self.target_y, self.map_height - SCREEN_HEIGHT))
    
    def update(self, dt: float):
        """
        Update camera position.
        
        Args:
            dt: Delta time in seconds
        """
        # Smooth camera movement
        if self.smoothing > 0:
            self.x += (self.target_x - self.x) * (1 - self.smoothing)
            self.y += (self.target_y - self.y) * (1 - self.smoothing)
        else:
            self.x = self.target_x
            self.y = self.target_y
        
        # Update screen shake
        if self.shake_duration > 0:
            self.shake_duration -= dt
            
            if self.shake_duration <= 0:
                self.shake_offset_x = 0
                self.shake_offset_y = 0
            else:
                import random
                self.shake_offset_x = random.randint(-self.shake_amount, self.shake_amount)
                self.shake_offset_y = random.randint(-self.shake_amount, self.shake_amount)
    
    def get_offset(self) -> tuple:
        """
        Get camera offset including shake.
        
        Returns:
            (x, y) offset tuple
        """
        return (
            int(self.x + self.shake_offset_x),
            int(self.y + self.shake_offset_y)
        )
    
    def shake(self, amount: int = 5, duration: float = 0.3):
        """
        Start screen shake effect.
        
        Args:
            amount: Shake intensity in pixels
            duration: Shake duration in seconds
        """
        self.shake_amount = amount
        self.shake_duration = duration
    
    def world_to_screen(self, world_x: int, world_y: int) -> tuple:
        """
        Convert world coordinates to screen coordinates.
        
        Args:
            world_x: World X coordinate
            world_y: World Y coordinate
        
        Returns:
            (screen_x, screen_y) tuple
        """
        offset_x, offset_y = self.get_offset()
        return (world_x - offset_x, world_y - offset_y)
    
    def screen_to_world(self, screen_x: int, screen_y: int) -> tuple:
        """
        Convert screen coordinates to world coordinates.
        
        Args:
            screen_x: Screen X coordinate
            screen_y: Screen Y coordinate
        
        Returns:
            (world_x, world_y) tuple
        """
        offset_x, offset_y = self.get_offset()
        return (screen_x + offset_x, screen_y + offset_y)
    
    def is_visible(self, world_x: int, world_y: int, width: int = TILE_SIZE, height: int = TILE_SIZE) -> bool:
        """
        Check if a rectangle is visible on screen.
        
        Args:
            world_x: World X coordinate
            world_y: World Y coordinate
            width: Rectangle width
            height: Rectangle height
        
        Returns:
            True if visible
        """
        offset_x, offset_y = self.get_offset()
        
        # Convert to screen space
        screen_x = world_x - offset_x
        screen_y = world_y - offset_y
        
        # Check if on screen
        return (screen_x + width >= 0 and 
                screen_x < SCREEN_WIDTH and
                screen_y + height >= 0 and
                screen_y < SCREEN_HEIGHT)
    
    def get_rect(self) -> pygame.Rect:
        """
        Get camera viewport rectangle in world space.
        
        Returns:
            Camera rect
        """
        offset_x, offset_y = self.get_offset()
        return pygame.Rect(offset_x, offset_y, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    def set_map_size(self, map_width: int, map_height: int):
        """
        Update map size for boundary clamping.
        
        Args:
            map_width: Map width in pixels
            map_height: Map height in pixels
        """
        self.map_width = map_width
        self.map_height = map_height
