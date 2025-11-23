"""
Map Class
Tile-based map system for the game world.
"""

import pygame
import random
from typing import List, Optional, Tuple, Dict
from world.tile import Tile, TileType
from utils.constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from systems.sprite_manager import SpriteManager


class Map:
    """
    A tile-based map for world exploration.
    """
    
    def __init__(self, width: int, height: int, default_tile: str = TileType.GRASS):
        """
        Initialize the map.
        
        Args:
            width: Map width in tiles
            height: Map height in tiles
            default_tile: Default tile type
        """
        self.width = width
        self.height = height
        self.default_tile_type = default_tile
        
        # Create tile grid
        self.tiles: List[List[Tile]] = []

        # Load tile sprites
        sprite_manager = SpriteManager()
        self.tile_sprites = sprite_manager.create_tile_sprites(TILE_SIZE)

        self._create_tiles()
        self._apply_tile_sprites()

        # Map properties
        self.name = "Unnamed Map"
        self.spawn_point = (width // 2, height // 2)  # Default center spawn

        # Encounter settings
        self.allow_encounters = True
        self.encounter_groups = []  # List of enemy groups
    
    def _create_tiles(self):
        """Create the tile grid."""
        self.tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                tile = Tile(x, y, self.default_tile_type)
                row.append(tile)
            self.tiles.append(row)

    def _apply_tile_sprites(self):
        """Apply sprite textures to all tiles based on their type."""
        if not self.tile_sprites:
            print("Warning: No tile sprites loaded, using colored rectangles")
            return

        tiles_updated = 0
        for row in self.tiles:
            for tile in row:
                # Check if we have a sprite for this tile type
                if tile.tile_type in self.tile_sprites:
                    tile.sprite = self.tile_sprites[tile.tile_type]
                    tiles_updated += 1

        print(f"Applied sprites to {tiles_updated} tiles")
    
    def get_tile(self, tile_x: int, tile_y: int) -> Optional[Tile]:
        """
        Get tile at grid position.
        
        Args:
            tile_x: Tile X coordinate
            tile_y: Tile Y coordinate
        
        Returns:
            Tile or None if out of bounds
        """
        if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
            return self.tiles[tile_y][tile_x]
        return None
    
    def get_tile_at_world_pos(self, world_x: int, world_y: int) -> Optional[Tile]:
        """
        Get tile at world position.
        
        Args:
            world_x: World X coordinate (pixels)
            world_y: World Y coordinate (pixels)
        
        Returns:
            Tile or None if out of bounds
        """
        tile_x = int(world_x // TILE_SIZE)
        tile_y = int(world_y // TILE_SIZE)
        return self.get_tile(tile_x, tile_y)
    
    def set_tile(self, tile_x: int, tile_y: int, tile_type: str):
        """
        Set tile type at position.

        Args:
            tile_x: Tile X coordinate
            tile_y: Tile Y coordinate
            tile_type: New tile type
        """
        tile = self.get_tile(tile_x, tile_y)
        if tile:
            tile.tile_type = tile_type
            tile.color = tile._get_color()
            tile._setup_tile_properties()

            # Apply sprite if available
            if tile_type in self.tile_sprites:
                tile.sprite = self.tile_sprites[tile_type]
    
    def is_walkable(self, tile_x: int, tile_y: int) -> bool:
        """
        Check if a tile is walkable.
        
        Args:
            tile_x: Tile X coordinate
            tile_y: Tile Y coordinate
        
        Returns:
            True if walkable
        """
        tile = self.get_tile(tile_x, tile_y)
        return tile.walkable if tile else False
    
    def is_walkable_world(self, world_x: int, world_y: int) -> bool:
        """
        Check if a world position is walkable.
        
        Args:
            world_x: World X coordinate (pixels)
            world_y: World Y coordinate (pixels)
        
        Returns:
            True if walkable
        """
        tile = self.get_tile_at_world_pos(world_x, world_y)
        return tile.walkable if tile else False
    
    def check_encounter(self, tile_x: int, tile_y: int) -> bool:
        """
        Check if an encounter should occur.
        
        Args:
            tile_x: Tile X coordinate
            tile_y: Tile Y coordinate
        
        Returns:
            True if encounter triggered
        """
        if not self.allow_encounters:
            return False
        
        tile = self.get_tile(tile_x, tile_y)
        if not tile or not tile.encounter_zone:
            return False
        
        # Roll for encounter
        roll = random.random()
        return roll < tile.encounter_rate
    
    def get_spawn_position(self) -> Tuple[int, int]:
        """
        Get spawn position in world coordinates.
        
        Returns:
            (world_x, world_y) tuple
        """
        tile_x, tile_y = self.spawn_point
        return (tile_x * TILE_SIZE, tile_y * TILE_SIZE)
    
    def set_spawn_point(self, tile_x: int, tile_y: int):
        """
        Set player spawn point.
        
        Args:
            tile_x: Tile X coordinate
            tile_y: Tile Y coordinate
        """
        if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
            self.spawn_point = (tile_x, tile_y)
    
    def fill_rect(self, start_x: int, start_y: int, width: int, height: int, tile_type: str):
        """
        Fill a rectangle with a tile type.
        
        Args:
            start_x: Starting X tile coordinate
            start_y: Starting Y tile coordinate
            width: Width in tiles
            height: Height in tiles
            tile_type: Tile type to fill with
        """
        for y in range(start_y, start_y + height):
            for x in range(start_x, start_x + width):
                self.set_tile(x, y, tile_type)
    
    def create_border(self, tile_type: str = TileType.WALL):
        """
        Create a border around the map.
        
        Args:
            tile_type: Tile type for border
        """
        # Top and bottom
        for x in range(self.width):
            self.set_tile(x, 0, tile_type)
            self.set_tile(x, self.height - 1, tile_type)
        
        # Left and right
        for y in range(self.height):
            self.set_tile(0, y, tile_type)
            self.set_tile(self.width - 1, y, tile_type)
    
    def create_room(self, start_x: int, start_y: int, width: int, height: int, 
                   floor_type: str = TileType.WOOD, wall_type: str = TileType.WALL):
        """
        Create a room with walls.
        
        Args:
            start_x: Room start X
            start_y: Room start Y
            width: Room width
            height: Room height
            floor_type: Floor tile type
            wall_type: Wall tile type
        """
        # Fill floor
        self.fill_rect(start_x, start_y, width, height, floor_type)
        
        # Create walls
        for x in range(start_x, start_x + width):
            self.set_tile(x, start_y, wall_type)
            self.set_tile(x, start_y + height - 1, wall_type)
        
        for y in range(start_y, start_y + height):
            self.set_tile(start_x, y, wall_type)
            self.set_tile(start_x + width - 1, y, wall_type)
    
    def add_door(self, tile_x: int, tile_y: int):
        """
        Add a door at position.
        
        Args:
            tile_x: X coordinate
            tile_y: Y coordinate
        """
        self.set_tile(tile_x, tile_y, TileType.DOOR)
    
    def render(self, surface: pygame.Surface, camera_x: int, camera_y: int):
        """
        Render visible tiles.
        
        Args:
            surface: Surface to draw on
            camera_x: Camera X position
            camera_y: Camera Y position
        """
        # Calculate visible tile range
        start_x = max(0, int(camera_x // TILE_SIZE) - 1)
        start_y = max(0, int(camera_y // TILE_SIZE) - 1)
        end_x = min(self.width, int((camera_x + SCREEN_WIDTH) // TILE_SIZE) + 2)
        end_y = min(self.height, int((camera_y + SCREEN_HEIGHT) // TILE_SIZE) + 2)
        
        # Render visible tiles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.tiles[y][x]
                tile.render(surface, camera_x, camera_y)
    
    def get_world_size(self) -> Tuple[int, int]:
        """
        Get map size in world coordinates (pixels).
        
        Returns:
            (width, height) in pixels
        """
        return (self.width * TILE_SIZE, self.height * TILE_SIZE)
    
    @staticmethod
    def create_test_map() -> 'Map':
        """
        Create a test map for development.
        
        Returns:
            Test Map instance
        """
        # Create 30x30 map
        test_map = Map(30, 30, TileType.GRASS)
        test_map.name = "Test Island"
        
        # Create border
        test_map.create_border(TileType.WATER)
        
        # Create a town area in center
        test_map.create_room(10, 10, 10, 8, TileType.WOOD, TileType.WALL)
        test_map.add_door(14, 10)  # North door
        test_map.add_door(14, 17)  # South door
        
        # Add some stone paths
        for x in range(14, 16):
            for y in range(5, 10):
                test_map.set_tile(x, y, TileType.STONE)
            for y in range(18, 25):
                test_map.set_tile(x, y, TileType.STONE)
        
        # Add water feature
        test_map.fill_rect(3, 3, 4, 4, TileType.WATER)
        
        # Add sand beach
        for x in range(1, 29):
            test_map.set_tile(x, 1, TileType.SAND)
            test_map.set_tile(x, 28, TileType.SAND)
        for y in range(1, 29):
            test_map.set_tile(1, y, TileType.SAND)
            test_map.set_tile(28, y, TileType.SAND)
        
        # Set spawn point
        test_map.set_spawn_point(15, 20)
        
        return test_map
    
    def __repr__(self) -> str:
        """String representation."""
        return f"Map('{self.name}', {self.width}x{self.height})"
