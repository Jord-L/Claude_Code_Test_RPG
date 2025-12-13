"""
Load Game State
Basic load game menu.
"""

import pygame
import os
from states.state import State
from ui.button import Button
from ui.text_box import CenteredText
from utils.constants import *


class LoadGameState(State):
    """
    Load game menu for selecting save files.
    """

    def __init__(self, game):
        super().__init__(game)

        self.title_text = None
        self.back_button = None
        self.save_dir = "saves"

        # Create saves directory if it doesn't exist
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        self._setup_ui()

    def _setup_ui(self):
        """Set up UI elements."""
        # Title
        self.title_text = CenteredText(
            x=SCREEN_WIDTH // 2,
            y=100,
            text="Load Game",
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
        print("Load Game: Returning to main menu")
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
        text = "No save files found"
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surface, text_rect)

        # Draw hint
        hint_font = pygame.font.Font(None, 28)
        hint_text = "Save functionality will be added later"
        hint_surface = hint_font.render(hint_text, True, (150, 150, 150))
        hint_rect = hint_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(hint_surface, hint_rect)

        # Draw back button
        if self.back_button:
            self.back_button.render(screen)

    def startup(self, persistent):
        print("Load Game menu loaded")

    def cleanup(self):
        print("Load Game menu cleanup")
        return {}
