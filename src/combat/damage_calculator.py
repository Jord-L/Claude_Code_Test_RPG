"""
Damage Calculator
Handles damage calculations for combat including type advantages and resistances.
"""

from typing import Dict, Optional
from entities.character import Character
import random


class DamageCalculator:
    """
    Calculates damage in combat with support for:
    - Physical/Elemental damage types
    - Critical hits
    - Type advantages/resistances
    - Devil Fruit interactions
    """
    
    def __init__(self):
        """Initialize damage calculator."""
        # Type advantage multipliers
        self.type_advantages = {
            "Fire": {"Ice": 1.5, "Plant": 1.5, "Water": 0.5},
            "Ice": {"Water": 1.5, "Fire": 0.5},
            "Lightning": {"Water": 1.5, "Earth": 0.5},
            "Water": {"Fire": 1.5, "Lightning": 0.5},
            "Earth": {"Lightning": 1.5, "Plant": 0.5},
            "Plant": {"Water": 1.5, "Fire": 0.5}
        }
        
        # Base damage variance (damage is multiplied by random value in this range)
        self.damage_variance = (0.85, 1.0)
    
    def calculate_physical_damage(
        self,
        attacker: Character,
        defender: Character,
        base_damage: Optional[int] = None
    ) -> int:
        """
        Calculate physical damage from attacker to defender.
        
        Args:
            attacker: Attacking character
            defender: Defending character
            base_damage: Optional base damage (uses attacker's attack if not provided)
        
        Returns:
            Final damage amount
        """
        # Get base damage
        if base_damage is None:
            base_damage = attacker.get_attack_power()
        
        # Apply damage variance
        variance = random.uniform(*self.damage_variance)
        damage = base_damage * variance
        
        # Check for critical hit
        if self._roll_critical(attacker):
            crit_multiplier = attacker.stats.get_critical_damage()
            damage *= crit_multiplier
            print("  Critical Hit!")
        
        # Apply defense
        defense = defender.get_defense_power()
        defense_reduction = defense * 0.5  # 50% of defense reduces damage
        damage = max(1, damage - defense_reduction)
        
        # Check for Logia intangibility
        if defender.devil_fruit and defender.devil_fruit.has_intangibility():
            # Physical attacks don't hit Logia users (unless Haki is implemented later)
            # TODO: Check for Haki or natural counter
            print("  Attack passed through!")
            return 0
        
        return int(damage)
    
    def calculate_ability_damage(
        self,
        attacker: Character,
        defender: Character,
        base_damage: int,
        damage_type: str = "Physical"
    ) -> int:
        """
        Calculate ability damage (Devil Fruit or special skill).
        
        Args:
            attacker: Character using ability
            defender: Target character
            base_damage: Base damage of the ability
            damage_type: Type of damage (Physical, Elemental, etc.)
        
        Returns:
            Final damage amount
        """
        # Start with base damage
        damage = float(base_damage)
        
        # Apply damage variance
        variance = random.uniform(*self.damage_variance)
        damage *= variance
        
        # Check for critical hit
        if self._roll_critical(attacker):
            crit_multiplier = attacker.stats.get_critical_damage()
            damage *= crit_multiplier
            print("  Critical Hit!")
        
        # Handle different damage types
        if damage_type == "Physical":
            # Apply defense like physical attacks
            defense = defender.get_defense_power()
            defense_reduction = defense * 0.5
            damage = max(1, damage - defense_reduction)
            
            # Check for Logia intangibility
            if defender.devil_fruit and defender.devil_fruit.has_intangibility():
                print("  Attack passed through!")
                return 0
        
        elif damage_type == "Elemental":
            # Elemental damage ignores physical defense
            # But check for type advantages
            damage = self._apply_elemental_modifiers(damage, attacker, defender)
            
            # Elemental abilities can hit Logia users if same element or counter element
            # For now, just reduce damage against Logia
            if defender.devil_fruit and defender.devil_fruit.has_intangibility():
                # Check if it's a matching or counter element
                attacker_element = self._get_character_element(attacker)
                defender_element = self._get_character_element(defender)
                
                if attacker_element and defender_element:
                    if attacker_element == defender_element:
                        # Same element - no effect
                        print("  Attack has no effect on the same element!")
                        return 0
                    elif self._is_counter_element(attacker_element, defender_element):
                        # Counter element - extra damage
                        print("  Super effective!")
                        damage *= 1.5
                else:
                    # Different element - reduced damage
                    damage *= 0.25
        
        elif damage_type == "True":
            # True damage ignores all defenses and resistances
            pass
        
        # Apply Devil Fruit modifiers
        damage = self._apply_devil_fruit_modifiers(damage, attacker, defender)
        
        return int(max(1, damage))
    
    def _roll_critical(self, character: Character) -> bool:
        """
        Roll for critical hit.
        
        Args:
            character: Character to check critical chance
        
        Returns:
            True if critical hit
        """
        crit_chance = character.stats.get_critical_chance()
        return random.random() * 100 < crit_chance
    
    def _get_character_element(self, character: Character) -> Optional[str]:
        """
        Get character's elemental type from Devil Fruit.
        
        Args:
            character: Character to check
        
        Returns:
            Element name or None
        """
        if not character.devil_fruit:
            return None
        
        return character.devil_fruit.element
    
    def _apply_elemental_modifiers(
        self,
        damage: float,
        attacker: Character,
        defender: Character
    ) -> float:
        """
        Apply elemental type advantages/disadvantages.
        
        Args:
            damage: Base damage
            attacker: Attacking character
            defender: Defending character
        
        Returns:
            Modified damage
        """
        attacker_element = self._get_character_element(attacker)
        defender_element = self._get_character_element(defender)
        
        if not attacker_element or not defender_element:
            return damage
        
        # Check type chart
        if attacker_element in self.type_advantages:
            advantages = self.type_advantages[attacker_element]
            
            if defender_element in advantages:
                multiplier = advantages[defender_element]
                damage *= multiplier
                
                if multiplier > 1.0:
                    print("  It's super effective!")
                elif multiplier < 1.0:
                    print("  It's not very effective...")
        
        return damage
    
    def _is_counter_element(self, attacking_element: str, defending_element: str) -> bool:
        """
        Check if attacking element counters defending element.
        
        Args:
            attacking_element: Attacker's element
            defending_element: Defender's element
        
        Returns:
            True if counter
        """
        if attacking_element not in self.type_advantages:
            return False
        
        advantages = self.type_advantages[attacking_element]
        return defending_element in advantages and advantages[defending_element] > 1.0
    
    def _apply_devil_fruit_modifiers(
        self,
        damage: float,
        attacker: Character,
        defender: Character
    ) -> float:
        """
        Apply Devil Fruit-specific modifiers to damage.
        
        Args:
            damage: Base damage
            attacker: Attacking character
            defender: Defending character
        
        Returns:
            Modified damage
        """
        # Attacker bonuses
        if attacker.devil_fruit:
            # Mastery level bonus (1% per level)
            mastery_bonus = 1.0 + (attacker.devil_fruit.mastery_level * 0.01)
            damage *= mastery_bonus
        
        # Defender resistances
        if defender.devil_fruit:
            # Some fruits have specific resistances
            # TODO: Implement fruit-specific resistance system
            pass
        
        return damage
    
    def calculate_healing(
        self,
        healer: Character,
        target: Character,
        base_healing: int
    ) -> int:
        """
        Calculate healing amount.
        
        Args:
            healer: Character performing healing
            target: Character being healed
            base_healing: Base healing amount
        
        Returns:
            Final healing amount
        """
        # Apply variance
        variance = random.uniform(0.9, 1.1)
        healing = base_healing * variance
        
        # Intelligence affects healing (if healer has high INT)
        if hasattr(healer.stats, 'get_intelligence'):
            int_bonus = healer.stats.get_intelligence() * 0.1
            healing *= (1.0 + int_bonus / 100.0)
        
        # Some Devil Fruits boost healing
        if healer.devil_fruit:
            # TODO: Check for healing-boost fruits
            pass
        
        return int(max(1, healing))
    
    def calculate_status_duration(
        self,
        attacker: Character,
        defender: Character,
        base_duration: int
    ) -> int:
        """
        Calculate how long a status effect lasts.
        
        Args:
            attacker: Character applying status
            defender: Character receiving status
            base_duration: Base duration in turns
        
        Returns:
            Final duration
        """
        duration = base_duration
        
        # Willpower can reduce status duration
        will_resistance = defender.stats.get_willpower() * 0.01
        duration = max(1, int(duration * (1.0 - will_resistance / 100.0)))
        
        return duration
    
    def get_flee_chance(
        self,
        fleeing_party: list[Character],
        enemy_party: list[Character]
    ) -> float:
        """
        Calculate chance of successfully fleeing.
        
        Args:
            fleeing_party: Party attempting to flee
            enemy_party: Enemy party
        
        Returns:
            Flee chance as percentage (0-100)
        """
        # Calculate average speed of both parties
        flee_speed = sum(c.get_speed() for c in fleeing_party if c.is_alive)
        flee_speed /= max(1, len([c for c in fleeing_party if c.is_alive]))
        
        enemy_speed = sum(c.get_speed() for c in enemy_party if c.is_alive)
        enemy_speed /= max(1, len([c for c in enemy_party if c.is_alive]))
        
        # Base 50% chance
        flee_chance = 50.0
        
        # +/- 5% per speed difference
        speed_diff = flee_speed - enemy_speed
        flee_chance += speed_diff * 5.0
        
        # Clamp between 10% and 90%
        flee_chance = max(10.0, min(90.0, flee_chance))
        
        return flee_chance
    
    def calculate_exp_reward(self, defeated_enemies: list[Character]) -> int:
        """
        Calculate experience reward from defeated enemies.
        
        Args:
            defeated_enemies: List of defeated enemies
        
        Returns:
            Total experience points
        """
        total_exp = 0
        
        for enemy in defeated_enemies:
            # Base: 10 exp per enemy level
            base_exp = enemy.level * 10
            
            # Bonus for higher level enemies
            if enemy.level >= 10:
                base_exp = int(base_exp * 1.5)
            
            total_exp += base_exp
        
        return total_exp
    
    def calculate_berries_reward(self, defeated_enemies: list[Character]) -> int:
        """
        Calculate berries reward from defeated enemies.
        
        Args:
            defeated_enemies: List of defeated enemies
        
        Returns:
            Total berries
        """
        total_berries = 0
        
        for enemy in defeated_enemies:
            # Base: 50 berries per enemy level
            base_berries = enemy.level * 50
            
            # Random variance (80-120%)
            variance = random.uniform(0.8, 1.2)
            berries = int(base_berries * variance)
            
            total_berries += berries
        
        return total_berries
