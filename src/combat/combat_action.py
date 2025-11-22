"""
Combat Action Classes
Represents different types of actions that can be taken in combat.
"""

from enum import Enum, auto
from typing import Optional, Dict, List
from entities.character import Character


class ActionType(Enum):
    """Types of combat actions."""
    ATTACK = auto()      # Basic physical attack
    DEFEND = auto()      # Defensive stance
    ABILITY = auto()     # Devil Fruit ability or special skill
    ITEM = auto()        # Use an item
    RUN = auto()         # Attempt to flee


class CombatAction:
    """
    Represents a single action in combat.
    """
    
    def __init__(
        self,
        action_type: ActionType,
        actor: Character,
        target: Optional[Character] = None,
        ability_data: Optional[Dict] = None,
        item_data: Optional[Dict] = None
    ):
        """
        Initialize a combat action.
        
        Args:
            action_type: Type of action
            actor: Character performing the action
            target: Target character (optional, depends on action)
            ability_data: Ability data if action_type is ABILITY
            item_data: Item data if action_type is ITEM
        """
        self.action_type = action_type
        self.actor = actor
        self.target = target
        self.ability_data = ability_data
        self.item_data = item_data
        
        # Action result (filled in after execution)
        self.success = False
        self.damage_dealt = 0
        self.healing_done = 0
        self.effects_applied: List[str] = []
        self.message = ""
    
    @classmethod
    def create_attack(cls, actor: Character, target: Character) -> 'CombatAction':
        """
        Create an attack action.
        
        Args:
            actor: Attacking character
            target: Target character
        
        Returns:
            CombatAction for attack
        """
        return cls(ActionType.ATTACK, actor, target)
    
    @classmethod
    def create_defend(cls, actor: Character) -> 'CombatAction':
        """
        Create a defend action.
        
        Args:
            actor: Character defending
        
        Returns:
            CombatAction for defend
        """
        return cls(ActionType.DEFEND, actor)
    
    @classmethod
    def create_ability(
        cls,
        actor: Character,
        ability_data: Dict,
        target: Optional[Character] = None
    ) -> 'CombatAction':
        """
        Create an ability action.
        
        Args:
            actor: Character using ability
            ability_data: Devil Fruit ability data
            target: Target character (if single-target)
        
        Returns:
            CombatAction for ability
        """
        return cls(ActionType.ABILITY, actor, target, ability_data=ability_data)
    
    @classmethod
    def create_item(
        cls,
        actor: Character,
        item_data: Dict,
        target: Optional[Character] = None
    ) -> 'CombatAction':
        """
        Create an item use action.
        
        Args:
            actor: Character using item
            item_data: Item data
            target: Target character (defaults to actor if healing item)
        
        Returns:
            CombatAction for item use
        """
        return cls(ActionType.ITEM, actor, target, item_data=item_data)
    
    @classmethod
    def create_run(cls, actor: Character) -> 'CombatAction':
        """
        Create a run/flee action.
        
        Args:
            actor: Character attempting to flee
        
        Returns:
            CombatAction for flee attempt
        """
        return cls(ActionType.RUN, actor)
    
    def get_description(self) -> str:
        """
        Get a human-readable description of this action.
        
        Returns:
            Action description string
        """
        if self.action_type == ActionType.ATTACK:
            target_name = self.target.name if self.target else "???"
            return f"{self.actor.name} attacks {target_name}"
        
        elif self.action_type == ActionType.DEFEND:
            return f"{self.actor.name} defends"
        
        elif self.action_type == ActionType.ABILITY:
            ability_name = self.ability_data.get("name", "Unknown") if self.ability_data else "Unknown"
            if self.target:
                return f"{self.actor.name} uses {ability_name} on {self.target.name}"
            else:
                return f"{self.actor.name} uses {ability_name}"
        
        elif self.action_type == ActionType.ITEM:
            item_name = self.item_data.get("name", "Unknown") if self.item_data else "Unknown"
            if self.target and self.target != self.actor:
                return f"{self.actor.name} uses {item_name} on {self.target.name}"
            else:
                return f"{self.actor.name} uses {item_name}"
        
        elif self.action_type == ActionType.RUN:
            return f"{self.actor.name} tries to run"
        
        return f"{self.actor.name} does something"
    
    def get_ap_cost(self) -> int:
        """
        Get the AP cost of this action.
        
        Returns:
            AP cost (0 for most actions)
        """
        if self.action_type == ActionType.ABILITY and self.ability_data:
            return self.ability_data.get("ap_cost", 0)
        
        return 0
    
    def can_execute(self) -> bool:
        """
        Check if this action can be executed.
        
        Returns:
            True if action is valid and can be executed
        """
        # Check if actor is alive and can act
        if not self.actor.is_alive or not self.actor.can_act:
            return False
        
        # Check AP cost for abilities
        if self.action_type == ActionType.ABILITY:
            ap_cost = self.get_ap_cost()
            if self.actor.current_ap < ap_cost:
                return False
        
        # Check if target is valid (if needed)
        if self.action_type in [ActionType.ATTACK, ActionType.ABILITY]:
            if self.target and not self.target.is_alive:
                return False
        
        return True
    
    def __str__(self) -> str:
        """String representation."""
        return self.get_description()
    
    def __repr__(self) -> str:
        """Debug representation."""
        return f"CombatAction({self.action_type.name}, actor={self.actor.name}, target={self.target.name if self.target else None})"


