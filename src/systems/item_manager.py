"""
Item Manager
Manages loading and accessing weapon and item data.
"""

from typing import Dict, List, Optional
from systems.data_loader import data_loader


class ItemManager:
    """
    Manages weapon and item data from the database.
    Singleton pattern for global access.
    """
    
    _instance = None
    
    def __new__(cls):
        """Ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the Item manager."""
        if self._initialized:
            return
        
        # Storage for weapons
        self.weapons_by_id: Dict[str, Dict] = {}
        self.weapons_by_type: Dict[str, List[Dict]] = {
            "swords": [],
            "guns": [],
            "staffs": [],
            "polearms": [],
            "bows": [],
            "fists": []
        }
        
        # Storage for items
        self.items_by_id: Dict[str, Dict] = {}
        self.items_by_type: Dict[str, List[Dict]] = {
            "consumables": [],
            "materials": [],
            "key_items": []
        }
        
        # Indices
        self.weapon_index: Optional[Dict] = None
        self.item_index: Optional[Dict] = None
        
        # Load status
        self.loaded = False
        
        self._initialized = True
        print("ItemManager initialized")
    
    def load_all_data(self) -> bool:
        """
        Load all weapon and item data from the database.
        
        Returns:
            True if successful
        """
        print("Loading Items and Weapons...")
        
        # Load weapons
        weapons_loaded = self._load_weapons()
        
        # Load items
        items_loaded = self._load_items()
        
        self.loaded = weapons_loaded and items_loaded
        
        # Print summary
        print(f"Loaded {len(self.weapons_by_id)} Weapons:")
        for weapon_type, weapons in self.weapons_by_type.items():
            if weapons:
                print(f"  - {weapon_type.title()}: {len(weapons)}")
        
        print(f"Loaded {len(self.items_by_id)} Items:")
        for item_type, items in self.items_by_type.items():
            if items:
                print(f"  - {item_type.title()}: {len(items)}")
        
        return self.loaded
    
    def _load_weapons(self) -> bool:
        """Load all weapons."""
        # Load weapon index
        self.weapon_index = data_loader.load_index("Weapons")
        if not self.weapon_index:
            print("Warning: Could not load Weapons index")
            return False
        
        # Load each weapon type
        weapon_types = ["Swords", "Guns", "Staffs", "Polearms", "Bows", "Fists"]
        
        for weapon_type in weapon_types:
            weapons = data_loader.load_all_in_category("Weapons", weapon_type)
            
            for weapon in weapons:
                weapon_id = weapon.get("id")
                if weapon_id:
                    self.weapons_by_id[weapon_id] = weapon
                    self.weapons_by_type[weapon_type.lower()].append(weapon)
        
        return True
    
    def _load_items(self) -> bool:
        """Load all items."""
        # Load item index
        self.item_index = data_loader.load_index("Inventory")
        if not self.item_index:
            print("Warning: Could not load Inventory index")
            return False
        
        # Load each item type
        item_types = ["Consumables", "Materials", "KeyItems"]
        
        for item_type in item_types:
            items = data_loader.load_all_in_category("Inventory", item_type)
            
            for item in items:
                item_id = item.get("id")
                if item_id:
                    self.items_by_id[item_id] = item
                    # Convert "KeyItems" to "key_items" for dict key
                    type_key = item_type.lower()
                    if "key" in type_key:
                        type_key = "key_items"
                    self.items_by_type[type_key].append(item)
        
        return True
    
    # Weapon methods
    
    def get_weapon_by_id(self, weapon_id: str) -> Optional[Dict]:
        """
        Get a weapon by its ID.
        
        Args:
            weapon_id: Weapon ID
        
        Returns:
            Weapon data dictionary or None
        """
        return self.weapons_by_id.get(weapon_id)
    
    def get_weapons_by_type(self, weapon_type: str) -> List[Dict]:
        """
        Get all weapons of a specific type.
        
        Args:
            weapon_type: "swords", "guns", "staffs", "polearms", "bows", "fists"
        
        Returns:
            List of weapon data dictionaries
        """
        return self.weapons_by_type.get(weapon_type.lower(), [])
    
    def get_starting_weapons(self) -> List[Dict]:
        """
        Get weapons suitable for starting characters.
        
        Returns:
            List of low-level weapons
        """
        starting = []
        for weapon in self.weapons_by_id.values():
            requirements = weapon.get("requirements", {})
            level = requirements.get("level", 1)
            if level <= 1:  # Level 1 weapons
                starting.append(weapon)
        return starting
    
    def get_weapons_by_grade(self, grade: str) -> List[Dict]:
        """
        Get weapons by grade.
        
        Args:
            grade: "Common", "Skillful", "Great", "O Wazamono", "Supreme"
        
        Returns:
            List of weapons with that grade
        """
        result = []
        for weapon in self.weapons_by_id.values():
            if weapon.get("grade", "").lower() == grade.lower():
                result.append(weapon)
        return result
    
    def search_weapons(self, query: str) -> List[Dict]:
        """
        Search for weapons by name or description.
        
        Args:
            query: Search query (case-insensitive)
        
        Returns:
            List of matching weapons
        """
        query = query.lower()
        results = []
        
        for weapon in self.weapons_by_id.values():
            name = weapon.get("name", "").lower()
            description = weapon.get("description", "").lower()
            
            if query in name or query in description:
                results.append(weapon)
        
        return results
    
    # Item methods
    
    def get_item_by_id(self, item_id: str) -> Optional[Dict]:
        """
        Get an item by its ID.
        
        Args:
            item_id: Item ID
        
        Returns:
            Item data dictionary or None
        """
        return self.items_by_id.get(item_id)
    
    def get_items_by_type(self, item_type: str) -> List[Dict]:
        """
        Get all items of a specific type.
        
        Args:
            item_type: "consumables", "materials", "key_items"
        
        Returns:
            List of item data dictionaries
        """
        return self.items_by_type.get(item_type.lower(), [])
    
    def get_consumables(self) -> List[Dict]:
        """Get all consumable items."""
        return self.items_by_type["consumables"]
    
    def get_materials(self) -> List[Dict]:
        """Get all material items."""
        return self.items_by_type["materials"]
    
    def get_key_items(self) -> List[Dict]:
        """Get all key items."""
        return self.items_by_type["key_items"]
    
    def search_items(self, query: str) -> List[Dict]:
        """
        Search for items by name or description.
        
        Args:
            query: Search query (case-insensitive)
        
        Returns:
            List of matching items
        """
        query = query.lower()
        results = []
        
        for item in self.items_by_id.values():
            name = item.get("name", "").lower()
            description = item.get("description", "").lower()
            
            if query in name or query in description:
                results.append(item)
        
        return results
    
    # General methods
    
    def get_all_weapons(self) -> List[Dict]:
        """Get all loaded weapons."""
        return list(self.weapons_by_id.values())
    
    def get_all_items(self) -> List[Dict]:
        """Get all loaded items."""
        return list(self.items_by_id.values())
    
    def get_item_stats(self) -> Dict[str, int]:
        """
        Get statistics about loaded items and weapons.
        
        Returns:
            Dictionary with counts
        """
        return {
            "total_weapons": len(self.weapons_by_id),
            "swords": len(self.weapons_by_type["swords"]),
            "guns": len(self.weapons_by_type["guns"]),
            "staffs": len(self.weapons_by_type["staffs"]),
            "polearms": len(self.weapons_by_type["polearms"]),
            "bows": len(self.weapons_by_type["bows"]),
            "fists": len(self.weapons_by_type["fists"]),
            "total_items": len(self.items_by_id),
            "consumables": len(self.items_by_type["consumables"]),
            "materials": len(self.items_by_type["materials"]),
            "key_items": len(self.items_by_type["key_items"])
        }
    
    def validate_weapon_data(self, weapon: Dict) -> bool:
        """
        Validate weapon data structure.
        
        Args:
            weapon: Weapon data dictionary
        
        Returns:
            True if valid
        """
        required_fields = ["id", "name", "grade", "rarity", "requirements", "stats"]
        
        for field in required_fields:
            if field not in weapon:
                print(f"Invalid weapon data: missing '{field}'")
                return False
        
        return True
    
    def validate_item_data(self, item: Dict) -> bool:
        """
        Validate item data structure.
        
        Args:
            item: Item data dictionary
        
        Returns:
            True if valid
        """
        required_fields = ["id", "name", "description", "rarity"]
        
        for field in required_fields:
            if field not in item:
                print(f"Invalid item data: missing '{field}'")
                return False
        
        return True
    
    def reload_data(self) -> bool:
        """
        Reload all item and weapon data from disk.
        
        Returns:
            True if successful
        """
        # Clear current data
        self.weapons_by_id.clear()
        self.items_by_id.clear()
        for weapon_list in self.weapons_by_type.values():
            weapon_list.clear()
        for item_list in self.items_by_type.values():
            item_list.clear()
        
        # Clear cache
        data_loader.clear_cache()
        
        # Reload
        return self.load_all_data()


# Global instance
item_manager = ItemManager()
