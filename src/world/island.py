"""
Island System
Manages islands in the One Piece world with unique maps, NPCs, and encounters.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from world.map import Map
from utils.constants import TILE_SIZE


@dataclass
class IslandConnection:
    """Connection to another island via ship travel."""

    destination_island: str
    unlock_condition: Optional[str] = None  # Quest/story flag required
    travel_time: float = 5.0  # Seconds of travel animation
    berries_cost: int = 0  # Cost to travel (0 = free)


@dataclass
class NPCData:
    """NPC spawn data for an island."""

    npc_id: str
    name: str
    tile_x: int
    tile_y: int
    npc_type: str = "generic"  # generic, shopkeeper, quest_giver, crew_member
    dialogue_id: Optional[str] = None
    shop_id: Optional[str] = None
    quest_id: Optional[str] = None


@dataclass
class InteractiveObject:
    """Interactive object on an island (chest, door, sign, etc.)."""

    object_id: str
    object_type: str  # chest, door, sign, berry_pile, barrel
    tile_x: int
    tile_y: int
    interaction_type: str = "examine"  # examine, open, read, take
    item_rewards: List[Tuple[str, int]] = field(default_factory=list)  # [(item_id, quantity)]
    berries_reward: int = 0
    message: Optional[str] = None
    unlock_condition: Optional[str] = None
    one_time: bool = True  # Can only interact once


@dataclass
class EncounterZone:
    """Battle encounter zone on an island."""

    zone_id: str
    tiles: List[Tuple[int, int]]  # List of (x, y) tile coordinates
    enemy_groups: List[str]  # Enemy group IDs that can appear
    min_level: int = 1
    max_level: int = 10
    encounter_rate: float = 0.05  # 5% per step


class Island:
    """
    Represents an island in the One Piece world.
    Each island has a unique map, NPCs, shops, and story content.
    """

    def __init__(self, island_id: str, name: str, map_instance: Map):
        """
        Initialize an island.

        Args:
            island_id: Unique island identifier
            name: Display name
            map_instance: Map instance for this island
        """
        self.island_id = island_id
        self.name = name
        self.map = map_instance

        # Island metadata
        self.description = ""
        self.region = "East Blue"  # East Blue, Grand Line, New World
        self.recommended_level = 1
        self.music_id: Optional[str] = None

        # NPCs and objects
        self.npcs: List[NPCData] = []
        self.interactive_objects: List[InteractiveObject] = []

        # Encounters
        self.encounter_zones: List[EncounterZone] = []
        self.default_encounter_rate = 0.03  # 3% per step

        # Travel
        self.connections: List[IslandConnection] = []
        self.dock_position: Optional[Tuple[int, int]] = None  # Where ship docks

        # Story
        self.story_arc: Optional[str] = None
        self.unlock_condition: Optional[str] = None
        self.visited = False
        self.completed_interactions: List[str] = []  # Object IDs already used

    def add_npc(self, npc_data: NPCData):
        """Add an NPC to the island."""
        self.npcs.append(npc_data)

    def add_interactive_object(self, obj: InteractiveObject):
        """Add an interactive object to the island."""
        self.interactive_objects.append(obj)

    def add_encounter_zone(self, zone: EncounterZone):
        """Add an encounter zone to the island."""
        self.encounter_zones.append(zone)

    def add_connection(self, connection: IslandConnection):
        """Add a connection to another island."""
        self.connections.append(connection)

    def get_npc_at(self, tile_x: int, tile_y: int) -> Optional[NPCData]:
        """Get NPC at tile position."""
        for npc in self.npcs:
            if npc.tile_x == tile_x and npc.tile_y == tile_y:
                return npc
        return None

    def get_object_at(self, tile_x: int, tile_y: int) -> Optional[InteractiveObject]:
        """Get interactive object at tile position."""
        for obj in self.interactive_objects:
            if obj.tile_x == tile_x and obj.tile_y == tile_y:
                return obj
        return None

    def get_encounter_zone_at(self, tile_x: int, tile_y: int) -> Optional[EncounterZone]:
        """Get encounter zone at tile position."""
        for zone in self.encounter_zones:
            if (tile_x, tile_y) in zone.tiles:
                return zone
        return None

    def is_object_used(self, object_id: str) -> bool:
        """Check if an interactive object has been used."""
        return object_id in self.completed_interactions

    def mark_object_used(self, object_id: str):
        """Mark an interactive object as used."""
        if object_id not in self.completed_interactions:
            self.completed_interactions.append(object_id)

    def can_travel_to(self, destination: str, story_flags: Dict[str, bool]) -> bool:
        """
        Check if can travel to a destination island.

        Args:
            destination: Destination island ID
            story_flags: Current story progression flags

        Returns:
            True if travel is allowed
        """
        for connection in self.connections:
            if connection.destination_island == destination:
                # Check unlock condition
                if connection.unlock_condition:
                    return story_flags.get(connection.unlock_condition, False)
                return True
        return False

    def get_available_destinations(self, story_flags: Dict[str, bool]) -> List[IslandConnection]:
        """Get list of islands that can be traveled to."""
        available = []
        for connection in self.connections:
            if connection.unlock_condition:
                if story_flags.get(connection.unlock_condition, False):
                    available.append(connection)
            else:
                available.append(connection)
        return available


class IslandManager:
    """
    Manages all islands in the game world.
    Handles island loading, travel, and persistence.
    """

    def __init__(self):
        """Initialize island manager."""
        self.islands: Dict[str, Island] = {}
        self.current_island_id: Optional[str] = None
        self.story_flags: Dict[str, bool] = {}

    def register_island(self, island: Island):
        """
        Register an island with the manager.

        Args:
            island: Island to register
        """
        self.islands[island.island_id] = island
        print(f"Registered island: {island.name} ({island.island_id})")

    def get_island(self, island_id: str) -> Optional[Island]:
        """Get island by ID."""
        return self.islands.get(island_id)

    def get_current_island(self) -> Optional[Island]:
        """Get currently active island."""
        if self.current_island_id:
            return self.islands.get(self.current_island_id)
        return None

    def set_current_island(self, island_id: str):
        """
        Set the current active island.

        Args:
            island_id: Island ID to set as current
        """
        if island_id in self.islands:
            self.current_island_id = island_id
            island = self.islands[island_id]
            island.visited = True
            print(f"Changed island to: {island.name}")
        else:
            print(f"Warning: Island {island_id} not found!")

    def travel_to_island(self, destination_id: str) -> bool:
        """
        Travel to another island.

        Args:
            destination_id: Destination island ID

        Returns:
            True if travel successful
        """
        current = self.get_current_island()

        if not current:
            print("No current island set!")
            return False

        # Check if can travel
        if not current.can_travel_to(destination_id, self.story_flags):
            print(f"Cannot travel to {destination_id} - requirements not met")
            return False

        # Check if destination exists
        if destination_id not in self.islands:
            print(f"Destination island {destination_id} not found!")
            return False

        # Perform travel
        self.set_current_island(destination_id)
        return True

    def set_story_flag(self, flag: str, value: bool = True):
        """Set a story progression flag."""
        self.story_flags[flag] = value
        print(f"Story flag set: {flag} = {value}")

    def get_story_flag(self, flag: str) -> bool:
        """Get story progression flag value."""
        return self.story_flags.get(flag, False)

    def get_visited_islands(self) -> List[Island]:
        """Get list of islands that have been visited."""
        return [island for island in self.islands.values() if island.visited]

    def get_available_islands(self) -> List[Island]:
        """Get list of islands that can be traveled to from current island."""
        current = self.get_current_island()
        if not current:
            return []

        available_connections = current.get_available_destinations(self.story_flags)
        return [self.islands[conn.destination_island] for conn in available_connections
                if conn.destination_island in self.islands]

    def save_state(self) -> Dict:
        """
        Save island manager state.

        Returns:
            State dictionary
        """
        return {
            "current_island": self.current_island_id,
            "story_flags": self.story_flags.copy(),
            "visited_islands": [iid for iid, island in self.islands.items() if island.visited],
            "completed_interactions": {
                iid: island.completed_interactions.copy()
                for iid, island in self.islands.items()
            }
        }

    def load_state(self, state: Dict):
        """
        Load island manager state.

        Args:
            state: State dictionary
        """
        self.current_island_id = state.get("current_island")
        self.story_flags = state.get("story_flags", {})

        # Mark visited islands
        for island_id in state.get("visited_islands", []):
            if island_id in self.islands:
                self.islands[island_id].visited = True

        # Restore completed interactions
        completed = state.get("completed_interactions", {})
        for island_id, interactions in completed.items():
            if island_id in self.islands:
                self.islands[island_id].completed_interactions = interactions.copy()
