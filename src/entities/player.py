"""
Player Character Class
Extended character class specifically for the player.
"""

from typing import Dict, List, Optional, TYPE_CHECKING
from entities.character import Character
from entities.stats import Stats
from utils.constants import STARTING_BERRIES
from systems.item_system import Inventory

if TYPE_CHECKING:
    from systems.party_manager import PartyManager


class Player(Character):
    """
    Player character with additional functionality.
    Manages inventory, berries, and player-specific features.
    """
    
    def __init__(self, name: str, level: int = 1):
        """
        Initialize the player character.
        
        Args:
            name: Player name
            level: Starting level
        """
        super().__init__(name, level)
        
        # Player-specific attributes
        self.berries = STARTING_BERRIES

        # New inventory system
        self.inventory = Inventory(max_slots=50)

        # Legacy inventory (deprecated, kept for compatibility)
        self.old_inventory = []
        self.key_items = []
        
        # Bounty
        self.bounty = 0
        
        # Reputation
        self.reputation = {
            "pirates": 0,
            "marines": 0,
            "civilians": 0
        }
        
        # Discovered locations
        self.discovered_islands = []
        self.unlocked_fast_travel = []
        
        # Statistics
        self.stats_tracker = {
            "battles_won": 0,
            "enemies_defeated": 0,
            "berries_earned": 0,
            "berries_spent": 0,
            "islands_visited": 0,
            "deaths": 0,
            "playtime": 0.0
        }
        
        # Background/appearance (for character creation)
        self.background = None
        self.appearance = {}

        # Party management (initialized later to avoid circular import)
        self.party_manager: Optional['PartyManager'] = None
    
    # Berries (currency)
    
    def add_berries(self, amount: int):
        """
        Add berries.
        
        Args:
            amount: Amount to add
        """
        self.berries += amount
        self.stats_tracker["berries_earned"] += amount
    
    def spend_berries(self, amount: int) -> bool:
        """
        Spend berries.
        
        Args:
            amount: Amount to spend
        
        Returns:
            True if had enough berries
        """
        if self.berries >= amount:
            self.berries -= amount
            self.stats_tracker["berries_spent"] += amount
            return True
        return False
    
    def has_berries(self, amount: int) -> bool:
        """Check if player has enough berries."""
        return self.berries >= amount
    
    # Inventory management
    
    def add_item(self, item_id: str, quantity: int = 1) -> bool:
        """
        Add item to inventory.
        
        Args:
            item_id: Item ID
            quantity: Amount to add
        
        Returns:
            True if added successfully
        """
        # Check if item is stackable and already in inventory
        for inv_item in self.inventory:
            if inv_item["id"] == item_id:
                # Stack it
                inv_item["quantity"] += quantity
                return True
        
        # Add new item
        self.inventory.append({
            "id": item_id,
            "quantity": quantity
        })
        return True
    
    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        """
        Remove item from inventory.
        
        Args:
            item_id: Item ID
            quantity: Amount to remove
        
        Returns:
            True if had enough to remove
        """
        for inv_item in self.inventory:
            if inv_item["id"] == item_id:
                if inv_item["quantity"] >= quantity:
                    inv_item["quantity"] -= quantity
                    
                    # Remove if quantity is 0
                    if inv_item["quantity"] <= 0:
                        self.inventory.remove(inv_item)
                    
                    return True
        return False
    
    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        """
        Check if player has an item.
        
        Args:
            item_id: Item ID
            quantity: Required quantity
        
        Returns:
            True if player has enough
        """
        for inv_item in self.inventory:
            if inv_item["id"] == item_id:
                return inv_item["quantity"] >= quantity
        return False
    
    def get_item_quantity(self, item_id: str) -> int:
        """
        Get quantity of an item in inventory.
        
        Args:
            item_id: Item ID
        
        Returns:
            Quantity owned
        """
        for inv_item in self.inventory:
            if inv_item["id"] == item_id:
                return inv_item["quantity"]
        return 0
    
    def use_item(self, item_id: str, item_data: Dict) -> bool:
        """
        Use a consumable item.
        
        Args:
            item_id: Item ID
            item_data: Full item data
        
        Returns:
            True if used successfully
        """
        if not self.has_item(item_id):
            return False
        
        # Apply effects
        effects = item_data.get("effects", [])
        for effect in effects:
            effect_type = effect.get("type", "")
            value = effect.get("value", 0)
            
            if effect_type == "Restore HP":
                self.heal(value)
                print(f"Restored {value} HP!")
            elif effect_type == "Restore AP":
                self.restore_ap(value)
                print(f"Restored {value} AP!")
        
        # Remove item from inventory
        self.remove_item(item_id, 1)
        return True
    
    # Key items
    
    def add_key_item(self, item_id: str):
        """Add a key item (cannot be sold/discarded)."""
        if item_id not in self.key_items:
            self.key_items.append(item_id)
            print(f"Obtained key item: {item_id}")
    
    def has_key_item(self, item_id: str) -> bool:
        """Check if player has a key item."""
        return item_id in self.key_items
    
    # Reputation
    
    def change_reputation(self, faction: str, amount: int):
        """
        Change reputation with a faction.
        
        Args:
            faction: Faction name (pirates, marines, civilians)
            amount: Amount to change (can be negative)
        """
        if faction in self.reputation:
            self.reputation[faction] += amount
            
            # Clamp between -100 and 100
            self.reputation[faction] = max(-100, min(100, self.reputation[faction]))
    
    def get_reputation(self, faction: str) -> int:
        """Get reputation with a faction."""
        return self.reputation.get(faction, 0)
    
    # Bounty
    
    def increase_bounty(self, amount: int):
        """Increase bounty."""
        self.bounty += amount
        print(f"Bounty increased by {amount:,} Berries!")
        print(f"Current bounty: {self.bounty:,} Berries")
    
    def clear_bounty(self):
        """Clear bounty (e.g., after serving time)."""
        self.bounty = 0
    
    # World exploration
    
    def discover_island(self, island_id: str):
        """Discover a new island."""
        if island_id not in self.discovered_islands:
            self.discovered_islands.append(island_id)
            self.stats_tracker["islands_visited"] += 1
            print(f"Discovered new island: {island_id}")
    
    def unlock_fast_travel(self, island_id: str):
        """Unlock fast travel to an island."""
        if island_id not in self.unlocked_fast_travel:
            self.unlocked_fast_travel.append(island_id)
            print(f"Fast travel unlocked: {island_id}")
    
    def can_fast_travel_to(self, island_id: str) -> bool:
        """Check if can fast travel to an island."""
        return island_id in self.unlocked_fast_travel
    
    # Statistics tracking
    
    def record_battle_victory(self, enemies_defeated: int = 1):
        """Record a battle victory."""
        self.stats_tracker["battles_won"] += 1
        self.stats_tracker["enemies_defeated"] += enemies_defeated
    
    def record_death(self):
        """Record a death."""
        self.stats_tracker["deaths"] += 1
    
    def update_playtime(self, delta_time: float):
        """Update total playtime."""
        self.stats_tracker["playtime"] += delta_time
    
    def get_playtime_formatted(self) -> str:
        """Get playtime in readable format."""
        total_seconds = int(self.stats_tracker["playtime"])
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    # Level up customization
    
    def _apply_level_up_bonuses(self):
        """Player can choose stat increases (can be customized)."""
        # Default: balanced growth
        self.stats.increase_stat("strength", 2)
        self.stats.increase_stat("defense", 1)
        self.stats.increase_stat("agility", 1)
        self.stats.increase_stat("intelligence", 1)
        self.stats.increase_stat("willpower", 2)
        
        # Gain mastery exp for Devil Fruit
        if self.devil_fruit:
            self.devil_fruit.gain_mastery_exp(50)
    
    # Death handling
    
    def on_death(self):
        """Player-specific death handling."""
        super().on_death()
        self.record_death()
        
        # Player loses some berries on death
        berries_lost = int(self.berries * 0.1)  # Lose 10%
        self.berries -= berries_lost
        print(f"Lost {berries_lost:,} Berries...")
    
    # Character creation
    
    def set_appearance(self, appearance_data: Dict):
        """Set character appearance."""
        self.appearance = appearance_data
    
    def set_background(self, background_id: str):
        """Set character background."""
        self.background = background_id
    
    # Saving/loading
    
    def to_dict(self) -> Dict:
        """
        Convert player to dictionary for saving.
        
        Returns:
            Dictionary representation
        """
        data = super().to_dict()
        
        # Add player-specific data
        data.update({
            "berries": self.berries,
            "inventory": self.inventory.copy(),
            "key_items": self.key_items.copy(),
            "bounty": self.bounty,
            "reputation": self.reputation.copy(),
            "discovered_islands": self.discovered_islands.copy(),
            "unlocked_fast_travel": self.unlocked_fast_travel.copy(),
            "statistics": self.stats_tracker.copy(),
            "background": self.background,
            "appearance": self.appearance.copy()
        })
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Player':
        """
        Create Player from saved data.
        
        Args:
            data: Saved player data
        
        Returns:
            Player instance
        """
        # Create player
        player = cls(
            name=data.get("name", "Player"),
            level=data.get("level", 1)
        )
        
        # Restore basic data
        player.experience = data.get("experience", 0)
        player.exp_to_next_level = data.get("exp_to_next_level", 100)
        player.current_hp = data.get("current_hp", player.max_hp)
        player.current_ap = data.get("current_ap", player.max_ap)
        player.is_alive = data.get("is_alive", True)
        
        # Restore stats
        if "stats" in data:
            player.stats = Stats.from_dict(data["stats"])
        
        # Restore player-specific data
        player.berries = data.get("berries", STARTING_BERRIES)
        player.inventory = data.get("inventory", [])
        player.key_items = data.get("key_items", [])
        player.bounty = data.get("bounty", 0)
        player.reputation = data.get("reputation", {"pirates": 0, "marines": 0, "civilians": 0})
        player.discovered_islands = data.get("discovered_islands", [])
        player.unlocked_fast_travel = data.get("unlocked_fast_travel", [])
        player.stats_tracker = data.get("statistics", {})
        player.background = data.get("background")
        player.appearance = data.get("appearance", {})
        
        # Restore Devil Fruit if present
        if "devil_fruit" in data:
            # Note: Would need to load fruit_data from devil_fruit_manager
            # This is just the save structure
            pass
        
        return player
    
    def __str__(self) -> str:
        """String representation."""
        fruit_text = f" [{self.devil_fruit.name}]" if self.devil_fruit else ""
        return f"{self.name}{fruit_text} (Lv. {self.level}) - HP: {self.current_hp}/{self.max_hp} | Berries: {self.berries:,}"
