"""
Optimized Data Loader
High-performance JSON data loading with caching, lazy loading, and indexing.
"""

import json
import os
import time
from typing import Dict, Any, List, Optional
from functools import lru_cache
from utils.logger import get_logger


class PerformanceMonitor:
    """Monitor and track data loading performance."""

    def __init__(self):
        self.cache_hits = 0
        self.cache_misses = 0
        self.load_times = []
        self.total_loads = 0

    def record_cache_hit(self):
        """Record a cache hit."""
        self.cache_hits += 1

    def record_cache_miss(self):
        """Record a cache miss."""
        self.cache_misses += 1

    def record_load_time(self, duration: float):
        """Record load duration in seconds."""
        self.load_times.append(duration)
        self.total_loads += 1

    def get_hit_rate(self) -> float:
        """Get cache hit rate percentage."""
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return (self.cache_hits / total) * 100

    def get_average_load_time(self) -> float:
        """Get average load time in milliseconds."""
        if not self.load_times:
            return 0.0
        return (sum(self.load_times) / len(self.load_times)) * 1000

    def print_stats(self):
        """Print performance statistics."""
        print("\n" + "="*60)
        print("DATA LOADER PERFORMANCE STATS")
        print("="*60)
        print(f"Total loads: {self.total_loads}")
        print(f"Cache hits: {self.cache_hits}")
        print(f"Cache misses: {self.cache_misses}")
        print(f"Hit rate: {self.get_hit_rate():.1f}%")
        print(f"Average load time: {self.get_average_load_time():.2f}ms")
        if self.load_times:
            print(f"Min load time: {min(self.load_times)*1000:.2f}ms")
            print(f"Max load time: {max(self.load_times)*1000:.2f}ms")
        print("="*60 + "\n")


