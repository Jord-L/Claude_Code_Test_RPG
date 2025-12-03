"""
Tile Class
Represents a single tile in the game world.
"""

import pygame
from typing import Optional
from utils.constants import TILE_SIZE


class TileType:
    """Enum for tile types."""
    GRASS = "grass"
    WATER = "water"
    SAND = "sand"
    STONE = "stone"
    WOOD = "wood"
    WALL = "wall"
    DOOR = "door"
    DIRT = "dirt"
    ROCK = "rock"
    TREE = "tree"

    # Special tiles
    BATTLE_ZONE = "battle_zone"  # Trigger random encounters
    SAFE_ZONE = "safe_zone"      # No encounters
    TOWN = "town"
    SHOP = "shop"


class Tile:
    """
    A single tile in the game world.
    """
    
    def __init__(self, x: int, y: int, tile_type: str = TileType.GRASS):
        """
        Initialize a tile.
        
        Args:
            x: X position in tile coordinates
            y: Y position in tile coordinates
            tile_type: Type of tile
        """
        self.x = x
        self.y = y
        self.tile_type = tile_type
        
        # World position (pixels)
        self.world_x = x * TILE_SIZE
        self.world_y = y * TILE_SIZE
        
        # Properties
        self.walkable = True
        self.encounter_zone = False
        self.encounter_rate = 0.0
        
        # Visual
        self.color = self._get_color()
        self.sprite: Optional[pygame.Surface] = None
        
        # Set properties based on type
        self._setup_tile_properties()
    
    def _setup_tile_properties(self):
        """Set tile properties based on type."""
        if self.tile_type == TileType.GRASS:
            self.walkable = True
            self.encounter_zone = True
            self.encounter_rate = 0.02  # 2% per step
        
        elif self.tile_type == TileType.WATER:
            self.walkable = False  # Can't walk on water
            self.encounter_zone = False
        
        elif self.tile_type == TileType.SAND:
            self.walkable = True
            self.encounter_zone = True
            self.encounter_rate = 0.015  # 1.5% per step
        
        elif self.tile_type == TileType.STONE:
            self.walkable = True
            self.encounter_zone = False  # Stone paths are safe
        
        elif self.tile_type == TileType.WALL:
            self.walkable = False
            self.encounter_zone = False
        
        elif self.tile_type == TileType.DOOR:
            self.walkable = True
            self.encounter_zone = False
        
        elif self.tile_type == TileType.BATTLE_ZONE:
            self.walkable = True
            self.encounter_zone = True
            self.encounter_rate = 0.05  # 5% per step (higher)
        
        elif self.tile_type == TileType.SAFE_ZONE:
            self.walkable = True
            self.encounter_zone = False
        
        elif self.tile_type == TileType.TOWN:
            self.walkable = True
            self.encounter_zone = False
        
        elif self.tile_type == TileType.WOOD:
            self.walkable = True
            self.encounter_zone = False

        elif self.tile_type == TileType.DIRT:
            self.walkable = True
            self.encounter_zone = True
            self.encounter_rate = 0.03  # 3% per step

        elif self.tile_type == TileType.ROCK:
            self.walkable = False
            self.encounter_zone = False

        elif self.tile_type == TileType.TREE:
            self.walkable = False
            self.encounter_zone = False
    
    def _get_color(self) -> tuple:
        """
        Get color for tile type.
        
        Returns:
            RGB color tuple
        """
        colors = {
            TileType.GRASS: (34, 139, 34),      # Forest green
            TileType.WATER: (0, 119, 190),      # Ocean blue
            TileType.SAND: (238, 214, 175),     # Sandy beige
            TileType.STONE: (128, 128, 128),    # Gray
            TileType.WOOD: (139, 90, 43),       # Brown
            TileType.WALL: (64, 64, 64),        # Dark gray
            TileType.DOOR: (160, 82, 45),       # Sienna
            TileType.DIRT: (101, 67, 33),       # Dark brown
            TileType.ROCK: (105, 105, 105),     # Dim gray
            TileType.TREE: (0, 100, 0),         # Dark green
            TileType.BATTLE_ZONE: (50, 150, 50), # Green
            TileType.SAFE_ZONE: (100, 149, 237), # Cornflower blue
            TileType.TOWN: (210, 180, 140),     # Tan
            TileType.SHOP: (255, 215, 0),       # Gold
        }
        return colors.get(self.tile_type, (255, 255, 255))
    
    def set_walkable(self, walkable: bool):
        """Set whether tile is walkable."""
        self.walkable = walkable
    
    def set_encounter_rate(self, rate: float):
        """Set encounter rate (0.0 to 1.0)."""
        self.encounter_rate = max(0.0, min(1.0, rate))
        self.encounter_zone = rate > 0
    
    def render(self, surface: pygame.Surface, camera_x: int = 0, camera_y: int = 0):
        """
        Render the tile.
        
        Args:
            surface: Surface to draw on
            camera_x: Camera X offset
            camera_y: Camera Y offset
        """
        # Calculate screen position
        screen_x = self.world_x - camera_x
        screen_y = self.world_y - camera_y
        
        # Draw tile
        if self.sprite:
            surface.blit(self.sprite, (screen_x, screen_y))
        else:
            # Draw colored rectangle
            rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(surface, self.color, rect)
            
            # Draw border for clarity
            pygame.draw.rect(surface, (0, 0, 0), rect, 1)
    
    def get_rect(self) -> pygame.Rect:
        """Get tile's world rect."""
        return pygame.Rect(self.world_x, self.world_y, TILE_SIZE, TILE_SIZE)
    
    def contains_point(self, world_x: int, world_y: int) -> bool:
        """
        Check if a world point is within this tile.
        
        Args:
            world_x: World X coordinate
            world_y: World Y coordinate
        
        Returns:
            True if point is in tile
        """
        return self.get_rect().collidepoint(world_x, world_y)
    
    def __repr__(self) -> str:
        """String representation."""
        return f"Tile({self.x}, {self.y}, {self.tile_type})"
