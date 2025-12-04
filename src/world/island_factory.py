"""
Island Factory
Creates the 8 islands of the East Blue with unique maps and content.
"""

import random
from typing import List, Tuple
from world.map import Map
from world.tile import TileType
from world.island import (
    Island, NPCData, InteractiveObject, EncounterZone, IslandConnection
)


class IslandFactory:
    """Factory for creating pre-built islands."""

    @staticmethod
    def create_foosha_village() -> Island:
        """
        Create Foosha Village - the starting island.
        Small peaceful village where Alex grew up.
        """
        # Create map (30x30 tiles)
        map_instance = Map(30, 30, TileType.GRASS)
        map_instance.name = "Foosha Village"
        map_instance.spawn_point = (15, 25)  # Start near bottom

        # Create island
        island = Island("foosha_village", "Foosha Village", map_instance)
        island.description = "A peaceful village in the East Blue where Alex grew up."
        island.recommended_level = 1
        island.story_arc = "Romance Dawn"
        island.dock_position = (15, 28)

        # Build map layout
        IslandFactory._build_foosha_village_map(map_instance)

        # Add NPCs
        island.add_npc(NPCData(
            npc_id="mayor",
            name="Mayor Woop Slap",
            tile_x=15,
            tile_y=10,
            npc_type="quest_giver",
            dialogue_id="mayor_greeting"
        ))

        island.add_npc(NPCData(
            npc_id="makino",
            name="Mira",
            tile_x=12,
            tile_y=12,
            npc_type="shopkeeper",
            shop_id="makino_bar",
            dialogue_id="makino_greeting"
        ))

        island.add_npc(NPCData(
            npc_id="villager_1",
            name="Villager",
            tile_x=18,
            tile_y=15,
            dialogue_id="villager_generic"
        ))

        # Add interactive objects
        island.add_interactive_object(InteractiveObject(
            object_id="chest_1",
            object_type="chest",
            tile_x=8,
            tile_y=8,
            item_rewards=[("health_potion_small", 3), ("wooden_sword", 1)],
            berries_reward=500,
            message="Found starter supplies!"
        ))

        island.add_interactive_object(InteractiveObject(
            object_id="sign_1",
            object_type="sign",
            tile_x=15,
            tile_y=20,
            interaction_type="read",
            message="Welcome to Foosha Village!\nA peaceful place in the East Blue.",
            one_time=False
        ))

        # Add simple encounter zone (bandits in the forest)
        forest_tiles = [(x, y) for x in range(0, 5) for y in range(0, 10)]
        island.add_encounter_zone(EncounterZone(
            zone_id="forest_bandits",
            tiles=forest_tiles,
            enemy_groups=["bandit"],
            min_level=1,
            max_level=3,
            encounter_rate=0.03
        ))

        # Add connection to Shell Town (unlocked by default)
        island.add_connection(IslandConnection(
            destination_island="shell_town",
            berries_cost=100
        ))

        return island

    @staticmethod
    def create_shell_town() -> Island:
        """
        Create Shell Town - Marine base town.
        Where Alex meets Kane.
        """
        # Create map (35x35 tiles)
        map_instance = Map(35, 35, TileType.STONE)
        map_instance.name = "Shell Town"
        map_instance.spawn_point = (17, 30)

        island = Island("shell_town", "Shell Town", map_instance)
        island.description = "A town dominated by a Marine base. Captain Morgan rules with an iron fist."
        island.recommended_level = 3
        island.story_arc = "Romance Dawn"
        island.dock_position = (17, 33)

        # Build map
        IslandFactory._build_shell_town_map(map_instance)

        # Add NPCs
        island.add_npc(NPCData(
            npc_id="zoro",
            name="Kane",
            tile_x=17,
            tile_y=15,
            npc_type="crew_member",
            dialogue_id="zoro_recruitment",
            quest_id="recruit_zoro"
        ))

        island.add_npc(NPCData(
            npc_id="weapons_dealer",
            name="Weapons Dealer",
            tile_x=25,
            tile_y=20,
            npc_type="shopkeeper",
            shop_id="shell_weapons"
        ))

        # Marine encounter zone
        marine_tiles = [(x, y) for x in range(10, 25) for y in range(10, 20)]
        island.add_encounter_zone(EncounterZone(
            zone_id="marine_base",
            tiles=marine_tiles,
            enemy_groups=["marine_soldier"],
            min_level=3,
            max_level=5,
            encounter_rate=0.05
        ))

        # Connections
        island.add_connection(IslandConnection(
            destination_island="foosha_village",
            berries_cost=100
        ))
        island.add_connection(IslandConnection(
            destination_island="orange_town",
            berries_cost=200
        ))

        return island

    @staticmethod
    def create_orange_town() -> Island:
        """
        Create Orange Town - town terrorized by Buggy the Clown.
        Where Alex meets Marina.
        """
        map_instance = Map(40, 40, TileType.DIRT)
        map_instance.name = "Orange Town"
        map_instance.spawn_point = (20, 35)

        island = Island("orange_town", "Orange Town", map_instance)
        island.description = "Once peaceful, now terrorized by Buggy the Clown and his pirate crew."
        island.recommended_level = 5
        island.story_arc = "Orange Town"
        island.dock_position = (20, 38)

        IslandFactory._build_orange_town_map(map_instance)

        # NPCs
        island.add_npc(NPCData(
            npc_id="nami",
            name="Marina",
            tile_x=20,
            tile_y=20,
            npc_type="crew_member",
            dialogue_id="nami_recruitment",
            quest_id="recruit_nami"
        ))

        island.add_npc(NPCData(
            npc_id="pet_food_owner",
            name="Hocker",
            tile_x=15,
            tile_y=15,
            npc_type="quest_giver",
            quest_id="save_orange_town"
        ))

        # Buggy pirate encounter zones
        pirate_tiles = [(x, y) for x in range(15, 30) for y in range(10, 25)]
        island.add_encounter_zone(EncounterZone(
            zone_id="buggy_pirates",
            tiles=pirate_tiles,
            enemy_groups=["pirate"],
            min_level=5,
            max_level=7,
            encounter_rate=0.06
        ))

        # Connections
        island.add_connection(IslandConnection(
            destination_island="shell_town",
            berries_cost=200
        ))
        island.add_connection(IslandConnection(
            destination_island="syrup_village",
            berries_cost=300
        ))

        return island

    @staticmethod
    def create_syrup_village() -> Island:
        """
        Create Syrup Village - Finn's home village.
        Where Kuro's plan unfolds.
        """
        map_instance = Map(45, 45, TileType.GRASS)
        map_instance.name = "Syrup Village"
        map_instance.spawn_point = (22, 40)

        island = Island("syrup_village", "Syrup Village", map_instance)
        island.description = "A peaceful village with a large mansion on the hill."
        island.recommended_level = 7
        island.story_arc = "Syrup Village"
        island.dock_position = (22, 43)

        IslandFactory._build_syrup_village_map(map_instance)

        # NPCs
        island.add_npc(NPCData(
            npc_id="usopp",
            name="Finn",
            tile_x=22,
            tile_y=25,
            npc_type="crew_member",
            dialogue_id="usopp_recruitment",
            quest_id="recruit_usopp"
        ))

        island.add_npc(NPCData(
            npc_id="kaya",
            name="Kaya",
            tile_x=22,
            tile_y=10,
            npc_type="quest_giver",
            quest_id="stop_kuro"
        ))

        island.add_npc(NPCData(
            npc_id="merry",
            name="Merry",
            tile_x=20,
            tile_y=10,
            dialogue_id="merry_going"
        ))

        # Black Cat Pirates encounter
        cat_pirate_tiles = [(x, y) for x in range(10, 35) for y in range(15, 30)]
        island.add_encounter_zone(EncounterZone(
            zone_id="black_cat_pirates",
            tiles=cat_pirate_tiles,
            enemy_groups=["pirate"],
            min_level=7,
            max_level=9,
            encounter_rate=0.05
        ))

        # Connections
        island.add_connection(IslandConnection(
            destination_island="orange_town",
            berries_cost=300
        ))
        island.add_connection(IslandConnection(
            destination_island="baratie",
            berries_cost=500
        ))

        return island

    @staticmethod
    def create_baratie() -> Island:
        """
        Create Baratie - the floating restaurant.
        Where Alex meets Marcus.
        """
        map_instance = Map(30, 30, TileType.WOOD)  # Wooden ship floors
        map_instance.name = "Baratie"
        map_instance.spawn_point = (15, 25)

        island = Island("baratie", "Baratie", map_instance)
        island.description = "A famous floating restaurant on the sea. Home to the finest chefs."
        island.recommended_level = 10
        island.story_arc = "Baratie"
        island.dock_position = (15, 28)

        IslandFactory._build_baratie_map(map_instance)

        # NPCs
        island.add_npc(NPCData(
            npc_id="sanji",
            name="Marcus",
            tile_x=15,
            tile_y=15,
            npc_type="crew_member",
            dialogue_id="sanji_recruitment",
            quest_id="recruit_sanji"
        ))

        island.add_npc(NPCData(
            npc_id="zeff",
            name="Red-Leg Zeff",
            tile_x=15,
            tile_y=10,
            npc_type="quest_giver",
            quest_id="protect_baratie"
        ))

        island.add_npc(NPCData(
            npc_id="chef",
            name="Chef",
            tile_x=12,
            tile_y=15,
            npc_type="shopkeeper",
            shop_id="baratie_food"
        ))

        # Don Krieg pirates encounter
        pirate_tiles = [(x, y) for x in range(5, 25) for y in range(18, 28)]
        island.add_encounter_zone(EncounterZone(
            zone_id="krieg_pirates",
            tiles=pirate_tiles,
            enemy_groups=["pirate"],
            min_level=10,
            max_level=12,
            encounter_rate=0.07
        ))

        # Connections
        island.add_connection(IslandConnection(
            destination_island="syrup_village",
            berries_cost=500
        ))
        island.add_connection(IslandConnection(
            destination_island="arlong_park",
            berries_cost=1000
        ))

        return island

    @staticmethod
    def create_arlong_park() -> Island:
        """
        Create Arlong Park - Fish-man pirate base.
        Marina's arc climax.
        """
        map_instance = Map(50, 50, TileType.STONE)
        map_instance.name = "Arlong Park"
        map_instance.spawn_point = (25, 45)

        island = Island("arlong_park", "Arlong Park", map_instance)
        island.description = "A stronghold controlled by the Fish-man pirate Arlong."
        island.recommended_level = 15
        island.story_arc = "Arlong Park"
        island.dock_position = (25, 48)

        IslandFactory._build_arlong_park_map(map_instance)

        # NPCs
        island.add_npc(NPCData(
            npc_id="nojiko",
            name="Nojiko",
            tile_x=10,
            tile_y=40,
            npc_type="quest_giver",
            quest_id="free_cocoyashi"
        ))

        island.add_npc(NPCData(
            npc_id="genzo",
            name="Genzo",
            tile_x=12,
            tile_y=40,
            dialogue_id="genzo_talk"
        ))

        # Fish-man encounter zones
        fishman_tiles = [(x, y) for x in range(15, 40) for y in range(10, 35)]
        island.add_encounter_zone(EncounterZone(
            zone_id="fishman_pirates",
            tiles=fishman_tiles,
            enemy_groups=["sea_beast", "pirate"],
            min_level=15,
            max_level=18,
            encounter_rate=0.08
        ))

        # Connections
        island.add_connection(IslandConnection(
            destination_island="baratie",
            berries_cost=1000
        ))
        island.add_connection(IslandConnection(
            destination_island="loguetown",
            berries_cost=2000,
            unlock_condition="defeated_arlong"
        ))

        return island

    @staticmethod
    def create_loguetown() -> Island:
        """
        Create Loguetown - the town of the beginning and the end.
        Where Gold Roger was executed. Last stop before Grand Line.
        """
        map_instance = Map(60, 60, TileType.STONE)
        map_instance.name = "Loguetown"
        map_instance.spawn_point = (30, 55)

        island = Island("loguetown", "Loguetown", map_instance)
        island.description = "The town where the Pirate King was born and executed. Gateway to the Grand Line."
        island.recommended_level = 20
        island.story_arc = "Loguetown"
        island.dock_position = (30, 58)

        IslandFactory._build_loguetown_map(map_instance)

        # NPCs
        island.add_npc(NPCData(
            npc_id="weapon_shop_owner",
            name="Ippon-Matsu",
            tile_x=25,
            tile_y=35,
            npc_type="shopkeeper",
            shop_id="loguetown_weapons"
        ))

        island.add_npc(NPCData(
            npc_id="armor_shop_owner",
            name="Armor Dealer",
            tile_x=35,
            tile_y=35,
            npc_type="shopkeeper",
            shop_id="loguetown_armor"
        ))

        island.add_npc(NPCData(
            npc_id="bartolomeo",
            name="Bartolomeo",
            tile_x=30,
            tile_y=40,
            dialogue_id="barto_fanboy"
        ))

        # Marine encounter (Smoker's forces)
        marine_tiles = [(x, y) for x in range(20, 45) for y in range(20, 45)]
        island.add_encounter_zone(EncounterZone(
            zone_id="loguetown_marines",
            tiles=marine_tiles,
            enemy_groups=["marine_soldier"],
            min_level=20,
            max_level=25,
            encounter_rate=0.10
        ))

        # Interactive - Execution Platform
        island.add_interactive_object(InteractiveObject(
            object_id="execution_platform",
            object_type="sign",
            tile_x=30,
            tile_y=25,
            interaction_type="examine",
            message="The execution platform where Gold Roger, the Pirate King, met his end.\n'You want my treasure? You can have it! I left everything in one place!'",
            one_time=False
        ))

        # Connections
        island.add_connection(IslandConnection(
            destination_island="arlong_park",
            berries_cost=2000
        ))
        island.add_connection(IslandConnection(
            destination_island="reverse_mountain",
            berries_cost=5000,
            unlock_condition="ready_for_grand_line"
        ))

        return island

    @staticmethod
    def create_reverse_mountain() -> Island:
        """
        Create Reverse Mountain - entrance to the Grand Line.
        Dangerous mountain where seas flow upward.
        """
        map_instance = Map(40, 60, TileType.ROCK)
        map_instance.name = "Reverse Mountain"
        map_instance.spawn_point = (20, 55)

        island = Island("reverse_mountain", "Reverse Mountain", map_instance)
        island.description = "The mysterious mountain where four seas meet. Entrance to the Grand Line."
        island.recommended_level = 25
        island.story_arc = "Entering Grand Line"
        island.dock_position = (20, 58)

        IslandFactory._build_reverse_mountain_map(map_instance)

        # NPCs
        island.add_npc(NPCData(
            npc_id="crocus",
            name="Crocus",
            tile_x=20,
            tile_y=30,
            npc_type="quest_giver",
            quest_id="navigate_reverse_mountain"
        ))

        # Laboon interaction
        island.add_interactive_object(InteractiveObject(
            object_id="laboon",
            object_type="examine",
            tile_x=20,
            tile_y=10,
            interaction_type="examine",
            message="A massive whale... crying at the mountain wall.\nCrocus: 'That's Laboon. He's been waiting for his crew for 50 years...'",
            one_time=False
        ))

        # Sea King encounters (dangerous waters)
        sea_tiles = [(x, y) for x in range(0, 40) for y in range(0, 20)]
        island.add_encounter_zone(EncounterZone(
            zone_id="sea_kings",
            tiles=sea_tiles,
            enemy_groups=["sea_beast"],
            min_level=25,
            max_level=30,
            encounter_rate=0.12
        ))

        # Connection back to Loguetown
        island.add_connection(IslandConnection(
            destination_island="loguetown",
            berries_cost=5000
        ))

        # Future: Connection to Grand Line islands would go here
        # island.add_connection(IslandConnection(
        #     destination_island="whiskey_peak",
        #     unlock_condition="completed_reverse_mountain"
        # ))

        return island

    # Helper methods to build map layouts

    @staticmethod
    def _build_foosha_village_map(map_instance: Map):
        """Build Foosha Village map layout."""
        # Create a simple village with houses, paths, and forest

        # Central plaza (stone path)
        for x in range(12, 19):
            for y in range(10, 16):
                map_instance.set_tile(x, y, TileType.STONE)

        # Water on the south (ocean)
        for x in range(0, 30):
            for y in range(28, 30):
                map_instance.set_tile(x, y, TileType.WATER)

        # Forest on the north
        for x in range(0, 30):
            for y in range(0, 8):
                map_instance.set_tile(x, y, TileType.TREE)

        # Houses (use walls for building outlines)
        # Mayor's house
        for x in range(13, 18):
            for y in range(8, 11):
                if x == 13 or x == 17 or y == 8 or y == 10:
                    map_instance.set_tile(x, y, TileType.WALL)

        # Mira's bar
        for x in range(10, 15):
            for y in range(11, 14):
                if x == 10 or x == 14 or y == 11 or y == 13:
                    map_instance.set_tile(x, y, TileType.WALL)

        # Dock area
        for x in range(14, 17):
            for y in range(26, 28):
                map_instance.set_tile(x, y, TileType.WOOD)

    @staticmethod
    def _build_shell_town_map(map_instance: Map):
        """Build Shell Town map layout."""
        # Marine base on the north
        for x in range(12, 23):
            for y in range(10, 18):
                if x == 12 or x == 22 or y == 10 or y == 17:
                    map_instance.set_tile(x, y, TileType.WALL)
                else:
                    map_instance.set_tile(x, y, TileType.STONE)

        # Town streets
        for x in range(0, 35):
            if x % 5 == 0:
                for y in range(20, 30):
                    map_instance.set_tile(x, y, TileType.STONE)

        # Ocean
        for x in range(0, 35):
            for y in range(32, 35):
                map_instance.set_tile(x, y, TileType.WATER)

        # Dock
        for x in range(16, 19):
            for y in range(30, 32):
                map_instance.set_tile(x, y, TileType.WOOD)

    @staticmethod
    def _build_orange_town_map(map_instance: Map):
        """Build Orange Town map layout."""
        # Damaged buildings (mix of normal and walls)
        for i in range(5):
            x_start = 10 + i * 6
            for x in range(x_start, x_start + 4):
                for y in range(15 + i * 3, 18 + i * 3):
                    if random.random() < 0.6:  # Some destroyed
                        map_instance.set_tile(x, y, TileType.WALL)

        # Central square
        for x in range(18, 23):
            for y in range(18, 23):
                map_instance.set_tile(x, y, TileType.STONE)

        # Ocean
        for x in range(0, 40):
            for y in range(37, 40):
                map_instance.set_tile(x, y, TileType.WATER)

    @staticmethod
    def _build_syrup_village_map(map_instance: Map):
        """Build Syrup Village map layout."""
        # Kaya's mansion on hill (north)
        for x in range(18, 27):
            for y in range(8, 13):
                if x == 18 or x == 26 or y == 8 or y == 12:
                    map_instance.set_tile(x, y, TileType.WALL)
                else:
                    map_instance.set_tile(x, y, TileType.WOOD)

        # Village houses
        for i in range(3):
            x_base = 10 + i * 8
            for x in range(x_base, x_base + 5):
                for y in range(25, 28):
                    if x == x_base or x == x_base + 4 or y == 25 or y == 27:
                        map_instance.set_tile(x, y, TileType.WALL)

        # Ocean
        for x in range(0, 45):
            for y in range(42, 45):
                map_instance.set_tile(x, y, TileType.WATER)

    @staticmethod
    def _build_baratie_map(map_instance: Map):
        """Build Baratie (floating restaurant) map layout."""
        # Entire structure is wooden (ship)
        for x in range(5, 25):
            for y in range(10, 25):
                map_instance.set_tile(x, y, TileType.WOOD)

        # Kitchen area
        for x in range(13, 18):
            for y in range(13, 18):
                map_instance.set_tile(x, y, TileType.STONE)

        # Dining tables (walls as furniture)
        for i in range(3):
            x = 8 + i * 5
            map_instance.set_tile(x, 15, TileType.WALL)
            map_instance.set_tile(x, 20, TileType.WALL)

        # Surrounding water
        for x in range(0, 30):
            for y in range(0, 30):
                if x < 5 or x >= 25 or y < 10 or y >= 25:
                    map_instance.set_tile(x, y, TileType.WATER)

    @staticmethod
    def _build_arlong_park_map(map_instance: Map):
        """Build Arlong Park map layout."""
        # Main building
        for x in range(20, 35):
            for y in range(15, 30):
                if x == 20 or x == 34 or y == 15 or y == 29:
                    map_instance.set_tile(x, y, TileType.WALL)
                else:
                    map_instance.set_tile(x, y, TileType.STONE)

        # Pool area (water inside compound)
        for x in range(24, 31):
            for y in range(19, 26):
                map_instance.set_tile(x, y, TileType.WATER)

        # Village area (south)
        for x in range(8, 18):
            for y in range(38, 45):
                map_instance.set_tile(x, y, TileType.DIRT)

        # Ocean
        for x in range(0, 50):
            for y in range(47, 50):
                map_instance.set_tile(x, y, TileType.WATER)

    @staticmethod
    def _build_loguetown_map(map_instance: Map):
        """Build Loguetown map layout."""
        # Execution platform (center)
        for x in range(28, 33):
            for y in range(23, 27):
                if y == 23:
                    map_instance.set_tile(x, y, TileType.WOOD)  # Platform
                else:
                    map_instance.set_tile(x, y, TileType.STONE)

        # Town streets (grid pattern)
        for x in range(0, 60):
            if x % 10 == 0:
                for y in range(15, 50):
                    map_instance.set_tile(x, y, TileType.STONE)

        for y in range(15, 50):
            if y % 10 == 0:
                for x in range(0, 60):
                    map_instance.set_tile(x, y, TileType.STONE)

        # Weapon shop
        for x in range(23, 28):
            for y in range(33, 37):
                if x == 23 or x == 27 or y == 33 or y == 36:
                    map_instance.set_tile(x, y, TileType.WALL)

        # Armor shop
        for x in range(33, 38):
            for y in range(33, 37):
                if x == 33 or x == 37 or y == 33 or y == 36:
                    map_instance.set_tile(x, y, TileType.WALL)

        # Ocean
        for x in range(0, 60):
            for y in range(57, 60):
                map_instance.set_tile(x, y, TileType.WATER)

    @staticmethod
    def _build_reverse_mountain_map(map_instance: Map):
        """Build Reverse Mountain map layout."""
        # Mountain slope (rocks getting higher)
        for y in range(0, 60):
            # Create mountain shape
            height_factor = (60 - y) / 60.0
            width = int(20 * (1 - height_factor))

            center_x = 20
            for x in range(center_x - width, center_x + width):
                if 0 <= x < 40:
                    map_instance.set_tile(x, y, TileType.ROCK)

        # Water channels (the upward-flowing canals)
        for y in range(30, 60):
            map_instance.set_tile(18, y, TileType.WATER)
            map_instance.set_tile(22, y, TileType.WATER)

        # Summit area
        for x in range(18, 23):
            for y in range(8, 13):
                map_instance.set_tile(x, y, TileType.STONE)

    @staticmethod
    def create_all_islands() -> List[Island]:
        """
        Create all 8 East Blue islands.

        Returns:
            List of all islands
        """
        return [
            IslandFactory.create_foosha_village(),
            IslandFactory.create_shell_town(),
            IslandFactory.create_orange_town(),
            IslandFactory.create_syrup_village(),
            IslandFactory.create_baratie(),
            IslandFactory.create_arlong_park(),
            IslandFactory.create_loguetown(),
            IslandFactory.create_reverse_mountain()
        ]
