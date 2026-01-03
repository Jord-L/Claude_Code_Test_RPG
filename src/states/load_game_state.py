"""
Load Game State
Display saved games and allow loading them.
"""

import pygame
import os
import json
from datetime import datetime
from states.state import State
from ui.button import Button
from ui.text_box import CenteredText
from utils.constants import *
from utils.save_manager import get_save_manager
from entities.player import Player


class CharacterButton(Button):
    """Button for a character with their latest save information."""

    def __init__(self, x: int, y: int, width: int, height: int, character_data: dict, callback):
        """
        Initialize character button.

        Args:
            x: X position
            y: Y position
            width: Button width
            height: Button height
            character_data: Dictionary with character data
            callback: Callback function when clicked
        """
        self.character_data = character_data

        # Create display text
        name = character_data.get("character_name", "Unknown")
        level = character_data.get("level", 1)
        playtime = character_data.get("playtime_formatted", "0h 0m")
        text = f"{name} - Lv.{level} - {playtime}"

        super().__init__(x, y, width, height, text, callback)


class LoadGameState(State):
    """Load game menu - displays character selection."""

    def __init__(self, game):
        super().__init__(game)

        # Save manager
        self.save_manager = get_save_manager()

        # UI elements
        self.title_text = None
        self.no_saves_text = None
        self.character_buttons = []
        self.back_button = None

        # Character data
        self.characters = []
        self.has_characters = False

        self._load_character_data()
        self._setup_ui()

    def _load_character_data(self):
        """Load information about all character directories."""
        self.characters = []
        self.has_characters = False

        # Get all characters from save manager
        all_characters = self.save_manager.get_all_characters()

        self.characters = all_characters
        self.has_characters = len(all_characters) > 0

    def _setup_ui(self):
        """Set up UI elements."""
        # Title
        self.title_text = CenteredText(
            x=SCREEN_WIDTH // 2,
            y=80,
            text="Select Character",
            font_size=64,
            color=WHITE,
            centered=True
        )

        # If no characters, show message
        if not self.has_characters:
            self.no_saves_text = CenteredText(
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2,
                text="No characters found",
                font_size=36,
                color=(150, 150, 150),
                centered=True
            )
        else:
            # Create buttons for each character
            button_width = 600
            button_height = 60
            start_y = 200
            spacing = 80

            for i, character_data in enumerate(self.characters):
                button = CharacterButton(
                    x=SCREEN_WIDTH // 2 - button_width // 2,
                    y=start_y + (i * spacing),
                    width=button_width,
                    height=button_height,
                    character_data=character_data,
                    callback=lambda cd=character_data: self._on_load_character(cd)
                )
                self.character_buttons.append(button)

        # Back button
        self.back_button = Button(
            x=SCREEN_WIDTH // 2 - 100,
            y=SCREEN_HEIGHT - 100,
            width=200,
            height=50,
            text="Back to Menu",
            callback=self._on_back
        )

    def _on_load_character(self, character_data: dict):
        """
        Load the selected character's latest save.

        Args:
            character_data: Dictionary with character information
        """
        character_name = character_data.get('character_name', 'Unknown')
        directory_name = character_data.get('directory_name', character_name)
        level = character_data.get('level', 1)
        playtime = character_data.get('playtime_formatted', '0h 0m')

        print(f"\n{'='*60}")
        print(f"LOADING CHARACTER: {character_name}")
        print(f"{'='*60}")
        print(f"  Level: {level}")
        print(f"  Playtime: {playtime}")

        # Load the character's latest save
        latest_save = self.save_manager.get_character_latest_save(directory_name)

        if latest_save:
            try:
                # Extract character data
                save_character_data = latest_save.get('character', {})

                # Reconstruct the player from saved data
                player = Player.from_dict(save_character_data)

                print(f"✓ Player loaded: {player.name}")
                print(f"✓ Level: {player.level}")
                print(f"✓ Devil Fruit: {player.devil_fruit.name if player.devil_fruit else 'None'}")
                print(f"\n🎮 Transitioning to world state...")
                print(f"{'='*60}\n")

                # Store the loaded player to pass to world state
                self.loaded_player = player

                # Transition to world state
                self.state_manager.change_state("world")

            except Exception as e:
                print(f"✗ Error loading character: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"✗ Failed to load character {character_name}")

    def _on_back(self):
        """Return to main menu."""
        print("Load Game: Returning to main menu")
        self.state_manager.change_state(STATE_MENU)

    def handle_event(self, event: pygame.event.Event):
        """Handle input events."""
        # ESC to go back
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._on_back()
                return

        # Handle character buttons
        for button in self.character_buttons:
            button.handle_event(event)

        # Handle back button
        if self.back_button:
            self.back_button.handle_event(event)

    def update(self, dt: float):
        """Update state."""
        # Update character buttons
        for button in self.character_buttons:
            button.update(dt)

        if self.back_button:
            self.back_button.update(dt)

    def render(self, screen: pygame.Surface):
        """Render load game menu."""
        screen.fill(BLACK)

        # Draw title
        if self.title_text:
            self.title_text.render(screen)

        # Draw no characters message or character buttons
        if not self.has_characters:
            if self.no_saves_text:
                self.no_saves_text.render(screen)

            # Draw hint text
            hint_font = pygame.font.Font(None, 28)
            hint_text = "Create a new character to get started"
            hint_surface = hint_font.render(hint_text, True, (150, 150, 150))
            hint_rect = hint_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            screen.blit(hint_surface, hint_rect)
        else:
            # Draw character buttons
            for button in self.character_buttons:
                button.render(screen)

            # Draw info text
            info_font = pygame.font.Font(None, 24)
            info_text = "Select a character to load their latest save"
            info_surface = info_font.render(info_text, True, (150, 150, 150))
            info_rect = info_surface.get_rect(center=(SCREEN_WIDTH // 2, 550))
            screen.blit(info_surface, info_rect)

        # Draw back button
        if self.back_button:
            self.back_button.render(screen)

        # Draw instructions
        font = pygame.font.Font(None, 24)
        instructions = "ESC or Back button to return to menu"
        text_surface = font.render(instructions, True, (150, 150, 150))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        screen.blit(text_surface, text_rect)

    def startup(self, persistent):
        """Called when state becomes active."""
        print("Load Game menu loaded")
        # Reload character data in case it changed
        self._load_character_data()
        # Rebuild UI
        self.character_buttons = []
        self._setup_ui()

    def cleanup(self):
        """Called when leaving state."""
        print("Load Game menu cleanup")

        # If we loaded a player, pass it to the next state
        if hasattr(self, 'loaded_player'):
            print(f"Passing loaded player to next state: {self.loaded_player.name}")
            return {'player': self.loaded_player}

        return {}
