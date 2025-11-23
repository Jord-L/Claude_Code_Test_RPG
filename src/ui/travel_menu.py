"""
Island Travel Menu
UI for traveling between islands via ship.
"""

import pygame
from typing import Optional, Callable, List
from world.island import Island, IslandConnection
from ui.panel import Panel
from ui.button import Button
from utils.constants import *


class IslandCard:
    """Visual card for an island destination."""

    def __init__(self, x: int, y: int, width: int, height: int):
        """Initialize island card."""
        self.rect = pygame.Rect(x, y, width, height)
        self.island: Optional[Island] = None
        self.connection: Optional[IslandConnection] = None
        self.is_selected = False
        self.is_hovered = False

        # Colors
        self.bg_color = DARK_GRAY
        self.selected_color = UI_HIGHLIGHT_COLOR
        self.hover_color = LIGHT_GRAY
        self.locked_color = (60, 40, 40)

        # Fonts
        self.title_font = pygame.font.Font(None, 24)
        self.text_font = pygame.font.Font(None, 18)

    def set_island(self, island: Island, connection: IslandConnection):
        """Set island to display."""
        self.island = island
        self.connection = connection

    def set_selected(self, selected: bool):
        """Set selection state."""
        self.is_selected = selected

    def set_hovered(self, hovered: bool):
        """Set hover state."""
        self.is_hovered = hovered

    def contains_point(self, x: int, y: int) -> bool:
        """Check if point is within card."""
        return self.rect.collidepoint(x, y)

    def render(self, surface: pygame.Surface):
        """Render the island card."""
        if not self.island:
            return

        # Determine background color
        if self.is_selected:
            bg = self.selected_color
        elif self.is_hovered:
            bg = self.hover_color
        else:
            bg = self.bg_color

        # Draw background
        pygame.draw.rect(surface, bg, self.rect)

        # Draw island name
        name_text = self.title_font.render(self.island.name, True, WHITE)
        name_x = self.rect.x + 10
        name_y = self.rect.y + 10
        surface.blit(name_text, (name_x, name_y))

        # Draw recommended level
        level_text = f"Lv. {self.island.recommended_level}"
        level_surface = self.text_font.render(level_text, True, YELLOW)
        surface.blit(level_surface, (name_x, name_y + 30))

        # Draw travel cost
        cost_text = f"Cost: {self.connection.berries_cost:,} ฿"
        cost_surface = self.text_font.render(cost_text, True, GREEN if self.connection.berries_cost == 0 else WHITE)
        surface.blit(cost_surface, (name_x, name_y + 50))

        # Draw visited indicator
        if self.island.visited:
            visited_text = self.text_font.render("✓ Visited", True, CYAN)
            surface.blit(visited_text, (name_x, name_y + 70))

        # Draw border
        border_width = 3 if self.is_selected else 1
        pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, border_width)


