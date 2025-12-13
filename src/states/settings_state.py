"""
Settings State
Allows players to configure game settings.
"""

import pygame
from states.state import State
from ui.button import Button
from ui.panel import Panel
from ui.text_box import CenteredText
from utils.constants import *


class SettingsState(State):
    """
    Settings menu for configuring game options.
    """

    def __init__(self, game):
        """
        Initialize settings state.

        Args:
            game: Game instance
        """
        super().__init__(game)

        # Settings data
        self.settings = {
            "music_volume": 0.7,
            "sfx_volume": 0.8,
            "fullscreen": False,
            "show_fps": False,
            "battle_speed": "Normal"  # Slow, Normal, Fast
        }

        # UI Components
        self.title_text = None
        self.main_panel = None
        self.buttons = []
        self.back_button = None

        # Battle speed options
        self.battle_speed_options = ["Slow", "Normal", "Fast"]
        self.battle_speed_index = 1  # Default to Normal

        self._setup_ui()

    def _setup_ui(self):
        """Set up UI elements."""
        # Title
        self.title_text = CenteredText(
            x=SCREEN_WIDTH // 2,
            y=50,
            text="Settings",
            font_size=64,
            color=UI_TEXT_COLOR,
            centered=True
        )

        # Main panel
        self.main_panel = Panel(
            x=SCREEN_WIDTH // 2 - 400,
            y=150,
            width=800,
            height=450
        )
        self.main_panel.bg_color = UI_BG_COLOR
        self.main_panel.border_color = UI_BORDER_COLOR
        self.main_panel.border_width = 3

        # Create setting buttons
        y_start = 200
        y_spacing = 80

        # Music Volume
        music_minus = Button(
            x=SCREEN_WIDTH // 2 - 200,
            y=y_start,
            width=60,
            height=40,
            text="-",
            callback=lambda: self._adjust_volume("music", -0.1)
        )
        self.buttons.append(music_minus)

        music_plus = Button(
            x=SCREEN_WIDTH // 2 + 140,
            y=y_start,
            width=60,
            height=40,
            text="+",
            callback=lambda: self._adjust_volume("music", 0.1)
        )
        self.buttons.append(music_plus)

        # SFX Volume
        sfx_minus = Button(
            x=SCREEN_WIDTH // 2 - 200,
            y=y_start + y_spacing,
            width=60,
            height=40,
            text="-",
            callback=lambda: self._adjust_volume("sfx", -0.1)
        )
        self.buttons.append(sfx_minus)

        sfx_plus = Button(
            x=SCREEN_WIDTH // 2 + 140,
            y=y_start + y_spacing,
            width=60,
            height=40,
            text="+",
            callback=lambda: self._adjust_volume("sfx", 0.1)
        )
        self.buttons.append(sfx_plus)

        # Fullscreen Toggle
        fullscreen_button = Button(
            x=SCREEN_WIDTH // 2 + 50,
            y=y_start + y_spacing * 2,
            width=150,
            height=40,
            text="Off",
            callback=self._toggle_fullscreen
        )
        self.buttons.append(fullscreen_button)

        # Show FPS Toggle
        fps_button = Button(
            x=SCREEN_WIDTH // 2 + 50,
            y=y_start + y_spacing * 3,
            width=150,
            height=40,
            text="Off",
            callback=self._toggle_fps
        )
        self.buttons.append(fps_button)

        # Battle Speed
        battle_speed_button = Button(
            x=SCREEN_WIDTH // 2 + 50,
            y=y_start + y_spacing * 4,
            width=150,
            height=40,
            text="Normal",
            callback=self._cycle_battle_speed
        )
        self.buttons.append(battle_speed_button)

        # Back button
        self.back_button = Button(
            x=SCREEN_WIDTH // 2 - 100,
            y=SCREEN_HEIGHT - 100,
            width=200,
            height=50,
            text="Back to Menu",
            callback=self._on_back
        )
        self.buttons.append(self.back_button)

    def _adjust_volume(self, volume_type: str, delta: float):
        """
        Adjust volume setting.

        Args:
            volume_type: "music" or "sfx"
            delta: Amount to change (+/- 0.1)
        """
        key = f"{volume_type}_volume"
        self.settings[key] = max(0.0, min(1.0, self.settings[key] + delta))
        print(f"Settings: {volume_type.title()} volume set to {int(self.settings[key] * 100)}%")

        # TODO: Apply to actual audio system
        # if volume_type == "music":
        #     pygame.mixer.music.set_volume(self.settings[key])

    def _toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.settings["fullscreen"] = not self.settings["fullscreen"]
        status = "On" if self.settings["fullscreen"] else "Off"
        print(f"Settings: Fullscreen {status}")

        # Update button text
        for button in self.buttons:
            if button and button.text in ["On", "Off"] and button.y == 280:
                button.text = status

        # TODO: Apply fullscreen toggle
        # if self.settings["fullscreen"]:
        #     pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        # else:
        #     pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def _toggle_fps(self):
        """Toggle FPS display."""
        self.settings["show_fps"] = not self.settings["show_fps"]
        status = "On" if self.settings["show_fps"] else "Off"
        print(f"Settings: Show FPS {status}")

        # Update button text
        for button in self.buttons:
            if button and button.text in ["On", "Off"] and button.y == 360:
                button.text = status

    def _cycle_battle_speed(self):
        """Cycle through battle speed options."""
        self.battle_speed_index = (self.battle_speed_index + 1) % len(self.battle_speed_options)
        speed = self.battle_speed_options[self.battle_speed_index]
        self.settings["battle_speed"] = speed
        print(f"Settings: Battle speed set to {speed}")

        # Update button text
        for button in self.buttons:
            if button and button.text in self.battle_speed_options:
                button.text = speed

    def _on_back(self):
        """Return to main menu."""
        print("Settings: Returning to main menu")
        self.state_manager.change_state(STATE_MENU)

    def handle_event(self, event: pygame.event.Event):
        """
        Handle settings input.

        Args:
            event: Pygame event
        """
        # ESC to go back
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._on_back()

        # Handle button events
        for button in self.buttons:
            if button:
                button.handle_event(event)

    def update(self, dt: float):
        """
        Update settings state.

        Args:
            dt: Delta time
        """
        # Update buttons
        for button in self.buttons:
            if button:
                button.update(dt)

    def render(self, screen: pygame.Surface):
        """
        Render settings menu.

        Args:
            screen: Pygame surface to render to
        """
        # Clear screen
        screen.fill(BLACK)

        # Draw title
        self.title_text.render(screen)

        # Draw main panel
        self.main_panel.render(screen)

        # Draw setting labels
        font = pygame.font.Font(None, 36)
        y_start = 200
        y_spacing = 80

        settings_labels = [
            "Music Volume:",
            "SFX Volume:",
            "Fullscreen:",
            "Show FPS:",
            "Battle Speed:"
        ]

        for i, label in enumerate(settings_labels):
            y_pos = y_start + (i * y_spacing)

            # Draw label
            label_surface = font.render(label, True, UI_TEXT_COLOR)
            screen.blit(label_surface, (SCREEN_WIDTH // 2 - 350, y_pos + 5))

            # Draw value
            if i == 0:  # Music volume
                value = f"{int(self.settings['music_volume'] * 100)}%"
            elif i == 1:  # SFX volume
                value = f"{int(self.settings['sfx_volume'] * 100)}%"
            elif i == 2:  # Fullscreen
                value = "On" if self.settings["fullscreen"] else "Off"
            elif i == 3:  # Show FPS
                value = "On" if self.settings["show_fps"] else "Off"
            elif i == 4:  # Battle speed
                value = self.settings["battle_speed"]

            if i < 2:  # Volume settings - show value between buttons
                value_surface = font.render(value, True, UI_HIGHLIGHT_COLOR)
                value_rect = value_surface.get_rect(center=(SCREEN_WIDTH // 2 - 30, y_pos + 20))
                screen.blit(value_surface, value_rect)

        # Draw buttons
        for button in self.buttons:
            if button:
                button.render(screen)

        # Draw hint text
        hint_font = pygame.font.Font(None, 28)
        hint_text = "ESC to go back"
        hint_surface = hint_font.render(hint_text, True, UI_TEXT_COLOR)
        screen.blit(hint_surface, (10, SCREEN_HEIGHT - 30))

    def startup(self, persistent):
        """Called when state becomes active."""
        print("Settings menu loaded")

    def cleanup(self):
        """Called when state is removed."""
        print("Settings menu cleanup")
        return {}
