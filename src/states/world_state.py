"""
World State
Game state for overworld exploration.
"""

import pygame
from typing import Optional
from states.state import State
from entities.player import Player
from world.map import Map
from world.camera import Camera
from world.player_controller import PlayerController
from utils.constants import *


class WorldState(State):
    """
    Game state for world exploration.
    Handles player movement, map rendering, and encounters.
    """
    
    def __init__(self, game):
        """
        Initialize world state.
        
        Args:
            game: Main game instance
        """
        super().__init__(game)
        
        # World components
        self.current_map: Optional[Map] = None
        self.camera: Optional[Camera] = None
        self.player_controller: Optional[PlayerController] = None
        
        # State
        self.paused = False
        self.ready_for_battle = False
        self.battle_triggered = False
        
        # UI
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        
        # Debug
        self.show_debug = True
    
    def startup(self, persistent):
        """
        Called when state becomes active.
        
        Args:
            persistent: Data from previous state
        """
        print("World State: Starting up...")
        
        # Get player from persistent data or create new
        if "player" in persistent:
            player = persistent["player"]
        else:
            # Create test player
            player = Player("Luffy")
            player.level = 5
            player.max_hp = 150
            player.current_hp = 150
            player.base_attack = 20
            player.base_defense = 15
            player.base_speed = 18
            
            # Add Devil Fruit for testing
            player.devil_fruit = {
                "id": "gomu_gomu",
                "name": "Gomu Gomu no Mi",
                "type": "paramecia"
            }
            player.max_ap = 50
            player.current_ap = 50
        
        # Load or create map
        if "current_map" in persistent:
            self.current_map = persistent["current_map"]
        else:
            # Create test map
            self.current_map = Map.create_test_map()
        
        # Create player controller
        self.player_controller = PlayerController(player, self.current_map)
        
        # Create camera
        map_width, map_height = self.current_map.get_world_size()
        self.camera = Camera(map_width, map_height)
        
        # Center camera on player
        player_x, player_y = self.player_controller.get_center_position()
        self.camera.center_on(player_x, player_y)
        
        # Reset flags
        self.paused = False
        self.battle_triggered = False
        
        print(f"World State: Loaded map '{self.current_map.name}'")
        print(f"World State: Player at {self.player_controller.get_tile_position()}")
    
    def cleanup(self):
        """
        Called when leaving state.
        
        Returns:
            Persistent data dictionary
        """
        return {
            "player": self.player_controller.player,
            "current_map": self.current_map,
            "player_position": self.player_controller.get_position()
        }
    
    def handle_event(self, event):
        """
        Handle pygame events.
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            # Debug toggle
            if event.key == pygame.K_F3:
                self.show_debug = not self.show_debug
            
            # Pause (ESC)
            elif event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
                print(f"Game {'paused' if self.paused else 'unpaused'}")
            
            # Manual battle trigger (for testing)
            elif event.key == pygame.K_b:
                print("Manual battle trigger!")
                self.battle_triggered = True
        
        # Pass input to player controller
        if not self.paused:
            self.player_controller.handle_event(event)
    
    def update(self, dt):
        """
        Update world state.
        
        Args:
            dt: Delta time in seconds
        """
        if self.paused:
            return
        
        # Update player
        event = self.player_controller.update(dt)
        
        # Check for encounters
        if event == "encounter":
            print("Random encounter triggered!")
            self.battle_triggered = True
        
        # Update camera to follow player
        player_x, player_y = self.player_controller.get_center_position()
        self.camera.center_on(player_x, player_y)
        self.camera.update(dt)
        
        # Update player playtime
        self.player_controller.player.update_playtime(dt)
        
        # Check if should transition to battle
        if self.battle_triggered:
            self._prepare_battle()
    
    def _prepare_battle(self):
        """Prepare to transition to battle state."""
        print("Preparing for battle...")
        
        # Mark state as done
        self.done = True
        self.next_state = "battle"
        
        # Persistent data for battle state
        # Battle state will use this to set up the encounter
        self.persist = {
            "player": self.player_controller.player,
            "current_map": self.current_map,
            "player_position": self.player_controller.get_position(),
            "return_to_world": True
        }
    
    def render(self, surface):
        """
        Render world state.
        
        Args:
            surface: Surface to draw on
        """
        # Clear screen
        surface.fill(BLACK)
        
        # Get camera offset
        camera_x, camera_y = self.camera.get_offset()
        
        # Render map
        self.current_map.render(surface, camera_x, camera_y)
        
        # Render player
        self.player_controller.render(surface, camera_x, camera_y)
        
        # Render UI
        self._render_ui(surface)
        
        # Render pause overlay
        if self.paused:
            self._render_pause_overlay(surface)
    
    def _render_ui(self, surface: pygame.Surface):
        """Render UI elements."""
        # Player info (top-left)
        player = self.player_controller.player
        
        # Background panel
        panel_rect = pygame.Rect(10, 10, 300, 120)
        pygame.draw.rect(surface, UI_BG_COLOR, panel_rect)
        pygame.draw.rect(surface, UI_BORDER_COLOR, panel_rect, 2)
        
        # Player name
        name_text = self.font.render(f"{player.name} - Lv.{player.level}", True, WHITE)
        surface.blit(name_text, (20, 20))
        
        # HP bar
        hp_text = self.small_font.render("HP:", True, WHITE)
        surface.blit(hp_text, (20, 50))
        
        hp_bar_rect = pygame.Rect(60, 50, 200, 20)
        pygame.draw.rect(surface, DARK_GRAY, hp_bar_rect)
        
        hp_percent = player.current_hp / player.max_hp if player.max_hp > 0 else 0
        hp_fill_width = int(200 * hp_percent)
        if hp_fill_width > 0:
            hp_color = GREEN if hp_percent > 0.5 else (YELLOW if hp_percent > 0.25 else RED)
            hp_fill_rect = pygame.Rect(60, 50, hp_fill_width, 20)
            pygame.draw.rect(surface, hp_color, hp_fill_rect)
        
        pygame.draw.rect(surface, WHITE, hp_bar_rect, 1)
        
        hp_value_text = self.small_font.render(f"{player.current_hp}/{player.max_hp}", True, WHITE)
        surface.blit(hp_value_text, (hp_bar_rect.centerx - hp_value_text.get_width() // 2, 52))
        
        # Berries
        berries_text = self.small_font.render(f"Berries: {player.berries:,}", True, YELLOW)
        surface.blit(berries_text, (20, 80))
        
        # Location
        location_text = self.small_font.render(f"Location: {self.current_map.name}", True, LIGHT_GRAY)
        surface.blit(location_text, (20, 105))
        
        # Controls hint (bottom-center)
        controls = "WASD/Arrows: Move | ESC: Pause | B: Battle (test) | F3: Debug"
        controls_text = self.small_font.render(controls, True, LIGHT_GRAY)
        controls_x = (SCREEN_WIDTH - controls_text.get_width()) // 2
        surface.blit(controls_text, (controls_x, SCREEN_HEIGHT - 30))
        
        # Debug info
        if self.show_debug:
            self._render_debug_info(surface)
    
    def _render_debug_info(self, surface: pygame.Surface):
        """Render debug information."""
        debug_y = 150
        debug_lines = [
            f"FPS: {int(self.game.clock.get_fps())}",
            f"Player Pos: {self.player_controller.get_position()}",
            f"Tile Pos: {self.player_controller.get_tile_position()}",
            f"Camera: {self.camera.get_offset()}",
            f"Moving: {self.player_controller.moving}",
            f"Facing: {self.player_controller.facing}",
            f"Steps: {self.player_controller.steps_since_last_encounter}"
        ]
        
        for i, line in enumerate(debug_lines):
            debug_text = self.small_font.render(line, True, CYAN)
            surface.blit(debug_text, (SCREEN_WIDTH - 250, debug_y + i * 25))
    
    def _render_pause_overlay(self, surface: pygame.Surface):
        """Render pause screen overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        # Pause text
        pause_font = pygame.font.Font(None, 80)
        pause_text = pause_font.render("PAUSED", True, WHITE)
        pause_x = (SCREEN_WIDTH - pause_text.get_width()) // 2
        pause_y = SCREEN_HEIGHT // 3
        surface.blit(pause_text, (pause_x, pause_y))
        
        # Resume instruction
        resume_text = self.font.render("Press ESC to resume", True, LIGHT_GRAY)
        resume_x = (SCREEN_WIDTH - resume_text.get_width()) // 2
        resume_y = pause_y + 100
        surface.blit(resume_text, (resume_x, resume_y))
