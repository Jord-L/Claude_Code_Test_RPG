"""
Equipment Menu UI
Visual equipment management for viewing and equipping items.
"""

import pygame
from typing import Optional, Callable, List, TYPE_CHECKING
from systems.item_system import Equipment, Weapon, Armor, Accessory
from systems.equipment_manager import EquipmentSlots
from systems.item_system import Inventory
from ui.panel import Panel
from ui.button import Button
from utils.constants import *

if TYPE_CHECKING:
    from entities.character import Character


class EquipmentSlotUI:
    """Visual representation of an equipment slot."""

    def __init__(self, x: int, y: int, slot_type: str, size: int = 80):
        """
        Initialize equipment slot UI.

        Args:
            x: X position
            y: Y position
            slot_type: Type of slot (weapon/armor/accessory)
            size: Slot size in pixels
        """
        self.rect = pygame.Rect(x, y, size, size)
        self.slot_type = slot_type
        self.equipment: Optional[Equipment] = None
        self.is_selected = False
        self.is_hovered = False

        # Colors
        self.bg_color = DARK_GRAY
        self.border_color = UI_BORDER_COLOR
        self.selected_color = UI_HIGHLIGHT_COLOR
        self.hover_color = LIGHT_GRAY
        self.empty_color = (60, 60, 70)

        # Fonts
        self.label_font = pygame.font.Font(None, 18)
        self.name_font = pygame.font.Font(None, 20)

    def set_equipment(self, equipment: Optional[Equipment]):
        """Set the equipment to display."""
        self.equipment = equipment

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
        """Render the equipment slot."""
        # Determine background color
        if self.is_selected:
            bg = self.selected_color
        elif self.is_hovered:
            bg = self.hover_color
        else:
            bg = self.bg_color if self.equipment else self.empty_color

        # Draw background
        pygame.draw.rect(surface, bg, self.rect)

        # Draw slot label
        label_text = self.slot_type.capitalize()
        label_surface = self.label_font.render(label_text, True, LIGHT_GRAY)
        label_x = self.rect.x + (self.rect.width - label_surface.get_width()) // 2
        surface.blit(label_surface, (label_x, self.rect.y + 5))

        # Draw equipment if present
        if self.equipment:
            # Equipment icon (colored square based on rarity)
            icon_size = 40
            icon_rect = pygame.Rect(
                self.rect.x + (self.rect.width - icon_size) // 2,
                self.rect.y + 25,
                icon_size,
                icon_size
            )
            equipment_color = self.equipment.get_color()
            pygame.draw.rect(surface, equipment_color, icon_rect)

            # Equipment type indicator
            type_indicator = ""
            if isinstance(self.equipment, Weapon):
                type_indicator = "⚔"
            elif isinstance(self.equipment, Armor):
                type_indicator = "🛡"
            elif isinstance(self.equipment, Accessory):
                type_indicator = "💍"

            if type_indicator:
                type_surface = self.name_font.render(type_indicator, True, WHITE)
                type_x = icon_rect.centerx - type_surface.get_width() // 2
                type_y = icon_rect.centery - type_surface.get_height() // 2
                surface.blit(type_surface, (type_x, type_y))

        else:
            # Empty slot placeholder
            empty_text = "Empty"
            empty_surface = self.label_font.render(empty_text, True, (100, 100, 110))
            empty_x = self.rect.x + (self.rect.width - empty_surface.get_width()) // 2
            empty_y = self.rect.y + (self.rect.height - empty_surface.get_height()) // 2
            surface.blit(empty_surface, (empty_x, empty_y))

        # Draw border
        border_width = 2 if self.is_selected else 1
        pygame.draw.rect(surface, self.border_color, self.rect, border_width)


