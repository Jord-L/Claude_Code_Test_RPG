"""
Settings Manager
Handles loading, saving, and applying game settings.
"""

import json
import os
from typing import Dict, Any
from utils.logger import get_logger


class SettingsManager:
    """Manages game settings persistence and application."""

    DEFAULT_SETTINGS = {
        "music_volume": 0.7,
        "sfx_volume": 0.8,
        "text_speed": 0.5,
        "fullscreen": False,
        "aspect_ratio": "16:9",
        "battle_animations": True,
        "auto_save": True,
        "difficulty": "Normal"
    }

    def __init__(self, settings_file: str = "saves/settings.json"):
        """
        Initialize settings manager.

        Args:
            settings_file: Path to settings JSON file
        """
        self.logger = get_logger()
        self.settings_file = settings_file
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.logger.debug(f"Settings manager initialized with file: {settings_file}")

    def load(self) -> Dict[str, Any]:
        """
        Load settings from file.

        Returns:
            Dictionary of settings
        """
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)

                # Merge with defaults (in case new settings were added)
                self.settings = self.DEFAULT_SETTINGS.copy()
                self.settings.update(loaded_settings)

                self.logger.info(f"Settings loaded from {self.settings_file}")
                self.logger.debug(f"Loaded settings: {self.settings}")
            else:
                self.logger.info("No settings file found, using defaults")
                self.settings = self.DEFAULT_SETTINGS.copy()

        except Exception as e:
            self.logger.error(f"Error loading settings: {e}")
            self.logger.warning("Using default settings")
            self.settings = self.DEFAULT_SETTINGS.copy()

        return self.settings.copy()

    def save(self, settings: Dict[str, Any] = None) -> bool:
        """
        Save settings to file.

        Args:
            settings: Dictionary of settings to save (uses current if None)

        Returns:
            True if successful, False otherwise
        """
        if settings is not None:
            self.settings = settings

        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)

            # Write settings to file
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)

            self.logger.info(f"Settings saved to {self.settings_file}")
            self.logger.debug(f"Saved settings: {self.settings}")
            return True

        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")
            return False

    def get(self, key: str, default=None) -> Any:
        """
        Get a setting value.

        Args:
            key: Setting key
            default: Default value if key not found

        Returns:
            Setting value
        """
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a setting value.

        Args:
            key: Setting key
            value: Setting value
        """
        self.settings[key] = value
        self.logger.debug(f"Setting updated: {key} = {value}")

    def get_all(self) -> Dict[str, Any]:
        """
        Get all settings.

        Returns:
            Dictionary of all settings
        """
        return self.settings.copy()

    def reset_to_defaults(self) -> None:
        """Reset all settings to default values."""
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.logger.info("Settings reset to defaults")

    def apply_to_game(self, game) -> None:
        """
        Apply settings to the game.

        Args:
            game: Game instance
        """
        import pygame
        from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

        self.logger.info("Applying settings to game...")

        # Apply fullscreen
        fullscreen = self.settings.get("fullscreen", False)
        aspect_ratio = self.settings.get("aspect_ratio", "16:9")

        try:
            if fullscreen:
                # Get current display info
                display_info = pygame.display.Info()
                self.logger.debug(f"Display info: {display_info.current_w}x{display_info.current_h}")

                # Set fullscreen mode
                game.screen = pygame.display.set_mode(
                    (display_info.current_w, display_info.current_h),
                    pygame.FULLSCREEN
                )
                self.logger.info("Fullscreen mode enabled")
            else:
                # Calculate window size based on aspect ratio
                width, height = self._calculate_resolution(aspect_ratio)

                # Set windowed mode
                game.screen = pygame.display.set_mode((width, height))
                self.logger.info(f"Windowed mode set to {width}x{height} ({aspect_ratio})")

        except Exception as e:
            self.logger.error(f"Error applying display settings: {e}")
            # Fallback to default
            game.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Apply music volume (if music system exists)
        music_volume = self.settings.get("music_volume", 0.7)
        try:
            pygame.mixer.music.set_volume(music_volume)
            self.logger.debug(f"Music volume set to {int(music_volume * 100)}%")
        except Exception as e:
            self.logger.debug(f"Could not set music volume: {e}")

        # Note: SFX volume, text speed, battle animations, auto-save, and difficulty
        # are stored in settings but applied when needed by specific game systems

        self.logger.info("Settings applied successfully")

    def _calculate_resolution(self, aspect_ratio: str) -> tuple:
        """
        Calculate window resolution based on aspect ratio.

        Args:
            aspect_ratio: Aspect ratio string (e.g., "16:9")

        Returns:
            Tuple of (width, height)
        """
        from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

        # Aspect ratio to resolution mapping (based on 720p height)
        aspect_ratios = {
            "16:9": (1280, 720),
            "16:10": (1152, 720),
            "4:3": (960, 720),
            "21:9": (1680, 720)
        }

        return aspect_ratios.get(aspect_ratio, (SCREEN_WIDTH, SCREEN_HEIGHT))


# Global settings manager instance
_settings_manager = None


def get_settings_manager() -> SettingsManager:
    """
    Get the global settings manager instance.

    Returns:
        SettingsManager instance
    """
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = SettingsManager()
    return _settings_manager
