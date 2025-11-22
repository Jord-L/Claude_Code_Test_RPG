"""
Resource Loader
Handles loading and caching of game assets (images, sounds, fonts, etc.)
"""

import pygame
import os
from utils.helpers import get_file_path


class ResourceLoader:
    """Singleton class for loading and caching game resources."""
    
    _instance = None
    
    def __new__(cls):
        """Ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the resource loader."""
        if self._initialized:
            return
        
        # Cache dictionaries
        self.images = {}
        self.sounds = {}
        self.music = {}
        self.fonts = {}
        
        # Asset paths
        self.assets_path = get_file_path("assets")
        self.sprites_path = os.path.join(self.assets_path, "sprites")
        self.audio_path = os.path.join(self.assets_path, "audio")
        self.fonts_path = os.path.join(self.assets_path, "fonts")
        
        self._initialized = True
        print("ResourceLoader initialized")
    
    def load_image(self, filename, colorkey=None, scale=None):
        """Load an image from the sprites directory.
        
        Args:
            filename: Name of the image file
            colorkey: Color to set as transparent (RGB tuple or -1 for top-left pixel)
            scale: Tuple (width, height) to scale the image, or None
        
        Returns:
            pygame.Surface or None if failed
        """
        # Check cache first
        cache_key = f"{filename}_{colorkey}_{scale}"
        if cache_key in self.images:
            return self.images[cache_key]
        
        # Try to load the image
        filepath = os.path.join(self.sprites_path, filename)
        
        try:
            image = pygame.image.load(filepath)
            
            # Set colorkey if specified
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey)
            
            # Convert for better performance
            if colorkey:
                image = image.convert()
            else:
                image = image.convert_alpha()
            
            # Scale if specified
            if scale is not None:
                image = pygame.transform.scale(image, scale)
            
            # Cache and return
            self.images[cache_key] = image
            return image
            
        except pygame.error as e:
            print(f"Failed to load image '{filename}': {e}")
            # Return a placeholder surface
            placeholder = pygame.Surface((32, 32))
            placeholder.fill((255, 0, 255))  # Magenta placeholder
            self.images[cache_key] = placeholder
            return placeholder
    
    def load_sound(self, filename):
        """Load a sound effect.
        
        Args:
            filename: Name of the sound file
        
        Returns:
            pygame.mixer.Sound or None if failed
        """
        # Check cache
        if filename in self.sounds:
            return self.sounds[filename]
        
        # Try to load
        filepath = os.path.join(self.audio_path, "sfx", filename)
        
        try:
            sound = pygame.mixer.Sound(filepath)
            self.sounds[filename] = sound
            return sound
        except pygame.error as e:
            print(f"Failed to load sound '{filename}': {e}")
            return None
    
    def load_music(self, filename):
        """Load background music.
        
        Args:
            filename: Name of the music file
        
        Returns:
            Path to music file or None if failed
        """
        filepath = os.path.join(self.audio_path, "music", filename)
        
        if os.path.exists(filepath):
            self.music[filename] = filepath
            return filepath
        else:
            print(f"Music file not found: '{filename}'")
            return None
    
    def play_music(self, filename, loops=-1, volume=0.7):
        """Play background music.
        
        Args:
            filename: Name of the music file
            loops: Number of times to loop (-1 for infinite)
            volume: Volume level (0.0 to 1.0)
        """
        music_path = self.load_music(filename)
        if music_path:
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loops)
            except pygame.error as e:
                print(f"Failed to play music '{filename}': {e}")
    
    def stop_music(self):
        """Stop currently playing music."""
        pygame.mixer.music.stop()
    
    def load_font(self, filename=None, size=24):
        """Load a font.
        
        Args:
            filename: Name of font file, or None for default font
            size: Font size
        
        Returns:
            pygame.font.Font
        """
        cache_key = f"{filename}_{size}"
        
        # Check cache
        if cache_key in self.fonts:
            return self.fonts[cache_key]
        
        # Load font
        if filename is None:
            # Use default font
            font = pygame.font.Font(None, size)
        else:
            filepath = os.path.join(self.fonts_path, filename)
            try:
                font = pygame.font.Font(filepath, size)
            except:
                print(f"Failed to load font '{filename}', using default")
                font = pygame.font.Font(None, size)
        
        self.fonts[cache_key] = font
        return font
    
    def clear_cache(self):
        """Clear all cached resources."""
        self.images.clear()
        self.sounds.clear()
        self.music.clear()
        self.fonts.clear()
        print("Resource cache cleared")


# Global instance
resource_loader = ResourceLoader()
