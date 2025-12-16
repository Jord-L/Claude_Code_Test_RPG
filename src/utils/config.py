"""
Environment Configuration
Load and manage environment variables and configuration.
"""

import os
from typing import Any, Optional
from utils.logger import get_logger


class Config:
    """
    Configuration manager for environment variables.

    Loads from .env file and provides typed access to settings.
    """

    def __init__(self):
        """Initialize configuration."""
        self.logger = get_logger()
        self._config = {}
        self._load_env_file()
        self._set_defaults()
        self.logger.info(f"Configuration loaded: {self.game_env} mode")

    def _load_env_file(self):
        """Load .env file if it exists."""
        env_file = '.env'

        if os.path.exists(env_file):
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        # Skip comments and empty lines
                        if not line or line.startswith('#'):
                            continue

                        # Parse KEY=VALUE
                        if '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            # Also set as environment variable
                            os.environ[key] = value
                            self._config[key] = value

                self.logger.info(f"Loaded .env file: {len(self._config)} settings")

            except Exception as e:
                self.logger.warning(f"Could not load .env file: {e}")
        else:
            self.logger.info("No .env file found, using defaults")

    def _set_defaults(self):
        """Set default values for required settings."""
        defaults = {
            'GAME_ENV': 'development',
            'DEBUG_MODE': 'true',
            'SHOW_FPS': 'true',
            'LOG_LEVEL': 'DEBUG',
            'ENABLE_DATA_CACHING': 'true',
            'ENABLE_LAZY_LOADING': 'true',
            'MAX_CACHE_SIZE_MB': '50',
            'DEFAULT_RESOLUTION': '1280x720',
            'DEFAULT_FULLSCREEN': 'false',
            'TARGET_FPS': '60',
            'DATABASE_PATH': 'Databases',
            'SAVES_PATH': 'saves',
            'ASSETS_PATH': 'assets',
            'SKIP_INTRO': 'false',
            'FAST_BATTLE_ANIMATIONS': 'false',
            'AUTO_SAVE_ENABLED': 'true',
            'ENABLE_PERFORMANCE_MONITORING': 'true',
            'SHOW_LOAD_TIMES': 'false'
        }

        for key, default_value in defaults.items():
            if key not in self._config:
                self._config[key] = os.environ.get(key, default_value)

    def get(self, key: str, default: Any = None) -> Optional[str]:
        """
        Get a configuration value as string.

        Args:
            key: Configuration key
            default: Default value if not found

        Returns:
            Configuration value or default
        """
        return self._config.get(key, os.environ.get(key, default))

    def get_bool(self, key: str, default: bool = False) -> bool:
        """
        Get a configuration value as boolean.

        Args:
            key: Configuration key
            default: Default value if not found

        Returns:
            Boolean value
        """
        value = self.get(key)
        if value is None:
            return default

        return value.lower() in ('true', 'yes', '1', 'on')

    def get_int(self, key: str, default: int = 0) -> int:
        """
        Get a configuration value as integer.

        Args:
            key: Configuration key
            default: Default value if not found

        Returns:
            Integer value
        """
        value = self.get(key)
        if value is None:
            return default

        try:
            return int(value)
        except (ValueError, TypeError):
            self.logger.warning(f"Invalid integer value for {key}: {value}, using default {default}")
            return default

    def get_float(self, key: str, default: float = 0.0) -> float:
        """
        Get a configuration value as float.

        Args:
            key: Configuration key
            default: Default value if not found

        Returns:
            Float value
        """
        value = self.get(key)
        if value is None:
            return default

        try:
            return float(value)
        except (ValueError, TypeError):
            self.logger.warning(f"Invalid float value for {key}: {value}, using default {default}")
            return default

    # Convenience properties for common settings

    @property
    def game_env(self) -> str:
        """Get game environment (development/production/testing)."""
        return self.get('GAME_ENV', 'development')

    @property
    def is_development(self) -> bool:
        """Check if in development mode."""
        return self.game_env == 'development'

    @property
    def is_production(self) -> bool:
        """Check if in production mode."""
        return self.game_env == 'production'

    @property
    def is_testing(self) -> bool:
        """Check if in testing mode."""
        return self.game_env == 'testing'

    @property
    def debug_mode(self) -> bool:
        """Get debug mode setting."""
        return self.get_bool('DEBUG_MODE', True)

    @property
    def show_fps(self) -> bool:
        """Get show FPS setting."""
        return self.get_bool('SHOW_FPS', True)

    @property
    def log_level(self) -> str:
        """Get log level."""
        return self.get('LOG_LEVEL', 'DEBUG')

    @property
    def enable_data_caching(self) -> bool:
        """Get data caching setting."""
        return self.get_bool('ENABLE_DATA_CACHING', True)

    @property
    def enable_lazy_loading(self) -> bool:
        """Get lazy loading setting."""
        return self.get_bool('ENABLE_LAZY_LOADING', True)

    @property
    def max_cache_size_mb(self) -> int:
        """Get max cache size in MB."""
        return self.get_int('MAX_CACHE_SIZE_MB', 50)

    @property
    def default_resolution(self) -> str:
        """Get default resolution."""
        return self.get('DEFAULT_RESOLUTION', '1280x720')

    @property
    def default_fullscreen(self) -> bool:
        """Get default fullscreen setting."""
        return self.get_bool('DEFAULT_FULLSCREEN', False)

    @property
    def target_fps(self) -> int:
        """Get target FPS."""
        return self.get_int('TARGET_FPS', 60)

    @property
    def database_path(self) -> str:
        """Get database path."""
        return self.get('DATABASE_PATH', 'Databases')

    @property
    def saves_path(self) -> str:
        """Get saves path."""
        return self.get('SAVES_PATH', 'saves')

    @property
    def assets_path(self) -> str:
        """Get assets path."""
        return self.get('ASSETS_PATH', 'assets')

    @property
    def skip_intro(self) -> bool:
        """Get skip intro setting."""
        return self.get_bool('SKIP_INTRO', False)

    @property
    def fast_battle_animations(self) -> bool:
        """Get fast battle animations setting."""
        return self.get_bool('FAST_BATTLE_ANIMATIONS', False)

    @property
    def auto_save_enabled(self) -> bool:
        """Get auto-save enabled setting."""
        return self.get_bool('AUTO_SAVE_ENABLED', True)

    @property
    def enable_performance_monitoring(self) -> bool:
        """Get performance monitoring setting."""
        return self.get_bool('ENABLE_PERFORMANCE_MONITORING', True)

    @property
    def show_load_times(self) -> bool:
        """Get show load times setting."""
        return self.get_bool('SHOW_LOAD_TIMES', False)

    def print_config(self):
        """Print current configuration."""
        print("\n" + "="*60)
        print("GAME CONFIGURATION")
        print("="*60)
        print(f"Environment: {self.game_env}")
        print(f"Debug mode: {self.debug_mode}")
        print(f"Show FPS: {self.show_fps}")
        print(f"Log level: {self.log_level}")
        print(f"Data caching: {self.enable_data_caching}")
        print(f"Lazy loading: {self.enable_lazy_loading}")
        print(f"Max cache size: {self.max_cache_size_mb} MB")
        print(f"Target FPS: {self.target_fps}")
        print(f"Database path: {self.database_path}")
        print(f"Saves path: {self.saves_path}")
        print(f"Performance monitoring: {self.enable_performance_monitoring}")
        print("="*60 + "\n")


# Global configuration instance
_config = None


def get_config() -> Config:
    """
    Get the global configuration instance.

    Returns:
        Config instance
    """
    global _config
    if _config is None:
        _config = Config()
    return _config
