"""
Turn System
Manages turn order in combat based on character speed.
"""

from typing import List, Optional
from entities.character import Character


class TurnSystem:
    """
    Manages turn order in turn-based combat.
    Uses speed-based ordering with support for initiative rolls.
    """
    
    def __init__(self, combatants: List[Character]):
        """
        Initialize turn system.
        
        Args:
            combatants: List of all combatants in battle
        """
        self.combatants = combatants
        self.turn_order: List[Character] = []
        self.current_index = 0
        self.round_number = 0
        
        # Generate initial turn order
        self._generate_turn_order()
    
    def _generate_turn_order(self):
        """Generate turn order based on character speed."""
        # Sort combatants by speed (highest first)
        self.turn_order = sorted(
            [c for c in self.combatants if c.is_alive],
            key=lambda c: c.get_speed(),
            reverse=True
        )
        
        # Add some randomness for ties
        import random
        
        # Group by speed
        speed_groups = {}
        for char in self.turn_order:
            speed = char.get_speed()
            if speed not in speed_groups:
                speed_groups[speed] = []
            speed_groups[speed].append(char)
        
        # Shuffle within each speed group
        for speed, chars in speed_groups.items():
            if len(chars) > 1:
                random.shuffle(chars)
        
        # Rebuild turn order with shuffled groups
        self.turn_order = []
        for speed in sorted(speed_groups.keys(), reverse=True):
            self.turn_order.extend(speed_groups[speed])
        
        self.current_index = 0
        
        # Print turn order for debugging
        print("\n--- Turn Order ---")
        for i, char in enumerate(self.turn_order, 1):
            print(f"{i}. {char.name} (SPD: {char.get_speed()})")
        print("------------------\n")
    
    def get_next_actor(self) -> Optional[Character]:
        """
        Get the next character to act.
        
        Returns:
            Next character in turn order, or None if no valid actors
        """
        if not self.turn_order:
            return None
        
        # Find next alive character
        attempts = 0
        max_attempts = len(self.turn_order) * 2  # Prevent infinite loop
        
        while attempts < max_attempts:
            # Get current actor
            actor = self.turn_order[self.current_index]
            
            # Move to next index
            self.current_index = (self.current_index + 1) % len(self.turn_order)
            
            # Check if we completed a round
            if self.current_index == 0:
                self.round_number += 1
                print(f"\n--- Round {self.round_number} ---\n")
                
                # Regenerate turn order to account for defeated characters
                self._refresh_turn_order()
            
            # Check if this actor can act
            if actor.is_alive and actor.can_act:
                return actor
            
            attempts += 1
        
        # If we get here, no valid actors (shouldn't happen in normal gameplay)
        return None
    
    def _refresh_turn_order(self):
        """Refresh turn order, removing defeated characters."""
        # Get currently alive combatants
        alive_combatants = [c for c in self.combatants if c.is_alive]
        
        if not alive_combatants:
            self.turn_order = []
            return
        
        # Re-sort by speed
        self.turn_order = sorted(
            alive_combatants,
            key=lambda c: c.get_speed(),
            reverse=True
        )
        
        # Reset index
        self.current_index = 0
    
    def get_turn_order(self) -> List[Character]:
        """
        Get current turn order.
        
        Returns:
            List of characters in turn order
        """
        return self.turn_order.copy()
    
    def get_current_actor(self) -> Optional[Character]:
        """
        Get the current actor (last actor returned by get_next_actor).
        
        Returns:
            Current actor or None
        """
        if not self.turn_order:
            return None
        
        # Get previous index
        prev_index = (self.current_index - 1) % len(self.turn_order)
        return self.turn_order[prev_index]
    
    def peek_next_actor(self) -> Optional[Character]:
        """
        Peek at who will act next without advancing turn.
        
        Returns:
            Next actor or None
        """
        if not self.turn_order:
            return None
        
        # Find next alive character starting from current index
        for i in range(len(self.turn_order)):
            index = (self.current_index + i) % len(self.turn_order)
            actor = self.turn_order[index]
            
            if actor.is_alive and actor.can_act:
                return actor
        
        return None
    
    def get_turn_preview(self, num_turns: int = 5) -> List[Character]:
        """
        Get a preview of upcoming turns.
        
        Args:
            num_turns: Number of turns to preview
        
        Returns:
            List of upcoming actors
        """
        preview = []
        temp_index = self.current_index
        
        for _ in range(num_turns):
            # Find next alive character
            found = False
            for i in range(len(self.turn_order)):
                index = (temp_index + i) % len(self.turn_order)
                actor = self.turn_order[index]
                
                if actor.is_alive and actor.can_act:
                    preview.append(actor)
                    temp_index = (index + 1) % len(self.turn_order)
                    found = True
                    break
            
            if not found:
                break
        
        return preview
    
    def insert_turn(self, character: Character, priority: bool = False):
        """
        Insert a character into the turn order.
        Used for summoned creatures or special abilities.
        
        Args:
            character: Character to insert
            priority: If True, insert at front of queue
        """
        if priority:
            # Insert right after current turn
            self.turn_order.insert(self.current_index, character)
        else:
            # Insert based on speed
            for i, char in enumerate(self.turn_order):
                if character.get_speed() > char.get_speed():
                    self.turn_order.insert(i, character)
                    return
            
            # If not inserted, add to end
            self.turn_order.append(character)
    
    def remove_from_turn_order(self, character: Character):
        """
        Remove a character from turn order.
        Used when character is defeated or removed from battle.
        
        Args:
            character: Character to remove
        """
        if character in self.turn_order:
            # Adjust current index if needed
            char_index = self.turn_order.index(character)
            if char_index < self.current_index:
                self.current_index -= 1
            
            self.turn_order.remove(character)
            
            # Ensure index is valid
            if self.turn_order:
                self.current_index = self.current_index % len(self.turn_order)
            else:
                self.current_index = 0
    
    def get_round_number(self) -> int:
        """Get current round number."""
        return self.round_number
    
    def reset(self):
        """Reset turn system for a new battle."""
        self.current_index = 0
        self.round_number = 0
        self._generate_turn_order()
