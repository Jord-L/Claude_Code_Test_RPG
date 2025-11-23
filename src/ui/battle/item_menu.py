"""
Battle Item Menu
Item selection UI for use during battle.
"""

import pygame
from typing import List, Optional, Callable
from systems.item_system import Item, InventorySlot
from ui.panel import Panel
from utils.constants import *


class BattleItemSlot:
    """Visual representation of an item in battle menu."""

    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initialize item slot.

        Args:
            x: X position
            y: Y position
            width: Slot width
            height: Slot height
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.slot: Optional[InventorySlot] = None
        self.is_selected = False
        self.is_hovered = False

        # Colors
        self.bg_color = DARK_GRAY
        self.selected_color = UI_HIGHLIGHT_COLOR
        self.hover_color = LIGHT_GRAY

        # Fonts
        self.name_font = pygame.font.Font(None, 22)
        self.qty_font = pygame.font.Font(None, 18)

    def set_slot(self, slot: Optional[InventorySlot]):
        """Set the inventory slot to display."""
        self.slot = slot

    def set_selected(self, selected: bool):
        """Set selection state."""
        self.is_selected = selected

    def set_hovered(self, hovered: bool):
        """Set hover state."""
        self.is_hovered = hovered

    def contains_point(self, x: int, y: int) -> bool:
        """Check if point is within slot."""
        return self.rect.collidepoint(x, y)

    def render(self, surface: pygame.Surface):
        """Render the item slot."""
        if not self.slot:
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

        # Draw item icon (small colored square)
        icon_size = 20
        icon_rect = pygame.Rect(
            self.rect.x + 5,
            self.rect.y + (self.rect.height - icon_size) // 2,
            icon_size,
            icon_size
        )
        item_color = self.slot.item.get_color()
        pygame.draw.rect(surface, item_color, icon_rect)

        # Draw item name
        name_text = self.name_font.render(self.slot.item.name, True, WHITE)
        name_x = self.rect.x + 30
        name_y = self.rect.y + (self.rect.height - name_text.get_height()) // 2
        surface.blit(name_text, (name_x, name_y))

        # Draw quantity
        if self.slot.quantity > 1:
            qty_text = self.qty_font.render(f"x{self.slot.quantity}", True, LIGHT_GRAY)
            qty_x = self.rect.right - qty_text.get_width() - 5
            qty_y = self.rect.y + (self.rect.height - qty_text.get_height()) // 2
            surface.blit(qty_text, (qty_x, qty_y))

        # Draw border
        border_width = 2 if self.is_selected else 1
        pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, border_width)


