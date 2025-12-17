"""
Devil Fruit Manager
Manages loading and accessing Devil Fruit data.
"""

from typing import Dict, List, Optional
from systems.data_loader import data_loader


class DevilFruitManager:
    """
    Manages Devil Fruit data from the database.
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
        """Initialize the Devil Fruit manager."""
        if self._initialized:
            return
        
        # Storage for loaded fruits
        self.fruits_by_id: Dict[str, Dict] = {}
        self.fruits_by_type: Dict[str, List[Dict]] = {
            "paramecia": [],
            "zoan": [],
            "logia": []
        }
        self.fruits_by_subtype: Dict[str, List[Dict]] = {
            "regular": [],
            "ancient": [],
            "mythical": []
        }
        
        # Index data
        self.master_index: Optional[Dict] = None
        self.type_indices: Dict[str, Dict] = {}
        
        # Load status
        self.loaded = False
        
        self._initialized = True
        print("DevilFruitManager initialized")
    
    def load_all_fruits(self) -> bool:
        """
        Load all Devil Fruit data from the database.
        
        Returns:
            True if successful
        """
        print("Loading Devil Fruits...")
        
        # Load master index
        self.master_index = data_loader.load_index("DevilFruits")
        if not self.master_index:
            print("Error: Could not load Devil Fruits master index")
            return False
        
        # Load Paramecia fruits
        self._load_paramecia()
        
        # Load Logia fruits
        self._load_logia()
        
        # Load Zoan fruits (with subtypes)
        self._load_zoan()
        
        self.loaded = True
        
        # Print summary
        total = len(self.fruits_by_id)
        print(f"Loaded {total} Devil Fruits:")
        print(f"  - Paramecia: {len(self.fruits_by_type['paramecia'])}")
        print(f"  - Logia: {len(self.fruits_by_type['logia'])}")
        print(f"  - Zoan: {len(self.fruits_by_type['zoan'])}")
        print(f"    - Regular: {len(self.fruits_by_subtype['regular'])}")
        print(f"    - Ancient: {len(self.fruits_by_subtype['ancient'])}")
        print(f"    - Mythical: {len(self.fruits_by_subtype['mythical'])}")
        
        return True
    
    def _load_paramecia(self):
        """Load Paramecia Devil Fruits."""
        # Load index
        index = data_loader.load_json("DevilFruits/Paramecia/index.json")
        if not index:
            print("Error: Could not load Paramecia index")
            return

        self.type_indices["paramecia"] = index

        # Get fruits from index
        fruits = index.get("fruits", [])

        for fruit in fruits:
            fruit_id = fruit.get("id")
            if fruit_id:
                # Add type tag
                fruit["type"] = "paramecia"
                self.fruits_by_id[fruit_id] = fruit
                self.fruits_by_type["paramecia"].append(fruit)
    
    def _load_logia(self):
        """Load Logia Devil Fruits."""
        # Load index
        index = data_loader.load_json("DevilFruits/Logia/index.json")
        if not index:
            print("Error: Could not load Logia index")
            return

        self.type_indices["logia"] = index

        # Get fruits from index
        fruits = index.get("fruits", [])

        for fruit in fruits:
            fruit_id = fruit.get("id")
            if fruit_id:
                # Add type tag
                fruit["type"] = "logia"
                self.fruits_by_id[fruit_id] = fruit
                self.fruits_by_type["logia"].append(fruit)
    
    def _load_zoan(self):
        """Load Zoan Devil Fruits (all subtypes)."""
        # Load main Zoan index
        index = data_loader.load_json("DevilFruits/Zoan/index.json")
        if not index:
            print("Error: Could not load Zoan index")
            return

        self.type_indices["zoan"] = index

        # Get all fruits from single index file
        fruits = index.get("fruits", [])

        for fruit in fruits:
            fruit_id = fruit.get("id")
            if not fruit_id:
                continue

            # Add type tag
            fruit["type"] = "zoan"

            # Get subtype (Regular, Ancient, or Mythical)
            subtype = fruit.get("subtype", "Regular").lower()

            # Add to main collections
            self.fruits_by_id[fruit_id] = fruit
            self.fruits_by_type["zoan"].append(fruit)

            # Add to subtype collection
            if subtype in self.fruits_by_subtype:
                self.fruits_by_subtype[subtype].append(fruit)
            else:
                # Default to regular if subtype not recognized
                self.fruits_by_subtype["regular"].append(fruit)
    
    def get_fruit_by_id(self, fruit_id: str) -> Optional[Dict]:
        """
        Get a Devil Fruit by its ID.
        
        Args:
            fruit_id: Fruit ID (e.g., "gomu_gomu")
        
        Returns:
            Fruit data dictionary or None
        """
        return self.fruits_by_id.get(fruit_id)
    
    def get_fruits_by_type(self, fruit_type: str) -> List[Dict]:
        """
        Get all fruits of a specific type.
        
        Args:
            fruit_type: "paramecia", "zoan", or "logia"
        
        Returns:
            List of fruit data dictionaries
        """
        return self.fruits_by_type.get(fruit_type.lower(), [])
    
    def get_fruits_by_subtype(self, subtype: str) -> List[Dict]:
        """
        Get all Zoan fruits of a specific subtype.
        
        Args:
            subtype: "regular", "ancient", or "mythical"
        
        Returns:
            List of fruit data dictionaries
        """
        return self.fruits_by_subtype.get(subtype.lower(), [])
    
    def get_starting_fruits(self) -> List[Dict]:
        """
        Get all fruits marked as available at character creation.
        
        Returns:
            List of starting-available fruits
        """
        starting = []
        for fruit in self.fruits_by_id.values():
            if fruit.get("starting_available", False):
                starting.append(fruit)
        return starting
    
    def get_fruit_names(self, fruit_type: Optional[str] = None) -> List[str]:
        """
        Get list of fruit names.
        
        Args:
            fruit_type: Optional type filter
        
        Returns:
            List of fruit names
        """
        if fruit_type:
            fruits = self.get_fruits_by_type(fruit_type)
        else:
            fruits = list(self.fruits_by_id.values())
        
        return [fruit.get("name", "Unknown") for fruit in fruits]
    
    def get_all_fruits(self) -> List[Dict]:
        """
        Get all loaded Devil Fruits.
        
        Returns:
            List of all fruit data dictionaries
        """
        return list(self.fruits_by_id.values())
    
    def search_fruits(self, query: str) -> List[Dict]:
        """
        Search for fruits by name or description.
        
        Args:
            query: Search query (case-insensitive)
        
        Returns:
            List of matching fruits
        """
        query = query.lower()
        results = []
        
        for fruit in self.fruits_by_id.values():
            name = fruit.get("name", "").lower()
            translation = fruit.get("translation", "").lower()
            description = fruit.get("description", "").lower()
            
            if (query in name or 
                query in translation or 
                query in description):
                results.append(fruit)
        
        return results
    
    def get_fruit_abilities(self, fruit_id: str) -> List[Dict]:
        """
        Get all abilities for a specific fruit.
        
        Args:
            fruit_id: Fruit ID
        
        Returns:
            List of ability dictionaries
        """
        fruit = self.get_fruit_by_id(fruit_id)
        if fruit:
            return fruit.get("abilities", [])
        return []
    
    def get_fruit_stats(self) -> Dict[str, int]:
        """
        Get statistics about loaded fruits.
        
        Returns:
            Dictionary with fruit counts by type
        """
        return {
            "total": len(self.fruits_by_id),
            "paramecia": len(self.fruits_by_type["paramecia"]),
            "logia": len(self.fruits_by_type["logia"]),
            "zoan_total": len(self.fruits_by_type["zoan"]),
            "zoan_regular": len(self.fruits_by_subtype["regular"]),
            "zoan_ancient": len(self.fruits_by_subtype["ancient"]),
            "zoan_mythical": len(self.fruits_by_subtype["mythical"]),
            "starting_available": len(self.get_starting_fruits())
        }
    
    def validate_fruit_data(self, fruit: Dict) -> bool:
        """
        Validate that a fruit has required fields.
        
        Args:
            fruit: Fruit data dictionary
        
        Returns:
            True if valid
        """
        required_fields = ["id", "name", "description", "abilities"]
        
        for field in required_fields:
            if field not in fruit:
                print(f"Invalid fruit data: missing '{field}'")
                return False
        
        # Check abilities structure
        abilities = fruit.get("abilities", [])
        if not isinstance(abilities, list):
            print("Invalid fruit data: abilities must be a list")
            return False
        
        return True
    
    def reload_fruits(self) -> bool:
        """
        Reload all Devil Fruit data from disk.
        
        Returns:
            True if successful
        """
        # Clear current data
        self.fruits_by_id.clear()
        for type_list in self.fruits_by_type.values():
            type_list.clear()
        for subtype_list in self.fruits_by_subtype.values():
            subtype_list.clear()
        
        # Clear data loader cache for fruits
        data_loader.clear_cache()
        
        # Reload
        return self.load_all_fruits()


# Global instance
devil_fruit_manager = DevilFruitManager()
