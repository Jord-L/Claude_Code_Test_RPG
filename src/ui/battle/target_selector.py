"""
Target Selector
UI for selecting targets during battle (enemies or allies).
"""

import pygame
from typing import List, Optional, Callable
from entities.character import Character
from utils.constants import *


class TargetSelector:
    """
    Interface for selecting targets in battle.
    Shows available targets with visual indicators.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initialize target selector.
        
        Args:
            x: X position
            y: Y position
            width: Selector width
            height: Selector height
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = False
        self.active = False
        
        # Targets
        self.targets: List[Character] = []
        self.selected_index = 0
        
        # Layout
        self.padding = 15
        self.target_height = 60
        self.target_spacing = 10
        
        # Colors
        self.bg_color = UI_BG_COLOR
        self.border_color = UI_BORDER_COLOR
        self.text_color = WHITE
        self.highlight_color = UI_HIGHLIGHT_COLOR
        self.dead_color = DARK_GRAY
        
        # Fonts
        self.font = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 32)
        self.info_font = pygame.font.Font(None, 22)
        
        # Title
        self.title = "Select Target"
        
        # Callbacks
        self.on_target_selected: Optional[Callable] = None
        self.on_cancel: Optional[Callable] = None
        
        # Selection mode
        self.allow_dead_targets = False  # For resurrection items/abilities
    
    def set_targets(self, targets: List[Character], allow_dead: bool = False):
        """
        Set available targets.
        
        Args:
            targets: List of characters that can be targeted
            allow_dead: Whether dead characters can be selected
        """
        self.targets = targets
        self.allow_dead_targets = allow_dead
        self.selected_index = 0
        self._ensure_valid_selection()
    
    def _ensure_valid_selection(self):
        """Ensure selected index points to a valid target."""
        if not self.targets:
            self.selected_index = 0
            return
        
        # If current selection is invalid, find next valid target
        if not self._is_valid_target(self.selected_index):
            self._move_selection(1)
    
    def _is_valid_target(self, index: int) -> bool:
        """
        Check if target at index is valid.
        
        Args:
            index: Target index
        
        Returns:
            True if target is valid
        """
        if not (0 <= index < len(self.targets)):
            return False
        
        target = self.targets[index]
        
        # Check if alive (unless dead targets allowed)
        if not self.allow_dead_targets and not target.is_alive:
            return False
        
        return True
    
    def _move_selection(self, direction: int):
        """
        Move selection up or down.
        
        Args:
            direction: 1 for down, -1 for up
        """
        if not self.targets:
            return
        
        start_index = self.selected_index
        attempts = 0
        max_attempts = len(self.targets)
        
        while attempts < max_attempts:
            self.selected_index = (self.selected_index + direction) % len(self.targets)
            
            if self._is_valid_target(self.selected_index):
                return  # Found a valid target
            
            attempts += 1
        
        # If we couldn't find a valid target, revert
        self.selected_index = start_index
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle input events.
        
        Args:
            event: Pygame event
        
        Returns:
            True if event was handled
        """
        if not self.visible or not self.active:
            return False
        
        # Keyboard navigation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self._move_selection(-1)
                return True
            
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self._move_selection(1)
                return True
            
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._select_current_target()
                return True
            
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                if self.on_cancel:
                    self.on_cancel()
                return True
        
        # Mouse navigation
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            target_index = self._get_target_at_position(mouse_pos)
            if target_index is not None and self._is_valid_target(target_index):
                self.selected_index = target_index
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = event.pos
                target_index = self._get_target_at_position(mouse_pos)
                if target_index is not None and self._is_valid_target(target_index):
                    self.selected_index = target_index
                    self._select_current_target()
                    return True
        
        return False
    
    def _get_target_at_position(self, pos: tuple) -> Optional[int]:
        """
        Get target index at mouse position.
        
        Args:
            pos: Mouse position (x, y)
        
        Returns:
            Target index or None
        """
        if not self.rect.collidepoint(pos):
            return None
        
        # Calculate which target the mouse is over
        content_y = self.rect.y + 50  # After title
        
        for i, target in enumerate(self.targets):
            target_rect = pygame.Rect(
                self.rect.x + self.padding,
                content_y + i * (self.target_height + self.target_spacing),
                self.rect.width - self.padding * 2,
                self.target_height
            )
            
            if target_rect.collidepoint(pos):
                return i
        
        return None
    
    def _select_current_target(self):
        """Execute selection of current target."""
        if not self.targets or not self._is_valid_target(self.selected_index):
            return
        
        selected_target = self.targets[self.selected_index]
        
        # Call callback
        if self.on_target_selected:
            self.on_target_selected(selected_target)
    
    def update(self, dt: float):
        """
        Update selector state.
        
        Args:
            dt: Delta time in seconds
        """
        pass
    
    def render(self, surface: pygame.Surface):
        """
        Draw the target selector.
        
        Args:
            surface: Surface to draw on
        """
        if not self.visible:
            return
        
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        
        # Draw border
        border_color = self.border_color if self.active else DARK_GRAY
        pygame.draw.rect(surface, border_color, self.rect, 3)
        
        # Draw title
        title_surface = self.title_font.render(self.title, True, self.text_color)
        title_x = self.rect.x + (self.rect.width - title_surface.get_width()) // 2
        title_y = self.rect.y + 10
        surface.blit(title_surface, (title_x, title_y))
        
        # Draw separator line
        line_y = self.rect.y + 45
        pygame.draw.line(
            surface,
            self.border_color,
            (self.rect.x + self.padding, line_y),
            (self.rect.right - self.padding, line_y),
            2
        )
        
        # Draw targets
        content_y = self.rect.y + 50
        
        for i, target in enumerate(self.targets):
            self._render_target(surface, target, i, content_y)
        
        # Draw hint text
        hint_text = "↑↓ Select | Enter: Confirm | Esc: Cancel"
        hint_surface = self.info_font.render(hint_text, True, LIGHT_GRAY)
        hint_x = self.rect.x + (self.rect.width - hint_surface.get_width()) // 2
        hint_y = self.rect.bottom - 25
        surface.blit(hint_surface, (hint_x, hint_y))
    
    def _render_target(self, surface: pygame.Surface, target: Character, index: int, start_y: int):
        """
        Render a single target option.
        
        Args:
            surface: Surface to draw on
            target: Target character
            index: Target index
            start_y: Y position to start rendering
        """
        target_y = start_y + index * (self.target_height + self.target_spacing)
        target_rect = pygame.Rect(
            self.rect.x + self.padding,
            target_y,
            self.rect.width - self.padding * 2,
            self.target_height
        )
        
        # Determine colors and validity
        is_selected = (index == self.selected_index)
        is_valid = self._is_valid_target(index)
        is_alive = target.is_alive
        
        if not is_alive:
            bg_color = self.dead_color
            text_color = GRAY
        elif is_selected and is_valid:
            bg_color = self.highlight_color
            text_color = BLACK
        elif is_valid:
            bg_color = GRAY
            text_color = self.text_color
        else:
            bg_color = DARK_GRAY
            text_color = GRAY
        
        # Draw target background
        pygame.draw.rect(surface, bg_color, target_rect)
        pygame.draw.rect(surface, self.border_color, target_rect, 2)
        
        # Draw selection indicator
        if is_selected and self.active and is_valid:
            indicator_rect = pygame.Rect(
                target_rect.x + 5,
                target_rect.centery - 15,
                5,
                30
            )
            pygame.draw.rect(surface, RED, indicator_rect)
        
        # Draw target name
        name_surface = self.font.render(target.name, True, text_color)
        name_x = target_rect.x + 20
        name_y = target_rect.y + 8
        surface.blit(name_surface, (name_x, name_y))
        
        # Draw level
        level_text = f"Lv.{target.level}"
        level_surface = self.info_font.render(level_text, True, text_color)
        level_x = target_rect.right - level_surface.get_width() - 10
        level_y = target_rect.y + 8
        surface.blit(level_surface, (level_x, level_y))
        
        # Draw HP bar (small)
        hp_bar_rect = pygame.Rect(
            target_rect.x + 20,
            target_rect.y + 35,
            target_rect.width - 40,
            15
        )
        
        # HP background
        pygame.draw.rect(surface, DARK_GRAY, hp_bar_rect)
        
        # HP fill
        hp_percent = target.current_hp / target.max_hp if target.max_hp > 0 else 0
        fill_width = int(hp_bar_rect.width * hp_percent)
        
        if fill_width > 0:
            # Color based on HP
            if hp_percent > 0.5:
                hp_color = GREEN
            elif hp_percent > 0.25:
                hp_color = YELLOW
            else:
                hp_color = RED
            
            fill_rect = pygame.Rect(hp_bar_rect.x, hp_bar_rect.y, fill_width, hp_bar_rect.height)
            pygame.draw.rect(surface, hp_color, fill_rect)
        
        # HP border
        pygame.draw.rect(surface, WHITE, hp_bar_rect, 1)
        
        # HP text
        hp_text = f"{target.current_hp}/{target.max_hp}"
        hp_text_surface = self.info_font.render(hp_text, True, text_color)
        hp_text_x = hp_bar_rect.centerx - hp_text_surface.get_width() // 2
        hp_text_y = hp_bar_rect.centery - hp_text_surface.get_height() // 2
        surface.blit(hp_text_surface, (hp_text_x, hp_text_y))
        
        # Draw status (Defeated, etc.)
        if not is_alive:
            status_surface = self.font.render("[DEFEATED]", True, RED)
            status_x = target_rect.right - status_surface.get_width() - 10
            status_y = target_rect.y + 35
            surface.blit(status_surface, (status_x, status_y))
    
    def set_active(self, active: bool):
        """
        Set whether selector is active (can receive input).
        
        Args:
            active: Active state
        """
        self.active = active
    
    def set_visible(self, visible: bool):
        """
        Set selector visibility.
        
        Args:
            visible: Visible state
        """
        self.visible = visible
    
    def get_selected_target(self) -> Optional[Character]:
        """
        Get the currently selected target.
        
        Returns:
            Selected character or None
        """
        if self.targets and 0 <= self.selected_index < len(self.targets):
            if self._is_valid_target(self.selected_index):
                return self.targets[self.selected_index]
        return None
    
    def show(self, targets: List[Character], allow_dead: bool = False):
        """
        Show the target selector with given targets.
        
        Args:
            targets: List of targetable characters
            allow_dead: Whether dead characters can be selected
        """
        self.set_targets(targets, allow_dead)
        self.set_visible(True)
        self.set_active(True)
    
    def hide(self):
        """Hide the target selector."""
        self.set_visible(False)
        self.set_active(False)
