"""
Enemy AI
Simple AI system for enemy decision-making in combat.
"""

import random
from typing import List, Optional
from entities.character import Character
from combat.combat_action import CombatAction, ActionType, ActionFactory


class EnemyAI:
    """
    Simple AI for enemy combat decisions.
    Uses basic heuristics to choose actions.
    """
    
    def __init__(self, enemy: Character, difficulty: str = "normal"):
        """
        Initialize enemy AI.
        
        Args:
            enemy: Enemy character this AI controls
            difficulty: AI difficulty ("easy", "normal", "hard")
        """
        self.enemy = enemy
        self.difficulty = difficulty
        
        # Behavior weights (can be customized per enemy type)
        self.attack_weight = 60
        self.defend_weight = 10
        self.ability_weight = 25
        self.item_weight = 5
        
        # Decision randomness (higher = more random)
        self.randomness = {
            "easy": 0.4,
            "normal": 0.2,
            "hard": 0.1
        }.get(difficulty, 0.2)
        
        # Memory of previous actions (for pattern avoidance)
        self.action_history: List[ActionType] = []
        self.max_history = 3
    
    def choose_action(
        self,
        player_party: List[Character],
        enemy_party: List[Character]
    ) -> CombatAction:
        """
        Choose an action for this enemy.
        
        Args:
            player_party: List of player characters
            enemy_party: List of enemy characters (allies)
        
        Returns:
            CombatAction to execute
        """
        # Get available actions
        available_actions = self._get_available_actions(player_party, enemy_party)
        
        # Choose action based on strategy
        action = self._select_action(available_actions, player_party, enemy_party)
        
        # Record in history
        self.action_history.append(action.action_type)
        if len(self.action_history) > self.max_history:
            self.action_history.pop(0)
        
        return action
    
    def _get_available_actions(
        self,
        player_party: List[Character],
        enemy_party: List[Character]
    ) -> dict:
        """
        Get all available actions for this enemy.
        
        Args:
            player_party: Player party
            enemy_party: Enemy party
        
        Returns:
            Dict of available actions by type
        """
        actions = {
            "attack": [],
            "defend": [],
            "ability": [],
            "item": []
        }
        
        # Get alive targets
        alive_players = [p for p in player_party if p.is_alive]
        
        if not alive_players:
            return actions
        
        # Attack options (one per target)
        for player in alive_players:
            actions["attack"].append(CombatAction.create_attack(self.enemy, player))
        
        # Defend option
        actions["defend"].append(CombatAction.create_defend(self.enemy))
        
        # Ability options (if has Devil Fruit)
        if self.enemy.devil_fruit:
            abilities = self.enemy.devil_fruit.get_available_abilities(self.enemy.current_ap)
            for ability in abilities:
                # Create action for each ability
                # Target will be chosen based on ability type
                target_type = ability.get("target", "Single")
                
                if target_type == "Single":
                    # Create one action per potential target
                    for player in alive_players:
                        actions["ability"].append(
                            CombatAction.create_ability(self.enemy, ability, player)
                        )
                else:
                    # Multi-target, create single action
                    actions["ability"].append(
                        CombatAction.create_ability(self.enemy, ability, alive_players[0])
                    )
        
        # Items (enemies typically don't use items in basic AI)
        # Can be added later for specific enemy types
        
        return actions
    
    def _select_action(
        self,
        available_actions: dict,
        player_party: List[Character],
        enemy_party: List[Character]
    ) -> CombatAction:
        """
        Select best action from available options.
        
        Args:
            available_actions: Available actions
            player_party: Player party
            enemy_party: Enemy party
        
        Returns:
            Selected CombatAction
        """
        # Calculate action scores
        action_scores = []
        
        # Score attack actions
        for action in available_actions["attack"]:
            score = self._score_attack(action, player_party)
            action_scores.append((action, score * self.attack_weight))
        
        # Score defend actions
        for action in available_actions["defend"]:
            score = self._score_defend(action, player_party, enemy_party)
            action_scores.append((action, score * self.defend_weight))
        
        # Score ability actions
        for action in available_actions["ability"]:
            score = self._score_ability(action, player_party)
            action_scores.append((action, score * self.ability_weight))
        
        # Add randomness based on difficulty
        for i, (action, score) in enumerate(action_scores):
            random_factor = 1.0 + random.uniform(-self.randomness, self.randomness)
            action_scores[i] = (action, score * random_factor)
        
        # Avoid repeating same action too much
        action_scores = self._apply_variety_penalty(action_scores)
        
        # Choose highest scoring action
        if action_scores:
            action_scores.sort(key=lambda x: x[1], reverse=True)
            return action_scores[0][0]
        
        # Fallback: random attack
        if available_actions["attack"]:
            return random.choice(available_actions["attack"])
        
        # Last resort: defend
        if available_actions["defend"]:
            return available_actions["defend"][0]
        
        # Should never reach here
        return CombatAction.create_defend(self.enemy)
    
    def _score_attack(
        self,
        action: CombatAction,
        player_party: List[Character]
    ) -> float:
        """
        Score an attack action.
        
        Args:
            action: Attack action to score
            player_party: Player party
        
        Returns:
            Score (0-1)
        """
        target = action.target
        if not target or not target.is_alive:
            return 0.0
        
        score = 0.5  # Base score
        
        # Prefer low HP targets (finish them off)
        hp_percent = target.get_hp_percentage()
        if hp_percent < 0.3:
            score += 0.3
        elif hp_percent < 0.5:
            score += 0.15
        
        # Prefer high threat targets (high attack)
        target_threat = target.get_attack_power() / 100.0
        score += min(0.2, target_threat * 0.01)
        
        # Slightly prefer players with Devil Fruits (strategic)
        if target.devil_fruit:
            score += 0.05
        
        return min(1.0, score)
    
    def _score_defend(
        self,
        action: CombatAction,
        player_party: List[Character],
        enemy_party: List[Character]
    ) -> float:
        """
        Score a defend action.
        
        Args:
            action: Defend action
            player_party: Player party
            enemy_party: Enemy party
        
        Returns:
            Score (0-1)
        """
        score = 0.3  # Base score (generally low priority)
        
        # Defend more if low on HP
        hp_percent = self.enemy.get_hp_percentage()
        if hp_percent < 0.25:
            score += 0.4
        elif hp_percent < 0.5:
            score += 0.2
        
        # Defend more if outnumbered
        alive_players = len([p for p in player_party if p.is_alive])
        alive_enemies = len([e for e in enemy_party if e.is_alive])
        if alive_enemies < alive_players:
            score += 0.2
        
        # Don't defend too often
        recent_defends = sum(1 for a in self.action_history if a == ActionType.DEFEND)
        if recent_defends > 0:
            score *= 0.5
        
        return min(1.0, score)
    
    def _score_ability(
        self,
        action: CombatAction,
        player_party: List[Character]
    ) -> float:
        """
        Score an ability action.
        
        Args:
            action: Ability action
            player_party: Player party
        
        Returns:
            Score (0-1)
        """
        target = action.target
        ability = action.ability_data
        
        if not ability:
            return 0.0
        
        score = 0.6  # Base score (good option)
        
        # Higher score for powerful abilities
        ap_cost = ability.get("ap_cost", 10)
        damage_potential = ability.get("base_damage", 50)
        
        # Normalize scores
        score += min(0.2, damage_potential / 500.0)
        
        # Prefer using abilities when have lots of AP
        ap_percent = self.enemy.get_ap_percentage()
        if ap_percent > 0.7:
            score += 0.2
        elif ap_percent < 0.3:
            score -= 0.3  # Save AP if running low
        
        # Multi-target abilities are better when multiple enemies alive
        target_type = ability.get("target", "Single")
        alive_players = len([p for p in player_party if p.is_alive])
        
        if target_type in ["Multi", "All"] and alive_players >= 3:
            score += 0.3
        
        # Single target abilities - prefer low HP targets
        if target_type == "Single" and target:
            hp_percent = target.get_hp_percentage()
            if hp_percent < 0.4:
                score += 0.2
        
        # Check if we have enough AP
        if self.enemy.current_ap < ap_cost:
            return 0.0
        
        return min(1.0, score)
    
    def _apply_variety_penalty(
        self,
        action_scores: List[tuple]
    ) -> List[tuple]:
        """
        Apply penalty to repeated actions for variety.
        
        Args:
            action_scores: List of (action, score) tuples
        
        Returns:
            Modified action scores
        """
        if not self.action_history:
            return action_scores
        
        # Count recent action types
        recent_types = {}
        for action_type in self.action_history:
            recent_types[action_type] = recent_types.get(action_type, 0) + 1
        
        # Apply penalties
        modified_scores = []
        for action, score in action_scores:
            action_type = action.action_type
            
            if action_type in recent_types:
                # Reduce score by 20% per recent use
                penalty = 0.8 ** recent_types[action_type]
                score *= penalty
            
            modified_scores.append((action, score))
        
        return modified_scores
    
    def set_behavior_weights(
        self,
        attack: int = 60,
        defend: int = 10,
        ability: int = 25,
        item: int = 5
    ):
        """
        Customize AI behavior weights.
        
        Args:
            attack: Attack weight
            defend: Defend weight
            ability: Ability weight
            item: Item weight
        """
        self.attack_weight = attack
        self.defend_weight = defend
        self.ability_weight = ability
        self.item_weight = item
    
    def reset_history(self):
        """Reset action history."""
        self.action_history.clear()


class AIFactory:
    """Factory for creating different AI personalities."""
    
    @staticmethod
    def create_aggressive_ai(enemy: Character, difficulty: str = "normal") -> EnemyAI:
        """Create an aggressive AI that focuses on attacking."""
        ai = EnemyAI(enemy, difficulty)
        ai.set_behavior_weights(attack=75, defend=5, ability=15, item=5)
        return ai
    
    @staticmethod
    def create_defensive_ai(enemy: Character, difficulty: str = "normal") -> EnemyAI:
        """Create a defensive AI that defends more often."""
        ai = EnemyAI(enemy, difficulty)
        ai.set_behavior_weights(attack=40, defend=30, ability=25, item=5)
        return ai
    
    @staticmethod
    def create_tactical_ai(enemy: Character, difficulty: str = "normal") -> EnemyAI:
        """Create a tactical AI that uses abilities more."""
        ai = EnemyAI(enemy, difficulty)
        ai.set_behavior_weights(attack=40, defend=10, ability=45, item=5)
        return ai
    
    @staticmethod
    def create_balanced_ai(enemy: Character, difficulty: str = "normal") -> EnemyAI:
        """Create a balanced AI (default behavior)."""
        return EnemyAI(enemy, difficulty)