class OptimizedDataLoader:
    """
    Optimized data loader with caching, lazy loading, and performance monitoring.

    Features:
    - LRU caching for frequently accessed data
    - Lazy loading - only load what's needed
    - Index building for fast lookups
    - Performance monitoring
    - Memory management
    """

    def __init__(self, base_path: str = "Databases"):
        """
        Initialize the optimized data loader.

        Args:
            base_path: Base directory for data files
        """
        self.logger = get_logger()
        self.base_path = base_path

        # Cache storage
        self.cache = {}
        self.indices = {}

        # Performance monitoring
        self.monitor = PerformanceMonitor()

        # Configuration
        self.enable_caching = True
        self.enable_lazy_loading = True
        self.max_cache_size_mb = 50

        self.logger.info("Optimized Data Loader initialized")
        self.logger.debug(f"Base path: {base_path}")

    def load_json(self, file_path: str, use_cache: bool = True) -> Optional[Dict]:
        """
        Load JSON file with optional caching.

        Args:
            file_path: Path to JSON file
            use_cache: Whether to use cache

        Returns:
            Dictionary data or None if error
        """
        # Check cache first
        if use_cache and self.enable_caching and file_path in self.cache:
            self.monitor.record_cache_hit()
            self.logger.debug(f"Cache hit: {file_path}")
            return self.cache[file_path]

        # Cache miss - load from disk
        self.monitor.record_cache_miss()

        start_time = time.time()

        try:
            full_path = os.path.join(self.base_path, file_path)

            if not os.path.exists(full_path):
                self.logger.warning(f"File not found: {full_path}")
                return None

            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            load_time = time.time() - start_time
            self.monitor.record_load_time(load_time)

            self.logger.debug(f"Loaded {file_path} in {load_time*1000:.2f}ms")

            # Store in cache if enabled
            if use_cache and self.enable_caching:
                self.cache[file_path] = data
                self._check_cache_size()

            return data

        except Exception as e:
            self.logger.error(f"Error loading {file_path}: {e}")
            return None

    def load_category(self, category: str, use_cache: bool = True) -> List[Dict]:
        """
        Load all files in a category directory.

        Args:
            category: Category name (folder name)
            use_cache: Whether to use cache

        Returns:
            List of loaded data dictionaries
        """
        cache_key = f"_category_{category}"

        # Check cache
        if use_cache and self.enable_caching and cache_key in self.cache:
            self.monitor.record_cache_hit()
            return self.cache[cache_key]

        self.monitor.record_cache_miss()

        start_time = time.time()

        category_path = os.path.join(self.base_path, category)

        if not os.path.exists(category_path):
            self.logger.warning(f"Category not found: {category}")
            return []

        data_list = []

        try:
            # Load all JSON files in category
            for filename in os.listdir(category_path):
                if filename.endswith('.json'):
                    file_path = os.path.join(category, filename)
                    data = self.load_json(file_path, use_cache=False)
                    if data:
                        data_list.append(data)

            load_time = time.time() - start_time
            self.monitor.record_load_time(load_time)

            self.logger.info(f"Loaded {len(data_list)} files from {category} in {load_time*1000:.2f}ms")

            # Cache the entire category
            if use_cache and self.enable_caching:
                self.cache[cache_key] = data_list
                self._check_cache_size()

            return data_list

        except Exception as e:
            self.logger.error(f"Error loading category {category}: {e}")
            return []

    def build_index(self, category: str, index_field: str) -> Dict[Any, List[Dict]]:
        """
        Build an index on a specific field for fast lookups.

        Args:
            category: Category to index
            index_field: Field name to index on

        Returns:
            Dictionary mapping field values to data items
        """
        index_key = f"{category}_{index_field}"

        # Check if index already exists
        if index_key in self.indices:
            self.logger.debug(f"Index already exists: {index_key}")
            return self.indices[index_key]

        start_time = time.time()

        # Load category data
        data_list = self.load_category(category)

        # Build index
        index = {}
        for item in data_list:
            if index_field in item:
                field_value = item[index_field]
                if field_value not in index:
                    index[field_value] = []
                index[field_value].append(item)

        self.indices[index_key] = index

        build_time = time.time() - start_time
        self.logger.info(f"Built index {index_key} in {build_time*1000:.2f}ms ({len(index)} unique values)")

        return index

    def query_index(self, category: str, index_field: str, value: Any) -> List[Dict]:
        """
        Query using a pre-built index for O(1) lookups.

        Args:
            category: Category name
            index_field: Field to query on
            value: Value to search for

        Returns:
            List of matching items
        """
        index_key = f"{category}_{index_field}"

        # Build index if it doesn't exist
        if index_key not in self.indices:
            self.build_index(category, index_field)

        index = self.indices[index_key]
        return index.get(value, [])

    def preload_category(self, category: str):
        """
        Preload a category into cache at startup.

        Args:
            category: Category to preload
        """
        self.logger.info(f"Preloading category: {category}")
        self.load_category(category, use_cache=True)

    def clear_cache(self):
        """Clear all cached data."""
        self.cache.clear()
        self.logger.info("Cache cleared")

    def clear_indices(self):
        """Clear all built indices."""
        self.indices.clear()
        self.logger.info("Indices cleared")

    def get_cache_size_mb(self) -> float:
        """
        Get approximate cache size in megabytes.

        Returns:
            Cache size in MB
        """
        import sys
        total_size = sum(sys.getsizeof(v) for v in self.cache.values())
        return total_size / (1024 * 1024)

    def _check_cache_size(self):
        """Check if cache exceeds size limit and evict if needed."""
        current_size = self.get_cache_size_mb()

        if current_size > self.max_cache_size_mb:
            self.logger.warning(f"Cache size ({current_size:.2f}MB) exceeds limit ({self.max_cache_size_mb}MB)")
            # Simple eviction: clear half the cache (LRU would be better but more complex)
            keys_to_remove = list(self.cache.keys())[:len(self.cache)//2]
            for key in keys_to_remove:
                del self.cache[key]
            self.logger.info(f"Evicted {len(keys_to_remove)} items from cache")

    def print_memory_info(self):
        """Print memory usage information."""
        print("\n" + "="*60)
        print("MEMORY USAGE")
        print("="*60)
        print(f"Cache size: {self.get_cache_size_mb():.2f} MB")
        print(f"Cached items: {len(self.cache)}")
        print(f"Built indices: {len(self.indices)}")
        print(f"Max cache size: {self.max_cache_size_mb} MB")
        print("="*60 + "\n")


# Global instance
_optimized_loader = None


def get_optimized_loader() -> OptimizedDataLoader:
    """
    Get the global optimized data loader instance.

    Returns:
        OptimizedDataLoader instance
    """
    global _optimized_loader
    if _optimized_loader is None:
        _optimized_loader = OptimizedDataLoader()
    return _optimized_loader
