"""
Inventory Menu UI
Visual inventory management with grid display and item tooltips.
"""

import pygame
import os
from typing import Optional, Callable, List, TYPE_CHECKING, Dict
from systems.item_system import Item, Inventory, InventorySlot, Equipment
from systems.item_loader import get_item_loader
from ui.panel import Panel
from ui.button import Button
from utils.constants import *

if TYPE_CHECKING:
    from entities.character import Character


# Icon cache to avoid reloading images
_icon_cache: Dict[str, pygame.Surface] = {}


def load_item_icon(icon_path: str, size: tuple = (44, 44)) -> Optional[pygame.Surface]:
    """
    Load an item icon from file with caching.

    Args:
        icon_path: Path to icon file (relative to assets/icons/)
        size: Target size for icon

    Returns:
        Loaded and scaled icon surface, or None if not found
    """
    # Check cache first
    cache_key = f"{icon_path}_{size[0]}x{size[1]}"
    if cache_key in _icon_cache:
        return _icon_cache[cache_key]

    # Try to load from assets/icons/
    full_path = os.path.join("assets", "icons", icon_path)

    if os.path.exists(full_path):
        try:
            icon = pygame.image.load(full_path)
            icon = pygame.transform.scale(icon, size)
            _icon_cache[cache_key] = icon
            return icon
        except pygame.error as e:
            print(f"Failed to load icon {full_path}: {e}")
            return None

    return None


class ItemSlotUI:
    """Visual representation of a single inventory slot."""

    def __init__(self, x: int, y: int, size: int = 50):
        """
        Initialize item slot UI.

        Args:
            x: X position
            y: Y position
            size: Slot size in pixels
        """
        self.rect = pygame.Rect(x, y, size, size)
        self.slot: Optional[InventorySlot] = None
        self.is_selected = False
        self.is_hovered = False

        # Colors
        self.bg_color = DARK_GRAY
        self.border_color = UI_BORDER_COLOR
        self.selected_color = UI_HIGHLIGHT_COLOR
        self.hover_color = LIGHT_GRAY

        # Font
        self.font = pygame.font.Font(None, 18)

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
        """Render the slot."""
        # Determine background color
        if self.is_selected:
            bg = self.selected_color
        elif self.is_hovered:
            bg = self.hover_color
        else:
            bg = self.bg_color

        # Draw background
        pygame.draw.rect(surface, bg, self.rect)

        # Draw item if present
        if self.slot and self.slot.item:
            icon_size = self.rect.width - 6
            icon_x = self.rect.x + 3
            icon_y = self.rect.y + 3

            # Try to load and display icon if available
            icon_displayed = False
            if self.slot.item.icon:
                icon_surface = load_item_icon(self.slot.item.icon, (icon_size, icon_size))
                if icon_surface:
                    surface.blit(icon_surface, (icon_x, icon_y))
                    icon_displayed = True

            # Fallback to colored square based on rarity
            if not icon_displayed:
                icon_rect = pygame.Rect(icon_x, icon_y, icon_size, icon_size)
                item_color = self.slot.item.get_color()
                pygame.draw.rect(surface, item_color, icon_rect)

            # Quantity if stackable
            if self.slot.item.stackable and self.slot.quantity > 1:
                qty_text = self.font.render(str(self.slot.quantity), True, WHITE)
                qty_x = self.rect.right - qty_text.get_width() - 2
                qty_y = self.rect.bottom - qty_text.get_height() - 2

                # Draw shadow
                shadow = self.font.render(str(self.slot.quantity), True, BLACK)
                surface.blit(shadow, (qty_x + 1, qty_y + 1))
                # Draw text
                surface.blit(qty_text, (qty_x, qty_y))

        # Draw border
        border_width = 2 if self.is_selected else 1
        pygame.draw.rect(surface, self.border_color, self.rect, border_width)


