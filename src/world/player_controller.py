"""
Player Controller
Handles player movement and input in the overworld.
"""

import pygame
from typing import Optional, Tuple
from entities.player import Player
from world.map import Map
from utils.constants import TILE_SIZE, PLAYER_SPEED


class Direction:
    """Direction constants."""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class PlayerController:
    """
    Controls player movement in the overworld.
    """
    
    def __init__(self, player: Player, game_map: Map):
        """
        Initialize player controller.
        
        Args:
            player: Player instance
            game_map: Current map
        """
        self.player = player
        self.map = game_map
        
        # Position (world coordinates, pixels)
        spawn_x, spawn_y = game_map.get_spawn_position()
        self.x = spawn_x
        self.y = spawn_y
        
        # Movement
        self.speed = PLAYER_SPEED
        self.moving = False
        self.facing = Direction.DOWN
        
        # Step counter for encounters
        self.steps_since_last_encounter = 0
        self.step_threshold = TILE_SIZE  # One tile = one step
        self.step_accumulator = 0
        
        # Visual
        self.sprite_size = TILE_SIZE
        self.color = (255, 100, 100)  # Red for player
        
        # Input buffering
        self.input_buffer = {
            "up": False,
            "down": False,
            "left": False,
            "right": False
        }
    
    def handle_event(self, event: pygame.event.Event):
        """
        Handle input events.
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.input_buffer["up"] = True
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.input_buffer["down"] = True
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.input_buffer["left"] = True
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.input_buffer["right"] = True
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.input_buffer["up"] = False
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.input_buffer["down"] = False
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.input_buffer["left"] = False
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.input_buffer["right"] = False
    
    def update(self, dt: float) -> Optional[str]:
        """
        Update player movement.
        
        Args:
            dt: Delta time in seconds
        
        Returns:
            Event type if triggered ("encounter", etc.) or None
        """
        # Store old position
        old_x = self.x
        old_y = self.y
        
        # Calculate movement
        dx = 0
        dy = 0
        
        if self.input_buffer["up"]:
            dy -= self.speed
            self.facing = Direction.UP
            self.moving = True
        elif self.input_buffer["down"]:
            dy += self.speed
            self.facing = Direction.DOWN
            self.moving = True
        
        if self.input_buffer["left"]:
            dx -= self.speed
            self.facing = Direction.LEFT
            self.moving = True
        elif self.input_buffer["right"]:
            dx += self.speed
            self.facing = Direction.RIGHT
            self.moving = True
        
        # Check if no input
        if dx == 0 and dy == 0:
            self.moving = False
            return None
        
        # Try to move
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check collision
        if self._can_move_to(new_x, new_y):
            self.x = new_x
            self.y = new_y
            
            # Track steps for encounters
            distance_moved = abs(new_x - old_x) + abs(new_y - old_y)
            self.step_accumulator += distance_moved
            
            if self.step_accumulator >= self.step_threshold:
                self.step_accumulator = 0
                self.steps_since_last_encounter += 1
                
                # Check for random encounter
                if self._check_encounter():
                    return "encounter"
        
        return None
    
    def _can_move_to(self, world_x: float, world_y: float) -> bool:
        """
        Check if player can move to position.
        
        Args:
            world_x: Target X position
            world_y: Target Y position
        
        Returns:
            True if valid move
        """
        # Check all four corners of the player sprite
        corners = [
            (world_x, world_y),  # Top-left
            (world_x + self.sprite_size - 1, world_y),  # Top-right
            (world_x, world_y + self.sprite_size - 1),  # Bottom-left
            (world_x + self.sprite_size - 1, world_y + self.sprite_size - 1)  # Bottom-right
        ]
        
        for corner_x, corner_y in corners:
            if not self.map.is_walkable_world(int(corner_x), int(corner_y)):
                return False
        
        return True
    
    def _check_encounter(self) -> bool:
        """
        Check if a random encounter should occur.
        
        Returns:
            True if encounter triggered
        """
        # Get current tile
        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)
        
        # Check encounter
        if self.map.check_encounter(tile_x, tile_y):
            self.steps_since_last_encounter = 0
            return True
        
        return False
    
    def get_position(self) -> Tuple[int, int]:
        """
        Get player position.
        
        Returns:
            (x, y) tuple
        """
        return (int(self.x), int(self.y))
    
    def get_tile_position(self) -> Tuple[int, int]:
        """
        Get player tile position.
        
        Returns:
            (tile_x, tile_y) tuple
        """
        return (int(self.x // TILE_SIZE), int(self.y // TILE_SIZE))
    
    def get_center_position(self) -> Tuple[int, int]:
        """
        Get player center position.
        
        Returns:
            (center_x, center_y) tuple
        """
        return (
            int(self.x + self.sprite_size // 2),
            int(self.y + self.sprite_size // 2)
        )
    
    def set_position(self, world_x: int, world_y: int):
        """
        Set player position.
        
        Args:
            world_x: World X coordinate
            world_y: World Y coordinate
        """
        self.x = world_x
        self.y = world_y
    
    def set_tile_position(self, tile_x: int, tile_y: int):
        """
        Set player position by tile coordinates.
        
        Args:
            tile_x: Tile X coordinate
            tile_y: Tile Y coordinate
        """
        self.x = tile_x * TILE_SIZE
        self.y = tile_y * TILE_SIZE
    
    def teleport_to_spawn(self):
        """Teleport player to map spawn point."""
        spawn_x, spawn_y = self.map.get_spawn_position()
        self.set_position(spawn_x, spawn_y)
    
    def render(self, surface: pygame.Surface, camera_x: int, camera_y: int):
        """
        Render player sprite.
        
        Args:
            surface: Surface to draw on
            camera_x: Camera X offset
            camera_y: Camera Y offset
        """
        # Calculate screen position
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        # Draw player (simple colored square for now)
        rect = pygame.Rect(screen_x, screen_y, self.sprite_size, self.sprite_size)
        pygame.draw.rect(surface, self.color, rect)
        
        # Draw border
        pygame.draw.rect(surface, (0, 0, 0), rect, 2)
        
        # Draw facing direction indicator (small triangle)
        self._draw_direction_indicator(surface, screen_x, screen_y)
    
    def _draw_direction_indicator(self, surface: pygame.Surface, screen_x: int, screen_y: int):
        """Draw a small indicator showing facing direction."""
        center_x = screen_x + self.sprite_size // 2
        center_y = screen_y + self.sprite_size // 2
        indicator_size = 6
        
        if self.facing == Direction.UP:
            points = [
                (center_x, screen_y + 5),
                (center_x - indicator_size, screen_y + 5 + indicator_size),
                (center_x + indicator_size, screen_y + 5 + indicator_size)
            ]
        elif self.facing == Direction.DOWN:
            points = [
                (center_x, screen_y + self.sprite_size - 5),
                (center_x - indicator_size, screen_y + self.sprite_size - 5 - indicator_size),
                (center_x + indicator_size, screen_y + self.sprite_size - 5 - indicator_size)
            ]
        elif self.facing == Direction.LEFT:
            points = [
                (screen_x + 5, center_y),
                (screen_x + 5 + indicator_size, center_y - indicator_size),
                (screen_x + 5 + indicator_size, center_y + indicator_size)
            ]
        else:  # RIGHT
            points = [
                (screen_x + self.sprite_size - 5, center_y),
                (screen_x + self.sprite_size - 5 - indicator_size, center_y - indicator_size),
                (screen_x + self.sprite_size - 5 - indicator_size, center_y + indicator_size)
            ]
        
        pygame.draw.polygon(surface, (255, 255, 255), points)
    
    def get_rect(self) -> pygame.Rect:
        """Get player collision rectangle."""
        return pygame.Rect(int(self.x), int(self.y), self.sprite_size, self.sprite_size)
    
    def __repr__(self) -> str:
        """String representation."""
        return f"PlayerController({self.player.name}, pos=({int(self.x)}, {int(self.y)}))"
