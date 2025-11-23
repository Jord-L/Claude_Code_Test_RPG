"""
Sprite and Animation Management System
Handles loading, caching, and animating sprites for the game.
"""

import pygame
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class SpriteAnimation:
    """
    Represents a single animation (e.g., idle, run, jump).
    Manages frames and timing for smooth animation playback.
    """

    def __init__(self, name: str, frames: List[pygame.Surface], frame_duration: float = 0.1):
        """
        Initialize sprite animation.

        Args:
            name: Animation name (idle, run, etc.)
            frames: List of pygame surfaces for each frame
            frame_duration: Time in seconds per frame
        """
        self.name = name
        self.frames = frames
        self.frame_duration = frame_duration
        self.frame_count = len(frames)

        # Animation state
        self.current_frame = 0
        self.elapsed_time = 0.0
        self.is_looping = True
        self.is_playing = True
        self.finished = False

    def update(self, dt: float):
        """
        Update animation frame based on delta time.

        Args:
            dt: Delta time in seconds
        """
        if not self.is_playing or self.finished:
            return

        self.elapsed_time += dt

        # Check if we should advance to next frame
        if self.elapsed_time >= self.frame_duration:
            self.elapsed_time = 0.0
            self.current_frame += 1

            # Handle looping
            if self.current_frame >= self.frame_count:
                if self.is_looping:
                    self.current_frame = 0
                else:
                    self.current_frame = self.frame_count - 1
                    self.finished = True

    def get_current_frame(self) -> pygame.Surface:
        """Get the current frame surface."""
        return self.frames[self.current_frame]

    def reset(self):
        """Reset animation to first frame."""
        self.current_frame = 0
        self.elapsed_time = 0.0
        self.finished = False

    def play(self):
        """Start/resume playing animation."""
        self.is_playing = True

    def pause(self):
        """Pause animation."""
        self.is_playing = False

    def set_looping(self, loop: bool):
        """Set whether animation should loop."""
        self.is_looping = loop


class AnimationController:
    """
    Controls multiple animations for a single entity.
    Handles animation transitions and state management.
    """

    def __init__(self):
        """Initialize animation controller."""
        self.animations: Dict[str, SpriteAnimation] = {}
        self.current_animation: Optional[SpriteAnimation] = None
        self.current_animation_name: str = "idle"
        self.flip_horizontal = False
        self.flip_vertical = False

    def add_animation(self, animation: SpriteAnimation):
        """
        Add an animation to the controller.

        Args:
            animation: SpriteAnimation to add
        """
        self.animations[animation.name] = animation

        # Set as current if first animation
        if self.current_animation is None:
            self.current_animation = animation
            self.current_animation_name = animation.name

    def play_animation(self, name: str, reset: bool = True):
        """
        Play a specific animation.

        Args:
            name: Name of animation to play
            reset: Whether to reset animation to first frame
        """
        if name not in self.animations:
            print(f"Warning: Animation '{name}' not found!")
            return

        # Only change if different animation
        if self.current_animation_name != name:
            self.current_animation = self.animations[name]
            self.current_animation_name = name

            if reset:
                self.current_animation.reset()

            self.current_animation.play()

    def update(self, dt: float):
        """
        Update current animation.

        Args:
            dt: Delta time in seconds
        """
        if self.current_animation:
            self.current_animation.update(dt)

    def get_current_frame(self) -> Optional[pygame.Surface]:
        """Get current animation frame."""
        if self.current_animation is None:
            return None

        frame = self.current_animation.get_current_frame()

        # Apply flipping if needed
        if self.flip_horizontal or self.flip_vertical:
            frame = pygame.transform.flip(frame, self.flip_horizontal, self.flip_vertical)

        return frame

    def set_flip(self, horizontal: bool = False, vertical: bool = False):
        """
        Set sprite flipping.

        Args:
            horizontal: Flip horizontally
            vertical: Flip vertically
        """
        self.flip_horizontal = horizontal
        self.flip_vertical = vertical


