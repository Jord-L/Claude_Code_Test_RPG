"""
Battle Manager
Orchestrates turn-based combat between player party and enemies.
"""

import pygame
from typing import List, Optional, Dict, Callable
from entities.character import Character
from entities.player import Player
from combat.turn_system import TurnSystem
from combat.combat_action import CombatAction, ActionType
from combat.damage_calculator import DamageCalculator
from utils.constants import *


class BattleResult:
    """Result of a battle."""
    
    def __init__(self, victory: bool, exp_gained: int = 0, berries_gained: int = 0, items_gained: List[str] = None):
        """
        Initialize battle result.
        
        Args:
            victory: True if player won
            exp_gained: Experience points gained
            berries_gained: Berries earned
            items_gained: List of item IDs obtained
        """
        self.victory = victory
        self.exp_gained = exp_gained
        self.berries_gained = berries_gained
        self.items_gained = items_gained or []
        self.fled = False


class BattleManager:
    """
    Manages turn-based combat between player party and enemies.
    Handles turn order, action execution, and battle flow.
    """
    
    def __init__(self, player_party: List[Character], enemies: List[Character]):
        """
        Initialize battle manager.
        
        Args:
            player_party: List of player-controlled characters
            enemies: List of enemy characters
        """
        # Combatants
        self.player_party = player_party
        self.enemies = enemies
        self.all_combatants = player_party + enemies
        
        # Battle state
        self.battle_active = True
        self.current_turn = 0
        self.battle_log: List[str] = []
        
        # Turn system
        self.turn_system = TurnSystem(self.all_combatants)
        self.current_actor: Optional[Character] = None
        
        # Damage calculator
        self.damage_calculator = DamageCalculator()
        
        # Action queue (for simultaneous actions if needed)
        self.action_queue: List[CombatAction] = []
        
        # Battle result
        self.result: Optional[BattleResult] = None
        
        # Callbacks
        self.on_action_executed: Optional[Callable] = None
        self.on_turn_start: Optional[Callable] = None
        self.on_battle_end: Optional[Callable] = None
        
        # Status effects to process each turn
        self.status_effects_active = True
        
        # Initialize battle
        self._initialize_battle()
    
    def _initialize_battle(self):
        """Initialize battle state."""
        self.add_to_log("Battle Start!")
        self.add_to_log("")
        
        # List combatants
        self.add_to_log("Player Party:")
        for char in self.player_party:
            self.add_to_log(f"  - {char.name} (Lv. {char.level})")
        
        self.add_to_log("")
        self.add_to_log("Enemies:")
        for enemy in self.enemies:
            self.add_to_log(f"  - {enemy.name} (Lv. {enemy.level})")
        
        self.add_to_log("")
        self.add_to_log("="*40)
        
        # Start first turn
        self._start_next_turn()
    
    def _start_next_turn(self):
        """Start the next combatant's turn."""
        if not self.battle_active:
            return
        
        # Get next actor
        self.current_actor = self.turn_system.get_next_actor()
        
        if not self.current_actor:
            # Should not happen, but handle gracefully
            self.add_to_log("Error: No valid actor for turn!")
            self.battle_active = False
            return
        
        # Increment turn counter
        self.current_turn += 1
        
        # Process status effects at start of turn
        if self.status_effects_active:
            self._process_status_effects(self.current_actor)
        
        # Check if actor is still alive and can act
        if not self.current_actor.is_alive:
            self.add_to_log(f"{self.current_actor.name} is defeated and cannot act!")
            self._end_turn()
            return
        
        if not self.current_actor.can_act:
            self.add_to_log(f"{self.current_actor.name} cannot act!")
            self._end_turn()
            return
        
        # Announce turn
        self.add_to_log(f"--- {self.current_actor.name}'s Turn ---")
        
        # Trigger callback
        if self.on_turn_start:
            self.on_turn_start(self.current_actor)
    
    def execute_action(self, action: CombatAction) -> bool:
        """
        Execute a combat action.
        
        Args:
            action: CombatAction to execute
        
        Returns:
            True if action was executed successfully
        """
        if not self.battle_active:
            return False
        
        if not self.current_actor:
            return False
        
        # Validate action
        if action.actor != self.current_actor:
            self.add_to_log("Error: Action actor does not match current actor!")
            return False
        
        # Execute based on action type
        success = False
        
        if action.action_type == ActionType.ATTACK:
            success = self._execute_attack(action)
        
        elif action.action_type == ActionType.DEFEND:
            success = self._execute_defend(action)
        
        elif action.action_type == ActionType.ABILITY:
            success = self._execute_ability(action)
        
        elif action.action_type == ActionType.ITEM:
            success = self._execute_item(action)
        
        elif action.action_type == ActionType.RUN:
            success = self._execute_run(action)
        
        # Trigger callback
        if success and self.on_action_executed:
            self.on_action_executed(action)
        
        # End turn if action was successful
        if success:
            self._end_turn()
        
        return success
    
    def _execute_attack(self, action: CombatAction) -> bool:
        """
        Execute a basic attack action.
        
        Args:
            action: Attack action
        
        Returns:
            True if successful
        """
        actor = action.actor
        target = action.target
        
        if not target or not target.is_alive:
            self.add_to_log(f"{actor.name} attacks, but the target is already defeated!")
            return False
        
        # Check for dodge
        if target.can_dodge():
            self.add_to_log(f"{actor.name} attacks {target.name}, but {target.name} dodged!")
            return True
        
        # Calculate damage
        base_damage = actor.get_attack_power()
        final_damage = actor.calculate_damage(target, base_damage)
        
        # Apply damage
        actual_damage = target.take_damage(final_damage)
        
        # Log action
        self.add_to_log(f"{actor.name} attacks {target.name} for {actual_damage} damage!")
        
        # Check for knockout
        if not target.is_alive:
            self.add_to_log(f"{target.name} has been defeated!")
            self._check_battle_end()
        
        return True
    
    def _execute_defend(self, action: CombatAction) -> bool:
        """
        Execute a defend action.
        
        Args:
            action: Defend action
        
        Returns:
            True if successful
        """
        actor = action.actor
        
        # Apply defense buff (temporary, handled in next turn)
        # For now, just log it
        self.add_to_log(f"{actor.name} takes a defensive stance!")
        
        # TODO: Apply temporary defense buff that lasts until next turn
        
        return True
    
    def _execute_ability(self, action: CombatAction) -> bool:
        """
        Execute a Devil Fruit ability or special skill.
        
        Args:
            action: Ability action
        
        Returns:
            True if successful
        """
        actor = action.actor
        ability_data = action.ability_data
        
        if not ability_data:
            self.add_to_log(f"{actor.name} tried to use an ability, but no ability data provided!")
            return False
        
        ability_name = ability_data.get("name", "Unknown Ability")
        ap_cost = ability_data.get("ap_cost", 0)
        
        # Check AP cost
        if not actor.use_ap(ap_cost):
            self.add_to_log(f"{actor.name} doesn't have enough AP to use {ability_name}!")
            return False
        
        # Get targets
        target_type = ability_data.get("target", "Single")
        targets = self._get_ability_targets(action, target_type)
        
        if not targets:
            self.add_to_log(f"{actor.name} uses {ability_name}, but there are no valid targets!")
            # Refund AP since ability wasn't used
            actor.restore_ap(ap_cost)
            return False
        
        # Get damage type and calculate
        damage_type = ability_data.get("damage_type", "Physical")
        base_damage = ability_data.get("base_damage", actor.get_attack_power())
        
        # Execute on all targets
        self.add_to_log(f"{actor.name} uses {ability_name}!")
        
        for target in targets:
            if not target.is_alive:
                continue
            
            # Check for dodge (unless it's a guaranteed hit ability)
            if target.can_dodge() and not ability_data.get("guaranteed_hit", False):
                self.add_to_log(f"  {target.name} dodged!")
                continue
            
            # Calculate and apply damage
            final_damage = self.damage_calculator.calculate_ability_damage(
                actor, target, base_damage, damage_type
            )
            actual_damage = target.take_damage(final_damage)
            
            self.add_to_log(f"  {target.name} takes {actual_damage} damage!")
            
            # Apply status effects
            effects = ability_data.get("effects", [])
            for effect in effects:
                # TODO: Implement status effect system
                self.add_to_log(f"  {target.name} is affected by {effect}!")
            
            # Check for knockout
            if not target.is_alive:
                self.add_to_log(f"  {target.name} has been defeated!")
        
        # Check if battle ended
        self._check_battle_end()
        
        return True
    
    def _execute_item(self, action: CombatAction) -> bool:
        """
        Execute an item use action.
        
        Args:
            action: Item action
        
        Returns:
            True if successful
        """
        actor = action.actor
        item_data = action.item_data
        target = action.target or actor  # Default to self if no target
        
        if not item_data:
            self.add_to_log(f"{actor.name} tried to use an item, but no item data provided!")
            return False
        
        item_name = item_data.get("name", "Unknown Item")
        
        # Only players can use items (for now)
        if not isinstance(actor, Player):
            self.add_to_log(f"{actor.name} cannot use items!")
            return False
        
        # Check if player has item
        item_id = item_data.get("id", "")
        if not actor.has_item(item_id):
            self.add_to_log(f"{actor.name} doesn't have any {item_name}!")
            return False
        
        # Use item
        if actor.use_item(item_id, item_data):
            self.add_to_log(f"{actor.name} used {item_name}!")
            
            # Items are used by the Player.use_item method
            # Effects are already applied there
            
            return True
        else:
            self.add_to_log(f"{actor.name} failed to use {item_name}!")
            return False
    
    def _execute_run(self, action: CombatAction) -> bool:
        """
        Execute a run/flee action.
        
        Args:
            action: Run action
        
        Returns:
            True if successful
        """
        actor = action.actor
        
        # Only players can flee
        if actor not in self.player_party:
            self.add_to_log(f"{actor.name} cannot flee from battle!")
            return False
        
        # Calculate flee chance (based on speed difference)
        player_speed = sum(char.get_speed() for char in self.player_party) / len(self.player_party)
        enemy_speed = sum(enemy.get_speed() for enemy in self.enemies if enemy.is_alive) / max(1, len([e for e in self.enemies if e.is_alive]))
        
        # Base 50% chance, +/- 5% per speed difference
        speed_diff = player_speed - enemy_speed
        flee_chance = 50 + (speed_diff * 5)
        flee_chance = max(10, min(90, flee_chance))  # Clamp between 10% and 90%
        
        # Roll for flee
        import random
        if random.random() * 100 < flee_chance:
            self.add_to_log(f"{actor.name} fled from battle!")
            self.add_to_log("The party escaped successfully!")
            
            # End battle
            self.battle_active = False
            self.result = BattleResult(victory=False, exp_gained=0, berries_gained=0)
            self.result.fled = True
            
            if self.on_battle_end:
                self.on_battle_end(self.result)
            
            return True
        else:
            self.add_to_log(f"{actor.name} tried to flee, but couldn't escape!")
            return True  # Turn still ends even if flee fails
    
    def _get_ability_targets(self, action: CombatAction, target_type: str) -> List[Character]:
        """
        Get targets for an ability based on target type.
        
        Args:
            action: Combat action
            target_type: "Single", "Multi", "All", "Self", "Allies"
        
        Returns:
            List of target characters
        """
        targets = []
        actor = action.actor
        specified_target = action.target
        
        if target_type == "Single":
            if specified_target and specified_target.is_alive:
                targets = [specified_target]
        
        elif target_type == "Multi":
            # Multi-target abilities hit 2-3 random enemies
            import random
            if actor in self.player_party:
                alive_enemies = [e for e in self.enemies if e.is_alive]
                num_targets = min(3, len(alive_enemies))
                targets = random.sample(alive_enemies, num_targets)
            else:
                alive_players = [p for p in self.player_party if p.is_alive]
                num_targets = min(3, len(alive_players))
                targets = random.sample(alive_players, num_targets)
        
        elif target_type == "All":
            # All enemies or all players
            if actor in self.player_party:
                targets = [e for e in self.enemies if e.is_alive]
            else:
                targets = [p for p in self.player_party if p.is_alive]
        
        elif target_type == "Self":
            targets = [actor]
        
        elif target_type == "Allies":
            # All allies including self
            if actor in self.player_party:
                targets = [p for p in self.player_party if p.is_alive]
            else:
                targets = [e for e in self.enemies if e.is_alive]
        
        return targets
    
    def _end_turn(self):
        """End current turn and prepare for next."""
        # Process any end-of-turn effects
        # (Poison damage, regeneration, etc.)
        
        # Check if battle is still active
        if not self.battle_active:
            return
        
        # Start next turn
        self._start_next_turn()
    
    def _process_status_effects(self, character: Character):
        """
        Process status effects at the start of a character's turn.
        
        Args:
            character: Character to process
        """
        # TODO: Implement full status effect system
        # For now, just a placeholder
        pass
    
    def _check_battle_end(self):
        """Check if battle has ended (all enemies or all players defeated)."""
        # Check if all enemies defeated
        enemies_alive = any(enemy.is_alive for enemy in self.enemies)
        players_alive = any(player.is_alive for player in self.player_party)
        
        if not enemies_alive:
            # Victory!
            self.add_to_log("")
            self.add_to_log("="*40)
            self.add_to_log("VICTORY!")
            self.add_to_log("")
            
            # Calculate rewards
            exp_gained = self._calculate_exp_reward()
            berries_gained = self._calculate_berries_reward()
            items_gained = self._calculate_item_rewards()
            
            self.add_to_log(f"Gained {exp_gained} EXP!")
            self.add_to_log(f"Gained {berries_gained:,} Berries!")
            if items_gained:
                self.add_to_log(f"Found items: {', '.join(items_gained)}")
            
            # Apply rewards to player party
            self._apply_rewards(exp_gained, berries_gained, items_gained)
            
            # End battle
            self.battle_active = False
            self.result = BattleResult(
                victory=True,
                exp_gained=exp_gained,
                berries_gained=berries_gained,
                items_gained=items_gained
            )
            
            if self.on_battle_end:
                self.on_battle_end(self.result)
        
        elif not players_alive:
            # Defeat!
            self.add_to_log("")
            self.add_to_log("="*40)
            self.add_to_log("DEFEAT!")
            self.add_to_log("The party has been wiped out...")
            
            # End battle
            self.battle_active = False
            self.result = BattleResult(victory=False, exp_gained=0, berries_gained=0)
            
            if self.on_battle_end:
                self.on_battle_end(self.result)
    
    def _calculate_exp_reward(self) -> int:
        """Calculate experience reward from defeated enemies."""
        total_exp = 0
        for enemy in self.enemies:
            # Base exp: 10 * enemy level
            base_exp = enemy.level * 10
            total_exp += base_exp
        return total_exp
    
    def _calculate_berries_reward(self) -> int:
        """Calculate berries reward from defeated enemies."""
        total_berries = 0
        for enemy in self.enemies:
            # Base berries: 50 * enemy level
            base_berries = enemy.level * 50
            total_berries += base_berries
        return total_berries
    
    def _calculate_item_rewards(self) -> List[str]:
        """Calculate item drops from defeated enemies."""
        # TODO: Implement item drop system
        # For now, return empty list
        return []
    
    def _apply_rewards(self, exp: int, berries: int, items: List[str]):
        """
        Apply rewards to player party.
        
        Args:
            exp: Experience points to distribute
            berries: Berries to award
            items: Items to add to inventory
        """
        # Distribute exp evenly among alive party members
        alive_players = [p for p in self.player_party if isinstance(p, Player) and p.is_alive]
        
        if alive_players:
            exp_per_player = exp // len(alive_players)
            
            for player in alive_players:
                leveled_up = player.gain_experience(exp_per_player)
                
                if leveled_up:
                    self.add_to_log(f"{player.name} leveled up to level {player.level}!")
        
        # Award berries to first player (assumed to be main player)
        if self.player_party and isinstance(self.player_party[0], Player):
            main_player = self.player_party[0]
            main_player.add_berries(berries)
            main_player.record_battle_victory(len(self.enemies))
            
            # Add items
            for item_id in items:
                main_player.add_item(item_id, 1)
    
    def add_to_log(self, message: str):
        """
        Add a message to the battle log.
        
        Args:
            message: Message to add
        """
        self.battle_log.append(message)
        print(message)  # Also print to console for debugging
    
    def get_recent_log(self, num_lines: int = 5) -> List[str]:
        """
        Get the most recent battle log messages.
        
        Args:
            num_lines: Number of lines to retrieve
        
        Returns:
            List of recent log messages
        """
        return self.battle_log[-num_lines:]
    
    def get_alive_enemies(self) -> List[Character]:
        """Get list of alive enemies."""
        return [e for e in self.enemies if e.is_alive]
    
    def get_alive_players(self) -> List[Character]:
        """Get list of alive players."""
        return [p for p in self.player_party if p.is_alive]
    
    def is_player_turn(self) -> bool:
        """Check if it's currently a player's turn."""
        return self.current_actor in self.player_party if self.current_actor else False
    
    def get_valid_targets_for_action(self, action_type: ActionType) -> List[Character]:
        """
        Get valid targets for a specific action type.
        
        Args:
            action_type: Type of action
        
        Returns:
            List of valid targets
        """
        if action_type == ActionType.ATTACK or action_type == ActionType.ABILITY:
            # Can target alive enemies
            if self.is_player_turn():
                return self.get_alive_enemies()
            else:
                return self.get_alive_players()
        
        elif action_type == ActionType.ITEM:
            # Can target any alive party member
            if self.is_player_turn():
                return self.get_alive_players()
            else:
                return self.get_alive_enemies()
        
        elif action_type == ActionType.DEFEND or action_type == ActionType.RUN:
            # No target needed
            return []
        
        return []
    
    @property
    def turn_order(self) -> List[Character]:
        """
        Get current turn order from turn system.
        
        Returns:
            List of characters in turn order
        """
        return self.turn_system.get_turn_order()
