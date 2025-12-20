"""
Party Menu UI
Interface for viewing and managing party members.
"""

import pygame
from typing import Optional, Callable, List
from entities.character import Character
from systems.party_manager import PartyManager, CrewMember
from ui.panel import Panel
from ui.button import Button
from utils.constants import *


class PartyMemberCard:
    """Visual card displaying a single party member's info."""

    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initialize party member card.

        Args:
            x: X position
            y: Y position
            width: Card width
            height: Card height
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.member: Optional[Character] = None
        self.is_selected = False
        self.is_active = True  # Active vs Reserve

        # Visual
        self.bg_color = UI_BG_COLOR
        self.selected_color = UI_HIGHLIGHT_COLOR
        self.border_color = UI_BORDER_COLOR
        self.text_color = WHITE

        # Fonts
        self.name_font = pygame.font.Font(None, 24)
        self.info_font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 18)

    def set_member(self, member: Optional[Character], is_active: bool = True):
        """
        Set the member to display.

        Args:
            member: Character to display
            is_active: Whether in active party
        """
        self.member = member
        self.is_active = is_active

    def set_selected(self, selected: bool):
        """Set selection state."""
        self.is_selected = selected

    def contains_point(self, x: int, y: int) -> bool:
        """Check if point is within card."""
        return self.rect.collidepoint(x, y)

    def render(self, surface: pygame.Surface):
        """Render the card."""
        if not self.member:
            # Draw empty slot
            pygame.draw.rect(surface, DARK_GRAY, self.rect)
            pygame.draw.rect(surface, self.border_color, self.rect, 1)

            text = self.info_font.render("Empty Slot", True, LIGHT_GRAY)
            text_x = self.rect.centerx - text.get_width() // 2
            text_y = self.rect.centery - text.get_height() // 2
            surface.blit(text, (text_x, text_y))
            return

        # Draw background
        bg_color = self.selected_color if self.is_selected else self.bg_color
        pygame.draw.rect(surface, bg_color, self.rect)

        # Draw border (thicker if selected)
        border_width = 3 if self.is_selected else 2
        pygame.draw.rect(surface, self.border_color, self.rect, border_width)

        # Draw member info
        padding = 10
        y_offset = self.rect.y + padding

        # Name and level
        name_text = f"{self.member.name} Lv.{self.member.level}"
        name_surface = self.name_font.render(name_text, True, self.text_color)
        surface.blit(name_surface, (self.rect.x + padding, y_offset))
        y_offset += 25

        # Role (if CrewMember)
        if isinstance(self.member, CrewMember):
            role_text = f"{self.member.role}"
            if self.member.epithet:
                role_text = f'"{self.member.epithet}" - {self.member.role}'
            role_surface = self.small_font.render(role_text, True, LIGHT_GRAY)
            surface.blit(role_surface, (self.rect.x + padding, y_offset))
            y_offset += 20

        # HP bar
        hp_percent = self.member.current_hp / self.member.max_hp if self.member.max_hp > 0 else 0
        bar_width = self.rect.width - (padding * 2)
        bar_height = 20

        hp_bar_rect = pygame.Rect(self.rect.x + padding, y_offset, bar_width, bar_height)
        pygame.draw.rect(surface, DARK_GRAY, hp_bar_rect)

        if hp_percent > 0:
            fill_width = int(bar_width * hp_percent)
            fill_rect = pygame.Rect(self.rect.x + padding, y_offset, fill_width, bar_height)

            if hp_percent > 0.5:
                hp_color = GREEN
            elif hp_percent > 0.25:
                hp_color = YELLOW
            else:
                hp_color = RED

            pygame.draw.rect(surface, hp_color, fill_rect)

        pygame.draw.rect(surface, self.border_color, hp_bar_rect, 1)

        # HP text
        hp_text = f"HP: {self.member.current_hp}/{self.member.max_hp}"
        hp_surface = self.small_font.render(hp_text, True, WHITE)
        hp_x = hp_bar_rect.centerx - hp_surface.get_width() // 2
        hp_y = hp_bar_rect.centery - hp_surface.get_height() // 2
        surface.blit(hp_surface, (hp_x, hp_y))
        y_offset += 25

        # Status indicator
        if not self.member.is_alive:
            status_text = "FALLEN"
            status_color = RED
        elif self.is_active:
            status_text = "ACTIVE"
            status_color = GREEN
        else:
            status_text = "RESERVE"
            status_color = CYAN

        status_surface = self.small_font.render(status_text, True, status_color)
        surface.blit(status_surface, (self.rect.x + padding, y_offset))