class SpriteManager:
    """
    Singleton manager for loading and caching sprites.
    Handles sprite loading from disk with caching for performance.
    """

    _instance = None

    def __new__(cls):
        """Ensure only one instance exists (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(SpriteManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize sprite manager."""
        if self._initialized:
            return

        self._initialized = True
        self.sprite_cache: Dict[str, pygame.Surface] = {}
        self.animation_cache: Dict[str, List[pygame.Surface]] = {}

        # Base paths
        self.assets_path = Path(__file__).parent.parent.parent / "assets"
        self.sprites_path = self.assets_path / "sprites"

        print(f"SpriteManager initialized. Assets path: {self.assets_path}")

    def load_sprite(self, path: str, scale: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
        """
        Load a single sprite image with caching.

        Args:
            path: Relative path from assets directory
            scale: Optional (width, height) to scale sprite

        Returns:
            Loaded sprite surface or None if failed
        """
        # Check cache first
        cache_key = f"{path}_{scale}"
        if cache_key in self.sprite_cache:
            return self.sprite_cache[cache_key]

        # Build full path
        full_path = self.assets_path / path

        if not full_path.exists():
            print(f"Warning: Sprite not found at {full_path}")
            return None

        try:
            # Load image
            sprite = pygame.image.load(str(full_path)).convert_alpha()

            # Scale if requested
            if scale:
                sprite = pygame.transform.scale(sprite, scale)

            # Cache and return
            self.sprite_cache[cache_key] = sprite
            return sprite

        except pygame.error as e:
            print(f"Error loading sprite {path}: {e}")
            return None

    def load_animation_frames(self, directory: str, scale: Optional[Tuple[int, int]] = None,
                            frame_pattern: str = "*.png") -> List[pygame.Surface]:
        """
        Load all frames from a directory for animation.

        Args:
            directory: Directory path relative to assets
            scale: Optional (width, height) to scale frames
            frame_pattern: File pattern to match (default: *.png)

        Returns:
            List of loaded frame surfaces
        """
        # Check cache
        cache_key = f"{directory}_{scale}_{frame_pattern}"
        if cache_key in self.animation_cache:
            return self.animation_cache[cache_key]

        # Build full path
        full_path = self.assets_path / directory

        if not full_path.exists():
            print(f"Warning: Animation directory not found at {full_path}")
            return []

        try:
            # Get all matching files and sort them
            frames = []
            png_files = sorted(full_path.glob(frame_pattern),
                             key=lambda x: self._extract_number(x.name))

            for file_path in png_files:
                sprite = pygame.image.load(str(file_path)).convert_alpha()

                # Scale if requested
                if scale:
                    sprite = pygame.transform.scale(sprite, scale)

                frames.append(sprite)

            # Cache and return
            self.animation_cache[cache_key] = frames
            print(f"Loaded {len(frames)} frames from {directory}")
            return frames

        except Exception as e:
            print(f"Error loading animation frames from {directory}: {e}")
            return []

    def _extract_number(self, filename: str) -> int:
        """
        Extract number from filename for sorting.

        Args:
            filename: Filename to extract number from

        Returns:
            Extracted number or 0 if not found
        """
        import re
        numbers = re.findall(r'\d+', filename)
        return int(numbers[0]) if numbers else 0

    def create_player_animation_controller(self, sprite_size: int = 64) -> AnimationController:
        """
        Create animation controller for player character.
        Loads all player animations from assets.

        Args:
            sprite_size: Size to scale sprites to (default: 64x64)

        Returns:
            Configured AnimationController
        """
        controller = AnimationController()
        scale = (sprite_size, sprite_size)

        # Animation definitions: (folder_name, animation_name, frame_duration, loop)
        animations = [
            ("sprites/1-Player-Bomb Guy/1-Idle", "idle", 0.05, True),
            ("sprites/1-Player-Bomb Guy/2-Run", "run", 0.08, True),
            ("sprites/1-Player-Bomb Guy/3-Jump Anticipation", "jump_start", 0.1, False),
            ("sprites/1-Player-Bomb Guy/4-Jump", "jump", 0.1, False),
            ("sprites/1-Player-Bomb Guy/5-Fall", "fall", 0.08, True),
            ("sprites/1-Player-Bomb Guy/6-Ground", "land", 0.1, False),
            ("sprites/1-Player-Bomb Guy/7-Hit", "hit", 0.08, False),
            ("sprites/1-Player-Bomb Guy/8-Dead Hit", "dead_hit", 0.1, False),
            ("sprites/1-Player-Bomb Guy/9-Dead Ground", "dead", 0.1, False),
        ]

        for folder, name, duration, loop in animations:
            frames = self.load_animation_frames(folder, scale=scale)
            if frames:
                anim = SpriteAnimation(name, frames, duration)
                anim.set_looping(loop)
                controller.add_animation(anim)

        return controller

    def create_whale_enemy_animation_controller(self, sprite_size: int = 64) -> AnimationController:
        """
        Create animation controller for whale enemy.

        Args:
            sprite_size: Size to scale sprites to (default: 64x64)

        Returns:
            Configured AnimationController
        """
        controller = AnimationController()
        scale = (sprite_size, sprite_size)

        # Whale enemy animations
        animations = [
            ("sprites/6-Enemy-Whale/1-Idle", "idle", 0.05, True),
            ("sprites/6-Enemy-Whale/2-Run", "run", 0.08, True),
            ("sprites/6-Enemy-Whale/7-Hit", "hit", 0.08, False),
            ("sprites/6-Enemy-Whale/8-Dead Hit", "dead_hit", 0.1, False),
            ("sprites/6-Enemy-Whale/9-Dead Ground", "dead", 0.1, False),
        ]

        for folder, name, duration, loop in animations:
            frames = self.load_animation_frames(folder, scale=scale)
            if frames:
                anim = SpriteAnimation(name, frames, duration)
                anim.set_looping(loop)
                controller.add_animation(anim)

        return controller

    def load_tileset(self, tileset_path: str, tile_width: int, tile_height: int) -> Dict[int, pygame.Surface]:
        """
        Load a tileset and split it into individual tile sprites.

        Args:
            tileset_path: Path to tileset image relative to assets
            tile_width: Width of each tile in pixels
            tile_height: Height of each tile in pixels

        Returns:
            Dictionary mapping tile index to surface
        """
        # Build full path
        full_path = self.assets_path / tileset_path

        if not full_path.exists():
            print(f"Warning: Tileset not found at {full_path}")
            return {}

        try:
            # Load tileset image
            tileset_image = pygame.image.load(str(full_path)).convert_alpha()
            tileset_width, tileset_height = tileset_image.get_size()

            # Calculate grid dimensions
            cols = tileset_width // tile_width
            rows = tileset_height // tile_height

            tiles = {}
            tile_index = 0

            # Extract each tile
            for row in range(rows):
                for col in range(cols):
                    # Calculate position in tileset
                    x = col * tile_width
                    y = row * tile_height

                    # Extract tile
                    tile_surface = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
                    tile_surface.blit(tileset_image, (0, 0), (x, y, tile_width, tile_height))

                    tiles[tile_index] = tile_surface
                    tile_index += 1

            print(f"Loaded {len(tiles)} tiles from {tileset_path} ({cols}x{rows} grid)")
            return tiles

        except Exception as e:
            print(f"Error loading tileset {tileset_path}: {e}")
            return {}

    def create_tile_sprites(self, tile_size: int = 64) -> Dict[str, pygame.Surface]:
        """
        Create sprite dictionary for different tile types using the tileset.

        Args:
            tile_size: Size of tiles (default: 64x64)

        Returns:
            Dictionary mapping tile type to sprite surface
        """
        # Load the main tileset
        tiles = self.load_tileset("sprites/8-Tile-Sets/Tile-Sets (64-64).png", tile_size, tile_size)

        if not tiles:
            return {}

        # Map tile types to tileset indices
        # Based on the wooden deck tileset we have
        tile_mapping = {
            "wood": 0,      # Basic wooden plank
            "stone": 6,     # Different wood texture (lighter)
            "grass": 12,    # Different texture
            "sand": 18,     # Different texture
            "wall": 1,      # Wall-like texture
            "door": 7,      # Different pattern
            "water": 24,    # Different color/pattern
        }

        # Create sprite dict with tile type names
        tile_sprites = {}
        for tile_type, index in tile_mapping.items():
            if index in tiles:
                tile_sprites[tile_type] = tiles[index]

        print(f"Created {len(tile_sprites)} tile type sprites")
        return tile_sprites

    def clear_cache(self):
        """Clear all cached sprites and animations."""
        self.sprite_cache.clear()
        self.animation_cache.clear()
        print("Sprite cache cleared")
