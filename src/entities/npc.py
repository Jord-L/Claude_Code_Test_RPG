"""
NPC (Non-Player Character) System
NPCs that populate islands, provide quests, run shops, and give dialogue.
"""

import pygame
from typing import Optional, Dict, Any
from utils.constants import *


class NPC:
    """Non-player character with dialogue, quests, and shop interactions."""

    def __init__(self, npc_id: str, name: str, tile_x: int, tile_y: int):
        """
        Initialize NPC.

        Args:
            npc_id: Unique NPC identifier
            name: Display name
            tile_x: Tile X position
            tile_y: Tile Y position
        """
        self.npc_id = npc_id
        self.name = name
        self.tile_x = tile_x
        self.tile_y = tile_y

        # Position in pixels
        self.x = tile_x * TILE_SIZE
        self.y = tile_y * TILE_SIZE

        # NPC type
        self.npc_type = "generic"  # generic, shopkeeper, quest_giver, crew_member

        # Dialogue
        self.dialogue_id: Optional[str] = None
        self.current_dialogue_index = 0

        # Shop
        self.shop_id: Optional[str] = None

        # Quest
        self.quest_id: Optional[str] = None

        # Visual
        self.color = YELLOW  # NPCs are yellow
        self.size = TILE_SIZE - 10
        self.sprite: Optional[pygame.Surface] = None

        # Interaction
        self.can_interact = True
        self.interaction_range = TILE_SIZE * 1.5

    def is_in_range(self, player_x: int, player_y: int) -> bool:
        """
        Check if player is in interaction range.

        Args:
            player_x: Player X position (pixels)
            player_y: Player Y position (pixels)

        Returns:
            True if in range
        """
        dist_x = abs(self.x - player_x)
        dist_y = abs(self.y - player_y)
        distance = (dist_x ** 2 + dist_y ** 2) ** 0.5
        return distance <= self.interaction_range

    def interact(self) -> Dict[str, Any]:
        """
        Interact with NPC.

        Returns:
            Interaction result
        """
        result = {
            "npc_id": self.npc_id,
            "name": self.name,
            "type": self.npc_type
        }

        if self.dialogue_id:
            result["action"] = "dialogue"
            result["dialogue_id"] = self.dialogue_id

        elif self.shop_id:
            result["action"] = "shop"
            result["shop_id"] = self.shop_id

        elif self.quest_id:
            result["action"] = "quest"
            result["quest_id"] = self.quest_id

        else:
            result["action"] = "talk"
            result["message"] = f"{self.name}: Hello there!"

        return result

    def render(self, surface: pygame.Surface, camera_x: int, camera_y: int):
        """
        Render NPC.

        Args:
            surface: Surface to draw on
            camera_x: Camera X offset
            camera_y: Camera Y offset
        """
        # Calculate screen position
        screen_x = self.x + camera_x
        screen_y = self.y + camera_y

        # Only render if on screen
        if -TILE_SIZE < screen_x < SCREEN_WIDTH + TILE_SIZE and -TILE_SIZE < screen_y < SCREEN_HEIGHT + TILE_SIZE:
            if self.sprite:
                # Use sprite if available
                surface.blit(self.sprite, (screen_x, screen_y))
            else:
                # Draw colored rectangle
                npc_rect = pygame.Rect(screen_x + 5, screen_y + 5, self.size, self.size)
                pygame.draw.rect(surface, self.color, npc_rect)

                # Draw indicator above NPC
                indicator_y = screen_y - 10
                if self.npc_type == "shopkeeper":
                    indicator_text = "🏪"
                elif self.npc_type == "quest_giver":
                    indicator_text = "❗"
                elif self.npc_type == "crew_member":
                    indicator_text = "⭐"
                else:
                    indicator_text = "💬"

                font = pygame.font.Font(None, 20)
                text_surface = font.render(indicator_text, True, WHITE)
                surface.blit(text_surface, (screen_x + self.size // 2 - 5, indicator_y))

    def render_name(self, surface: pygame.Surface, camera_x: int, camera_y: int):
        """Render NPC name tag."""
        screen_x = self.x + camera_x
        screen_y = self.y + camera_y

        font = pygame.font.Font(None, 18)
        name_surface = font.render(self.name, True, WHITE)
        name_rect = name_surface.get_rect(center=(screen_x + self.size // 2, screen_y - 15))

        # Draw background
        bg_rect = name_rect.inflate(4, 2)
        pygame.draw.rect(surface, (0, 0, 0, 180), bg_rect)

        surface.blit(name_surface, name_rect)