class EquipmentTooltip:
    """Tooltip showing equipment details and stat bonuses."""

    def __init__(self):
        """Initialize tooltip."""
        self.equipment: Optional[Equipment] = None
        self.visible = False
        self.position = (0, 0)

        # Fonts
        self.title_font = pygame.font.Font(None, 24)
        self.text_font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 18)

        # Colors
        self.bg_color = (20, 20, 30, 240)
        self.border_color = WHITE

    def set_equipment(self, equipment: Optional[Equipment]):
        """Set equipment to display."""
        self.equipment = equipment
        self.visible = equipment is not None

    def set_position(self, x: int, y: int):
        """Set tooltip position."""
        self.position = (x, y)

    def hide(self):
        """Hide tooltip."""
        self.visible = False
        self.equipment = None

    def render(self, surface: pygame.Surface):
        """Render tooltip."""
        if not self.visible or not self.equipment:
            return

        # Build content
        lines = []
        title_color = self.equipment.get_color()

        # Stat bonuses
        stat_lines = []
        if self.equipment.stat_bonuses:
            stat_lines.append("Stat Bonuses:")
            for stat, bonus in self.equipment.stat_bonuses.items():
                stat_lines.append(f"  +{bonus} {stat.capitalize()}")

        # Equipment-specific stats
        specific_lines = []
        if isinstance(self.equipment, Weapon):
            specific_lines.append(f"Attack: {self.equipment.attack_power}")
            specific_lines.append(f"Speed: {self.equipment.attack_speed:.1f}x")
            if self.equipment.crit_bonus > 0:
                specific_lines.append(f"Crit: +{self.equipment.crit_bonus}%")
        elif isinstance(self.equipment, Armor):
            specific_lines.append(f"Defense: {self.equipment.defense}")
            if self.equipment.evasion_penalty != 0:
                specific_lines.append(f"Evasion: {self.equipment.evasion_penalty:+d}")

        # Level requirement
        level_line = f"Requires Level {self.equipment.level_requirement}"

        # Value
        value_line = f"Value: {self.equipment.value} Berries"

        # Calculate size
        width = 300
        line_height = 22
        padding = 10

        total_lines = 2 + len(stat_lines) + len(specific_lines) + 2  # Title + type + stats + specific + level + value
        height = padding * 2 + (total_lines * line_height)

        # Position (ensure on screen)
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
        title_text = self.title_font.render(self.equipment.name, True, title_color)
        surface.blit(title_text, (x + padding, current_y))
        current_y += line_height + 5

        # Type and rarity
        type_text = f"{self.equipment.item_type.value.capitalize()} - {self.equipment.rarity.value.capitalize()}"
        type_surface = self.small_font.render(type_text, True, LIGHT_GRAY)
        surface.blit(type_surface, (x + padding, current_y))
        current_y += line_height

        # Specific stats
        if specific_lines:
            for line in specific_lines:
                stat_surface = self.text_font.render(line, True, YELLOW)
                surface.blit(stat_surface, (x + padding, current_y))
                current_y += line_height

        # Stat bonuses
        if stat_lines:
            current_y += 5
            for line in stat_lines:
                stat_surface = self.text_font.render(line, True, GREEN)
                surface.blit(stat_surface, (x + padding, current_y))
                current_y += line_height

        # Level requirement
        current_y += 5
        level_surface = self.text_font.render(level_line, True, WHITE)
        surface.blit(level_surface, (x + padding, current_y))
        current_y += line_height

        # Value
        value_surface = self.text_font.render(value_line, True, YELLOW)
        surface.blit(value_surface, (x + padding, current_y))


