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


class SaveSlotButton(Button):
    """Button for a save slot with save file information."""

    def __init__(self, x: int, y: int, width: int, height: int, save_data: dict, callback):
        """
        Initialize save slot button.

        Args:
            x: X position
            y: Y position
            width: Button width
            height: Button height
            save_data: Dictionary with save file data
            callback: Callback function when clicked
        """
        self.save_data = save_data
        self.slot_number = save_data.get("slot", 1)

        # Create display text
        if save_data.get("exists", False):
            player_name = save_data.get("player_name", "Unknown")
            level = save_data.get("level", 1)
            playtime = save_data.get("playtime", "0h 0m")
            text = f"Slot {self.slot_number}: {player_name} (Lv.{level}) - {playtime}"
        else:
            text = f"Slot {self.slot_number}: Empty"

        super().__init__(x, y, width, height, text, callback)

        # Custom colors for empty slots
        if not save_data.get("exists", False):
            self.color = (80, 80, 80)
            self.hover_color = (100, 100, 100)


class LoadGameState(State):
    """Load game menu - displays saved games."""

    def __init__(self, game):
        super().__init__(game)

        # Save file directory
        self.saves_dir = "saves"

        # UI elements
        self.title_text = None
        self.no_saves_text = None
        self.save_buttons = []
        self.back_button = None

        # Save data
        self.save_slots = []
        self.has_saves = False

        self._ensure_saves_directory()
        self._load_save_data()
        self._setup_ui()

    def _ensure_saves_directory(self):
        """Create saves directory if it doesn't exist."""
        if not os.path.exists(self.saves_dir):
            os.makedirs(self.saves_dir)
            print(f"Created saves directory: {self.saves_dir}")

    def _load_save_data(self):
        """Load information about all save files."""
        self.save_slots = []

        # Check for save files (save_1.json, save_2.json, etc.)
        for slot in range(1, 4):  # 3 save slots
            save_path = os.path.join(self.saves_dir, f"save_{slot}.json")

            if os.path.exists(save_path):
                try:
                    with open(save_path, 'r') as f:
                        data = json.load(f)

                    # Extract key information
                    save_info = {
                        "slot": slot,
                        "exists": True,
                        "path": save_path,
                        "player_name": data.get("player", {}).get("name", "Unknown"),
                        "level": data.get("player", {}).get("level", 1),
                        "location": data.get("location", "Unknown"),
                        "playtime": data.get("playtime", "0h 0m"),
                        "timestamp": data.get("timestamp", "Unknown"),
                        "data": data
                    }
                    self.save_slots.append(save_info)
                    self.has_saves = True

                except Exception as e:
                    print(f"Error loading save file {save_path}: {e}")
                    # Add empty slot
                    self.save_slots.append({
                        "slot": slot,
                        "exists": False,
                        "path": save_path
                    })
            else:
                # Empty slot
                self.save_slots.append({
                    "slot": slot,
                    "exists": False,
                    "path": save_path
                })

    def _setup_ui(self):
        """Set up UI elements."""
        # Title
        self.title_text = CenteredText(
            x=SCREEN_WIDTH // 2,
            y=80,
            text="Load Game",
            font_size=64,
            color=WHITE,
            centered=True
        )

        # If no saves, show message
        if not self.has_saves:
            self.no_saves_text = CenteredText(
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2,
                text="No save files found",
                font_size=36,
                color=(150, 150, 150),
                centered=True
            )
        else:
            # Create buttons for each save slot
            button_width = 600
            button_height = 60
            start_y = 200
            spacing = 80

            for i, save_data in enumerate(self.save_slots):
                if save_data.get("exists", False):
                    button = SaveSlotButton(
                        x=SCREEN_WIDTH // 2 - button_width // 2,
                        y=start_y + (i * spacing),
                        width=button_width,
                        height=button_height,
                        save_data=save_data,
                        callback=lambda sd=save_data: self._on_load_save(sd)
                    )
                    self.save_buttons.append(button)

        # Back button
        self.back_button = Button(
            x=SCREEN_WIDTH // 2 - 100,
            y=SCREEN_HEIGHT - 100,
            width=200,
            height=50,
            text="Back to Menu",
            callback=self._on_back
        )

    def _on_load_save(self, save_data: dict):
        """
        Load the selected save file.

        Args:
            save_data: Dictionary with save file information
        """
        print(f"Loading save file: Slot {save_data['slot']}")
        print(f"  Player: {save_data['player_name']} (Level {save_data['level']})")
        print(f"  Location: {save_data['location']}")
        print(f"  Playtime: {save_data['playtime']}")

        # TODO: Actually load the game data and transition to world state
        # For now, just show a message
        print("TODO: Implement actual save loading")
        print("  Would pass player data to world state via persistent dict")

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

        # Handle save slot buttons
        for button in self.save_buttons:
            button.handle_event(event)

        # Handle back button
        if self.back_button:
            self.back_button.handle_event(event)

    def update(self, dt: float):
        """Update state."""
        # Update save slot buttons
        for button in self.save_buttons:
            button.update(dt)

        if self.back_button:
            self.back_button.update(dt)

    def render(self, screen: pygame.Surface):
        """Render load game menu."""
        screen.fill(BLACK)

        # Draw title
        if self.title_text:
            self.title_text.render(screen)

        # Draw no saves message or save slots
        if not self.has_saves:
            if self.no_saves_text:
                self.no_saves_text.render(screen)

            # Draw hint text
            hint_font = pygame.font.Font(None, 28)
            hint_text = "Start a new game to create a save file"
            hint_surface = hint_font.render(hint_text, True, (150, 150, 150))
            hint_rect = hint_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            screen.blit(hint_surface, hint_rect)
        else:
            # Draw save slot buttons
            for button in self.save_buttons:
                button.render(screen)

            # Draw info text
            info_font = pygame.font.Font(None, 24)
            info_text = "Click a save slot to load the game"
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
        # Reload save data in case it changed
        self._load_save_data()
        # Rebuild UI
        self.save_buttons = []
        self._setup_ui()

    def cleanup(self):
        """Called when leaving state."""
        print("Load Game menu cleanup")
        return {}
