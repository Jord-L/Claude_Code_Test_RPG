"""
Item Icon Utilities
Shared utilities for loading and caching item icons.
"""

import os
import pygame
from typing import Dict, Optional


# Icon cache to avoid reloading images
_icon_cache: Dict[str, pygame.Surface] = {}


def load_item_icon(icon_path: str, size: tuple = (44, 44)) -> Optional[pygame.Surface]:
    """
    Load an item icon from file with caching.

    Args:
        icon_path: Path to icon file (relative to assets/)
        size: Target size for icon

    Returns:
        Loaded and scaled icon surface, or None if not found
    """
    # Check cache first
    cache_key = f"{icon_path}_{size[0]}x{size[1]}"
    if cache_key in _icon_cache:
        return _icon_cache[cache_key]

    # Determine full path - handle both new (Raven Fantasy Icons) and old (items/) formats
    if icon_path.startswith("Free - Raven Fantasy Icons"):
        # New format: path already includes full directory structure
        full_path = os.path.join("assets", icon_path)
    else:
        # Old format: prepend assets/icons/
        full_path = os.path.join("assets", "icons", icon_path)

    if os.path.exists(full_path):
        try:
            icon = pygame.image.load(full_path)
            icon = pygame.transform.scale(icon, size)
            _icon_cache[cache_key] = icon
            return icon
        except pygame.error as e:
            print(f"Failed to load icon {full_path}: {e}")
            return None

    return None


def clear_icon_cache():
    """Clear the icon cache to free memory."""
    global _icon_cache
    _icon_cache.clear()
