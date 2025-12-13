"""
Settings State
Basic settings menu with TODO for bug fixes.
"""

import pygame
from states.state import State
from ui.button import Button
from ui.text_box import CenteredText
from utils.constants import *


class SettingsState(State):
    """
    Settings menu (simplified version with known bugs).

    TODO: Fix settings bugs:
    - Button states not updating properly
    - Volume changes not persisting
    - Fullscreen toggle needs work
    """

    def __init__(self, game):
        super().__init__(game)

        self.title_text = None
        self.back_button = None
        self._setup_ui()

    def _setup_ui(self):
        """Set up UI elements."""
        # Title
        self.title_text = CenteredText(
            x=SCREEN_WIDTH // 2,
            y=100,
            text="Settings",
            font_size=64,
            color=WHITE,
            centered=True
        )

        # Back button
        self.back_button = Button(
            x=SCREEN_WIDTH // 2 - 100,
            y=SCREEN_HEIGHT - 100,
            width=200,
            height=50,
            text="Back to Menu",
            callback=self._on_back
        )

    def _on_back(self):
        """Return to main menu."""
        print("Settings: Returning to main menu")
        self.state_manager.change_state(STATE_MENU)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._on_back()

        if self.back_button:
            self.back_button.handle_event(event)

    def update(self, dt: float):
        if self.back_button:
            self.back_button.update(dt)

    def render(self, screen: pygame.Surface):
        screen.fill(BLACK)

        # Draw title
        if self.title_text:
            self.title_text.render(screen)

        # Draw placeholder text
        font = pygame.font.Font(None, 36)
        text = "Settings menu - TODO: Implement full features"
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surface, text_rect)

        # Draw note about bugs
        bug_font = pygame.font.Font(None, 28)
        bug_text = "Note: Settings has known bugs - marked with TODO in code"
        bug_surface = bug_font.render(bug_text, True, (255, 200, 0))
        bug_rect = bug_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(bug_surface, bug_rect)

        # Draw back button
        if self.back_button:
            self.back_button.render(screen)

    def startup(self, persistent):
        print("Settings menu loaded (with known bugs - see TODO)")

    def cleanup(self):
        print("Settings menu cleanup")
        return {}
