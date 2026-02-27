"""
Chest Menu UI
Interface for transferring items between chest and player inventory.
"""

import pygame
from typing import Optional, Callable
from systems.item_system import Inventory
from ui.panel import Panel
from ui.button import Button
from ui.item_icons import load_item_icon
from utils.constants import *


class ChestMenu:
    """UI for interacting with chest storage."""

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize chest menu.

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.visible = False

        # Menu dimensions
        self.width = 700
        self.height = 500
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2

        # Create panel
        self.panel = Panel(self.x, self.y, self.width, self.height, "Chest")

        # Storage
        self.chest_inventory: Optional[Inventory] = None
        self.player_inventory: Optional[Inventory] = None
        self.selected_chest_slot = -1
        self.selected_player_slot = -1

        # Fonts
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)

        # Close button
        self.close_button = Button(
            x=self.x + self.width - 120,
            y=self.y + self.height - 60,
            width=100,
            height=40,
            text="Close",
            callback=self.hide
        )

        # Transfer buttons
        self.take_button = Button(
            x=self.x + self.width // 2 - 100,
            y=self.y + self.height // 2 - 25,
            width=90,
            height=50,
            text="Take →",
            callback=self._on_take
        )

        self.store_button = Button(
            x=self.x + self.width // 2 + 10,
            y=self.y + self.height // 2 - 25,
            width=90,
            height=50,
            text="← Store",
            callback=self._on_store
        )

        # Take All button
        self.take_all_button = Button(
            x=self.x + 20,
            y=self.y + self.height - 60,
            width=100,
            height=40,
            text="Take All",
            callback=self._on_take_all
        )

        # Callbacks
        self.on_close: Optional[Callable] = None

    def show(self, chest_inventory: Inventory, player_inventory: Inventory):
        """
        Show the chest menu.

        Args:
            chest_inventory: Chest's inventory
            player_inventory: Player's inventory
        """
        self.chest_inventory = chest_inventory
        self.player_inventory = player_inventory
        self.visible = True
        self.selected_chest_slot = -1
        self.selected_player_slot = -1

    def hide(self):
        """Hide the chest menu."""
        self.visible = False
        if self.on_close:
            self.on_close()

    def handle_event(self, event: pygame.event.Event):
        """Handle input events."""
        if not self.visible:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check chest slots
            chest_slot = self._get_chest_slot_at_pos(mouse_pos)
            if chest_slot is not None:
                self.selected_chest_slot = chest_slot
                self.selected_player_slot = -1

            # Check player slots
            player_slot = self._get_player_slot_at_pos(mouse_pos)
            if player_slot is not None:
                self.selected_player_slot = player_slot
                self.selected_chest_slot = -1

        # Handle buttons
        self.close_button.handle_event(event)
        self.take_button.handle_event(event)
        self.store_button.handle_event(event)
        self.take_all_button.handle_event(event)

    def update(self, dt: float):
        """Update menu state."""
        if not self.visible:
            return

        self.close_button.update(dt)
        self.take_button.update(dt)
        self.store_button.update(dt)
        self.take_all_button.update(dt)

    def render(self, surface: pygame.Surface):
        """Render the chest menu."""
        if not self.visible:
            return

        # Draw panel
        self.panel.render(surface)

        # Draw chest inventory label
        chest_label = self.font.render("Chest", True, WHITE)
        surface.blit(chest_label, (self.x + 20, self.y + 50))

        # Draw player inventory label
        player_label = self.font.render("Your Inventory", True, WHITE)
        surface.blit(player_label, (self.x + self.width // 2 + 20, self.y + 50))

        # Draw chest slots
        self._render_chest_slots(surface)

        # Draw player slots
        self._render_player_slots(surface)

        # Draw buttons
        self.close_button.render(surface)
        self.take_button.render(surface)
        self.store_button.render(surface)
        self.take_all_button.render(surface)

    def _render_chest_slots(self, surface: pygame.Surface):
        """Render chest inventory slots."""
        if not self.chest_inventory:
            return

        slot_size = 50
        slots_per_row = 5
        start_x = self.x + 20
        start_y = self.y + 90

        for i, slot in enumerate(self.chest_inventory.slots):
            if i >= 20:  # Limit to 20 slots for display
                break

            row = i // slots_per_row
            col = i % slots_per_row
            slot_x = start_x + col * (slot_size + 5)
            slot_y = start_y + row * (slot_size + 5)

            # Determine slot color
            if i == self.selected_chest_slot:
                bg_color = UI_HIGHLIGHT_COLOR
            else:
                bg_color = DARK_GRAY

            # Draw slot background
            rect = pygame.Rect(slot_x, slot_y, slot_size, slot_size)
            pygame.draw.rect(surface, bg_color, rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, rect, 2)

            # Draw item if present
            if slot and not slot.is_empty():
                icon_size = slot_size - 6
                icon_x = slot_x + 3
                icon_y = slot_y + 3

                # Try to load and display icon
                icon_displayed = False
                if slot.item.icon:
                    icon_surface = load_item_icon(slot.item.icon, (icon_size, icon_size))
                    if icon_surface:
                        surface.blit(icon_surface, (icon_x, icon_y))
                        icon_displayed = True

                # Fallback to colored square
                if not icon_displayed:
                    item_color = slot.item.get_color()
                    item_rect = pygame.Rect(icon_x, icon_y, icon_size, icon_size)
                    pygame.draw.rect(surface, item_color, item_rect)

                # Draw quantity
                if slot.quantity > 1:
                    qty_text = self.small_font.render(str(slot.quantity), True, WHITE)
                    surface.blit(qty_text, (rect.right - qty_text.get_width() - 3, rect.bottom - qty_text.get_height() - 3))

    def _render_player_slots(self, surface: pygame.Surface):
        """Render player inventory slots."""
        if not self.player_inventory:
            return

        slot_size = 50
        slots_per_row = 5
        start_x = self.x + self.width // 2 + 20
        start_y = self.y + 90

        for i, slot in enumerate(self.player_inventory.slots):
            if i >= 20:  # Limit to 20 slots for display
                break

            row = i // slots_per_row
            col = i % slots_per_row
            slot_x = start_x + col * (slot_size + 5)
            slot_y = start_y + row * (slot_size + 5)

            # Determine slot color
            if i == self.selected_player_slot:
                bg_color = UI_HIGHLIGHT_COLOR
            else:
                bg_color = DARK_GRAY

            # Draw slot background
            rect = pygame.Rect(slot_x, slot_y, slot_size, slot_size)
            pygame.draw.rect(surface, bg_color, rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, rect, 2)

            # Draw item if present
            if slot and not slot.is_empty():
                icon_size = slot_size - 6
                icon_x = slot_x + 3
                icon_y = slot_y + 3

                # Try to load and display icon
                icon_displayed = False
                if slot.item.icon:
                    icon_surface = load_item_icon(slot.item.icon, (icon_size, icon_size))
                    if icon_surface:
                        surface.blit(icon_surface, (icon_x, icon_y))
                        icon_displayed = True

                # Fallback to colored square
                if not icon_displayed:
                    item_color = slot.item.get_color()
                    item_rect = pygame.Rect(icon_x, icon_y, icon_size, icon_size)
                    pygame.draw.rect(surface, item_color, item_rect)

                # Draw quantity
                if slot.quantity > 1:
                    qty_text = self.small_font.render(str(slot.quantity), True, WHITE)
                    surface.blit(qty_text, (rect.right - qty_text.get_width() - 3, rect.bottom - qty_text.get_height() - 3))

    def _get_chest_slot_at_pos(self, pos: tuple) -> Optional[int]:
        """Get chest slot index at mouse position."""
        if not self.chest_inventory:
            return None

        slot_size = 50
        slots_per_row = 5
        start_x = self.x + 20
        start_y = self.y + 90

        for i in range(min(20, len(self.chest_inventory.slots))):
            row = i // slots_per_row
            col = i % slots_per_row
            slot_x = start_x + col * (slot_size + 5)
            slot_y = start_y + row * (slot_size + 5)

            rect = pygame.Rect(slot_x, slot_y, slot_size, slot_size)
            if rect.collidepoint(pos):
                return i

        return None

    def _get_player_slot_at_pos(self, pos: tuple) -> Optional[int]:
        """Get player slot index at mouse position."""
        if not self.player_inventory:
            return None

        slot_size = 50
        slots_per_row = 5
        start_x = self.x + self.width // 2 + 20
        start_y = self.y + 90

        for i in range(min(20, len(self.player_inventory.slots))):
            row = i // slots_per_row
            col = i % slots_per_row
            slot_x = start_x + col * (slot_size + 5)
            slot_y = start_y + row * (slot_size + 5)

            rect = pygame.Rect(slot_x, slot_y, slot_size, slot_size)
            if rect.collidepoint(pos):
                return i

        return None

    def _on_take(self):
        """Take item from chest to player inventory."""
        if self.selected_chest_slot < 0 or not self.chest_inventory or not self.player_inventory:
            return

        slot = self.chest_inventory.slots[self.selected_chest_slot]
        if slot and not slot.is_empty():
            # Transfer item
            if self.player_inventory.add_item(slot.item, 1):
                self.chest_inventory.remove_item_at(self.selected_chest_slot, 1)
                print(f"Took {slot.item.name} from chest")

    def _on_store(self):
        """Store item from player inventory to chest."""
        if self.selected_player_slot < 0 or not self.chest_inventory or not self.player_inventory:
            return

        slot = self.player_inventory.slots[self.selected_player_slot]
        if slot and not slot.is_empty():
            # Transfer item
            if self.chest_inventory.add_item(slot.item, 1):
                self.player_inventory.remove_item_at(self.selected_player_slot, 1)
                print(f"Stored {slot.item.name} in chest")

    def _on_take_all(self):
        """Take all items from chest to player inventory."""
        if not self.chest_inventory or not self.player_inventory:
            return

        items_taken = 0
        inventory_full = False

        # First collect all items and their slot indices
        items_to_take = []
        for i, slot in enumerate(self.chest_inventory.slots):
            if slot and not slot.is_empty():
                items_to_take.append((i, slot.item, slot.quantity))

        # Now transfer items
        for slot_idx, item, quantity in items_to_take:
            if inventory_full:
                break
            for _ in range(quantity):
                if self.player_inventory.add_item(item, 1):
                    self.chest_inventory.remove_item_at(slot_idx, 1)
                    items_taken += 1
                else:
                    print("Inventory full!")
                    inventory_full = True
                    break

        if items_taken > 0:
            print(f"Took {items_taken} items from chest")
        self.selected_chest_slot = -1
