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
from world.island import IslandManager
from world.island_factory import IslandFactory
from systems.party_manager import PartyManager
from systems.equipment_manager import EquipmentManager
from ui.party_menu import PartyMenu
from ui.inventory_menu import InventoryMenu
from ui.equipment_menu import EquipmentMenu
from ui.travel_menu import TravelMenu
from ui.button import Button
from utils.party_helpers import create_starter_crew
from utils.item_helpers import add_starter_items
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
        self.island_manager: Optional[IslandManager] = None
        
        # State
        self.paused = False
        self.ready_for_battle = False
        self.battle_triggered = False
        
        # UI
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)

        # Party menu
        self.party_menu = PartyMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.party_menu.on_close = self._on_party_menu_close

        # Inventory menu
        self.inventory_menu = InventoryMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.inventory_menu.on_close = self._on_inventory_menu_close
        self.inventory_menu.on_equipment_changed = self._on_equipment_changed

        # Equipment menu
        self.equipment_menu = EquipmentMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.equipment_menu.on_close = self._on_equipment_menu_close
        self.equipment_menu.on_equip_requested = self._on_equip_requested_from_equipment

        # Travel menu
        self.travel_menu = TravelMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.travel_menu.on_travel = self._on_travel_selected
        self.travel_menu.on_close = self._on_travel_menu_close

        # Pause menu buttons
        button_width = 300
        button_height = 50
        button_spacing = 20
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = SCREEN_HEIGHT // 2 - 50

        self.pause_resume_button = Button(
            x=center_x,
            y=start_y,
            width=button_width,
            height=button_height,
            text="Resume",
            callback=self._on_resume
        )

        self.pause_menu_button = Button(
            x=center_x,
            y=start_y + button_height + button_spacing,
            width=button_width,
            height=button_height,
            text="Back to Main Menu",
            callback=self._on_back_to_menu
        )

        # Debug
        self.show_debug = True
    
    def startup(self, persistent):
        """
        Called when state becomes active.

        Args:
            persistent: Data from previous state
        """
        print("\n" + "="*60)
        print("WORLD STATE STARTUP - Initializing game world")
        print("="*60)
        print(f"Received persistent data keys: {list(persistent.keys())}")

        # Get player from persistent data or create new
        if "player" in persistent:
            player = persistent["player"]
            print(f"✓ Using player from character creation: {player.name}")
            print(f"   Level: {player.level}")
            print(f"   Devil Fruit: {player.devil_fruit.name if player.devil_fruit else 'None'}")
        else:
            print("⚠ No player in persistent data - creating test player")
            # Create test player
            player = Player("Alex")
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
        
        # Initialize island manager
        if not hasattr(self, 'island_manager') or self.island_manager is None:
            self.island_manager = IslandManager()

            # Register all East Blue islands
            print("\nInitializing East Blue islands...")
            for island in IslandFactory.create_all_islands():
                self.island_manager.register_island(island)

            # Start at Foosha Village
            self.island_manager.set_current_island("foosha_village")
            print(f"Starting location: {self.island_manager.get_current_island().name}\n")

        # Get current map from island
        current_island = self.island_manager.get_current_island()
        if current_island:
            self.current_map = current_island.map
        else:
            # Fallback to test map if no island
            self.current_map = Map.create_test_map()
        
        # Initialize party manager if not already set
        if not hasattr(player, 'party_manager') or player.party_manager is None:
            player.party_manager = PartyManager(player)
            print(f"Initialized party manager for {player.name}")
            print(f"Starting solo - no party members added")

            # Add starter items for testing/demo
            print("\nAdding starter items...")
            add_starter_items(player.inventory)

        # Set party menu's party manager
        self.party_menu.set_party_manager(player.party_manager)

        # Initialize equipment slots for all party members
        equipment_manager = EquipmentManager()
        equipment_manager.get_or_create_slots(player)
        for member in player.party_manager.get_all_members():
            equipment_manager.get_or_create_slots(member)

        # Set inventory and equipment menus
        self.inventory_menu.set_inventory(player.inventory, player)
        self.equipment_menu.set_character(player, player.inventory)

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

        print(f"\n✓ World State: Loaded map '{self.current_map.name}'")
        print(f"✓ World State: Player at {self.player_controller.get_tile_position()}")
        print(f"✓ World State: Camera centered on player")
        print("="*60)
        print("✅ WORLD STATE INITIALIZATION COMPLETE")
        print("="*60 + "\n")
    
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
        # Menus get priority (check in order)
        if self.party_menu.visible:
            self.party_menu.handle_event(event)
            return

        if self.inventory_menu.visible:
            self.inventory_menu.handle_event(event)
            return

        if self.equipment_menu.visible:
            self.equipment_menu.handle_event(event)
            return

        if self.travel_menu.visible:
            self.travel_menu.handle_event(event)
            return

        if event.type == pygame.KEYDOWN:
            # Debug toggle
            if event.key == pygame.K_F3:
                self.show_debug = not self.show_debug

            # Party menu (P key)
            elif event.key == pygame.K_p:
                self.party_menu.show()
                print("Party menu opened!")

            # Inventory menu (I key)
            elif event.key == pygame.K_i:
                self.inventory_menu.show()
                print("Inventory menu opened!")

            # Equipment menu (E key)
            elif event.key == pygame.K_e:
                self.equipment_menu.show()
                print("Equipment menu opened!")

            # Travel menu (T key)
            elif event.key == pygame.K_t:
                if self.island_manager and self.player_controller:
                    current_island = self.island_manager.get_current_island()
                    available = self.island_manager.get_available_islands()
                    connections = current_island.connections if current_island else []
                    self.travel_menu.set_destinations(
                        current_island,
                        available,
                        connections,
                        self.player_controller.player.berries
                    )
                    self.travel_menu.show()
                    print("Travel menu opened!")

            # Pause (ESC)
            elif event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
                print(f"Game {'paused' if self.paused else 'unpaused'}")

            # Manual battle trigger (for testing)
            elif event.key == pygame.K_b:
                print("Manual battle trigger!")
                self.battle_triggered = True

        # Handle pause menu buttons when paused
        if self.paused:
            self.pause_resume_button.handle_event(event)
            self.pause_menu_button.handle_event(event)
        else:
            # Pass input to player controller only when not paused
            self.player_controller.handle_event(event)
    
    def update(self, dt):
        """
        Update world state.

        Args:
            dt: Delta time in seconds
        """
        if self.paused:
            # Update pause menu buttons
            self.pause_resume_button.update(dt)
            self.pause_menu_button.update(dt)
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

        # Render menus (on top of everything)
        self.party_menu.render(surface)
        self.inventory_menu.render(surface)
        self.equipment_menu.render(surface)
        self.travel_menu.render(surface)
    
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
        controls = "WASD: Move | P: Party | I: Inv | E: Equip | T: Travel | B: Battle | ESC: Pause | F3: Debug"
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

        # Render pause menu buttons
        self.pause_resume_button.render(surface)
        self.pause_menu_button.render(surface)

    def _on_resume(self):
        """Resume game from pause menu."""
        self.paused = False
        print("Game resumed")

    def _on_back_to_menu(self):
        """Return to main menu from pause menu."""
        print("Returning to main menu...")
        self.paused = False
        self.state_manager.change_state(STATE_MENU)

    def _on_party_menu_close(self):
        """Callback when party menu is closed."""
        print("Party menu closed")

    def _on_inventory_menu_close(self):
        """Callback when inventory menu is closed."""
        print("Inventory menu closed")

    def _on_equipment_changed(self):
        """Callback when equipment is equipped/unequipped."""
        # Refresh equipment menu display
        if hasattr(self, 'player_controller') and self.player_controller:
            player = self.player_controller.player
            self.equipment_menu.set_character(player, player.inventory)
            print("Equipment menu refreshed")

    def _on_equipment_menu_close(self):
        """Callback when equipment menu is closed."""
        print("Equipment menu closed")

    def _on_equip_requested_from_equipment(self):
        """Callback when user clicks Equip button in equipment menu."""
        # Hide equipment menu
        self.equipment_menu.hide()
        # Open inventory menu
        self.inventory_menu.show()
        print("Opened inventory to select equipment")

    def _on_travel_menu_close(self):
        """Callback when travel menu is closed."""
        print("Travel menu closed")

    def _on_travel_selected(self, destination_id: str):
        """Handle island travel."""
        if self.island_manager and self.player_controller:
            player = self.player_controller.player

            # Get travel cost
            current_island = self.island_manager.get_current_island()
            if current_island:
                for conn in current_island.connections:
                    if conn.destination_island == destination_id:
                        # Check if can afford
                        if player.berries >= conn.berries_cost:
                            # Deduct cost
                            player.berries -= conn.berries_cost

                            # Travel to island
                            if self.island_manager.travel_to_island(destination_id):
                                # Update map
                                new_island = self.island_manager.get_current_island()
                                self.current_map = new_island.map

                                # Move player to spawn point
                                spawn_x, spawn_y = new_island.map.spawn_point
                                self.player_controller.set_position(spawn_x * 64, spawn_y * 64)

                                # Close menu
                                self.travel_menu.hide()
                                print(f"Traveled to {new_island.name}!")
                            else:
                                print("Travel failed!")
                        else:
                            print("Not enough berries!")
                        break
