"""
Settings State
Manage game settings like volume, fullscreen, and controls.
"""

import pygame
from states.state import State
from ui.button import Button
from ui.text_box import CenteredText
from utils.constants import *
from utils.settings_manager import get_settings_manager


class Slider:
    """Simple slider UI component for numeric values."""

    def __init__(self, x: int, y: int, width: int, min_val: float, max_val: float, initial_val: float, label: str):
        """
        Initialize slider.

        Args:
            x: X position (left edge)
            y: Y position (center)
            width: Width of slider track
            min_val: Minimum value
            max_val: Maximum value
            initial_val: Initial value
            label: Label text
        """
        self.x = x
        self.y = y
        self.width = width
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label

        self.handle_radius = 8
        self.track_height = 4
        self.dragging = False

        self.font = pygame.font.Font(None, 24)

    def get_handle_x(self) -> int:
        """Get the X position of the slider handle."""
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        return int(self.x + ratio * self.width)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle input events.

        Args:
            event: Pygame event

        Returns:
            True if value changed
        """
        changed = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                handle_x = self.get_handle_x()
                mouse_x, mouse_y = event.pos

                # Check if clicking on handle
                if (abs(mouse_x - handle_x) <= self.handle_radius and
                    abs(mouse_y - self.y) <= self.handle_radius):
                    self.dragging = True
                # Or clicking on track
                elif (self.x <= mouse_x <= self.x + self.width and
                      abs(mouse_y - self.y) <= 10):
                    # Jump to clicked position
                    ratio = (mouse_x - self.x) / self.width
                    ratio = max(0, min(1, ratio))
                    old_value = self.value
                    self.value = self.min_val + ratio * (self.max_val - self.min_val)
                    changed = old_value != self.value

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, _ = event.pos
                ratio = (mouse_x - self.x) / self.width
                ratio = max(0, min(1, ratio))
                old_value = self.value
                self.value = self.min_val + ratio * (self.max_val - self.min_val)
                changed = old_value != self.value

        return changed

    def render(self, screen: pygame.Surface):
        """Render the slider."""
        # Label
        label_surface = self.font.render(self.label, True, WHITE)
        screen.blit(label_surface, (self.x, self.y - 28))

        # Value display
        value_text = f"{int(self.value * 100)}%"
        value_surface = self.font.render(value_text, True, UI_TEXT_COLOR)
        screen.blit(value_surface, (self.x + self.width + 15, self.y - 10))

        # Track
        track_rect = pygame.Rect(
            self.x,
            self.y - self.track_height // 2,
            self.width,
            self.track_height
        )
        pygame.draw.rect(screen, (100, 100, 100), track_rect)

        # Filled portion
        handle_x = self.get_handle_x()
        filled_rect = pygame.Rect(
            self.x,
            self.y - self.track_height // 2,
            handle_x - self.x,
            self.track_height
        )
        pygame.draw.rect(screen, UI_HIGHLIGHT_COLOR, filled_rect)

        # Handle
        handle_color = UI_BUTTON_HOVER if self.dragging else WHITE
        pygame.draw.circle(screen, handle_color, (handle_x, self.y), self.handle_radius)
        pygame.draw.circle(screen, BLACK, (handle_x, self.y), self.handle_radius, 2)


class ToggleButton(Button):
    """Button that toggles between ON/OFF states."""

    def __init__(self, x: int, y: int, width: int, height: int, label: str, initial_state: bool, callback):
        """
        Initialize toggle button.

        Args:
            x: X position
            y: Y position
            width: Button width
            height: Button height
            label: Label text
            initial_state: Initial ON/OFF state
            callback: Callback function(new_state)
        """
        self.label = label
        self.state = initial_state
        self._callback = callback

        # Initialize with current state text
        text = f"{label}: {'ON' if initial_state else 'OFF'}"
        super().__init__(x, y, width, height, text, self._on_click)

    def _on_click(self):
        """Handle click - toggle state."""
        self.state = not self.state
        self.text = f"{self.label}: {'ON' if self.state else 'OFF'}"
        self._callback(self.state)


class CycleButton(Button):
    """Button that cycles through multiple options."""

    def __init__(self, x: int, y: int, width: int, height: int, label: str, options: list, initial_index: int, callback):
        """
        Initialize cycle button.

        Args:
            x: X position
            y: Y position
            width: Button width
            height: Button height
            label: Label text
            options: List of option values
            initial_index: Initial option index
            callback: Callback function(new_value)
        """
        self.label = label
        self.options = options
        self.current_index = initial_index
        self._callback = callback

        # Initialize with current option text
        text = f"{label}: {options[initial_index]}"
        super().__init__(x, y, width, height, text, self._on_click)

    def _on_click(self):
        """Handle click - cycle to next option."""
        self.current_index = (self.current_index + 1) % len(self.options)
        self.text = f"{self.label}: {self.options[self.current_index]}"
        self._callback(self.options[self.current_index])

    def get_value(self):
        """Get current selected value."""
        return self.options[self.current_index]


class SettingsState(State):
    """Settings menu for game configuration."""

    def __init__(self, game):
        super().__init__(game)

        print("SettingsState: Initializing...")

        # Current active tab
        self.active_tab = "Audio"  # Audio, Video, or Gameplay

        # Get settings manager
        self.settings_manager = get_settings_manager()

        # Load current settings
        settings = self.settings_manager.get_all()
        self.music_volume = settings.get("music_volume", 0.7)
        self.sfx_volume = settings.get("sfx_volume", 0.8)
        self.text_speed = settings.get("text_speed", 0.5)
        self.fullscreen = settings.get("fullscreen", False)
        self.resolution = settings.get("resolution", "1280x720")
        self.battle_animations = settings.get("battle_animations", True)
        self.auto_save = settings.get("auto_save", True)
        self.difficulty = settings.get("difficulty", "Normal")

        # UI elements
        self.title_text = None
        self.tab_buttons = {}  # Tab switching buttons
        self.music_slider = None
        self.sfx_slider = None
        self.text_speed_slider = None
        self.fullscreen_toggle = None
        self.resolution_cycle = None
        self.battle_animations_toggle = None
        self.auto_save_toggle = None
        self.difficulty_cycle = None
        self.back_button = None

        print("SettingsState: Setting up UI...")
        try:
            self._setup_ui()
            print("SettingsState: UI setup complete!")
        except Exception as e:
            print(f"SettingsState: ERROR during UI setup: {e}")
            import traceback
            traceback.print_exc()

    def _setup_ui(self):
        """Set up UI elements."""
        # Title
        self.title_text = CenteredText(
            x=SCREEN_WIDTH // 2,
            y=60,
            text="Settings",
            font_size=56,
            color=WHITE,
            centered=True
        )

        # Tab buttons
        tab_y = 130
        tab_width = 160
        tab_height = 45
        tab_spacing = 20
        total_tab_width = (tab_width * 3) + (tab_spacing * 2)
        start_x = (SCREEN_WIDTH - total_tab_width) // 2

        self.tab_buttons = {
            "Audio": Button(
                x=start_x,
                y=tab_y,
                width=tab_width,
                height=tab_height,
                text="Audio",
                callback=lambda: self._switch_tab("Audio")
            ),
            "Video": Button(
                x=start_x + tab_width + tab_spacing,
                y=tab_y,
                width=tab_width,
                height=tab_height,
                text="Video",
                callback=lambda: self._switch_tab("Video")
            ),
            "Gameplay": Button(
                x=start_x + (tab_width + tab_spacing) * 2,
                y=tab_y,
                width=tab_width,
                height=tab_height,
                text="Gameplay",
                callback=lambda: self._switch_tab("Gameplay")
            )
        }

        # Settings position (centered)
        center_x = SCREEN_WIDTH // 2
        content_y = 220
        slider_width = 400
        button_width = 300
        button_height = 50
        vertical_spacing = 80

        # AUDIO TAB - Music and SFX volume sliders
        self.music_slider = Slider(
            x=center_x - slider_width // 2,
            y=content_y,
            width=slider_width,
            min_val=0.0,
            max_val=1.0,
            initial_val=self.music_volume,
            label="Music Volume"
        )

        self.sfx_slider = Slider(
            x=center_x - slider_width // 2,
            y=content_y + vertical_spacing,
            width=slider_width,
            min_val=0.0,
            max_val=1.0,
            initial_val=self.sfx_volume,
            label="SFX Volume"
        )

        # VIDEO TAB - Fullscreen toggle and resolution
        self.fullscreen_toggle = ToggleButton(
            x=center_x - button_width // 2,
            y=content_y,
            width=button_width,
            height=button_height,
            label="Fullscreen",
            initial_state=self.fullscreen,
            callback=self._on_fullscreen_toggle
        )

        # Determine initial resolution index
        resolution_options = [
            "1280x720",   # HD
            "1600x900",   # HD+
            "1920x1080",  # Full HD
            "2560x1440",  # 2K
            "3840x2160"   # 4K
        ]
        try:
            resolution_index = resolution_options.index(self.resolution)
        except ValueError:
            resolution_index = 0  # Default to 1280x720

        self.resolution_cycle = CycleButton(
            x=center_x - button_width // 2,
            y=content_y + vertical_spacing,
            width=button_width,
            height=button_height,
            label="Resolution",
            options=resolution_options,
            initial_index=resolution_index,
            callback=self._on_resolution_change
        )

        # GAMEPLAY TAB - Text speed, battle animations, auto-save, difficulty
        self.text_speed_slider = Slider(
            x=center_x - slider_width // 2,
            y=content_y,
            width=slider_width,
            min_val=0.0,
            max_val=1.0,
            initial_val=self.text_speed,
            label="Text Speed"
        )

        self.battle_animations_toggle = ToggleButton(
            x=center_x - button_width // 2,
            y=content_y + vertical_spacing,
            width=button_width,
            height=button_height,
            label="Battle Animations",
            initial_state=self.battle_animations,
            callback=self._on_battle_animations_toggle
        )

        self.auto_save_toggle = ToggleButton(
            x=center_x - button_width // 2,
            y=content_y + vertical_spacing * 2,
            width=button_width,
            height=button_height,
            label="Auto-Save",
            initial_state=self.auto_save,
            callback=self._on_auto_save_toggle
        )

        # Determine initial difficulty index
        difficulty_options = ["Easy", "Normal", "Hard"]
        try:
            difficulty_index = difficulty_options.index(self.difficulty)
        except ValueError:
            difficulty_index = 1  # Default to Normal

        self.difficulty_cycle = CycleButton(
            x=center_x - button_width // 2,
            y=content_y + vertical_spacing * 3,
            width=button_width,
            height=button_height,
            label="Difficulty",
            options=difficulty_options,
            initial_index=difficulty_index,
            callback=self._on_difficulty_change
        )

        # Back button (centered at bottom, with more clearance)
        self.back_button = Button(
            x=SCREEN_WIDTH // 2 - 120,
            y=SCREEN_HEIGHT - 110,
            width=240,
            height=50,
            text="Back to Menu",
            callback=self._on_back
        )

    def _switch_tab(self, tab_name: str):
        """Switch to a different settings tab."""
        print(f"Switching to {tab_name} tab")
        self.active_tab = tab_name

    def _on_fullscreen_toggle(self, enabled: bool):
        """Handle fullscreen toggle."""
        print(f"Fullscreen: {'Enabled' if enabled else 'Disabled'}")
        self.fullscreen = enabled

        # Apply fullscreen immediately
        try:
            if enabled:
                # Get current display info
                display_info = pygame.display.Info()
                self.game.screen = pygame.display.set_mode(
                    (display_info.current_w, display_info.current_h),
                    pygame.FULLSCREEN
                )
                print(f"Switched to fullscreen: {display_info.current_w}x{display_info.current_h}")
            else:
                # Return to windowed mode with current resolution
                width, height = self._parse_resolution(self.resolution)
                self.game.screen = pygame.display.set_mode((width, height))
                print(f"Switched to windowed mode: {width}x{height}")
        except Exception as e:
            print(f"Error toggling fullscreen: {e}")

    def _on_resolution_change(self, resolution: str):
        """Handle resolution change."""
        print(f"Resolution changed to: {resolution}")
        self.resolution = resolution

        # Apply resolution immediately (only if not in fullscreen)
        if not self.fullscreen:
            try:
                width, height = self._parse_resolution(resolution)
                self.game.screen = pygame.display.set_mode((width, height))
                print(f"Window resized to: {width}x{height}")
            except Exception as e:
                print(f"Error changing resolution: {e}")

    def _on_battle_animations_toggle(self, enabled: bool):
        """Handle battle animations toggle."""
        print(f"Battle Animations: {'Enabled' if enabled else 'Disabled'}")
        self.battle_animations = enabled

    def _on_auto_save_toggle(self, enabled: bool):
        """Handle auto-save toggle."""
        print(f"Auto-Save: {'Enabled' if enabled else 'Disabled'}")
        self.auto_save = enabled

    def _on_difficulty_change(self, difficulty: str):
        """Handle difficulty change."""
        print(f"Difficulty changed to: {difficulty}")
        self.difficulty = difficulty

    def _parse_resolution(self, resolution: str) -> tuple:
        """
        Parse resolution string to width and height.

        Args:
            resolution: Resolution string (e.g., "1920x1080")

        Returns:
            Tuple of (width, height)
        """
        try:
            width, height = resolution.split('x')
            return (int(width), int(height))
        except (ValueError, AttributeError):
            # Fallback to default if parsing fails
            return (SCREEN_WIDTH, SCREEN_HEIGHT)

    def _on_back(self):
        """Return to main menu."""
        # Save all settings
        settings = {
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
            "text_speed": self.text_speed,
            "fullscreen": self.fullscreen,
            "resolution": self.resolution,
            "battle_animations": self.battle_animations,
            "auto_save": self.auto_save,
            "difficulty": self.difficulty
        }

        self.settings_manager.save(settings)

        print("Settings: Returning to main menu")
        print(f"Final settings:")
        print(f"  Music: {int(self.music_volume * 100)}%")
        print(f"  SFX: {int(self.sfx_volume * 100)}%")
        print(f"  Text Speed: {int(self.text_speed * 100)}%")
        print(f"  Fullscreen: {self.fullscreen}")
        print(f"  Resolution: {self.resolution}")
        print(f"  Battle Animations: {self.battle_animations}")
        print(f"  Auto-Save: {self.auto_save}")
        print(f"  Difficulty: {self.difficulty}")

        # Apply music volume
        try:
            pygame.mixer.music.set_volume(self.music_volume)
        except Exception as e:
            print(f"Could not set music volume: {e}")

        self.state_manager.change_state(STATE_MENU)

    def handle_event(self, event: pygame.event.Event):
        """Handle input events."""
        # ESC to go back
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._on_back()
                return

        # Handle tab buttons
        for tab_button in self.tab_buttons.values():
            tab_button.handle_event(event)

        # Handle settings based on active tab
        if self.active_tab == "Audio":
            # Audio sliders
            if self.music_slider.handle_event(event):
                self.music_volume = self.music_slider.value
                print(f"Music volume: {int(self.music_volume * 100)}%")

            if self.sfx_slider.handle_event(event):
                self.sfx_volume = self.sfx_slider.value
                print(f"SFX volume: {int(self.sfx_volume * 100)}%")

        elif self.active_tab == "Video":
            # Video settings
            if self.fullscreen_toggle:
                self.fullscreen_toggle.handle_event(event)

            if self.resolution_cycle:
                self.resolution_cycle.handle_event(event)

        elif self.active_tab == "Gameplay":
            # Gameplay settings
            if self.text_speed_slider.handle_event(event):
                self.text_speed = self.text_speed_slider.value
                print(f"Text speed: {int(self.text_speed * 100)}%")

            if self.battle_animations_toggle:
                self.battle_animations_toggle.handle_event(event)

            if self.auto_save_toggle:
                self.auto_save_toggle.handle_event(event)

            if self.difficulty_cycle:
                self.difficulty_cycle.handle_event(event)

        # Handle back button (always active)
        if self.back_button:
            self.back_button.handle_event(event)

    def update(self, dt: float):
        """Update state."""
        # Update tab buttons
        for tab_button in self.tab_buttons.values():
            tab_button.update(dt)

        # Update settings based on active tab
        if self.active_tab == "Video":
            if self.fullscreen_toggle:
                self.fullscreen_toggle.update(dt)

            if self.resolution_cycle:
                self.resolution_cycle.update(dt)

        elif self.active_tab == "Gameplay":
            if self.battle_animations_toggle:
                self.battle_animations_toggle.update(dt)

            if self.auto_save_toggle:
                self.auto_save_toggle.update(dt)

            if self.difficulty_cycle:
                self.difficulty_cycle.update(dt)

        # Always update back button
        if self.back_button:
            self.back_button.update(dt)

    def render(self, screen: pygame.Surface):
        """Render settings menu."""
        screen.fill(BLACK)

        # Draw title
        if self.title_text:
            self.title_text.render(screen)

        # Draw tab buttons with active indicator
        for tab_name, tab_button in self.tab_buttons.items():
            # Highlight active tab
            if tab_name == self.active_tab:
                # Draw golden highlight border around active tab
                highlight_rect = pygame.Rect(
                    tab_button.rect.x - 3,
                    tab_button.rect.y - 3,
                    tab_button.rect.width + 6,
                    tab_button.rect.height + 6
                )
                pygame.draw.rect(screen, UI_HIGHLIGHT_COLOR, highlight_rect, 3)

            tab_button.render(screen)

        # Render settings based on active tab
        if self.active_tab == "Audio":
            # Audio settings
            if self.music_slider:
                self.music_slider.render(screen)
            if self.sfx_slider:
                self.sfx_slider.render(screen)

        elif self.active_tab == "Video":
            # Video settings
            if self.fullscreen_toggle:
                self.fullscreen_toggle.render(screen)
            if self.resolution_cycle:
                self.resolution_cycle.render(screen)

        elif self.active_tab == "Gameplay":
            # Gameplay settings
            if self.text_speed_slider:
                self.text_speed_slider.render(screen)
            if self.battle_animations_toggle:
                self.battle_animations_toggle.render(screen)
            if self.auto_save_toggle:
                self.auto_save_toggle.render(screen)
            if self.difficulty_cycle:
                self.difficulty_cycle.render(screen)

        # Draw back button (always visible)
        if self.back_button:
            self.back_button.render(screen)

        # Draw instructions
        inst_font = pygame.font.Font(None, 20)
        instructions = "Use mouse to adjust settings • ESC or Back button to return to menu"
        text_surface = inst_font.render(instructions, True, (150, 150, 150))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(text_surface, text_rect)

    def startup(self, persistent):
        """Called when state becomes active."""
        print("Settings menu loaded")

    def cleanup(self):
        """Called when leaving state."""
        print("Settings menu cleanup")
        return {}
