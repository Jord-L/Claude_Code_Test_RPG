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

        # Save manager
        self.save_manager = get_save_manager()

        # UI elements
        self.title_text = None
        self.no_saves_text = None
        self.save_buttons = []
        self.back_button = None

        # Save data
        self.save_slots = []
        self.has_saves = False

        self._load_save_data()
        self._setup_ui()

    def _load_save_data(self):
        """Load information about all save files."""
        self.save_slots = []
        self.has_saves = False

        # Get all save slot information from save manager
        all_saves = self.save_manager.get_all_saves()

        for save_info in all_saves:
            if save_info['exists']:
                # Format playtime
                playtime_seconds = save_info.get('playtime', 0)
                hours = int(playtime_seconds // 3600)
                minutes = int((playtime_seconds % 3600) // 60)
                playtime_str = f"{hours}h {minutes}m"

                # Format timestamp
                timestamp = save_info.get('timestamp', 'Unknown')
                try:
                    if timestamp != 'Unknown':
                        dt = datetime.fromisoformat(timestamp)
                        timestamp_str = dt.strftime("%Y-%m-%d %H:%M")
                    else:
                        timestamp_str = "Unknown"
                except:
                    timestamp_str = "Unknown"

                slot_data = {
                    "slot": save_info['slot'],
                    "exists": True,
                    "player_name": save_info.get('character_name', 'Unknown'),
                    "level": save_info.get('level', 1),
                    "location": save_info.get('location', 'Tutorial Island'),
                    "playtime": playtime_str,
                    "timestamp": timestamp_str
                }
                self.save_slots.append(slot_data)
                self.has_saves = True
            else:
                # Empty slot
                self.save_slots.append({
                    "slot": save_info['slot'],
                    "exists": False
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
            # Create buttons for ALL save slots (show empty ones too)
            button_width = 600
            button_height = 60
            start_y = 200
            spacing = 80

            for i, save_data in enumerate(self.save_slots):
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
        # Check if slot is empty
        if not save_data.get('exists', False):
            print(f"Slot {save_data['slot']} is empty - cannot load")
            return

        slot = save_data['slot']
        print(f"\n{'='*60}")
        print(f"LOADING SAVE FILE: Slot {slot}")
        print(f"{'='*60}")
        print(f"  Player: {save_data['player_name']} (Level {save_data['level']})")
        print(f"  Location: {save_data['location']}")
        print(f"  Playtime: {save_data['playtime']}")

        # Load the save file data
        loaded_data = self.save_manager.load_game(slot)

        if loaded_data:
            try:
                # Extract character data
                character_data = loaded_data.get('character', {})

                # Reconstruct the player from saved data
                player = Player.from_dict(character_data)

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
                print(f"✗ Error loading save file: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"✗ Failed to load save file from slot {slot}")

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

        # If we loaded a player, pass it to the next state
        if hasattr(self, 'loaded_player'):
            print(f"Passing loaded player to next state: {self.loaded_player.name}")
            return {'player': self.loaded_player}

        return {}