class ItemTooltip:
    """Tooltip showing item details."""

    def __init__(self):
        """Initialize tooltip."""
        self.item: Optional[Item] = None
        self.quantity: int = 0
        self.visible = False
        self.position = (0, 0)

        # Fonts
        self.title_font = pygame.font.Font(None, 24)
        self.text_font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 18)

        # Colors
        self.bg_color = (20, 20, 30, 240)  # Semi-transparent dark
        self.border_color = WHITE

    def set_item(self, item: Optional[Item], quantity: int = 1):
        """Set item to display."""
        self.item = item
        self.quantity = quantity
        self.visible = item is not None

    def set_position(self, x: int, y: int):
        """Set tooltip position."""
        self.position = (x, y)

    def hide(self):
        """Hide tooltip."""
        self.visible = False
        self.item = None

    def render(self, surface: pygame.Surface):
        """Render tooltip."""
        if not self.visible or not self.item:
            return

        # Build tooltip content
        lines = []

        # Title (item name with rarity color)
        title_color = self.item.get_color()

        # Description
        desc_lines = self._wrap_text(self.item.description, 40)

        # Stats for equipment
        stat_lines = []
        if isinstance(self.item, Equipment):
            if self.item.stat_bonuses:
                stat_lines.append("Stats:")
                for stat, bonus in self.item.stat_bonuses.items():
                    stat_lines.append(f"  +{bonus} {stat.capitalize()}")

            if self.item.level_requirement > 1:
                stat_lines.append(f"Level Required: {self.item.level_requirement}")

        # Value
        value_line = f"Value: {self.item.value} Berries"

        # Calculate tooltip size
        width = 300
        line_height = 22
        padding = 10

        # Title + type + (equip_slot if equipment) + desc + stats + value
        total_lines = 1 + 1 + len(desc_lines) + len(stat_lines) + 1
        if isinstance(self.item, Equipment):
            total_lines += 1  # Add line for equipment slot
        height = padding * 2 + (total_lines * line_height)

        # Position (ensure it stays on screen)
        x, y = self.position
        if x + width > SCREEN_WIDTH:
            x = SCREEN_WIDTH - width - 10
        if y + height > SCREEN_HEIGHT:
            y = SCREEN_HEIGHT - height - 10

        # Draw background
        tooltip_surface = pygame.Surface((width, height))
        tooltip_surface.set_alpha(240)
        tooltip_surface.fill((20, 20, 30))
        surface.blit(tooltip_surface, (x, y))

        # Draw border
        pygame.draw.rect(surface, self.border_color, (x, y, width, height), 2)

        # Draw content
        current_y = y + padding

        # Title
        title_text = self.title_font.render(self.item.name, True, title_color)
        surface.blit(title_text, (x + padding, current_y))
        current_y += line_height + 5

        # Type and rarity
        type_text = f"{self.item.item_type.value.capitalize()} - {self.item.rarity.value.capitalize()}"
        type_surface = self.small_font.render(type_text, True, LIGHT_GRAY)
        surface.blit(type_surface, (x + padding, current_y))
        current_y += line_height

        # Equipment slot (if equipment)
        if isinstance(self.item, Equipment):
            slot_text = f"Equips to: {self.item.equip_slot.capitalize()} Slot"
            slot_surface = self.small_font.render(slot_text, True, CYAN)
            surface.blit(slot_surface, (x + padding, current_y))
            current_y += line_height

        # Description
        for line in desc_lines:
            desc_surface = self.text_font.render(line, True, WHITE)
            surface.blit(desc_surface, (x + padding, current_y))
            current_y += line_height

        # Stats
        if stat_lines:
            current_y += 5
            for line in stat_lines:
                stat_surface = self.text_font.render(line, True, GREEN)
                surface.blit(stat_surface, (x + padding, current_y))
                current_y += line_height

        # Value
        current_y += 5
        value_surface = self.text_font.render(value_line, True, YELLOW)
        surface.blit(value_surface, (x + padding, current_y))

    def _wrap_text(self, text: str, max_chars: int) -> List[str]:
        """Wrap text to max characters per line."""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 <= max_chars:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)

        if current_line:
            lines.append(" ".join(current_line))

        return lines or [""]


