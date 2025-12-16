"""Test settings state rendering"""
import pygame
import sys
import os

sys.path.insert(0, 'src')

from states.settings_state import SettingsState
from states.state_manager import StateManager

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Create a mock game object
class MockGame:
    def __init__(self):
        self.screen = screen
        self.running = True

game = MockGame()

# Create state manager and settings state
state_manager = StateManager(game)
settings_state = SettingsState(game)
settings_state.state_manager = state_manager

# Set up the state
settings_state.startup({})

print("Settings state created and started")
print(f"Title text: {settings_state.title_text}")
print(f"Music slider: {settings_state.music_slider}")
print(f"Back button: {settings_state.back_button}")

# Try rendering
running = True
frames = 0
while running and frames < 60:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Update
    settings_state.update(0.016)

    # Render
    try:
        settings_state.render(screen)
        pygame.display.flip()
        frames += 1
    except Exception as e:
        print(f"Error rendering: {e}")
        import traceback
        traceback.print_exc()
        break

    clock.tick(60)

print(f"Rendered {frames} frames successfully")
pygame.quit()