class EquipmentMenu:
    """
    Equipment management menu.
    Shows character's current equipment and allows equipping/unequipping.
    """

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize equipment menu.

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.visible = False

        # Character reference
        self.character: Optional['Character'] = None
        self.inventory: Optional[Inventory] = None

        # Layout
        self.panel_width = 700
        self.panel_height = 600
        self.panel_x = (screen_width - self.panel_width) // 2
        self.panel_y = (screen_height - self.panel_height) // 2

        # Background panel
        self.panel = Panel(self.panel_x, self.panel_y, self.panel_width, self.panel_height)

        # Equipment slots
        self.equipment_slots: List[EquipmentSlotUI] = []
        self._create_equipment_slots()

        # Selection
        self.selected_slot: Optional[EquipmentSlotUI] = None
        self.hovered_slot: Optional[EquipmentSlotUI] = None

        # Tooltip
        self.tooltip = EquipmentTooltip()

        # Buttons
        self._create_buttons()

        # Callbacks
        self.on_close: Optional[Callable] = None

        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        self.info_font = pygame.font.Font(None, 22)
        self.stat_font = pygame.font.Font(None, 20)

    def _create_equipment_slots(self):
        """Create equipment slot UIs."""
        slot_size = 100
        start_x = self.panel_x + 50
        start_y = self.panel_y + 100

        # Weapon slot
        weapon_slot = EquipmentSlotUI(start_x, start_y, "weapon", slot_size)
        self.equipment_slots.append(weapon_slot)

        # Armor slot
        armor_slot = EquipmentSlotUI(start_x + 150, start_y, "armor", slot_size)
        self.equipment_slots.append(armor_slot)

        # Accessory slot
        accessory_slot = EquipmentSlotUI(start_x + 300, start_y, "accessory", slot_size)
        self.equipment_slots.append(accessory_slot)

    def _create_buttons(self):
        """Create menu buttons."""
        button_y = self.panel_y + self.panel_height - 60

        self.close_button = Button(
            self.panel_x + self.panel_width - 120,
            button_y,
            100, 40,
            "Close"
        )

        self.unequip_button = Button(
            self.panel_x + 20,
            button_y,
            120, 40,
            "Unequip"
        )
        self.unequip_button.set_enabled(False)

        self.equip_button = Button(
            self.panel_x + 160,
            button_y,
            120, 40,
            "Equip from Inv"
        )

    def set_character(self, character: 'Character', inventory: Inventory):
        """
        Set character to display equipment for.

        Args:
            character: Character instance
            inventory: Character's inventory
        """
        self.character = character
        self.inventory = inventory
        self._update_slots()

    def _update_slots(self):
        """Update equipment slots from character."""
        if not self.character or not self.character.equipment_slots:
            return

        equipment_slots = self.character.equipment_slots

        # Update each slot
        for slot_ui in self.equipment_slots:
            if slot_ui.slot_type == "weapon":
                slot_ui.set_equipment(equipment_slots.weapon)
            elif slot_ui.slot_type == "armor":
                slot_ui.set_equipment(equipment_slots.armor)
            elif slot_ui.slot_type == "accessory":
                slot_ui.set_equipment(equipment_slots.accessory)

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

            if self.unequip_button.enabled and self.unequip_button.rect.collidepoint((mouse_x, mouse_y)):
                self._unequip_selected()
                return

            if self.equip_button.rect.collidepoint((mouse_x, mouse_y)):
                # This would open inventory selection (future integration)
                print("Open inventory to select equipment (integration pending)")
                return

            # Check equipment slots
            for slot in self.equipment_slots:
                if slot.contains_point(mouse_x, mouse_y):
                    self._select_slot(slot)
                    break

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos

            # Update hover state
            new_hovered = None
            for slot in self.equipment_slots:
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
                    if self.hovered_slot.equipment:
                        self.tooltip.set_equipment(self.hovered_slot.equipment)
                        self.tooltip.set_position(mouse_x + 15, mouse_y + 15)
                    else:
                        self.tooltip.hide()
                else:
                    self.tooltip.hide()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
                self.hide()
                if self.on_close:
                    self.on_close()

    def _select_slot(self, slot: EquipmentSlotUI):
        """Select an equipment slot."""
        # Deselect previous
        if self.selected_slot:
            self.selected_slot.set_selected(False)

        # Select new
        self.selected_slot = slot
        slot.set_selected(True)

        # Enable/disable unequip button
        if slot.equipment:
            self.unequip_button.set_enabled(True)
        else:
            self.unequip_button.set_enabled(False)

    def _unequip_selected(self):
        """Unequip the selected equipment."""
        if not self.selected_slot or not self.selected_slot.equipment:
            return

        if not self.character or not self.character.equipment_slots:
            return

        equipment = self.selected_slot.equipment

        # Unequip
        unequipped = self.character.equipment_slots.unequip(equipment.equip_slot)

        if unequipped and self.inventory:
            # Add back to inventory
            self.inventory.add_item(unequipped, 1)
            print(f"Unequipped {unequipped.name}")

        # Update display
        self._update_slots()
        self.selected_slot.set_selected(False)
        self.selected_slot = None
        self.unequip_button.set_enabled(False)

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
        if self.character:
            title_text = f"{self.character.name}'s Equipment"
        else:
            title_text = "Equipment"
        title_surface = self.title_font.render(title_text, True, WHITE)
        title_x = self.panel_x + (self.panel_width - title_surface.get_width()) // 2
        surface.blit(title_surface, (title_x, self.panel_y + 15))

        # Draw equipment slots
        for slot in self.equipment_slots:
            slot.render(surface)

        # Draw stat summary
        if self.character:
            self._render_stats(surface)

        # Draw buttons
        self.unequip_button.render(surface)
        self.equip_button.render(surface)
        self.close_button.render(surface)

        # Draw tooltip (on top)
        self.tooltip.render(surface)

    def _render_stats(self, surface: pygame.Surface):
        """Render character stat summary."""
        stats_x = self.panel_x + 50
        stats_y = self.panel_y + 250

        # Title
        stats_title = self.info_font.render("Equipment Bonuses:", True, WHITE)
        surface.blit(stats_title, (stats_x, stats_y))
        stats_y += 30

        # Gather all stat bonuses
        total_bonuses = {}
        if self.character.equipment_slots:
            for equipment in [
                self.character.equipment_slots.weapon,
                self.character.equipment_slots.armor,
                self.character.equipment_slots.accessory
            ]:
                if equipment:
                    for stat, bonus in equipment.stat_bonuses.items():
                        total_bonuses[stat] = total_bonuses.get(stat, 0) + bonus

        # Display bonuses
        if total_bonuses:
            for stat, bonus in sorted(total_bonuses.items()):
                bonus_text = f"{stat.capitalize()}: +{bonus}"
                bonus_surface = self.stat_font.render(bonus_text, True, GREEN)
                surface.blit(bonus_surface, (stats_x, stats_y))
                stats_y += 25
        else:
            no_bonus_text = self.stat_font.render("No equipment bonuses", True, LIGHT_GRAY)
            surface.blit(no_bonus_text, (stats_x, stats_y))

        # Show current HP/AP
        stats_y += 20
        hp_text = f"HP: {self.character.current_hp}/{self.character.max_hp}"
        hp_surface = self.stat_font.render(hp_text, True, RED)
        surface.blit(hp_surface, (stats_x, stats_y))
        stats_y += 25

        if self.character.max_ap > 0:
            ap_text = f"AP: {self.character.current_ap}/{self.character.max_ap}"
            ap_surface = self.stat_font.render(ap_text, True, BLUE)
            surface.blit(ap_surface, (stats_x, stats_y))

    def set_visible(self, visible: bool):
        """Set menu visibility."""
        if visible:
            self.show()
        else:
            self.hide()
