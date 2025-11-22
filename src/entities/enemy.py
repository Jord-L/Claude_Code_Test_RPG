"""
Enemy Character Class
Extended character class for enemy combatants.
"""

from typing import Dict, Optional
from entities.character import Character
from entities.stats import Stats


class Enemy(Character):
    """
    Enemy character with AI behavior and rewards.
    """
    
    def __init__(
        self,
        name: str,
        level: int = 1,
        enemy_type: str = "Generic",
        difficulty: str = "normal"
    ):
        """
        Initialize an enemy character.
        
        Args:
            name: Enemy name
            level: Enemy level
            enemy_type: Type of enemy (for loot tables)
            difficulty: AI difficulty
        """
        super().__init__(name, level)
        
        # Enemy-specific attributes
        self.enemy_type = enemy_type
        self.difficulty = difficulty
        
        # Rewards
        self.exp_reward = level * 10
        self.berries_reward = level * 50
        self.item_drops = []  # List of (item_id, drop_chance) tuples
        
        # AI personality
        self.ai_personality = "balanced"  # aggressive, defensive, tactical, balanced
        
        # Enemy description
        self.description = ""
    
    def _apply_level_up_bonuses(self):
        """Apply stat increases on level up."""
        # Enemies get slightly different growth than players
        self.stats.increase_stat("strength", 2)
        self.stats.increase_stat("defense", 2)
        self.stats.increase_stat("agility", 1)
        self.stats.increase_stat("willpower", 1)
    
    def set_stats(
        self,
        strength: int,
        defense: int,
        agility: int,
        intelligence: int = None,
        willpower: int = None
    ):
        """
        Manually set enemy stats.
        
        Args:
            strength: Strength value
            defense: Defense value
            agility: Agility value
            intelligence: Intelligence value (optional)
            willpower: Willpower value (optional)
        """
        # Direct attribute assignment (Stats class doesn't have set_stat method)
        self.stats.strength = strength
        self.stats.defense = defense
        self.stats.agility = agility
        
        if intelligence is not None:
            self.stats.intelligence = intelligence
        
        if willpower is not None:
            self.stats.willpower = willpower
        
        # Recalculate max HP/AP
        self.max_hp = self.stats.get_max_hp(self.level)
        self.max_ap = self.stats.get_max_ap(self.level)
        self.current_hp = self.max_hp
        self.current_ap = self.max_ap
    
    def set_rewards(self, exp: int, berries: int):
        """
        Set rewards for defeating this enemy.
        
        Args:
            exp: Experience reward
            berries: Berries reward
        """
        self.exp_reward = exp
        self.berries_reward = berries
    
    def add_item_drop(self, item_id: str, chance: float):
        """
        Add an item to the drop table.
        
        Args:
            item_id: Item ID
            chance: Drop chance (0.0 to 1.0)
        """
        self.item_drops.append((item_id, chance))
    
    def get_drops(self) -> list:
        """
        Roll for item drops.
        
        Returns:
            List of item IDs that dropped
        """
        import random
        drops = []
        
        for item_id, chance in self.item_drops:
            if random.random() < chance:
                drops.append(item_id)
        
        return drops
    
    def to_dict(self) -> Dict:
        """
        Convert enemy to dictionary for saving.
        
        Returns:
            Dictionary representation
        """
        data = super().to_dict()
        
        # Add enemy-specific data
        data.update({
            "enemy_type": self.enemy_type,
            "difficulty": self.difficulty,
            "exp_reward": self.exp_reward,
            "berries_reward": self.berries_reward,
            "item_drops": self.item_drops,
            "ai_personality": self.ai_personality,
            "description": self.description
        })
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Enemy':
        """
        Create Enemy from dictionary.
        
        Args:
            data: Enemy data
        
        Returns:
            Enemy instance
        """
        enemy = cls(
            name=data.get("name", "Unknown Enemy"),
            level=data.get("level", 1),
            enemy_type=data.get("enemy_type", "Generic"),
            difficulty=data.get("difficulty", "normal")
        )
        
        # Restore stats
        if "stats" in data:
            enemy.stats = Stats.from_dict(data["stats"])
        
        # Restore state
        enemy.current_hp = data.get("current_hp", enemy.max_hp)
        enemy.current_ap = data.get("current_ap", enemy.max_ap)
        enemy.is_alive = data.get("is_alive", True)
        
        # Restore enemy data
        enemy.exp_reward = data.get("exp_reward", enemy.level * 10)
        enemy.berries_reward = data.get("berries_reward", enemy.level * 50)
        enemy.item_drops = data.get("item_drops", [])
        enemy.ai_personality = data.get("ai_personality", "balanced")
        enemy.description = data.get("description", "")
        
        # Restore Devil Fruit if present
        if "devil_fruit" in data:
            # Would need fruit data from manager
            pass
        
        return enemy
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.name} (Lv. {self.level}) - HP: {self.current_hp}/{self.max_hp}"
    
    def __repr__(self) -> str:
        """Debug representation."""
        return f"Enemy(name={self.name}, level={self.level}, type={self.enemy_type})"


