"""
Battle State
Game state for turn-based combat encounters.
Connects world exploration to the combat system.
"""

import pygame
import random
from typing import List, Optional
from states.state import State
from entities.player import Player
from entities.enemy import EnemyFactory
from combat.battle_manager import BattleManager
from ui.battle.battle_ui import BattleUI, UIState
from combat.combat_action import ActionFactory
from combat.enemy_ai import EnemyAI
from utils.constants import *
from utils.logger import get_logger


class BattleState(State):
    """
    Game state for combat encounters.
    """
    
    def __init__(self, game):
        """
        Initialize battle state.
        
        Args:
            game: Main game instance
        """
        super().__init__(game)
        
        self.logger = get_logger()
        
        # Battle components
        self.battle_manager: Optional[BattleManager] = None
        self.battle_ui: Optional[BattleUI] = None
        
        # Enemy AI controllers
        self.enemy_ais: List[EnemyAI] = []
        
        # State tracking
        self.battle_over = False
        self.victory = False
        self.return_to_world = False
        
        # Persistent data for return trip
        self.player_data = None
        self.world_data = None
    
    def startup(self, persistent):
        """
        Called when state becomes active.
        
        Args:
            persistent: Data from previous state
        """
        self.logger.info("Battle State: Starting up...")
        
        # Get player from persistent data
        if "player" not in persistent:
            self.logger.error("No player data provided to battle state!")
            raise ValueError("Battle state requires player data")
        
        player = persistent["player"]
        self.player_data = persistent
        
        # Check if returning from world
        self.return_to_world = persistent.get("return_to_world", False)
        if self.return_to_world:
            self.logger.info("Battle triggered from world exploration")
            self.world_data = {
                "current_map": persistent.get("current_map"),
                "player_position": persistent.get("player_position")
            }
        
        # Create enemy party
        enemies = self._create_enemy_party(player.level)
        self.logger.info(f"Created enemy party: {[e.name for e in enemies]}")
        
        # Create battle manager
        # Use party if available, otherwise just the player
        if hasattr(player, 'party_manager') and player.party_manager:
            player_party = player.party_manager.get_active_party()
        else:
            player_party = [player]

        self.battle_manager = BattleManager(player_party, enemies)
        
        # Create battle UI
        self.battle_ui = BattleUI(self.battle_manager)
        
        # Create AI controllers for enemies
        self.enemy_ais = []
        for enemy in enemies:
            ai = EnemyAI(enemy)
            ai.set_difficulty(enemy.ai_difficulty)
            ai.set_personality(enemy.ai_personality)
            self.enemy_ais.append(ai)
            self.logger.debug(f"Created AI for {enemy.name}: {enemy.ai_personality} / {enemy.ai_difficulty}")
        
        # Reset state
        self.battle_over = False
        self.victory = False
        
        self.logger.info(f"Battle started: Player vs {len(enemies)} enemies")
    
    def _create_enemy_party(self, player_level: int) -> List:
        """
        Create an enemy party based on player level.
        
        Args:
            player_level: Player's current level
        
        Returns:
            List of Enemy instances
        """
        # Determine number of enemies (1-3 for now)
        num_enemies = random.randint(1, 3)
        
        # Select enemy types based on level
        enemy_types = []
        if player_level < 3:
            enemy_types = ["bandit", "bandit", "marine_soldier"]
        elif player_level < 6:
            enemy_types = ["marine_soldier", "pirate", "sea_beast"]
        else:
            enemy_types = ["pirate", "sea_beast", "boss"]
        
        # Create enemies
        enemies = []
        for i in range(num_enemies):
            enemy_type = random.choice(enemy_types)
            
            # Adjust level slightly
            enemy_level = player_level + random.randint(-1, 1)
            enemy_level = max(1, enemy_level)
            
            # Create enemy
            enemy = EnemyFactory.create_enemy(enemy_type, enemy_level)
            enemy.name = f"{enemy.name} {i+1}" if num_enemies > 1 else enemy.name
            enemies.append(enemy)
        
        return enemies
    
    def cleanup(self):
        """
        Called when leaving state.
        
        Returns:
            Persistent data dictionary
        """
        persist = {
            "player": self.battle_manager.player_party[0] if self.battle_manager else self.player_data.get("player")
        }
        
        # If returning to world, include world data
        if self.return_to_world and self.world_data:
            persist.update(self.world_data)
        
        return persist
    
    def handle_event(self, event):
        """
        Handle pygame events.
        
        Args:
            event: Pygame event
        """
        # Pass events to battle UI
        if self.battle_ui and not self.battle_over:
            self.battle_ui.handle_event(event)
        
        # Handle result screen inputs
        if self.battle_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self._end_battle()
    
    def update(self, dt):
        """
        Update battle state.
        
        Args:
            dt: Delta time in seconds
        """
        if self.battle_over:
            return
        
        # Update battle UI
        if self.battle_ui:
            self.battle_ui.update(dt)
        
        # Check battle manager state
        if not self.battle_manager.battle_active:
            self._handle_battle_end()
            return
        
        # Handle turn logic
        if self.battle_manager.is_player_turn():
            self._handle_player_turn()
        else:
            self._handle_enemy_turn()
    
    def _handle_player_turn(self):
        """Handle player's turn."""
        # UI handles player input and action execution
        # Check if player submitted an action
        if self.battle_ui.state == UIState.WAITING:
            action = self.battle_ui.get_selected_action()
            
            if action:
                self.logger.info(f"Player action: {action.get_description()}")
                
                # Execute action
                self.battle_manager.execute_action(action)
                
                # Reset UI
                self.battle_ui.reset_for_next_turn()
    
    def _handle_enemy_turn(self):
        """Handle enemy's turn."""
        actor = self.battle_manager.current_actor
        
        # Find AI for this enemy
        ai = None
        for enemy_ai in self.enemy_ais:
            if enemy_ai.enemy == actor:
                ai = enemy_ai
                break
        
        if not ai:
            self.logger.error(f"No AI found for enemy: {actor.name}")
            # Skip turn
            self.battle_manager.advance_turn()
            return
        
        # AI chooses action
        all_enemies = self.battle_manager.enemy_party
        all_allies = self.battle_manager.player_party
        
        action = ai.choose_action(all_enemies, all_allies)
        
        if action:
            self.logger.info(f"Enemy action: {action.get_description()}")
            self.battle_manager.execute_action(action)
        else:
            self.logger.warning(f"AI returned no action for {actor.name}")
            self.battle_manager.advance_turn()
    
    def _handle_battle_end(self):
        """Handle battle completion."""
        self.logger.info("Battle ended!")
        
        # Determine outcome
        if self.battle_manager.is_victory():
            self.victory = True
            self._handle_victory()
        else:
            self.victory = False
            self._handle_defeat()
        
        self.battle_over = True
    
    def _handle_victory(self):
        """Handle battle victory."""
        self.logger.info("Victory!")
        
        # Get rewards
        rewards = self.battle_manager.get_rewards()
        
        # Apply rewards to player
        player = self.battle_manager.player_party[0]
        
        # Award experience
        old_level = player.level
        player.gain_experience(rewards["experience"])
        new_level = player.level
        
        # Award berries
        player.berries += rewards["berries"]
        
        self.logger.info(f"Rewards: {rewards['experience']} XP, {rewards['berries']} Berries")
        
        if new_level > old_level:
            self.logger.info(f"Level up! {old_level} -> {new_level}")
            # Camera shake for level up
            # self.game.camera.shake(10, 0.5)  # If camera exists
    
    def _handle_defeat(self):
        """Handle battle defeat."""
        self.logger.info("Defeat!")
        
        # TODO: Implement game over or return to menu
        # For now, just return to world with reduced HP
        player = self.battle_manager.player_party[0]
        player.current_hp = max(1, player.max_hp // 4)  # 25% HP
        
        self.logger.info(f"Player survived with {player.current_hp} HP")
    
    def _end_battle(self):
        """End battle and transition to next state."""
        self.logger.info("Ending battle state...")
        
        # Mark state as done
        self.done = True
        
        if self.return_to_world:
            # Return to world
            self.next_state = "world"
            self.logger.info("Returning to world state")
        else:
            # Go to menu
            self.next_state = "menu"
            self.logger.info("Returning to main menu")
    
    def render(self, surface):
        """
        Render battle state.
        
        Args:
            surface: Surface to draw on
        """
        # Clear screen
        surface.fill(BLACK)
        
        # Render battle UI
        if self.battle_ui:
            self.battle_ui.render(surface)
        
        # Render result overlay if battle is over
        if self.battle_over:
            self._render_result_screen(surface)
    
    def _render_result_screen(self, surface: pygame.Surface):
        """Render victory/defeat screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        # Title
        title_font = pygame.font.Font(None, 80)
        if self.victory:
            title_text = title_font.render("VICTORY!", True, GREEN)
        else:
            title_text = title_font.render("DEFEAT", True, RED)
        
        title_x = (SCREEN_WIDTH - title_text.get_width()) // 2
        title_y = SCREEN_HEIGHT // 3
        surface.blit(title_text, (title_x, title_y))
        
        # Rewards (if victory)
        if self.victory and self.battle_manager:
            rewards = self.battle_manager.get_rewards()
            player = self.battle_manager.player_party[0]
            
            reward_font = pygame.font.Font(None, 36)
            y_offset = title_y + 100
            
            # Experience
            xp_text = reward_font.render(f"Experience: +{rewards['experience']}", True, CYAN)
            xp_x = (SCREEN_WIDTH - xp_text.get_width()) // 2
            surface.blit(xp_text, (xp_x, y_offset))
            
            # Berries
            berries_text = reward_font.render(f"Berries: +{rewards['berries']}", True, YELLOW)
            berries_x = (SCREEN_WIDTH - berries_text.get_width()) // 2
            surface.blit(berries_text, (berries_x, y_offset + 50))
            
            # Level
            level_text = reward_font.render(f"Level: {player.level}", True, WHITE)
            level_x = (SCREEN_WIDTH - level_text.get_width()) // 2
            surface.blit(level_text, (level_x, y_offset + 100))
        
        # Continue instruction
        continue_font = pygame.font.Font(None, 32)
        continue_text = continue_font.render("Press ENTER to continue", True, LIGHT_GRAY)
        continue_x = (SCREEN_WIDTH - continue_text.get_width()) // 2
        continue_y = SCREEN_HEIGHT - 100
        surface.blit(continue_text, (continue_x, continue_y))