class PartyMenu:
    """
    Full party management menu.
    Shows active and reserve members, allows switching.
    """

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize party menu.

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.visible = False

        # Party manager reference
        self.party_manager: Optional[PartyManager] = None

        # Layout
        self.panel_width = 900
        self.panel_height = 650
        self.panel_x = (screen_width - self.panel_width) // 2
        self.panel_y = (screen_height - self.panel_height) // 2

        # Background panel
        self.panel = Panel(self.panel_x, self.panel_y, self.panel_width, self.panel_height)

        # Member cards
        self.active_cards: List[PartyMemberCard] = []
        self.reserve_cards: List[PartyMemberCard] = []
        self._create_member_cards()

        # Selection
        self.selected_card: Optional[PartyMemberCard] = None
        self.selected_for_swap: Optional[PartyMemberCard] = None

        # Buttons
        self.close_button = Button(
            self.panel_x + self.panel_width - 120,
            self.panel_y + self.panel_height - 60,
            100, 40, "Close"
        )

        self.swap_button = Button(
            self.panel_x + 20,
            self.panel_y + self.panel_height - 60,
            100, 40, "Swap"
        )
        self.swap_button.set_enabled(False)

        # Callbacks
        self.on_close: Optional[Callable] = None

        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        self.section_font = pygame.font.Font(None, 28)
        self.info_font = pygame.font.Font(None, 22)

    def _create_member_cards(self):
        """Create member card slots."""
        card_width = 200
        card_height = 140
        card_spacing = 10
        start_x = self.panel_x + 20
        start_y = self.panel_y + 80

        # Active party cards (4 slots)
        for i in range(4):
            x = start_x + (i % 2) * (card_width + card_spacing)
            y = start_y + (i // 2) * (card_height + card_spacing)
            card = PartyMemberCard(x, y, card_width, card_height)
            self.active_cards.append(card)

        # Reserve party cards (6 slots)
        reserve_start_y = start_y + 320
        for i in range(6):
            x = start_x + (i % 3) * (card_width + card_spacing)
            y = reserve_start_y + (i // 3) * (card_height + card_spacing)
            card = PartyMemberCard(x, y, card_width, card_height)
            card.is_active = False
            self.reserve_cards.append(card)

    def set_party_manager(self, party_manager: PartyManager):
        """
        Set the party manager to display.

        Args:
            party_manager: PartyManager instance
        """
        self.party_manager = party_manager
        self._update_cards()

    def _update_cards(self):
        """Update all member cards with current party data."""
        if not self.party_manager:
            return

        # Update active cards
        active_members = self.party_manager.get_active_party()
        for i, card in enumerate(self.active_cards):
            if i < len(active_members):
                card.set_member(active_members[i], is_active=True)
            else:
                card.set_member(None, is_active=True)

        # Update reserve cards
        reserve_members = self.party_manager.get_reserve_party()
        for i, card in enumerate(self.reserve_cards):
            if i < len(reserve_members):
                card.set_member(reserve_members[i], is_active=False)
            else:
                card.set_member(None, is_active=False)

    def show(self):
        """Show the menu."""
        self.visible = True
        self._update_cards()

    def hide(self):
        """Hide the menu."""
        self.visible = False
        self.selected_card = None
        self.selected_for_swap = None

    def handle_event(self, event: pygame.event.Event):
        """
        Handle input events.

        Args:
            event: Pygame event
        """
        if not self.visible:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Check close button
            if self.close_button.contains_point(mouse_x, mouse_y):
                self.hide()
                if self.on_close:
                    self.on_close()
                return

            # Check swap button
            if self.swap_button.enabled and self.swap_button.contains_point(mouse_x, mouse_y):
                self._perform_swap()
                return

            # Check member cards
            for card in self.active_cards + self.reserve_cards:
                if card.contains_point(mouse_x, mouse_y) and card.member:
                    self._select_card(card)
                    break

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                self.hide()
                if self.on_close:
                    self.on_close()

    def _select_card(self, card: PartyMemberCard):
        """
        Select a card for swapping.

        Args:
            card: Card to select
        """
        # Clear previous selection
        if self.selected_card:
            self.selected_card.set_selected(False)

        # If clicking same card, deselect
        if self.selected_card == card:
            self.selected_card = None
            self.selected_for_swap = None
            self.swap_button.set_enabled(False)
            return

        # First selection
        if not self.selected_for_swap:
            self.selected_for_swap = card
            card.set_selected(True)
            self.selected_card = card
            self.swap_button.set_enabled(False)

        # Second selection - check if valid swap
        else:
            # Cannot swap captain
            if self.selected_for_swap.member == self.party_manager.captain:
                print("Cannot swap the captain!")
                self.selected_for_swap.set_selected(False)
                self.selected_for_swap = None
                self.selected_card = None
                return

            # Must be one active and one reserve
            if self.selected_for_swap.is_active != card.is_active:
                self.selected_card = card
                card.set_selected(True)
                self.swap_button.set_enabled(True)
            else:
                # Both active or both reserve - start new selection
                self.selected_for_swap.set_selected(False)
                self.selected_for_swap = card
                card.set_selected(True)
                self.selected_card = card
                self.swap_button.set_enabled(False)

    def _perform_swap(self):
        """Perform the member swap."""
        if not self.selected_for_swap or not self.selected_card:
            return

        if not self.party_manager:
            return

        # Determine which is active and which is reserve
        if self.selected_for_swap.is_active:
            active_member = self.selected_for_swap.member
            reserve_member = self.selected_card.member
        else:
            active_member = self.selected_card.member
            reserve_member = self.selected_for_swap.member

        # Perform swap
        success = self.party_manager.swap_members(active_member, reserve_member)

        if success:
            print(f"Swapped {active_member.name} ↔ {reserve_member.name}")
            self._update_cards()

        # Clear selection
        self.selected_for_swap.set_selected(False)
        self.selected_card.set_selected(False)
        self.selected_for_swap = None
        self.selected_card = None
        self.swap_button.set_enabled(False)

    def update(self, dt: float):
        """
        Update menu state.

        Args:
            dt: Delta time
        """
        if not self.visible:
            return

    def render(self, surface: pygame.Surface):
        """
        Render the menu.

        Args:
            surface: Surface to draw on
        """
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
        title_surface = self.title_font.render("Party Management", True, WHITE)
        title_x = self.panel_x + (self.panel_width - title_surface.get_width()) // 2
        surface.blit(title_surface, (title_x, self.panel_y + 15))

        # Draw section labels
        active_label = self.section_font.render("Active Party (4/4)", True, CYAN)
        surface.blit(active_label, (self.panel_x + 20, self.panel_y + 55))

        reserve_label = self.section_font.render("Reserve (6/6)", True, LIGHT_GRAY)
        surface.blit(reserve_label, (self.panel_x + 20, self.panel_y + 375))

        # Draw member cards
        for card in self.active_cards:
            card.render(surface)

        for card in self.reserve_cards:
            card.render(surface)

        # Draw buttons
        self.close_button.render(surface)
        self.swap_button.render(surface)

        # Draw instructions
        if self.selected_for_swap:
            instruction = "Select another member to swap (Active ↔ Reserve)"
            instruction_surface = self.info_font.render(instruction, True, YELLOW)
            instruction_x = self.panel_x + (self.panel_width - instruction_surface.get_width()) // 2
            surface.blit(instruction_surface, (instruction_x, self.panel_y + self.panel_height - 140))

    def set_visible(self, visible: bool):
        """Set menu visibility."""
        if visible:
            self.show()
        else:
            self.hide()