class InventoryMenu:
    """
    Full inventory menu with grid display.
    """

    GRID_COLS = 10
    GRID_ROWS = 5
    SLOT_SIZE = 52
    SLOT_SPACING = 4

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize inventory menu.

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.visible = False

        # Inventory reference
        self.inventory: Optional[Inventory] = None
        self.character: Optional['Character'] = None

        # Layout
        self.panel_width = 800
        self.panel_height = 500
        self.panel_x = (screen_width - self.panel_width) // 2
        self.panel_y = (screen_height - self.panel_height) // 2

        # Background panel
        self.panel = Panel(self.panel_x, self.panel_y, self.panel_width, self.panel_height)

        # Item slots
        self.item_slots: List[ItemSlotUI] = []
        self._create_slot_grid()

        # Selection
        self.selected_slot: Optional[ItemSlotUI] = None
        self.hovered_slot: Optional[ItemSlotUI] = None

        # Tooltip
        self.tooltip = ItemTooltip()

        # Buttons
        self._create_buttons()

        # Callbacks
        self.on_close: Optional[Callable] = None
        self.on_use_item: Optional[Callable] = None

        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        self.info_font = pygame.font.Font(None, 22)

    def _create_slot_grid(self):
        """Create grid of item slots."""
        start_x = self.panel_x + 20
        start_y = self.panel_y + 80

        for row in range(self.GRID_ROWS):
            for col in range(self.GRID_COLS):
                x = start_x + col * (self.SLOT_SIZE + self.SLOT_SPACING)
                y = start_y + row * (self.SLOT_SIZE + self.SLOT_SPACING)

                slot = ItemSlotUI(x, y, self.SLOT_SIZE)
                self.item_slots.append(slot)

    def _create_buttons(self):
        """Create menu buttons."""
        button_y = self.panel_y + self.panel_height - 60

        self.close_button = Button(
            self.panel_x + self.panel_width - 120,
            button_y,
            100, 40,
            "Close"
        )

        self.sort_button = Button(
            self.panel_x + 20,
            button_y,
            100, 40,
            "Sort"
        )

        self.use_button = Button(
            self.panel_x + 140,
            button_y,
            100, 40,
            "Use"
        )
        self.use_button.set_enabled(False)

        self.equip_button = Button(
            self.panel_x + 260,
            button_y,
            100, 40,
            "Equip"
        )
        self.equip_button.set_enabled(False)

    def set_inventory(self, inventory: Inventory, character: Optional['Character'] = None):
        """
        Set inventory to display.

        Args:
            inventory: Inventory instance
            character: Character who owns the inventory (for equipping)
        """
        self.inventory = inventory
        self.character = character
        self._update_slots()

    def _update_slots(self):
        """Update slot display from inventory."""
        if not self.inventory:
            return

        # Get all items
        inventory_items = self.inventory.get_all_items()

        # Update slots
        for i, slot_ui in enumerate(self.item_slots):
            if i < len(inventory_items):
                slot_ui.set_slot(inventory_items[i])
            else:
                slot_ui.set_slot(None)

    def show(self):
        """Show the menu."""
        self.visible = True
        self._update_slots()

    def hide(self):
        """Hide the menu."""
        self.visible = False
        self.tooltip.hide()
        if self.selected_slot:
            self.selected_slot.set_selected(False)
        self.selected_slot = None

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

            # Check buttons
            if self.close_button.rect.collidepoint((mouse_x, mouse_y)):
                self.hide()
                if self.on_close:
                    self.on_close()
                return

            if self.sort_button.rect.collidepoint((mouse_x, mouse_y)):
                if self.inventory:
                    self.inventory.sort_by_rarity()
                    self._update_slots()
                return

            if self.use_button.enabled and self.use_button.rect.collidepoint((mouse_x, mouse_y)):
                if self.selected_slot and self.selected_slot.slot:
                    self._use_selected_item()
                return

            if self.equip_button.enabled and self.equip_button.rect.collidepoint((mouse_x, mouse_y)):
                if self.selected_slot and self.selected_slot.slot:
                    self._equip_selected_item()
                return

            # Check item slots
            for slot in self.item_slots:
                if slot.contains_point(mouse_x, mouse_y) and slot.slot:
                    self._select_slot(slot)
                    break

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos

            # Update hover state
            new_hovered = None
            for slot in self.item_slots:
                if slot.contains_point(mouse_x, mouse_y):
                    new_hovered = slot
                    break

            # Update hover
            if self.hovered_slot != new_hovered:
                if self.hovered_slot:
                    self.hovered_slot.set_hovered(False)

                self.hovered_slot = new_hovered

                if self.hovered_slot:
                    self.hovered_slot.set_hovered(True)
                    # Show tooltip
                    if self.hovered_slot.slot:
                        self.tooltip.set_item(self.hovered_slot.slot.item, self.hovered_slot.slot.quantity)
                        self.tooltip.set_position(mouse_x + 15, mouse_y + 15)
                    else:
                        self.tooltip.hide()
                else:
                    self.tooltip.hide()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
                self.hide()
                if self.on_close:
                    self.on_close()

    def _select_slot(self, slot: ItemSlotUI):
        """Select a slot."""
        # Deselect previous
        if self.selected_slot:
            self.selected_slot.set_selected(False)

        # Select new
        self.selected_slot = slot
        slot.set_selected(True)

        # Enable/disable use button
        if slot.slot and slot.slot.item.consumable:
            self.use_button.set_enabled(True)
        else:
            self.use_button.set_enabled(False)

        # Enable/disable equip button
        if slot.slot and isinstance(slot.slot.item, Equipment) and self.character and self.character.equipment_slots:
            # Check if can equip (level requirement)
            if slot.slot.item.can_equip(self.character):
                self.equip_button.set_enabled(True)
            else:
                self.equip_button.set_enabled(False)
        else:
            self.equip_button.set_enabled(False)

    def _use_selected_item(self):
        """Use the selected item."""
        if not self.selected_slot or not self.selected_slot.slot:
            return

        item = self.selected_slot.slot.item

        if not item.consumable:
            return

        # Callback to use item
        if self.on_use_item:
            self.on_use_item(item)

        # Remove one from inventory
        if self.inventory:
            self.inventory.remove_item(item.id, 1)
            self._update_slots()

            # Deselect if no more
            if not self.inventory.has_item(item.id):
                self.selected_slot.set_selected(False)
                self.selected_slot = None
                self.use_button.set_enabled(False)

    def _equip_selected_item(self):
        """Equip the selected equipment."""
        if not self.selected_slot or not self.selected_slot.slot:
            return

        if not self.character or not self.character.equipment_slots:
            return

        item = self.selected_slot.slot.item

        if not isinstance(item, Equipment):
            return

        # Check if can equip
        if not item.can_equip(self.character):
            print(f"Level {item.level_requirement} required to equip {item.name}!")
            return

        # Equip the item
        old_equipment = self.character.equipment_slots.equip(item)

        # Add old equipment back to inventory if there was one
        if old_equipment:
            self.inventory.add_item(old_equipment, 1)
            print(f"Unequipped {old_equipment.name}")

        # Remove equipped item from inventory
        self.inventory.remove_item(item.id, 1)
        print(f"Equipped {item.name} on {self.character.name}!")

        # Update slots
        self._update_slots()

        # Deselect
        if self.selected_slot:
            self.selected_slot.set_selected(False)
        self.selected_slot = None
        self.equip_button.set_enabled(False)

    def update(self, dt: float):
        """Update menu state."""
        pass

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
        title_surface = self.title_font.render("Inventory", True, WHITE)
        title_x = self.panel_x + (self.panel_width - title_surface.get_width()) // 2
        surface.blit(title_surface, (title_x, self.panel_y + 15))

        # Draw inventory info
        if self.inventory:
            info_text = f"Items: {len(self.inventory.slots)}/{self.inventory.max_slots}"
            info_surface = self.info_font.render(info_text, True, LIGHT_GRAY)
            surface.blit(info_surface, (self.panel_x + 20, self.panel_y + 50))

        # Draw item slots
        for slot in self.item_slots:
            slot.render(surface)

        # Draw buttons
        self.sort_button.render(surface)
        self.use_button.render(surface)
        self.equip_button.render(surface)
        self.close_button.render(surface)

        # Draw tooltip (on top)
        self.tooltip.render(surface)

    def set_visible(self, visible: bool):
        """Set menu visibility."""
        if visible:
            self.show()
        else:
            self.hide()
