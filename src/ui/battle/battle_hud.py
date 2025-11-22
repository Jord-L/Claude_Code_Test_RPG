"""
Battle HUD (Heads-Up Display)
Displays HP bars, turn order, and status information during battle.
"""

import pygame
from typing import List, Optional
from entities.character import Character
from utils.constants import *


class HPBar:
    """Visual HP bar for a single character."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initialize HP bar.
        
        Args:
            x: X position
            y: Y position
            width: Bar width
            height: Bar height
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        
        # Colors
        self.bg_color = DARK_GRAY
        self.hp_color = GREEN
        self.hp_low_color = YELLOW
        self.hp_critical_color = RED
        self.border_color = WHITE
        
        # Font
        self.font = pygame.font.Font(None, 20)
    
    def render(self, surface: pygame.Surface, character: Character, show_name: bool = True):
        """
        Render HP bar for a character.
        
        Args:
            surface: Surface to draw on
            character: Character to display
            show_name: Whether to show character name
        """
        if not self.visible:
            return
        
        # Calculate HP percentage
        hp_percent = character.current_hp / character.max_hp if character.max_hp > 0 else 0
        
        # Determine HP color
        if hp_percent > 0.5:
            hp_color = self.hp_color
        elif hp_percent > 0.25:
            hp_color = self.hp_low_color
        else:
            hp_color = self.hp_critical_color
        
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        
        # Draw HP fill
        fill_width = int(self.rect.width * hp_percent)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(surface, hp_color, fill_rect)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        
        # Draw HP text (centered in bar)
        hp_text = f"{character.current_hp}/{character.max_hp}"
        hp_surface = self.font.render(hp_text, True, WHITE)
        hp_x = self.rect.centerx - hp_surface.get_width() // 2
        hp_y = self.rect.centery - hp_surface.get_height() // 2
        surface.blit(hp_surface, (hp_x, hp_y))
        
        # Draw name above bar
        if show_name:
            name_surface = self.font.render(character.name, True, WHITE)
            name_x = self.rect.x
            name_y = self.rect.y - 25
            surface.blit(name_surface, (name_x, name_y))
        
        # Draw level
        if show_name:
            level_text = f"Lv.{character.level}"
            level_surface = self.font.render(level_text, True, LIGHT_GRAY)
            level_x = self.rect.right - level_surface.get_width()
            level_y = self.rect.y - 25
            surface.blit(level_surface, (level_x, level_y))
        
        # Draw status effects (if any)
        # TODO: Implement status effect icons


class APBar:
    """Visual AP (Ability Points) bar for Devil Fruit users."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initialize AP bar.
        
        Args:
            x: X position
            y: Y position
            width: Bar width
            height: Bar height
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        
        # Colors
        self.bg_color = DARK_GRAY
        self.ap_color = CYAN
        self.border_color = WHITE
        
        # Font
        self.font = pygame.font.Font(None, 18)
    
    def render(self, surface: pygame.Surface, character: Character):
        """
        Render AP bar for a character.
        
        Args:
            surface: Surface to draw on
            character: Character to display
        """
        if not self.visible:
            return
        
        # Skip if character has no AP
        if character.max_ap <= 0:
            return
        
        # Calculate AP percentage
        ap_percent = character.current_ap / character.max_ap if character.max_ap > 0 else 0
        
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        
        # Draw AP fill
        fill_width = int(self.rect.width * ap_percent)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(surface, self.ap_color, fill_rect)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, 1)
        
        # Draw AP text
        ap_text = f"AP: {character.current_ap}/{character.max_ap}"
        ap_surface = self.font.render(ap_text, True, WHITE)
        ap_x = self.rect.centerx - ap_surface.get_width() // 2
        ap_y = self.rect.centery - ap_surface.get_height() // 2
        surface.blit(ap_surface, (ap_x, ap_y))


