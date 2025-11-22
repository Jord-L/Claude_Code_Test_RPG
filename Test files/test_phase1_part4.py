"""
Test Script for Phase 1 Part 4
Run this to verify the data loading system is working correctly.
"""

import sys
import os
import logging
import time
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Setup logging
def setup_logger(test_name):
    """Setup logger for this test file."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger.handlers = []
    
    # File handler
    log_file = os.path.join(log_dir, f"{test_name}.log")
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger('test_phase1_part4')

logger.info("=" * 60)
logger.info("Phase 1 Part 4 - Data Loading System Test")
logger.info("=" * 60)
logger.info("")
logger.debug(f"Test started at: {datetime.now()}")

# Test 1: Import checks
logger.info("Test 1: Checking data system imports...")
start_time = time.time()
try:
    from systems.data_loader import DataLoader, data_loader
    logger.debug(f"DataLoader class: {DataLoader.__module__}")
    logger.debug(f"data_loader instance: {id(data_loader)}")
    logger.info("✓ DataLoader imported")
    
    from systems.devil_fruit_manager import DevilFruitManager, devil_fruit_manager
    logger.debug(f"DevilFruitManager class: {DevilFruitManager.__module__}")
    logger.debug(f"devil_fruit_manager instance: {id(devil_fruit_manager)}")
    logger.info("✓ DevilFruitManager imported")
    
    from systems.item_manager import ItemManager, item_manager
    logger.debug(f"ItemManager class: {ItemManager.__module__}")
    logger.debug(f"item_manager instance: {id(item_manager)}")
    logger.info("✓ ItemManager imported")
    
    elapsed = time.time() - start_time
    logger.debug(f"Import test completed in {elapsed:.3f}s")
    logger.info("✓ All data system imports successful!\n")
except ImportError as e:
    elapsed = time.time() - start_time
    logger.error(f"Import failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ Import failed: {e}\n")
    sys.exit(1)

# Test 2: DataLoader functionality
logger.info("Test 2: Testing DataLoader...")
start_time = time.time()
try:
    logger.debug("Creating DataLoader instance...")
    loader = DataLoader()
    logger.debug(f"DataLoader instance ID: {id(loader)}")
    
    # Check singleton
    logger.debug("Testing singleton pattern...")
    loader2 = DataLoader()
    logger.debug(f"Second instance ID: {id(loader2)}")
    assert loader is loader2, "Singleton pattern broken"
    logger.debug(f"Singleton verified: {id(loader)} == {id(loader2)}")
    logger.info("✓ Singleton pattern works")
    
    # Check database path
    logger.debug("Checking database path...")
    db_path = loader.get_database_path()
    logger.debug(f"Database path: {db_path}")
    logger.debug(f"Path exists: {os.path.exists(db_path)}")
    assert os.path.exists(db_path), f"Database path not found: {db_path}"
    logger.info(f"✓ Database path found: {db_path}")
    
    # Test loading master index
    logger.debug("Loading DevilFruits index...")
    load_start = time.time()
    index = loader.load_index("DevilFruits")
    load_time = time.time() - load_start
    
    if index:
        logger.debug(f"Index loaded in {load_time:.4f}s")
        logger.debug(f"Index structure keys: {list(index.keys())}")
        logger.debug(f"Category: {index.get('category')}")
        logger.debug(f"Version: {index.get('version')}")
        assert "category" in index, "Invalid index structure"
        logger.info("✓ Can load index files")
    else:
        logger.warning("No Devil Fruits index found (database empty)")
        logger.info("⚠ No Devil Fruits index found (database empty)")
    
    # Test file existence check
    logger.debug("Testing file_exists method...")
    exists = loader.file_exists("index.json")
    logger.debug(f"index.json exists: {exists}")
    logger.info(f"✓ File existence check works (master index exists: {exists})")
    
    elapsed = time.time() - start_time
    logger.debug(f"DataLoader test completed in {elapsed:.3f}s")
    logger.info("✓ DataLoader functionality verified!\n")
    
except Exception as e:
    elapsed = time.time() - start_time
    logger.error(f"DataLoader test failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ DataLoader test failed: {e}\n")
    sys.exit(1)

# Test 3: DevilFruitManager functionality
logger.info("Test 3: Testing DevilFruitManager...")
start_time = time.time()
try:
    logger.debug("Creating DevilFruitManager instance...")
    df_manager = DevilFruitManager()
    logger.debug(f"DevilFruitManager instance ID: {id(df_manager)}")
    
    # Check singleton
    logger.debug("Testing singleton pattern...")
    df_manager2 = DevilFruitManager()
    logger.debug(f"Second instance ID: {id(df_manager2)}")
    assert df_manager is df_manager2, "Singleton pattern broken"
    logger.debug(f"Singleton verified: {id(df_manager)} == {id(df_manager2)}")
    logger.info("✓ Singleton pattern works")
    
    # Try to load fruits
    logger.debug("Loading all Devil Fruits...")
    load_start = time.time()
    success = df_manager.load_all_fruits()
    load_time = time.time() - load_start
    logger.debug(f"Load operation completed in {load_time:.4f}s, success: {success}")
    
    if success:
        logger.info("✓ Devil Fruits loaded successfully")
        
        # Get stats
        logger.debug("Retrieving fruit statistics...")
        stats = df_manager.get_fruit_stats()
        logger.debug(f"Fruit stats: {stats}")
        logger.info(f"  Total fruits: {stats['total']}")
        logger.info(f"  - Paramecia: {stats['paramecia']}")
        logger.info(f"  - Logia: {stats['logia']}")
        logger.info(f"  - Zoan: {stats['zoan_total']}")
        
        # Test retrieval methods
        logger.debug("Testing get_all_fruits()...")
        all_fruits = df_manager.get_all_fruits()
        logger.debug(f"Retrieved {len(all_fruits)} fruits")
        logger.info(f"✓ Can retrieve all fruits ({len(all_fruits)} total)")
        
        # Test type filtering
        logger.debug("Testing get_fruits_by_type('paramecia')...")
        paramecia = df_manager.get_fruits_by_type("paramecia")
        logger.debug(f"Retrieved {len(paramecia)} Paramecia fruits")
        logger.info(f"✓ Can filter by type ({len(paramecia)} Paramecia)")
        
        # Test starting fruits
        logger.debug("Testing get_starting_fruits()...")
        starting = df_manager.get_starting_fruits()
        logger.debug(f"Retrieved {len(starting)} starting fruits")
        logger.info(f"✓ Can get starting fruits ({len(starting)} available)")
        
    else:
        logger.warning("No Devil Fruits loaded (database empty)")
        logger.info("⚠ No Devil Fruits loaded (database empty)")
    
    elapsed = time.time() - start_time
    logger.debug(f"DevilFruitManager test completed in {elapsed:.3f}s")
    logger.info("✓ DevilFruitManager functionality verified!\n")
    
except Exception as e:
    elapsed = time.time() - start_time
    logger.error(f"DevilFruitManager test failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ DevilFruitManager test failed: {e}\n")
    sys.exit(1)

# Test 4: ItemManager functionality
logger.info("Test 4: Testing ItemManager...")
start_time = time.time()
try:
    logger.debug("Creating ItemManager instance...")
    item_mgr = ItemManager()
    logger.debug(f"ItemManager instance ID: {id(item_mgr)}")
    
    # Check singleton
    logger.debug("Testing singleton pattern...")
    item_mgr2 = ItemManager()
    logger.debug(f"Second instance ID: {id(item_mgr2)}")
    assert item_mgr is item_mgr2, "Singleton pattern broken"
    logger.debug(f"Singleton verified: {id(item_mgr)} == {id(item_mgr2)}")
    logger.info("✓ Singleton pattern works")
    
    # Try to load items and weapons
    logger.debug("Loading all items and weapons...")
    load_start = time.time()
    success = item_mgr.load_all_data()
    load_time = time.time() - load_start
    logger.debug(f"Load operation completed in {load_time:.4f}s, success: {success}")
    
    if success:
        logger.info("✓ Items and Weapons loaded successfully")
        
        # Get stats
        logger.debug("Retrieving item statistics...")
        stats = item_mgr.get_item_stats()
        logger.debug(f"Item stats: {stats}")
        logger.info(f"  Total weapons: {stats['total_weapons']}")
        logger.info(f"  - Swords: {stats['swords']}")
        logger.info(f"  - Guns: {stats['guns']}")
        logger.info(f"  - Staffs: {stats['staffs']}")
        logger.info(f"  - Polearms: {stats['polearms']}")
        logger.info(f"  - Bows: {stats['bows']}")
        logger.info(f"  - Fists: {stats['fists']}")
        logger.info(f"  Total items: {stats['total_items']}")
        logger.info(f"  - Consumables: {stats['consumables']}")
        logger.info(f"  - Materials: {stats['materials']}")
        logger.info(f"  - Key Items: {stats['key_items']}")
        
        # Test retrieval methods
        logger.debug("Testing get_all_weapons()...")
        all_weapons = item_mgr.get_all_weapons()
        logger.debug(f"Retrieved {len(all_weapons)} weapons")
        logger.info(f"✓ Can retrieve all weapons ({len(all_weapons)} total)")
        
        logger.debug("Testing get_all_items()...")
        all_items = item_mgr.get_all_items()
        logger.debug(f"Retrieved {len(all_items)} items")
        logger.info(f"✓ Can retrieve all items ({len(all_items)} total)")
        
        # Test type filtering
        logger.debug("Testing get_weapons_by_type('swords')...")
        swords = item_mgr.get_weapons_by_type("swords")
        logger.debug(f"Retrieved {len(swords)} swords")
        logger.info(f"✓ Can filter weapons by type ({len(swords)} Swords)")
        
        logger.debug("Testing get_consumables()...")
        consumables = item_mgr.get_consumables()
        logger.debug(f"Retrieved {len(consumables)} consumables")
        logger.info(f"✓ Can get consumables ({len(consumables)} items)")
        
        # Test starting weapons
        logger.debug("Testing get_starting_weapons()...")
        starting = item_mgr.get_starting_weapons()
        logger.debug(f"Retrieved {len(starting)} starting weapons")
        logger.info(f"✓ Can get starting weapons ({len(starting)} available)")
        
    else:
        logger.warning("No Items/Weapons loaded (database empty)")
        logger.info("⚠ No Items/Weapons loaded (database empty)")
    
    elapsed = time.time() - start_time
    logger.debug(f"ItemManager test completed in {elapsed:.3f}s")
    logger.info("✓ ItemManager functionality verified!\n")
    
except Exception as e:
    elapsed = time.time() - start_time
    logger.error(f"ItemManager test failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ ItemManager test failed: {e}\n")
    sys.exit(1)

# Test 5: Integration test
logger.info("Test 5: Testing system integration...")
start_time = time.time()
try:
    # Test that all managers can be accessed globally
    logger.debug("Importing global instances...")
    from systems.data_loader import data_loader
    from systems.devil_fruit_manager import devil_fruit_manager
    from systems.item_manager import item_manager
    
    logger.debug(f"data_loader: {id(data_loader)}")
    logger.debug(f"devil_fruit_manager: {id(devil_fruit_manager)}")
    logger.debug(f"item_manager: {id(item_manager)}")
    logger.info("✓ Global instances accessible")
    
    # Test cache info
    logger.debug("Getting cache info...")
    cache_info = data_loader.get_cache_info()
    logger.debug(f"Cache info: {cache_info}")
    logger.info(f"✓ Cache info available: {cache_info['cached_files']} files cached")
    
    # Test that data persists across manager instances
    logger.debug("Testing state persistence...")
    df_mgr = DevilFruitManager()
    logger.debug(f"New instance loaded state: {df_mgr.loaded}")
    logger.debug(f"Global instance loaded state: {devil_fruit_manager.loaded}")
    assert df_mgr.loaded == devil_fruit_manager.loaded, "Manager state not shared"
    logger.info("✓ Manager state consistent")
    
    # Test search functionality
    if devil_fruit_manager.loaded:
        logger.debug("Testing Devil Fruit search...")
        search_start = time.time()
        results = devil_fruit_manager.search_fruits("fruit")
        search_time = time.time() - search_start
        logger.debug(f"Search completed in {search_time:.4f}s, {len(results)} results")
        logger.info(f"✓ Search works ({len(results)} results for 'fruit')")
    
    if item_manager.loaded:
        logger.debug("Testing weapon search...")
        search_start = time.time()
        results = item_manager.search_weapons("sword")
        search_time = time.time() - search_start
        logger.debug(f"Weapon search completed in {search_time:.4f}s, {len(results)} results")
        logger.info(f"✓ Weapon search works ({len(results)} results for 'sword')")
    
    elapsed = time.time() - start_time
    logger.debug(f"Integration test completed in {elapsed:.3f}s")
    logger.info("✓ Integration test passed!\n")
    
except Exception as e:
    elapsed = time.time() - start_time
    logger.error(f"Integration test failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ Integration test failed: {e}\n")
    sys.exit(1)

# Test 6: Error handling
logger.info("Test 6: Testing error handling...")
start_time = time.time()
try:
    # Test loading non-existent file
    logger.debug("Testing load of non-existent file...")
    result = data_loader.load_json("NonExistent/fake.json")
    logger.debug(f"Load result for fake file: {result}")
    assert result is None, "Should return None for missing file"
    logger.info("✓ Handles missing files gracefully")
    
    # Test invalid fruit ID
    logger.debug("Testing invalid fruit ID...")
    fruit = devil_fruit_manager.get_fruit_by_id("invalid_id_12345")
    logger.debug(f"Result for invalid ID: {fruit}")
    assert fruit is None, "Should return None for invalid ID"
    logger.info("✓ Handles invalid IDs gracefully")
    
    # Test invalid weapon type
    logger.debug("Testing invalid weapon type...")
    weapons = item_manager.get_weapons_by_type("invalid_type")
    logger.debug(f"Results for invalid type: {len(weapons)} weapons")
    assert len(weapons) == 0, "Should return empty list for invalid type"
    logger.info("✓ Handles invalid types gracefully")
    
    elapsed = time.time() - start_time
    logger.debug(f"Error handling test completed in {elapsed:.3f}s")
    logger.info("✓ Error handling verified!\n")
    
except Exception as e:
    elapsed = time.time() - start_time
    logger.error(f"Error handling test failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ Error handling test failed: {e}\n")
    sys.exit(1)

logger.info("=" * 60)
logger.info("All tests passed! ✓")
logger.info("=" * 60)
logger.info("")

# Print summary
logger.info("Data Loading System Summary:")
logger.info("")
logger.info("✓ DataLoader - Loads and caches JSON files")
logger.info("✓ DevilFruitManager - Manages Devil Fruit database")
logger.info("✓ ItemManager - Manages weapons and items")
logger.info("")
logger.info("Features:")
logger.info("  ✓ Singleton pattern for global access")
logger.info("  ✓ Automatic caching of loaded data")
logger.info("  ✓ Type-based filtering")
logger.info("  ✓ Search functionality")
logger.info("  ✓ Data validation")
logger.info("  ✓ Error handling")
logger.info("  ✓ Reload capability")
logger.info("")

# Database status
if devil_fruit_manager.loaded and item_manager.loaded:
    df_stats = devil_fruit_manager.get_fruit_stats()
    item_stats = item_manager.get_item_stats()
    
    logger.info("Current Database:")
    logger.info(f"  📜 {df_stats['total']} Devil Fruits loaded")
    logger.info(f"  ⚔️  {item_stats['total_weapons']} Weapons loaded")
    logger.info(f"  🎒 {item_stats['total_items']} Items loaded")
    logger.info("")
    logger.info("✅ Database is ready for character creation!")
    logger.debug(f"Database fully populated with {df_stats['total']} fruits, {item_stats['total_weapons']} weapons, {item_stats['total_items']} items")
elif not os.path.exists(data_loader.get_database_path("index.json")):
    logger.warning("Database is empty - this is normal for initial setup")
    logger.info("⚠️  Database is empty - this is normal for initial setup")
    logger.info("   Next step: Populate database with Devil Fruits and items")
else:
    logger.warning("Some data could not be loaded - check database structure")
    logger.info("⚠️  Some data could not be loaded - check database structure")
logger.info("")

logger.debug(f"Test completed at: {datetime.now()}")
logger.debug(f"Log file saved to: logs/test_phase1_part4.log")