class EnemyFactory:
    """Factory for creating common enemy types."""
    
    @staticmethod
    def create_bandit(level: int = 1) -> Enemy:
        """Create a bandit enemy."""
        enemy = Enemy("Bandit", level, "Bandit", "easy")
        enemy.set_stats(
            strength=10 + level * 2,
            defense=8 + level,
            agility=12 + level * 2
        )
        enemy.set_rewards(
            exp=level * 8,
            berries=level * 40
        )
        enemy.ai_personality = "aggressive"
        enemy.description = "A common thug looking for easy targets."
        return enemy
    
    @staticmethod
    def create_marine(level: int = 1) -> Enemy:
        """Create a Marine soldier enemy."""
        enemy = Enemy("Marine Soldier", level, "Marine", "normal")
        enemy.set_stats(
            strength=12 + level * 2,
            defense=12 + level * 2,
            agility=10 + level
        )
        enemy.set_rewards(
            exp=level * 12,
            berries=level * 60
        )
        enemy.ai_personality = "balanced"
        enemy.description = "A disciplined Marine soldier serving the World Government."
        return enemy
    
    @staticmethod
    def create_pirate(level: int = 1) -> Enemy:
        """Create a pirate enemy."""
        enemy = Enemy("Pirate", level, "Pirate", "normal")
        enemy.set_stats(
            strength=14 + level * 2,
            defense=8 + level,
            agility=11 + level
        )
        enemy.set_rewards(
            exp=level * 10,
            berries=level * 50
        )
        enemy.ai_personality = "aggressive"
        enemy.description = "A rival pirate seeking treasure and glory."
        return enemy
    
    @staticmethod
    def create_sea_beast(level: int = 1) -> Enemy:
        """Create a sea beast enemy."""
        enemy = Enemy("Sea Beast", level, "Beast", "normal")
        enemy.set_stats(
            strength=16 + level * 3,
            defense=14 + level * 2,
            agility=6 + level
        )
        enemy.set_rewards(
            exp=level * 15,
            berries=level * 30
        )
        enemy.ai_personality = "aggressive"
        enemy.description = "A dangerous creature from the seas."
        return enemy
    
    @staticmethod
    def create_boss(
        name: str,
        level: int,
        enemy_type: str = "Boss"
    ) -> Enemy:
        """
        Create a boss enemy with enhanced stats.
        
        Args:
            name: Boss name
            level: Boss level
            enemy_type: Boss type
        
        Returns:
            Boss enemy
        """
        enemy = Enemy(name, level, enemy_type, "hard")
        
        # Bosses have significantly higher stats
        enemy.set_stats(
            strength=20 + level * 4,
            defense=18 + level * 3,
            agility=12 + level * 2,
            intelligence=15 + level * 2,
            willpower=18 + level * 2
        )
        
        # Much better rewards
        enemy.set_rewards(
            exp=level * 50,
            berries=level * 200
        )
        
        # Multiply HP for boss
        enemy.max_hp = int(enemy.max_hp * 3)
        enemy.current_hp = enemy.max_hp
        
        # More AP
        enemy.max_ap = int(enemy.max_ap * 2)
        enemy.current_ap = enemy.max_ap
        
        enemy.ai_personality = "tactical"
        
        return enemy
    
    @staticmethod
    def create_custom_enemy(
        name: str,
        level: int,
        stats: Dict[str, int],
        rewards: Dict[str, int],
        enemy_type: str = "Custom",
        difficulty: str = "normal"
    ) -> Enemy:
        """
        Create a custom enemy with specific stats.
        
        Args:
            name: Enemy name
            level: Enemy level
            stats: Dict of stat values
            rewards: Dict with "exp" and "berries"
            enemy_type: Enemy type
            difficulty: AI difficulty
        
        Returns:
            Custom enemy
        """
        enemy = Enemy(name, level, enemy_type, difficulty)
        
        enemy.set_stats(
            strength=stats.get("strength", 10),
            defense=stats.get("defense", 10),
            agility=stats.get("agility", 10),
            intelligence=stats.get("intelligence", 10),
            willpower=stats.get("willpower", 10)
        )
        
        enemy.set_rewards(
            exp=rewards.get("exp", level * 10),
            berries=rewards.get("berries", level * 50)
        )
        
        return enemy