class BattleHUD:
    """
    Main battle HUD showing all combatant information.
    """
    
    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize battle HUD.
        
        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.visible = True
        
        # Player party display area (left side)
        self.player_area_rect = pygame.Rect(20, 20, 300, screen_height - 40)
        
        # Enemy display area (right side)
        self.enemy_area_rect = pygame.Rect(screen_width - 320, 20, 300, screen_height - 40)
        
        # Turn order display (top center)
        self.turn_order_rect = pygame.Rect(340, 10, screen_width - 680, 80)
        
        # Battle log area (bottom center)
        self.battle_log_rect = pygame.Rect(340, screen_height - 200, screen_width - 680, 180)
        
        # Colors
        self.bg_color = UI_BG_COLOR
        self.border_color = UI_BORDER_COLOR
        self.text_color = WHITE
        self.current_turn_color = UI_HIGHLIGHT_COLOR
        
        # Fonts
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 28)
        self.log_font = pygame.font.Font(None, 22)
        
        # HP/AP bars
        self.player_hp_bars: List[HPBar] = []
        self.player_ap_bars: List[APBar] = []
        self.enemy_hp_bars: List[HPBar] = []
        
        # Battle log
        self.log_messages: List[str] = []
        self.max_log_lines = 7
        
        # Current turn indicator
        self.current_actor: Optional[Character] = None
    
    def setup_combatants(self, player_party: List[Character], enemies: List[Character]):
        """
        Set up HUD for combatants.
        
        Args:
            player_party: List of player characters
            enemies: List of enemy characters
        """
        # Clear existing bars
        self.player_hp_bars.clear()
        self.player_ap_bars.clear()
        self.enemy_hp_bars.clear()
        
        # Create HP/AP bars for players
        bar_spacing = 80
        for i, player in enumerate(player_party):
            y_pos = self.player_area_rect.y + 10 + (i * bar_spacing)
            
            # HP bar
            hp_bar = HPBar(
                self.player_area_rect.x + 10,
                y_pos,
                self.player_area_rect.width - 20,
                30
            )
            self.player_hp_bars.append(hp_bar)
            
            # AP bar (below HP bar)
            ap_bar = APBar(
                self.player_area_rect.x + 10,
                y_pos + 35,
                self.player_area_rect.width - 20,
                15
            )
            self.player_ap_bars.append(ap_bar)
        
        # Create HP bars for enemies
        for i, enemy in enumerate(enemies):
            y_pos = self.enemy_area_rect.y + 10 + (i * bar_spacing)
            
            hp_bar = HPBar(
                self.enemy_area_rect.x + 10,
                y_pos,
                self.enemy_area_rect.width - 20,
                30
            )
            self.enemy_hp_bars.append(hp_bar)
    
    def set_current_actor(self, actor: Optional[Character]):
        """
        Set the character whose turn it currently is.
        
        Args:
            actor: Current actor
        """
        self.current_actor = actor
    
    def add_log_message(self, message: str):
        """
        Add a message to the battle log.
        
        Args:
            message: Message to add
        """
        self.log_messages.append(message)
        
        # Keep only recent messages
        if len(self.log_messages) > self.max_log_lines:
            self.log_messages = self.log_messages[-self.max_log_lines:]
    
    def clear_log(self):
        """Clear battle log."""
        self.log_messages.clear()
    
    def update(self, dt: float):
        """
        Update HUD state.
        
        Args:
            dt: Delta time in seconds
        """
        # Could add animations here
        pass
    
    def render(self, surface: pygame.Surface, player_party: List[Character], enemies: List[Character], turn_order: List[Character]):
        """
        Render the battle HUD.
        
        Args:
            surface: Surface to draw on
            player_party: List of player characters
            enemies: List of enemy characters
            turn_order: List showing turn order
        """
        if not self.visible:
            return
        
        # Render player area
        self._render_player_area(surface, player_party)
        
        # Render enemy area
        self._render_enemy_area(surface, enemies)
        
        # Render turn order
        self._render_turn_order(surface, turn_order)
        
        # Render battle log
        self._render_battle_log(surface)
    
    def _render_player_area(self, surface: pygame.Surface, player_party: List[Character]):
        """Render player party information."""
        # Draw background panel
        pygame.draw.rect(surface, self.bg_color, self.player_area_rect)
        pygame.draw.rect(surface, self.border_color, self.player_area_rect, 2)
        
        # Draw title
        title_surface = self.title_font.render("Your Party", True, self.text_color)
        title_x = self.player_area_rect.x + 10
        title_y = self.player_area_rect.y - 30
        surface.blit(title_surface, (title_x, title_y))
        
        # Draw HP and AP bars for each player
        for i, (player, hp_bar, ap_bar) in enumerate(zip(player_party, self.player_hp_bars, self.player_ap_bars)):
            # Highlight if it's this player's turn
            is_current = (player == self.current_actor)
            
            if is_current:
                highlight_rect = pygame.Rect(
                    hp_bar.rect.x - 5,
                    hp_bar.rect.y - 30,
                    hp_bar.rect.width + 10,
                    65
                )
                pygame.draw.rect(surface, self.current_turn_color, highlight_rect, 3)
            
            hp_bar.render(surface, player, show_name=True)
            ap_bar.render(surface, player)
    
    def _render_enemy_area(self, surface: pygame.Surface, enemies: List[Character]):
        """Render enemy information."""
        # Draw background panel
        pygame.draw.rect(surface, self.bg_color, self.enemy_area_rect)
        pygame.draw.rect(surface, self.border_color, self.enemy_area_rect, 2)
        
        # Draw title
        title_surface = self.title_font.render("Enemies", True, self.text_color)
        title_x = self.enemy_area_rect.x + 10
        title_y = self.enemy_area_rect.y - 30
        surface.blit(title_surface, (title_x, title_y))
        
        # Draw HP bars for each enemy
        for i, (enemy, hp_bar) in enumerate(zip(enemies, self.enemy_hp_bars)):
            # Skip defeated enemies (make bar semi-transparent or gray)
            if not enemy.is_alive:
                # Could add visual indication of defeat
                pass
            
            # Highlight if it's this enemy's turn
            is_current = (enemy == self.current_actor)
            
            if is_current:
                highlight_rect = pygame.Rect(
                    hp_bar.rect.x - 5,
                    hp_bar.rect.y - 30,
                    hp_bar.rect.width + 10,
                    50
                )
                pygame.draw.rect(surface, self.current_turn_color, highlight_rect, 3)
            
            hp_bar.render(surface, enemy, show_name=True)
    
    def _render_turn_order(self, surface: pygame.Surface, turn_order: List[Character]):
        """Render turn order display."""
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.turn_order_rect)
        pygame.draw.rect(surface, self.border_color, self.turn_order_rect, 2)
        
        # Draw title
        title_surface = self.font.render("Turn Order:", True, self.text_color)
        title_x = self.turn_order_rect.x + 10
        title_y = self.turn_order_rect.y + 10
        surface.blit(title_surface, (title_x, title_y))
        
        # Draw next few turns
        name_x = self.turn_order_rect.x + 120
        name_y = self.turn_order_rect.y + 10
        name_spacing = 25
        
        max_shown = 3  # Show next 3 turns
        shown_count = 0
        
        for character in turn_order[:max_shown]:
            if not character.is_alive:
                continue
            
            # Highlight current turn
            is_current = (character == self.current_actor)
            color = self.current_turn_color if is_current else self.text_color
            
            # Draw arrow for current
            if is_current:
                arrow_surface = self.font.render("▶", True, color)
                surface.blit(arrow_surface, (name_x - 20, name_y + (shown_count * name_spacing)))
            
            # Draw name
            name_surface = self.font.render(character.name, True, color)
            surface.blit(name_surface, (name_x, name_y + (shown_count * name_spacing)))
            
            shown_count += 1
    
    def _render_battle_log(self, surface: pygame.Surface):
        """Render battle log messages."""
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.battle_log_rect)
        pygame.draw.rect(surface, self.border_color, self.battle_log_rect, 2)
        
        # Draw title
        title_surface = self.title_font.render("Battle Log", True, self.text_color)
        title_x = self.battle_log_rect.x + 10
        title_y = self.battle_log_rect.y + 5
        surface.blit(title_surface, (title_x, title_y))
        
        # Draw separator
        line_y = self.battle_log_rect.y + 35
        pygame.draw.line(
            surface,
            self.border_color,
            (self.battle_log_rect.x + 10, line_y),
            (self.battle_log_rect.right - 10, line_y),
            1
        )
        
        # Draw log messages (most recent at bottom)
        message_y = self.battle_log_rect.y + 40
        message_spacing = 20
        
        for i, message in enumerate(self.log_messages):
            if not message:  # Skip empty lines
                message_y += message_spacing
                continue
            
            # Truncate long messages
            if len(message) > 70:
                message = message[:67] + "..."
            
            message_surface = self.log_font.render(message, True, self.text_color)
            surface.blit(message_surface, (self.battle_log_rect.x + 15, message_y))
            message_y += message_spacing
    
    def set_visible(self, visible: bool):
        """Set HUD visibility."""
        self.visible = visible