class BattleItemMenu:
    """
    Item selection menu for battle.
    Shows consumable items that can be used in battle.
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initialize battle item menu.

        Args:
            x: X position
            y: Y position
            width: Menu width
            height: Menu height
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = False
        self.active = False

        # Panel
        self.panel = Panel(x, y, width, height)

        # Item slots
        self.item_slots: List[BattleItemSlot] = []
        self.usable_items: List[InventorySlot] = []

        # Selection
        self.selected_index = 0
        self.hovered_index = -1

        # Callbacks
        self.on_item_selected: Optional[Callable[[Item], None]] = None
        self.on_cancel: Optional[Callable[[], None]] = None

        # Fonts
        self.title_font = pygame.font.Font(None, 28)
        self.desc_font = pygame.font.Font(None, 18)

        # Layout
        self.slot_height = 40
        self.slot_spacing = 5
        self.max_visible_slots = 6

    def set_items(self, inventory_slots: List[InventorySlot]):
        """
        Set items to display (filtered for battle-usable consumables).

        Args:
            inventory_slots: All inventory slots
        """
        # Filter for battle-usable consumables
        self.usable_items = [
            slot for slot in inventory_slots
            if slot.item.consumable and slot.item.usable_in_battle
        ]

        # Create visual slots
        self._create_item_slots()

        # Reset selection
        self.selected_index = 0 if self.usable_items else -1

    def _create_item_slots(self):
        """Create visual item slot UIs."""
        self.item_slots.clear()

        start_x = self.rect.x + 10
        start_y = self.rect.y + 50
        slot_width = self.rect.width - 20

        for i, slot in enumerate(self.usable_items[:self.max_visible_slots]):
            y = start_y + i * (self.slot_height + self.slot_spacing)
            item_slot = BattleItemSlot(start_x, y, slot_width, self.slot_height)
            item_slot.set_slot(slot)
            self.item_slots.append(item_slot)

    def set_visible(self, visible: bool):
        """Set visibility."""
        self.visible = visible
        if not visible:
            self.hovered_index = -1

    def set_active(self, active: bool):
        """Set active state."""
        self.active = active

    def handle_event(self, event: pygame.event.Event):
        """
        Handle input events.

        Args:
            event: Pygame event
        """
        if not self.visible or not self.active:
            return

        if event.type == pygame.KEYDOWN:
            # Navigate with arrow keys
            if event.key == pygame.K_UP:
                if self.selected_index > 0:
                    self.selected_index -= 1
                    self._update_selection()

            elif event.key == pygame.K_DOWN:
                if self.selected_index < len(self.usable_items) - 1:
                    self.selected_index += 1
                    self._update_selection()

            # Select with Enter/Space
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if 0 <= self.selected_index < len(self.usable_items):
                    item = self.usable_items[self.selected_index].item
                    if self.on_item_selected:
                        self.on_item_selected(item)

            # Cancel with Escape/Backspace
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                if self.on_cancel:
                    self.on_cancel()

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos

            # Update hover state
            new_hovered = -1
            for i, slot in enumerate(self.item_slots):
                if slot.contains_point(mouse_x, mouse_y):
                    new_hovered = i
                    break

            if self.hovered_index != new_hovered:
                # Clear old hover
                if 0 <= self.hovered_index < len(self.item_slots):
                    self.item_slots[self.hovered_index].set_hovered(False)

                # Set new hover
                self.hovered_index = new_hovered
                if 0 <= self.hovered_index < len(self.item_slots):
                    self.item_slots[self.hovered_index].set_hovered(True)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Check if clicked on item slot
            for i, slot in enumerate(self.item_slots):
                if slot.contains_point(mouse_x, mouse_y):
                    self.selected_index = i
                    self._update_selection()

                    # Select item
                    if 0 <= i < len(self.usable_items):
                        item = self.usable_items[i].item
                        if self.on_item_selected:
                            self.on_item_selected(item)
                    break

    def _update_selection(self):
        """Update visual selection state."""
        for i, slot in enumerate(self.item_slots):
            slot.set_selected(i == self.selected_index)

    def render(self, surface: pygame.Surface):
        """
        Render the menu.

        Args:
            surface: Surface to draw on
        """
        if not self.visible:
            return

        # Draw panel
        self.panel.render(surface)

        # Draw title
        title_text = self.title_font.render("Use Item", True, WHITE)
        title_x = self.rect.x + (self.rect.width - title_text.get_width()) // 2
        surface.blit(title_text, (title_x, self.rect.y + 10))

        # Draw item slots
        for slot in self.item_slots:
            slot.render(surface)

        # Draw item description if selected
        if 0 <= self.selected_index < len(self.usable_items):
            item = self.usable_items[self.selected_index].item
            desc_text = self.desc_font.render(item.description, True, LIGHT_GRAY)
            desc_y = self.rect.bottom - 30
            desc_x = self.rect.x + 10
            surface.blit(desc_text, (desc_x, desc_y))

        # Draw empty message if no items
        if not self.usable_items:
            empty_text = self.desc_font.render("No usable items in inventory", True, LIGHT_GRAY)
            empty_x = self.rect.x + (self.rect.width - empty_text.get_width()) // 2
            empty_y = self.rect.y + (self.rect.height - empty_text.get_height()) // 2
            surface.blit(empty_text, (empty_x, empty_y))

        # Draw controls hint
        controls_text = self.desc_font.render("↑↓: Navigate | Enter: Use | Esc: Cancel", True, LIGHT_GRAY)
        controls_x = self.rect.x + (self.rect.width - controls_text.get_width()) // 2
        surface.blit(controls_text, (controls_x, self.rect.bottom - 10))

    def update(self, dt: float):
        """Update menu state."""
        pass
