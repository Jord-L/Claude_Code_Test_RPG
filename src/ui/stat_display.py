"""
Stat Display Component
Displays character statistics in a formatted panel.
"""

import pygame
from typing import Optional
from entities.character import Character
from utils.constants import *


class StatDisplay:
    """
    Displays character stats in a clean, organized format.
    Shows HP, AP, and all base stats.
    """
    
    def __init__(self, x: int, y: int, width: int = 250, height: int = 200):
        """
        Initialize stat display.
        
        Args:
            x: X position (top-left)
            y: Y position (top-left)
            width: Display width
            height: Display height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Character data
        self.character: Optional[Character] = None
        
        # Fonts
        self.header_font = pygame.font.Font(None, 24)
        self.stat_font = pygame.font.Font(None, 20)
        self.value_font = pygame.font.Font(None, 20)
        
        # Colors
        self.bg_color = (30, 30, 50)
        self.border_color = UI_BORDER_COLOR
        self.header_color = UI_HIGHLIGHT_COLOR
        self.label_color = LIGHT_GRAY
        self.value_color = WHITE
        self.hp_color = GREEN
        self.ap_color = CYAN
    
    def set_character(self, character: Character):
        """
        Set the character to display.
        
        Args:
            character: Character instance
        """
        self.character = character
    
    def update(self, dt: float):
        """
        Update display.
        
        Args:
            dt: Delta time
        """
        pass  # Static display for now
    
    def render(self, screen: pygame.Surface):
        """
        Render the stat display.
        
        Args:
            screen: Surface to render to
        """
        if not self.character:
            self._render_placeholder(screen)
            return
        
        # Draw background
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.bg_color, bg_rect)
        pygame.draw.rect(screen, self.border_color, bg_rect, 2)
        
        # Draw header
        self._render_header(screen)
        
        # Draw HP and AP
        self._render_vitals(screen)
        
        # Draw base stats
        self._render_stats(screen)
    
    def _render_placeholder(self, screen: pygame.Surface):
        """Render placeholder when no character is set."""
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, GRAY, bg_rect)
        pygame.draw.rect(screen, WHITE, bg_rect, 2)
        
        text = self.header_font.render("No Character", True, WHITE)
        text_rect = text.get_rect(
            center=(self.x + self.width // 2, self.y + self.height // 2)
        )
        screen.blit(text, text_rect)
    
    def _render_header(self, screen: pygame.Surface):
        """Render the header section."""
        header_text = self.header_font.render("Stats", True, self.header_color)
        screen.blit(header_text, (self.x + 10, self.y + 10))
        
        # Level
        level_text = self.stat_font.render(
            f"Lv. {self.character.level}",
            True,
            self.value_color
        )
        screen.blit(
            level_text,
            (self.x + self.width - level_text.get_width() - 10, self.y + 12)
        )
        
        # Divider line
        pygame.draw.line(
            screen,
            self.border_color,
            (self.x + 5, self.y + 40),
            (self.x + self.width - 5, self.y + 40),
            2
        )
    
    def _render_vitals(self, screen: pygame.Surface):
        """Render HP and AP bars."""
        vitals_y = self.y + 50
        
        # HP
        hp_label = self.stat_font.render("HP:", True, self.label_color)
        screen.blit(hp_label, (self.x + 10, vitals_y))
        
        hp_text = self.value_font.render(
            f"{self.character.current_hp}/{self.character.max_hp}",
            True,
            self.hp_color
        )
        screen.blit(hp_text, (self.x + 50, vitals_y))
        
        # HP bar
        bar_width = self.width - 70
        bar_height = 8
        bar_x = self.x + 50
        bar_y = vitals_y + 25
        
        # Background
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, (50, 50, 50), bg_rect)
        
        # Fill
        hp_percent = self.character.get_hp_percentage()
        fill_width = int(bar_width * hp_percent)
        fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
        pygame.draw.rect(screen, self.hp_color, fill_rect)
        
        # Border
        pygame.draw.rect(screen, WHITE, bg_rect, 1)
        
        # AP
        ap_y = vitals_y + 40
        ap_label = self.stat_font.render("AP:", True, self.label_color)
        screen.blit(ap_label, (self.x + 10, ap_y))
        
        ap_text = self.value_font.render(
            f"{self.character.current_ap}/{self.character.max_ap}",
            True,
            self.ap_color
        )
        screen.blit(ap_text, (self.x + 50, ap_y))
        
        # AP bar
        ap_bar_y = ap_y + 25
        
        # Background
        bg_rect = pygame.Rect(bar_x, ap_bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, (50, 50, 50), bg_rect)
        
        # Fill
        ap_percent = self.character.get_ap_percentage()
        fill_width = int(bar_width * ap_percent)
        fill_rect = pygame.Rect(bar_x, ap_bar_y, fill_width, bar_height)
        pygame.draw.rect(screen, self.ap_color, fill_rect)
        
        # Border
        pygame.draw.rect(screen, WHITE, bg_rect, 1)
    
    def _render_stats(self, screen: pygame.Surface):
        """Render base character stats."""
        stats_start_y = self.y + 145
        line_height = 22
        
        # Get stats from character
        stats_data = [
            ("STR", self.character.stats.get_strength()),
            ("DEF", self.character.stats.get_defense_value()),
            ("AGI", self.character.stats.get_agility()),
            ("INT", self.character.stats.get_intelligence()),
            ("WILL", self.character.stats.get_willpower()),
        ]
        
        # Render in two columns
        col1_x = self.x + 15
        col2_x = self.x + self.width // 2 + 15
        
        for i, (stat_name, stat_value) in enumerate(stats_data):
            if i < 3:
                # Left column
                x = col1_x
                y = stats_start_y + i * line_height
            else:
                # Right column
                x = col2_x
                y = stats_start_y + (i - 3) * line_height
            
            # Stat name
            label = self.stat_font.render(f"{stat_name}:", True, self.label_color)
            screen.blit(label, (x, y))
            
            # Stat value
            value = self.value_font.render(str(stat_value), True, self.value_color)
            value_x = x + 50
            screen.blit(value, (value_x, y))
            
            # Bonus indicator if from Devil Fruit
            if self.character.devil_fruit:
                modifiers = self.character.devil_fruit.get_stat_modifiers()
                percent_mods = self.character.devil_fruit.get_percent_modifiers()
                
                # Check if this stat has a bonus
                stat_key = stat_name.lower()
                has_bonus = (stat_key in modifiers or stat_key in percent_mods)
                
                if has_bonus:
                    # Draw fruit indicator
                    fruit_color = self._get_fruit_color()
                    bonus_marker = self.stat_font.render("+", True, fruit_color)
                    screen.blit(bonus_marker, (value_x + value.get_width() + 5, y))
    
    def _get_fruit_color(self) -> tuple:
        """
        Get color based on Devil Fruit type.
        
        Returns:
            RGB color tuple
        """
        if not self.character or not self.character.devil_fruit:
            return WHITE
        
        fruit_type = self.character.devil_fruit.fruit_type
        
        if fruit_type == "logia":
            return (255, 100, 100)  # Red
        elif fruit_type == "zoan":
            return (255, 200, 100)  # Orange
        elif fruit_type == "paramecia":
            return (150, 100, 255)  # Purple
        
        return WHITE
    
    def get_rect(self) -> pygame.Rect:
        """
        Get the bounding rectangle.
        
        Returns:
            Pygame Rect
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)