class ActionFactory:
    """
    Factory class for creating combat actions.
    Provides convenient methods for creating common actions.
    """
    
    @staticmethod
    def basic_attack(actor: Character, target: Character) -> CombatAction:
        """Create a basic attack action."""
        return CombatAction.create_attack(actor, target)
    
    @staticmethod
    def defend(actor: Character) -> CombatAction:
        """Create a defend action."""
        return CombatAction.create_defend(actor)
    
    @staticmethod
    def use_ability(
        actor: Character,
        ability_data: Dict,
        target: Optional[Character] = None
    ) -> CombatAction:
        """Create an ability action."""
        return CombatAction.create_ability(actor, ability_data, target)
    
    @staticmethod
    def use_item(
        actor: Character,
        item_data: Dict,
        target: Optional[Character] = None
    ) -> CombatAction:
        """Create an item use action."""
        if not target:
            target = actor  # Default to self
        return CombatAction.create_item(actor, item_data, target)
    
    @staticmethod
    def flee(actor: Character) -> CombatAction:
        """Create a flee action."""
        return CombatAction.create_run(actor)
    
    @staticmethod
    def get_devil_fruit_actions(actor: Character) -> List[CombatAction]:
        """
        Get all available Devil Fruit abilities for a character.
        
        Args:
            actor: Character with Devil Fruit
        
        Returns:
            List of ability actions
        """
        actions = []
        
        if not actor.devil_fruit:
            return actions
        
        # Get available abilities (those the character has enough AP for)
        available_abilities = actor.devil_fruit.get_available_abilities(actor.current_ap)
        
        for ability in available_abilities:
            # Create action (target will be set later)
            action = CombatAction.create_ability(actor, ability, None)
            actions.append(action)
        
        return actions
    
    @staticmethod
    def get_available_actions(actor: Character) -> Dict[ActionType, List[CombatAction]]:
        """
        Get all available actions for a character.
        
        Args:
            actor: Character to get actions for
        
        Returns:
            Dictionary mapping ActionType to list of actions
        """
        actions = {
            ActionType.ATTACK: [],
            ActionType.DEFEND: [],
            ActionType.ABILITY: [],
            ActionType.ITEM: [],
            ActionType.RUN: []
        }
        
        # Attack is always available (target chosen later)
        actions[ActionType.ATTACK].append(CombatAction.create_attack(actor, None))
        
        # Defend is always available
        actions[ActionType.DEFEND].append(CombatAction.create_defend(actor))
        
        # Devil Fruit abilities
        if actor.devil_fruit:
            ability_actions = ActionFactory.get_devil_fruit_actions(actor)
            actions[ActionType.ABILITY].extend(ability_actions)
        
        # Items (only for players)
        from entities.player import Player
        if isinstance(actor, Player):
            # TODO: Get usable items from inventory
            # For now, items will be added during battle
            pass
        
        # Run is available for players
        if isinstance(actor, Player):
            actions[ActionType.RUN].append(CombatAction.create_run(actor))
        
        return actions
