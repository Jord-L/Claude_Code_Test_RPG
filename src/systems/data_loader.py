"""
Data Loader
Core system for loading and parsing JSON data files.
"""

import json
import os
from typing import Dict, List, Any, Optional


class DataLoader:
    """
    Handles loading and caching of JSON data files.
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
        """Initialize the data loader."""
        if self._initialized:
            return
        
        # Cache for loaded data
        self.cache: Dict[str, Any] = {}
        
        # Base paths
        self.project_root = self._find_project_root()
        self.database_path = os.path.join(self.project_root, "Databases")
        
        # Verify database exists
        if not os.path.exists(self.database_path):
            print(f"Warning: Database directory not found at {self.database_path}")
        
        self._initialized = True
        print(f"DataLoader initialized - Database: {self.database_path}")
    
    def _find_project_root(self) -> str:
        """Find the project root directory."""
        # Start from current file location
        current = os.path.dirname(os.path.abspath(__file__))
        
        # Go up directories until we find Databases folder
        while current != os.path.dirname(current):  # Not at root
            if os.path.exists(os.path.join(current, "Databases")):
                return current
            current = os.path.dirname(current)
        
        # If not found, use current directory
        return os.getcwd()
    
    def load_json(self, filepath: str, use_cache: bool = True) -> Optional[Dict]:
        """
        Load a JSON file.
        
        Args:
            filepath: Path to JSON file (relative to Database folder)
            use_cache: Whether to use cached data if available
        
        Returns:
            Parsed JSON data as dictionary, or None if failed
        """
        # Check cache first
        if use_cache and filepath in self.cache:
            return self.cache[filepath]
        
        # Build full path
        full_path = os.path.join(self.database_path, filepath)
        
        # Check if file exists
        if not os.path.exists(full_path):
            print(f"Error: File not found: {full_path}")
            return None
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Cache the data
            self.cache[filepath] = data
            
            return data
        
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {filepath}: {e}")
            return None
        
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None
    
    def load_index(self, category: str) -> Optional[Dict]:
        """
        Load an index.json file for a category.
        
        Args:
            category: Category name (e.g., "DevilFruits", "Weapons")
        
        Returns:
            Index data as dictionary
        """
        index_path = os.path.join(category, "index.json")
        return self.load_json(index_path)
    
    def load_all_in_category(self, category: str, 
                            subcategory: Optional[str] = None) -> List[Dict]:
        """
        Load all data files in a category.
        
        Args:
            category: Main category (e.g., "DevilFruits")
            subcategory: Optional subcategory (e.g., "Paramecia")
        
        Returns:
            List of all loaded data dictionaries
        """
        results = []
        
        # Build directory path
        if subcategory:
            dir_path = os.path.join(self.database_path, category, subcategory)
        else:
            dir_path = os.path.join(self.database_path, category)
        
        # Check if directory exists
        if not os.path.exists(dir_path):
            print(f"Warning: Directory not found: {dir_path}")
            return results
        
        # Load all JSON files (except index.json)
        for filename in os.listdir(dir_path):
            if filename.endswith('.json') and filename != 'index.json':
                if subcategory:
                    filepath = os.path.join(category, subcategory, filename)
                else:
                    filepath = os.path.join(category, filename)
                
                data = self.load_json(filepath)
                if data:
                    results.append(data)
        
        return results
    
    def save_json(self, filepath: str, data: Dict) -> bool:
        """
        Save data to a JSON file.
        
        Args:
            filepath: Path to save to (relative to Database folder)
            data: Data to save
        
        Returns:
            True if successful
        """
        full_path = os.path.join(self.database_path, filepath)
        
        try:
            # Ensure directory exists
            directory = os.path.dirname(full_path)
            os.makedirs(directory, exist_ok=True)
            
            # Write JSON with pretty formatting
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Update cache
            self.cache[filepath] = data
            
            return True
        
        except Exception as e:
            print(f"Error saving {filepath}: {e}")
            return False
    
    def clear_cache(self, filepath: Optional[str] = None):
        """
        Clear cached data.
        
        Args:
            filepath: Specific file to clear, or None to clear all
        """
        if filepath:
            if filepath in self.cache:
                del self.cache[filepath]
                print(f"Cleared cache for {filepath}")
        else:
            self.cache.clear()
            print("Cleared all cached data")
    
    def reload(self, filepath: str) -> Optional[Dict]:
        """
        Force reload a file, bypassing cache.
        
        Args:
            filepath: Path to reload
        
        Returns:
            Reloaded data
        """
        self.clear_cache(filepath)
        return self.load_json(filepath, use_cache=False)
    
    def get_database_path(self, relative_path: str = "") -> str:
        """
        Get full path to a database file/folder.
        
        Args:
            relative_path: Path relative to Database folder
        
        Returns:
            Full absolute path
        """
        return os.path.join(self.database_path, relative_path)
    
    def file_exists(self, filepath: str) -> bool:
        """
        Check if a database file exists.
        
        Args:
            filepath: Path relative to Database folder
        
        Returns:
            True if file exists
        """
        full_path = os.path.join(self.database_path, filepath)
        return os.path.exists(full_path)
    
    def list_files(self, directory: str, extension: str = ".json") -> List[str]:
        """
        List files in a database directory.
        
        Args:
            directory: Directory relative to Database folder
            extension: File extension filter
        
        Returns:
            List of filenames
        """
        full_path = os.path.join(self.database_path, directory)
        
        if not os.path.exists(full_path):
            return []
        
        files = []
        for filename in os.listdir(full_path):
            if filename.endswith(extension):
                files.append(filename)
        
        return sorted(files)
    
    def validate_json_structure(self, data: Dict, required_fields: List[str]) -> bool:
        """
        Validate that JSON data has required fields.
        
        Args:
            data: Data dictionary to validate
            required_fields: List of required field names
        
        Returns:
            True if all fields present
        """
        for field in required_fields:
            if field not in data:
                print(f"Validation error: Missing required field '{field}'")
                return False
        return True
    
    def get_cache_info(self) -> Dict[str, int]:
        """
        Get information about cached data.
        
        Returns:
            Dictionary with cache statistics
        """
        return {
            "cached_files": len(self.cache),
            "total_size_kb": sum(
                len(str(data)) for data in self.cache.values()
            ) // 1024
        }


# Global instance
data_loader = DataLoader()
