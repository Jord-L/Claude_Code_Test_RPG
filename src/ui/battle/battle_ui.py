"""
Battle UI
Main coordinator for all battle UI components.
Manages action menu, target selector, and battle HUD.
"""

import pygame
from typing import List, Optional, Callable
from entities.character import Character
from combat.battle_manager import BattleManager
from combat.combat_action import CombatAction, ActionType
from .action_menu import ActionMenu, ActionOption
from .target_selector import TargetSelector
from .battle_hud import BattleHUD
from utils.constants import *


class UIState:
    """Enum for UI states."""
    WAITING = "waiting"  # Waiting for turn
    ACTION_SELECTION = "action_selection"  # Selecting action
    TARGET_SELECTION = "target_selection"  # Selecting target
    ABILITY_SELECTION = "ability_selection"  # Selecting which ability
    ITEM_SELECTION = "item_selection"  # Selecting which item
    ANIMATING = "animating"  # Playing animation
    BATTLE_END = "battle_end"  # Battle finished


class BattleUI:
    """
    Main battle UI coordinator.
    Manages all battle UI components and their interactions.
    """
    
    def __init__(self, screen_width: int, screen_height: int, battle_manager: BattleManager):
        """
        Initialize battle UI.
        
        Args:
            screen_width: Screen width
            screen_height: Screen height
            battle_manager: Battle manager instance
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.battle_manager = battle_manager
        
        # UI State
        self.state = UIState.WAITING
        self.current_action_type: Optional[str] = None
        self.pending_action: Optional[CombatAction] = None
        
        # Components
        self._setup_components()
        
        # Callbacks from battle manager
        self.battle_manager.on_turn_start = self._on_turn_start
        self.battle_manager.on_action_executed = self._on_action_executed
        self.battle_manager.on_battle_end = self._on_battle_end
        
        # Animation timing
        self.animation_timer = 0.0
        self.animation_duration = 1.0  # seconds
        
        # Battle result display
        self.show_result = False
        self.result_message = ""
    
    def _setup_components(self):
        """Set up all UI components."""
        # Battle HUD (always visible)
        self.hud = BattleHUD(self.screen_width, self.screen_height)
        self.hud.setup_combatants(
            self.battle_manager.player_party,
            self.battle_manager.enemies
        )
        
        # Action Menu (bottom center)
        menu_width = 400
        menu_height = 350
        menu_x = (self.screen_width - menu_width) // 2
        menu_y = self.screen_height - menu_height - 20
        
        self.action_menu = ActionMenu(menu_x, menu_y, menu_width, menu_height)
        self.action_menu.on_action_selected = self._on_action_menu_selected
        self.action_menu.on_cancel = self._on_action_menu_cancel
        self.action_menu.set_visible(False)
        
        # Target Selector (center)
        selector_width = 500
        selector_height = 450
        selector_x = (self.screen_width - selector_width) // 2
        selector_y = (self.screen_height - selector_height) // 2
        
        self.target_selector = TargetSelector(selector_x, selector_y, selector_width, selector_height)
        self.target_selector.on_target_selected = self._on_target_selected
        self.target_selector.on_cancel = self._on_target_selection_cancel
        self.target_selector.set_visible(False)
        
        # TODO: Ability selection menu (Phase 2)
        # TODO: Item selection menu (Phase 2)
    
    def _on_turn_start(self, actor: Character):
        """
        Called when a new turn starts.
        
        Args:
            actor: Character whose turn it is
        """
        self.hud.set_current_actor(actor)
        
        # If it's a player's turn, show action menu
        if actor in self.battle_manager.player_party:
            self._show_action_menu(actor)
        else:
            # Enemy turn - will be handled by AI
            self.state = UIState.WAITING
    
    def _show_action_menu(self, actor: Character):
        """
        Show action menu for player turn.
        
        Args:
            actor: Acting character
        """
        self.state = UIState.ACTION_SELECTION
        
        # Build action menu options
        options = []
        
        # Attack (always available)
        options.append(ActionOption(
            "attack",
            "Attack",
            enabled=True
        ))
        
        # Defend (always available)
        options.append(ActionOption(
            "defend",
            "Defend",
            enabled=True
        ))
        
        # Devil Fruit Abilities (if character has Devil Fruit)
        has_abilities = hasattr(actor, 'devil_fruit') and actor.devil_fruit is not None
        options.append(ActionOption(
            "ability",
            "Devil Fruit",
            enabled=has_abilities
        ))
        
        # Items (if character has items - for Phase 2)
        has_items = hasattr(actor, 'inventory') and len(actor.inventory) > 0
        options.append(ActionOption(
            "item",
            "Item",
            enabled=has_items
        ))
        
        # Run (always available)
        options.append(ActionOption(
            "run",
            "Run",
            enabled=True
        ))
        
        self.action_menu.set_options(options)
        self.action_menu.set_visible(True)
        self.action_menu.set_active(True)
    
    def _on_action_menu_selected(self, action_type: str):
        """
        Called when an action is selected from menu.
        
        Args:
            action_type: Selected action type
        """
        self.current_action_type = action_type
        actor = self.battle_manager.current_actor
        
        if not actor:
            return
        
        # Handle based on action type
        if action_type == "attack":
            # Show target selector for enemies
            self._show_target_selector(
                self.battle_manager.get_alive_enemies(),
                "Select Attack Target"
            )
        
        elif action_type == "defend":
            # Defend doesn't need target - execute immediately
            self._execute_action(ActionType.DEFEND, target=None)
        
        elif action_type == "ability":
            # TODO: Show ability selection menu (Phase 2)
            # For now, just show a simple target selector
            # and use first ability if available
            if hasattr(actor, 'devil_fruit') and actor.devil_fruit:
                abilities = actor.devil_fruit.get("abilities", [])
                if abilities:
                    # Use first ability for now
                    self.pending_action = CombatAction(
                        actor,
                        ActionType.ABILITY,
                        ability_data=abilities[0]
                    )
                    self._show_target_selector(
                        self.battle_manager.get_alive_enemies(),
                        f"Select Target for {abilities[0]['name']}"
                    )
                else:
                    self.hud.add_log_message("No abilities available!")
                    self._show_action_menu(actor)
            else:
                self.hud.add_log_message("No Devil Fruit abilities!")
                self._show_action_menu(actor)
        
        elif action_type == "item":
            # TODO: Show item selection menu (Phase 2)
            self.hud.add_log_message("Item system not yet implemented!")
            self._show_action_menu(actor)
        
        elif action_type == "run":
            # Run doesn't need target - execute immediately
            self._execute_action(ActionType.RUN, target=None)
    
    def _on_action_menu_cancel(self):
        """Called when action menu is cancelled."""
        # Can't cancel on player turn - must select an action
        pass
    
    def _show_target_selector(self, targets: List[Character], title: str = "Select Target"):
        """
        Show target selector.
        
        Args:
            targets: List of possible targets
            title: Selector title
        """
        self.state = UIState.TARGET_SELECTION
        
        # Hide action menu
        self.action_menu.set_visible(False)
        self.action_menu.set_active(False)
        
        # Show target selector
        self.target_selector.title = title
        self.target_selector.show(targets)
    
    def _on_target_selected(self, target: Character):
        """
        Called when a target is selected.
        
        Args:
            target: Selected target
        """
        # Hide target selector
        self.target_selector.hide()
        
        # Execute action with target
        if self.current_action_type == "attack":
            self._execute_action(ActionType.ATTACK, target=target)
        
        elif self.current_action_type == "ability":
            # Use pending action (which has ability data)
            if self.pending_action:
                self.pending_action.target = target
                self.battle_manager.execute_action(self.pending_action)
                self.pending_action = None
        
        # Reset state
        self.current_action_type = None
    
    def _on_target_selection_cancel(self):
        """Called when target selection is cancelled."""
        # Go back to action menu
        self.target_selector.hide()
        actor = self.battle_manager.current_actor
        if actor:
            self._show_action_menu(actor)
    
    def _execute_action(self, action_type: ActionType, target: Optional[Character] = None):
        """
        Execute an action.
        
        Args:
            action_type: Type of action
            target: Target character (if applicable)
        """
        actor = self.battle_manager.current_actor
        
        if not actor:
            return
        
        # Create action
        action = CombatAction(actor, action_type, target=target)
        
        # Execute through battle manager
        success = self.battle_manager.execute_action(action)
        
        if success:
            # Hide menus
            self.action_menu.set_visible(False)
            self.action_menu.set_active(False)
            
            # Enter animation state briefly
            self.state = UIState.ANIMATING
            self.animation_timer = 0.0
        else:
            # Action failed - show menu again
            self._show_action_menu(actor)
    
    def _on_action_executed(self, action: CombatAction):
        """
        Called when an action is executed.
        
        Args:
            action: Executed action
        """
        # Action completed - could add visual effects here
        pass
    
    def _on_battle_end(self, result):
        """
        Called when battle ends.
        
        Args:
            result: Battle result
        """
        self.state = UIState.BATTLE_END
        self.show_result = True
        
        # Build result message
        if result.victory:
            self.result_message = "VICTORY!"
        elif result.fled:
            self.result_message = "ESCAPED!"
        else:
            self.result_message = "DEFEAT..."
        
        # Hide all menus
        self.action_menu.set_visible(False)
        self.target_selector.set_visible(False)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events.
        
        Args:
            event: Pygame event
        
        Returns:
            True if event was handled
        """
        # Pass events to active UI components based on state
        if self.state == UIState.ACTION_SELECTION:
            return self.action_menu.handle_event(event)
        
        elif self.state == UIState.TARGET_SELECTION:
            return self.target_selector.handle_event(event)
        
        elif self.state == UIState.BATTLE_END:
            # Allow Enter to continue after battle
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True  # Battle state will handle transition
        
        return False
    
    def update(self, dt: float):
        """
        Update UI state.
        
        Args:
            dt: Delta time in seconds
        """
        # Update HUD
        self.hud.update(dt)
        
        # Sync battle log with HUD
        recent_logs = self.battle_manager.get_recent_log(7)
        if recent_logs:
            # Clear and add messages
            self.hud.clear_log()
            for message in recent_logs:
                self.hud.add_log_message(message)
        
        # Update active components
        if self.state == UIState.ACTION_SELECTION:
            self.action_menu.update(dt)
        
        elif self.state == UIState.TARGET_SELECTION:
            self.target_selector.update(dt)
        
        elif self.state == UIState.ANIMATING:
            # Simple animation timer
            self.animation_timer += dt
            if self.animation_timer >= self.animation_duration:
                self.state = UIState.WAITING
    
    def render(self, surface: pygame.Surface):
        """
        Render battle UI.
        
        Args:
            surface: Surface to draw on
        """
        # Always render HUD
        self.hud.render(
            surface,
            self.battle_manager.player_party,
            self.battle_manager.enemies,
            self.battle_manager.turn_system.turn_order
        )
        
        # Render active UI components
        if self.action_menu.visible:
            self.action_menu.render(surface)
        
        if self.target_selector.visible:
            self.target_selector.render(surface)
        
        # Render battle result if shown
        if self.show_result:
            self._render_battle_result(surface)
    
    def _render_battle_result(self, surface: pygame.Surface):
        """
        Render battle result overlay.
        
        Args:
            surface: Surface to draw on
        """
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        # Result text
        result_font = pygame.font.Font(None, 100)
        result_surface = result_font.render(self.result_message, True, WHITE)
        result_x = (self.screen_width - result_surface.get_width()) // 2
        result_y = self.screen_height // 3
        surface.blit(result_surface, (result_x, result_y))
        
        # Show rewards if victory
        if self.battle_manager.result and self.battle_manager.result.victory:
            info_font = pygame.font.Font(None, 36)
            y_offset = result_y + 100
            
            # Experience
            exp_text = f"Experience: +{self.battle_manager.result.exp_gained}"
            exp_surface = info_font.render(exp_text, True, CYAN)
            exp_x = (self.screen_width - exp_surface.get_width()) // 2
            surface.blit(exp_surface, (exp_x, y_offset))
            y_offset += 50
            
            # Berries
            berries_text = f"Berries: +{self.battle_manager.result.berries_gained:,}"
            berries_surface = info_font.render(berries_text, True, YELLOW)
            berries_x = (self.screen_width - berries_surface.get_width()) // 2
            surface.blit(berries_surface, (berries_x, y_offset))
            y_offset += 50
            
            # Items (if any)
            if self.battle_manager.result.items_gained:
                items_text = f"Items: {', '.join(self.battle_manager.result.items_gained)}"
                items_surface = info_font.render(items_text, True, WHITE)
                items_x = (self.screen_width - items_surface.get_width()) // 2
                surface.blit(items_surface, (items_x, y_offset))
        
        # Continue prompt
        prompt_font = pygame.font.Font(None, 32)
        prompt_text = "Press ENTER to continue"
        prompt_surface = prompt_font.render(prompt_text, True, LIGHT_GRAY)
        prompt_x = (self.screen_width - prompt_surface.get_width()) // 2
        prompt_y = self.screen_height - 80
        surface.blit(prompt_surface, (prompt_x, prompt_y))
    
    def is_battle_over(self) -> bool:
        """Check if battle is finished."""
        return not self.battle_manager.battle_active
    
    def get_battle_result(self):
        """Get battle result."""
        return self.battle_manager.result
