"""
Helper Utilities
Common utility functions used throughout the game.
"""

import pygame
import os


def clamp(value, min_value, max_value):
    """Clamp a value between min and max.
    
    Args:
        value: The value to clamp
        min_value: Minimum allowed value
        max_value: Maximum allowed value
    
    Returns:
        Clamped value
    """
    return max(min_value, min(value, max_value))


def lerp(start, end, t):
    """Linear interpolation between two values.
    
    Args:
        start: Starting value
        end: Ending value
        t: Interpolation factor (0.0 to 1.0)
    
    Returns:
        Interpolated value
    """
    return start + (end - start) * t


def distance(pos1, pos2):
    """Calculate distance between two positions.
    
    Args:
        pos1: First position (x, y)
        pos2: Second position (x, y)
    
    Returns:
        Distance as float
    """
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return (dx * dx + dy * dy) ** 0.5


def rect_collision(rect1, rect2):
    """Check if two rectangles collide.
    
    Args:
        rect1: First pygame.Rect
        rect2: Second pygame.Rect
    
    Returns:
        True if collision detected
    """
    return rect1.colliderect(rect2)


def point_in_rect(point, rect):
    """Check if a point is inside a rectangle.
    
    Args:
        point: Point (x, y)
        rect: pygame.Rect
    
    Returns:
        True if point is inside rect
    """
    return rect.collidepoint(point)


def draw_text(surface, text, font, color, position, centered=False):
    """Draw text on a surface.
    
    Args:
        surface: Surface to draw on
        text: Text string to draw
        font: pygame.Font object
        color: Text color (RGB tuple)
        position: Position (x, y)
        centered: If True, center text at position
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if centered:
        text_rect.center = position
    else:
        text_rect.topleft = position
    
    surface.blit(text_surface, text_rect)


def create_gradient_surface(width, height, start_color, end_color, vertical=True):
    """Create a surface with a gradient.
    
    Args:
        width: Surface width
        height: Surface height
        start_color: Starting color (RGB)
        end_color: Ending color (RGB)
        vertical: If True, gradient goes top to bottom, else left to right
    
    Returns:
        pygame.Surface with gradient
    """
    surface = pygame.Surface((width, height))
    
    if vertical:
        for y in range(height):
            progress = y / height
            color = (
                int(lerp(start_color[0], end_color[0], progress)),
                int(lerp(start_color[1], end_color[1], progress)),
                int(lerp(start_color[2], end_color[2], progress))
            )
            pygame.draw.line(surface, color, (0, y), (width, y))
    else:
        for x in range(width):
            progress = x / width
            color = (
                int(lerp(start_color[0], end_color[0], progress)),
                int(lerp(start_color[1], end_color[1], progress)),
                int(lerp(start_color[2], end_color[2], progress))
            )
            pygame.draw.line(surface, color, (x, 0), (x, height))
    
    return surface


def format_time(seconds):
    """Format seconds into MM:SS format.
    
    Args:
        seconds: Time in seconds
    
    Returns:
        Formatted time string
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def format_number(number):
    """Format a number with comma separators.
    
    Args:
        number: Number to format
    
    Returns:
        Formatted string (e.g., "1,000,000")
    """
    return f"{number:,}"


def get_file_path(*path_parts):
    """Get a file path relative to the project root.
    
    Args:
        *path_parts: Path components
    
    Returns:
        Absolute file path
    """
    # Get the directory containing this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up to the src directory, then project root
    project_root = os.path.dirname(current_dir)
    # Join with provided path parts
    return os.path.join(project_root, *path_parts)


def ensure_directory_exists(directory_path):
    """Create directory if it doesn't exist.
    
    Args:
        directory_path: Path to directory
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")
