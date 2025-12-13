"""
Load Game State
Allows players to load saved games.
"""

import pygame
import os
import json
from typing import List, Dict, Optional
from states.state import State
from ui.button import Button
from ui.panel import Panel
from ui.text_box import CenteredText
from utils.constants import *


class SaveSlot:
    """Represents a save game slot."""

    def __init__(self, slot_id: int, data: Optional[Dict] = None):
        """
        Initialize save slot.

        Args:
            slot_id: Save slot number (1-3)
            data: Save data dict or None if empty
        """
        self.slot_id = slot_id
        self.data = data
        self.is_empty = data is None

        # Parse save data
        if not self.is_empty:
            self.player_name = data.get("player_name", "Unknown")
            self.level = data.get("level", 1)
            self.playtime = data.get("playtime", 0)
            self.location = data.get("location", "Unknown")
            self.timestamp = data.get("timestamp", "")
        else:
            self.player_name = "Empty Slot"
            self.level = 0
            self.playtime = 0
            self.location = ""
            self.timestamp = ""


class LoadGameState(State):
    """
    Load game menu for selecting save files.
    """

    def __init__(self, game):
        """
        Initialize load game state.

        Args:
            game: Game instance
        """
        super().__init__(game)

        # Save slots
        self.save_slots: List[SaveSlot] = []
        self.selected_slot = 0
        self.max_slots = 3

        # UI Components
        self.title_text = None
        self.main_panel = None
        self.slot_panels = []
        self.buttons = []
        self.load_button = None
        self.delete_button = None
        self.back_button = None

        # Save directory
        self.save_dir = "saves"

        self._load_saves()
        self._setup_ui()

    def _load_saves(self):
        """Load all save files."""
        self.save_slots = []

        # Create saves directory if it doesn't exist
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            print(f"Created save directory: {self.save_dir}")

        # Load each slot
        for slot_id in range(1, self.max_slots + 1):
            save_file = os.path.join(self.save_dir, f"save_{slot_id}.json")

            if os.path.exists(save_file):
                try:
                    with open(save_file, 'r') as f:
                        data = json.load(f)
                    self.save_slots.append(SaveSlot(slot_id, data))
                    print(f"Loaded save slot {slot_id}: {data.get('player_name', 'Unknown')}")
                except Exception as e:
                    print(f"Error loading save slot {slot_id}: {e}")
                    self.save_slots.append(SaveSlot(slot_id, None))
            else:
                # Empty slot
                self.save_slots.append(SaveSlot(slot_id, None))

    def _setup_ui(self):
        """Set up UI elements."""
        # Title
        self.title_text = CenteredText(
            x=SCREEN_WIDTH // 2,
            y=50,
            text="Load Game",
            font_size=64,
            color=UI_TEXT_COLOR,
            centered=True
        )

        # Create panels for each save slot
        panel_height = 120
        panel_spacing = 140
        start_y = 180

        for i in range(self.max_slots):
            panel = Panel(
                x=SCREEN_WIDTH // 2 - 400,
                y=start_y + (i * panel_spacing),
                width=800,
                height=panel_height
            )
            panel.bg_color = UI_BG_COLOR
            panel.border_color = UI_BORDER_COLOR
            panel.border_width = 3
            self.slot_panels.append(panel)

        # Load button
        self.load_button = Button(
            x=SCREEN_WIDTH // 2 - 220,
            y=SCREEN_HEIGHT - 100,
            width=200,
            height=50,
            text="Load Game",
            callback=self._on_load
        )
        self.buttons.append(self.load_button)

        # Delete button
        self.delete_button = Button(
            x=SCREEN_WIDTH // 2 + 20,
            y=SCREEN_HEIGHT - 100,
            width=200,
            height=50,
            text="Delete Save",
            callback=self._on_delete
        )
        self.buttons.append(self.delete_button)

        # Back button
        self.back_button = Button(
            x=SCREEN_WIDTH // 2 - 100,
            y=SCREEN_HEIGHT - 40,
            width=200,
            height=35,
            text="Back to Menu",
            callback=self._on_back
        )
        self.buttons.append(self.back_button)

        # Update button states
        self._update_button_states()

    def _update_button_states(self):
        """Update load/delete button enabled states."""
        selected_save = self.save_slots[self.selected_slot]

        # Load button only enabled if slot has save data
        self.load_button.enabled = not selected_save.is_empty

        # Delete button only enabled if slot has save data
        self.delete_button.enabled = not selected_save.is_empty

    def _on_load(self):
        """Load the selected save."""
        selected_save = self.save_slots[self.selected_slot]

        if not selected_save.is_empty:
            print(f"Loading save slot {selected_save.slot_id}: {selected_save.player_name}")
            # TODO: Actually load the game state
            # For now, just show a message
            print("Note: Save loading not fully implemented yet")
            print(f"  Player: {selected_save.player_name} (Level {selected_save.level})")
            print(f"  Location: {selected_save.location}")
            # self.state_manager.change_state(STATE_WORLD)  # Would load into world

    def _on_delete(self):
        """Delete the selected save."""
        selected_save = self.save_slots[self.selected_slot]

        if not selected_save.is_empty:
            save_file = os.path.join(self.save_dir, f"save_{selected_save.slot_id}.json")

            try:
                os.remove(save_file)
                print(f"Deleted save slot {selected_save.slot_id}")

                # Reload saves
                self._load_saves()
                self._update_button_states()

            except Exception as e:
                print(f"Error deleting save: {e}")

    def _on_back(self):
        """Return to main menu."""
        print("Load Game: Returning to main menu")
        self.state_manager.change_state(STATE_MENU)

    def handle_event(self, event: pygame.event.Event):
        """
        Handle input.

        Args:
            event: Pygame event
        """
        # Keyboard navigation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_slot = (self.selected_slot - 1) % self.max_slots
                self._update_button_states()

            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_slot = (self.selected_slot + 1) % self.max_slots
                self._update_button_states()

            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.load_button.enabled:
                    self._on_load()

            elif event.key == pygame.K_DELETE:
                if self.delete_button.enabled:
                    self._on_delete()

            elif event.key == pygame.K_ESCAPE:
                self._on_back()

        # Mouse click on slot panels
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()

                for i, panel in enumerate(self.slot_panels):
                    if panel.rect.collidepoint(mouse_pos):
                        self.selected_slot = i
                        self._update_button_states()
                        break

        # Handle button events
        for button in self.buttons:
            button.handle_event(event)

    def update(self, dt: float):
        """
        Update load game state.

        Args:
            dt: Delta time
        """
        # Update buttons
        for button in self.buttons:
            button.update(dt)

    def render(self, screen: pygame.Surface):
        """
        Render load game menu.

        Args:
            screen: Pygame surface to render to
        """
        # Clear screen
        screen.fill(BLACK)

        # Draw title
        self.title_text.render(screen)

        # Draw save slot panels
        font_large = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 28)

        for i, (panel, save_slot) in enumerate(zip(self.slot_panels, self.save_slots)):
            # Highlight selected slot
            if i == self.selected_slot:
                panel.border_color = UI_HIGHLIGHT_COLOR
                panel.border_width = 4
            else:
                panel.border_color = UI_BORDER_COLOR
                panel.border_width = 3

            panel.render(screen)

            # Draw slot content
            x_offset = panel.rect.x + 20
            y_offset = panel.rect.y + 15

            # Slot number
            slot_text = f"Slot {save_slot.slot_id}"
            slot_surface = font_large.render(slot_text, True, UI_TEXT_COLOR)
            screen.blit(slot_surface, (x_offset, y_offset))

            if save_slot.is_empty:
                # Empty slot
                empty_text = "[Empty]"
                empty_surface = font_small.render(empty_text, True, (150, 150, 150))
                screen.blit(empty_surface, (x_offset + 120, y_offset + 5))
            else:
                # Save info
                y_offset += 40

                # Player name and level
                player_text = f"{save_slot.player_name} - Level {save_slot.level}"
                player_surface = font_small.render(player_text, True, UI_TEXT_COLOR)
                screen.blit(player_surface, (x_offset, y_offset))

                # Location
                location_text = f"Location: {save_slot.location}"
                location_surface = font_small.render(location_text, True, UI_TEXT_COLOR)
                screen.blit(location_surface, (x_offset, y_offset + 30))

                # Playtime (convert seconds to hours:minutes)
                hours = save_slot.playtime // 3600
                minutes = (save_slot.playtime % 3600) // 60
                time_text = f"Playtime: {hours}h {minutes}m"
                time_surface = font_small.render(time_text, True, UI_TEXT_COLOR)
                screen.blit(time_surface, (x_offset + 450, y_offset + 30))

        # Draw buttons
        for button in self.buttons:
            button.render(screen)

        # Draw controls hint
        hint_font = pygame.font.Font(None, 28)
        hint_text = "↑↓ Select  |  ENTER Load  |  DEL Delete  |  ESC Back"
        hint_surface = hint_font.render(hint_text, True, UI_TEXT_COLOR)
        hint_rect = hint_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))
        screen.blit(hint_surface, hint_rect)

    def startup(self, persistent):
        """Called when state becomes active."""
        print("Load Game menu loaded")
        # Reload saves in case they changed
        self._load_saves()
        self._update_button_states()

    def cleanup(self):
        """Called when state is removed."""
        print("Load Game menu cleanup")
        return {}