class TravelMenu:
    """
    Menu for traveling between islands.
    Shows available destinations and handles ship travel.
    """

    def __init__(self, screen_width: int, screen_height: int):
        """Initialize travel menu."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.visible = False

        # Layout
        self.panel_width = 700
        self.panel_height = 600
        self.panel_x = (screen_width - self.panel_width) // 2
        self.panel_y = (screen_height - self.panel_height) // 2

        # Panel
        self.panel = Panel(self.panel_x, self.panel_y, self.panel_width, self.panel_height)

        # Island cards
        self.island_cards: List[IslandCard] = []
        self.available_islands: List[Island] = []
        self.selected_index = 0

        # Callbacks
        self.on_travel: Optional[Callable[[str], None]] = None
        self.on_close: Optional[Callable[[], None]] = None

        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        self.info_font = pygame.font.Font(None, 20)

        # Current island info
        self.current_island: Optional[Island] = None
        self.player_berries = 0

        # Buttons
        self._create_buttons()

    def _create_buttons(self):
        """Create menu buttons."""
        button_y = self.panel_y + self.panel_height - 60

        self.travel_button = Button(
            self.panel_x + 20,
            button_y,
            120, 40,
            "Set Sail"
        )
        self.travel_button.set_enabled(False)

        self.close_button = Button(
            self.panel_x + self.panel_width - 120,
            button_y,
            100, 40,
            "Close"
        )

    def set_destinations(self, current_island: Island, available: List[Island],
                        connections: List[IslandConnection], player_berries: int):
        """
        Set available destinations.

        Args:
            current_island: Current island
            available: List of available destination islands
            connections: Island connections
            player_berries: Player's current berries
        """
        self.current_island = current_island
        self.available_islands = available
        self.player_berries = player_berries

        # Create island cards
        self._create_island_cards(connections)

        # Reset selection
        self.selected_index = 0 if self.island_cards else -1
        self._update_selection()

    def _create_island_cards(self, connections: List[IslandConnection]):
        """Create visual island cards."""
        self.island_cards.clear()

        card_width = 320
        card_height = 100
        cards_per_row = 2
        spacing = 10

        start_x = self.panel_x + 20
        start_y = self.panel_y + 80

        for i, island in enumerate(self.available_islands):
            row = i // cards_per_row
            col = i % cards_per_row

            x = start_x + col * (card_width + spacing)
            y = start_y + row * (card_height + spacing)

            card = IslandCard(x, y, card_width, card_height)

            # Find connection for this island
            connection = None
            for conn in connections:
                if conn.destination_island == island.island_id:
                    connection = conn
                    break

            if connection:
                card.set_island(island, connection)
                self.island_cards.append(card)

    def show(self):
        """Show the menu."""
        self.visible = True

    def hide(self):
        """Hide the menu."""
        self.visible = False

    def handle_event(self, event: pygame.event.Event):
        """Handle input events."""
        if not self.visible:
            return

        if event.type == pygame.KEYDOWN:
            # Navigate with arrow keys
            if event.key == pygame.K_UP:
                if self.selected_index >= 2:
                    self.selected_index -= 2
                    self._update_selection()

            elif event.key == pygame.K_DOWN:
                if self.selected_index + 2 < len(self.island_cards):
                    self.selected_index += 2
                    self._update_selection()

            elif event.key == pygame.K_LEFT:
                if self.selected_index > 0:
                    self.selected_index -= 1
                    self._update_selection()

            elif event.key == pygame.K_RIGHT:
                if self.selected_index < len(self.island_cards) - 1:
                    self.selected_index += 1
                    self._update_selection()

            # Confirm with Enter
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.travel_button.is_enabled:
                    self._travel_to_selected()

            # Close with Escape
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_t:
                self.hide()
                if self.on_close:
                    self.on_close()

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos

            # Update hover state
            new_hovered = -1
            for i, card in enumerate(self.island_cards):
                if card.contains_point(mouse_x, mouse_y):
                    new_hovered = i
                    card.set_hovered(True)
                else:
                    card.set_hovered(False)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Check buttons
            if self.close_button.contains_point(mouse_x, mouse_y):
                self.hide()
                if self.on_close:
                    self.on_close()
                return

            if self.travel_button.is_enabled and self.travel_button.contains_point(mouse_x, mouse_y):
                self._travel_to_selected()
                return

            # Check island cards
            for i, card in enumerate(self.island_cards):
                if card.contains_point(mouse_x, mouse_y):
                    self.selected_index = i
                    self._update_selection()
                    break

    def _update_selection(self):
        """Update visual selection state."""
        for i, card in enumerate(self.island_cards):
            card.set_selected(i == self.selected_index)

        # Update travel button state
        if 0 <= self.selected_index < len(self.island_cards):
            card = self.island_cards[self.selected_index]
            can_afford = self.player_berries >= card.connection.berries_cost
            self.travel_button.set_enabled(can_afford)
        else:
            self.travel_button.set_enabled(False)

    def _travel_to_selected(self):
        """Travel to selected island."""
        if 0 <= self.selected_index < len(self.island_cards):
            card = self.island_cards[self.selected_index]
            if card.island and self.on_travel:
                self.on_travel(card.island.island_id)

    def update(self, dt: float):
        """Update menu state."""
        pass

    def render(self, surface: pygame.Surface):
        """Render the menu."""
        if not self.visible:
            return

        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        # Draw panel
        self.panel.render(surface)

        # Draw title
        title_text = self.title_font.render("Set Sail", True, WHITE)
        title_x = self.panel_x + (self.panel_width - title_text.get_width()) // 2
        surface.blit(title_text, (title_x, self.panel_y + 15))

        # Draw current location
        if self.current_island:
            location_text = f"Current: {self.current_island.name}"
            location_surface = self.info_font.render(location_text, True, CYAN)
            surface.blit(location_surface, (self.panel_x + 20, self.panel_y + 55))

        # Draw berries
        berries_text = f"Berries: {self.player_berries:,} ฿"
        berries_surface = self.info_font.render(berries_text, True, YELLOW)
        berries_x = self.panel_x + self.panel_width - berries_surface.get_width() - 20
        surface.blit(berries_surface, (berries_x, self.panel_y + 55))

        # Draw island cards
        for card in self.island_cards:
            card.render(surface)

        # Draw selected island description
        if 0 <= self.selected_index < len(self.island_cards):
            card = self.island_cards[self.selected_index]
            if card.island:
                desc_y = self.panel_y + self.panel_height - 120
                desc_text = card.island.description
                desc_surface = self.info_font.render(desc_text, True, LIGHT_GRAY)
                surface.blit(desc_surface, (self.panel_x + 20, desc_y))

        # Draw buttons
        self.travel_button.render(surface)
        self.close_button.render(surface)

        # Draw controls hint
        controls_text = "Arrow Keys: Navigate | Enter: Travel | T/Esc: Close"
        controls_surface = self.info_font.render(controls_text, True, LIGHT_GRAY)
        controls_x = self.panel_x + (self.panel_width - controls_surface.get_width()) // 2
        surface.blit(controls_surface, (controls_x, self.panel_y + self.panel_height - 15))
