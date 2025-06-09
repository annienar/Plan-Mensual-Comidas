"""
Enhanced cache implementation for LLM responses with performance optimizations.

This module provides an optimized caching system specifically designed for 
recipe processing with intelligent eviction policies and performance monitoring.
"""

from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple, Set, List
from dataclasses import dataclass, field
import time
import hashlib
import json
import logging
import re

logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    """Enhanced cache entry with access patterns and performance metrics."""
    value: Any
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    content_hash: str = ""
    size_bytes: int = 0
    processing_time: float = 0.0
    # NEW: Recipe-specific fields for similarity matching
    normalized_content: str = ""
    ingredient_signature: str = ""
    recipe_type: str = ""

    def is_expired(self, ttl: float) -> bool:
        """Check if entry is expired."""
        return time.time() - self.created_at > ttl

    def update_access(self) -> None:
        """Update access statistics."""
        self.last_accessed = time.time()
        self.access_count += 1

    def get_age(self) -> float:
        """Get age of entry in seconds."""
        return time.time() - self.created_at

    def get_access_frequency(self) -> float:
        """Calculate access frequency (accesses per hour)."""
        age_hours = self.get_age() / 3600
        return self.access_count / max(age_hours, 0.1)  # Avoid division by zero

@dataclass
class CacheStats:
    """Enhanced cache statistics for performance monitoring."""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    size: int = 0
    max_size: int = 0
    ttl: float = 0.0
    total_size_bytes: int = 0
    average_processing_time: float = 0.0
    # NEW: Similarity matching stats
    similarity_hits: int = 0
    content_deduplications: int = 0
    
    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    @property
    def enhanced_hit_rate(self) -> float:
        """Calculate enhanced hit rate including similarity hits."""
        total = self.hits + self.similarity_hits + self.misses
        return (self.hits + self.similarity_hits) / total if total > 0 else 0.0
    
    @property
    def memory_efficiency(self) -> float:
        """Calculate memory efficiency (hits per MB)."""
        mb_used = self.total_size_bytes / (1024 * 1024)
        return self.hits / max(mb_used, 0.1)

class RecipeContentAnalyzer:
    """Analyzes recipe content for intelligent caching and similarity matching."""
    
    # Spanish-English unit mappings for normalization
    UNIT_MAPPINGS = {
        # Volume
        'cup': 'taza', 'cups': 'tazas',
        'tablespoon': 'cucharada', 'tablespoons': 'cucharadas', 'tbsp': 'cucharada',
        'teaspoon': 'cucharadita', 'teaspoons': 'cucharaditas', 'tsp': 'cucharadita',
        'liter': 'litro', 'liters': 'litros', 'l': 'litro',
        'milliliter': 'ml', 'milliliters': 'ml',
        # Weight
        'pound': 'libra', 'pounds': 'libras', 'lb': 'libra', 'lbs': 'libras',
        'ounce': 'onza', 'ounces': 'onzas', 'oz': 'onza',
        'gram': 'gramo', 'grams': 'gramos', 'g': 'gramo',
        'kilogram': 'kilo', 'kilograms': 'kilos', 'kg': 'kilo',
        # Common ingredients
        'chicken': 'pollo', 'beef': 'carne', 'pork': 'cerdo',
        'onion': 'cebolla', 'garlic': 'ajo', 'tomato': 'tomate',
        'salt': 'sal', 'pepper': 'pimienta', 'oil': 'aceite'
    }
    
    @classmethod
    def normalize_recipe_content(cls, content: str) -> str:
        """Normalize recipe content for better cache matching."""
        # Convert to lowercase and strip
        normalized = content.lower().strip()
        
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Standardize units (English -> Spanish)
        for english, spanish in cls.UNIT_MAPPINGS.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(english) + r'\b'
            normalized = re.sub(pattern, spanish, normalized)
        
        # Standardize common number formats
        normalized = re.sub(r'(\d+)/(\d+)', r'\1-\2', normalized)  # 1/2 -> 1-2
        normalized = re.sub(r'(\d+)\.(\d+)', r'\1-\2', normalized)  # 1.5 -> 1-5
        
        # Remove common recipe formatting
        normalized = re.sub(r'[•\-\*]\s*', '', normalized)  # Remove bullet points
        normalized = re.sub(r'\d+\.\s*', '', normalized)    # Remove numbered steps
        
        return normalized
    
    @classmethod
    def extract_ingredient_signature(cls, content: str) -> str:
        """Extract ingredient signature for similarity matching."""
        # Find ingredient-like patterns (number + unit + ingredient)
        ingredient_patterns = [
            r'\d+\s*(taza|cucharada|cucharadita|gramo|kilo|litro|ml)\s+(?:de\s+)?(\w+)',
            r'(\w+)\s*[,:]',  # Ingredients in lists
            r'\b(pollo|carne|cerdo|pescado|arroz|pasta|tomate|cebolla|ajo)\b'  # Common ingredients
        ]
        
        ingredients = set()
        normalized = cls.normalize_recipe_content(content)
        
        for pattern in ingredient_patterns:
            matches = re.findall(pattern, normalized)
            for match in matches:
                if isinstance(match, tuple):
                    ingredients.update(match)
                else:
                    ingredients.add(match)
        
        # Sort and create signature
        return '|'.join(sorted(ingredients))
    
    @classmethod
    def detect_recipe_type(cls, content: str) -> str:
        """Detect recipe type for categorization."""
        content_lower = content.lower()
        
        # Simple recipe type detection
        if any(word in content_lower for word in ['pasta', 'spaghetti', 'linguine']):
            return 'pasta'
        elif any(word in content_lower for word in ['pollo', 'chicken']):
            return 'pollo'
        elif any(word in content_lower for word in ['arroz', 'rice']):
            return 'arroz'
        elif any(word in content_lower for word in ['ensalada', 'salad']):
            return 'ensalada'
        elif any(word in content_lower for word in ['sopa', 'soup']):
            return 'sopa'
        else:
            return 'general'
    
    @classmethod
    def calculate_similarity(cls, content1: str, content2: str) -> float:
        """Calculate similarity between two recipe contents."""
        # Normalize both contents
        norm1 = cls.normalize_recipe_content(content1)
        norm2 = cls.normalize_recipe_content(content2)
        
        # Simple word-based similarity
        words1 = set(norm1.split())
        words2 = set(norm2.split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        jaccard_similarity = len(intersection) / len(union) if union else 0
        
        # Boost similarity if ingredient signatures are similar
        sig1 = cls.extract_ingredient_signature(content1)
        sig2 = cls.extract_ingredient_signature(content2)
        
        if sig1 and sig2:
            sig_words1 = set(sig1.split('|'))
            sig_words2 = set(sig2.split('|'))
            sig_intersection = sig_words1.intersection(sig_words2)
            sig_union = sig_words1.union(sig_words2)
            
            ingredient_similarity = len(sig_intersection) / len(sig_union) if sig_union else 0
            
            # Weighted combination: 60% content, 40% ingredients
            return jaccard_similarity * 0.6 + ingredient_similarity * 0.4
        
        return jaccard_similarity

class SmartLLMCache:
    """Intelligent cache for LLM responses with advanced eviction and optimization."""

    def __init__(
        self, 
        max_size: int = 5000, 
        ttl: float = 14400.0,  # 4 hours
        cleanup_interval: float = 300.0,  # 5 minutes
        max_memory_mb: int = 100,  # 100MB max cache size
        eviction_strategy: str = "lru_frequency",  # lru, lru_frequency, or size_based
        similarity_threshold: float = 0.75  # NEW: Similarity threshold for cache hits
    ):
        """Initialize the smart cache.

        Args:
            max_size: Maximum number of entries
            ttl: Time to live in seconds
            cleanup_interval: Interval for cleanup in seconds
            max_memory_mb: Maximum memory usage in MB
            eviction_strategy: Eviction strategy to use
            similarity_threshold: Threshold for content similarity matching (0.0-1.0)
        """
        self.max_size = max_size
        self.ttl = ttl
        self.cleanup_interval = cleanup_interval
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.eviction_strategy = eviction_strategy
        self.similarity_threshold = similarity_threshold
        self.last_cleanup = time.time()

        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._stats = CacheStats(max_size=max_size, ttl=ttl)
        self._content_index: Dict[str, Set[str]] = {}  # Content hash to keys mapping
        # NEW: Enhanced indexes for similarity matching
        self._ingredient_index: Dict[str, Set[str]] = {}  # Ingredient signature to keys
        self._recipe_type_index: Dict[str, Set[str]] = {}  # Recipe type to keys
        self.analyzer = RecipeContentAnalyzer()

    def _calculate_size(self, value: Any) -> int:
        """Estimate size of cached value in bytes."""
        try:
            if hasattr(value, 'text'):
                # LLM response object
                return len(str(value.text).encode('utf-8')) + 500  # Base overhead
            else:
                return len(str(value).encode('utf-8'))
        except:
            return 1000  # Default estimate

    def _create_content_hash(self, value: Any) -> str:
        """Create content hash for deduplication."""
        try:
            if hasattr(value, 'text'):
                content = value.text
            else:
                content = str(value)
            return hashlib.md5(content.encode('utf-8')).hexdigest()[:16]
        except:
            return ""

    def _analyze_input_content(self, input_content: str) -> Tuple[str, str, str]:
        """Analyze input content for caching optimization."""
        normalized = self.analyzer.normalize_recipe_content(input_content)
        ingredient_sig = self.analyzer.extract_ingredient_signature(input_content)
        recipe_type = self.analyzer.detect_recipe_type(input_content)
        return normalized, ingredient_sig, recipe_type

    def get_similar_cached_entry(self, input_content: str) -> Optional[Any]:
        """Get cached entry using similarity matching - NEW PERFORMANCE BOOST!"""
        if not input_content.strip():
            return None
            
        normalized_input, ingredient_sig, recipe_type = self._analyze_input_content(input_content)
        
        # Quick ingredient signature lookup first
        if ingredient_sig in self._ingredient_index:
            for key in self._ingredient_index[ingredient_sig]:
                if key in self._cache:
                    entry = self._cache[key]
                    if not entry.is_expired(self.ttl):
                        entry.update_access()
                        self._stats.similarity_hits += 1
                        logger.info(f"🎯 Cache hit via ingredient signature: {ingredient_sig}")
                        return entry.value
        
        # Recipe type based lookup
        if recipe_type in self._recipe_type_index:
            candidates = []
            for key in self._recipe_type_index[recipe_type]:
                if key in self._cache:
                    entry = self._cache[key]
                    if not entry.is_expired(self.ttl):
                        candidates.append((key, entry))
            
            # Calculate similarity for type-matched candidates
            for key, entry in candidates:
                similarity = self.analyzer.calculate_similarity(
                    input_content, 
                    entry.normalized_content
                )
                
                if similarity >= self.similarity_threshold:
                    entry.update_access()
                    self._stats.similarity_hits += 1
                    logger.info(f"🎯 Cache hit via similarity: {similarity:.1%} for type '{recipe_type}'")
                    return entry.value
        
        return None

    def _cleanup_if_needed(self) -> None:
        """Perform cleanup if interval has passed."""
        if time.time() - self.last_cleanup > self.cleanup_interval:
            self._cleanup_expired()
            self._enforce_memory_limit()
            self.last_cleanup = time.time()

    def _cleanup_expired(self) -> None:
        """Remove expired entries."""
        expired_keys = []
        for key, entry in self._cache.items():
            if entry.is_expired(self.ttl):
                expired_keys.append(key)

        for key in expired_keys:
            self._remove_entry(key)
            self._stats.evictions += 1

        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")

    def _enforce_memory_limit(self) -> None:
        """Enforce memory limits by evicting entries."""
        if self._stats.total_size_bytes <= self.max_memory_bytes:
            return

        # Calculate how much to evict
        target_size = int(self.max_memory_bytes * 0.8)  # Target 80% of max
        bytes_to_evict = self._stats.total_size_bytes - target_size

        evicted = self._evict_by_strategy(bytes_to_evict)
        if evicted > 0:
            logger.info(f"Evicted {evicted} entries to free memory")

    def _evict_by_strategy(self, bytes_needed: int) -> int:
        """Evict entries based on configured strategy."""
        if self.eviction_strategy == "lru":
            return self._evict_lru(bytes_needed)
        elif self.eviction_strategy == "lru_frequency":
            return self._evict_lru_frequency(bytes_needed)
        elif self.eviction_strategy == "size_based":
            return self._evict_largest_first(bytes_needed)
        else:
            return self._evict_lru(bytes_needed)

    def _evict_lru(self, bytes_needed: int) -> int:
        """Evict least recently used entries."""
        evicted_count = 0
        bytes_freed = 0
        
        # Sort by last accessed time
        entries_by_access = sorted(
            self._cache.items(),
            key=lambda x: x[1].last_accessed
        )
        
        for key, entry in entries_by_access:
            if bytes_freed >= bytes_needed:
                break
            bytes_freed += entry.size_bytes
            self._remove_entry(key)
            evicted_count += 1
            self._stats.evictions += 1
            
        return evicted_count

    def _evict_lru_frequency(self, bytes_needed: int) -> int:
        """Evict based on LRU + access frequency."""
        evicted_count = 0
        bytes_freed = 0
        
        # Calculate eviction score (lower is better for eviction)
        entries_with_score = []
        for key, entry in self._cache.items():
            frequency = entry.get_access_frequency()
            recency = time.time() - entry.last_accessed
            score = frequency / max(recency, 1.0)  # Higher frequency and recency = higher score
            entries_with_score.append((key, entry, score))
        
        # Sort by score (ascending - lowest score evicted first)
        entries_with_score.sort(key=lambda x: x[2])
        
        for key, entry, score in entries_with_score:
            if bytes_freed >= bytes_needed:
                break
            bytes_freed += entry.size_bytes
            self._remove_entry(key)
            evicted_count += 1
            self._stats.evictions += 1
            
        return evicted_count

    def _evict_largest_first(self, bytes_needed: int) -> int:
        """Evict largest entries first."""
        evicted_count = 0
        bytes_freed = 0
        
        # Sort by size (descending)
        entries_by_size = sorted(
            self._cache.items(),
            key=lambda x: x[1].size_bytes,
            reverse=True
        )
        
        for key, entry in entries_by_size:
            if bytes_freed >= bytes_needed:
                break
            bytes_freed += entry.size_bytes
            self._remove_entry(key)
            evicted_count += 1
            self._stats.evictions += 1
            
        return evicted_count

    def _remove_entry(self, key: str) -> None:
        """Remove entry and update all indexes."""
        if key in self._cache:
            entry = self._cache[key]
            self._stats.size -= 1
            self._stats.total_size_bytes -= entry.size_bytes
            
            # Update content index
            if entry.content_hash and entry.content_hash in self._content_index:
                self._content_index[entry.content_hash].discard(key)
                if not self._content_index[entry.content_hash]:
                    del self._content_index[entry.content_hash]
            
            # NEW: Update enhanced indexes
            if entry.ingredient_signature and entry.ingredient_signature in self._ingredient_index:
                self._ingredient_index[entry.ingredient_signature].discard(key)
                if not self._ingredient_index[entry.ingredient_signature]:
                    del self._ingredient_index[entry.ingredient_signature]
            
            if entry.recipe_type and entry.recipe_type in self._recipe_type_index:
                self._recipe_type_index[entry.recipe_type].discard(key)
                if not self._recipe_type_index[entry.recipe_type]:
                    del self._recipe_type_index[entry.recipe_type]
            
            del self._cache[key]

    def get(self, key: str, input_content: str = "") -> Optional[Any]:
        """Get value from cache with smart deduplication and similarity matching."""
        self._cleanup_if_needed()

        # First try direct key lookup
        if key in self._cache:
            entry = self._cache[key]
            
            if not entry.is_expired(self.ttl):
                entry.update_access()
                self._stats.hits += 1
                logger.debug(f"🎯 Direct cache hit for key: {key}")
                return entry.value
            else:
                self._remove_entry(key)

        # NEW: Try similarity matching if input content provided
        if input_content:
            similar_entry = self.get_similar_cached_entry(input_content)
            if similar_entry:
                return similar_entry

        self._stats.misses += 1
        return None

    def set(self, key: str, value: Any, processing_time: float = 0.0, input_content: str = "") -> bool:
        """Set value in cache with enhanced indexing."""
        self._cleanup_if_needed()

        # Check if we need to evict due to size
        if len(self._cache) >= self.max_size:
            self._evict_by_strategy(1)  # Evict at least one entry

        # Calculate entry metadata
        size_bytes = self._calculate_size(value)
        content_hash = self._create_content_hash(value)
        
        # NEW: Analyze input content for enhanced caching
        normalized_content = ""
        ingredient_signature = ""
        recipe_type = ""
        
        if input_content:
            normalized_content, ingredient_signature, recipe_type = self._analyze_input_content(input_content)

        # Create enhanced entry
        entry = CacheEntry(
            value=value,
            size_bytes=size_bytes,
            content_hash=content_hash,
            processing_time=processing_time,
            normalized_content=normalized_content,
            ingredient_signature=ingredient_signature,
            recipe_type=recipe_type
        )

        # Store in cache
        self._cache[key] = entry

        # Update indexes
        if content_hash:
            if content_hash not in self._content_index:
                self._content_index[content_hash] = set()
            self._content_index[content_hash].add(key)
        
        # NEW: Update enhanced indexes
        if ingredient_signature:
            if ingredient_signature not in self._ingredient_index:
                self._ingredient_index[ingredient_signature] = set()
            self._ingredient_index[ingredient_signature].add(key)
        
        if recipe_type:
            if recipe_type not in self._recipe_type_index:
                self._recipe_type_index[recipe_type] = set()
            self._recipe_type_index[recipe_type].add(key)

        # Update stats
        self._stats.size += 1
        self._stats.total_size_bytes += size_bytes

        logger.debug(f"💾 Cached entry: key={key}, type={recipe_type}, ingredients={ingredient_signature[:50]}")
        return True

    def get_stats(self) -> Dict[str, Any]:
        """Get enhanced cache statistics."""
        processing_times = [entry.processing_time for entry in self._cache.values() if entry.processing_time > 0]
        avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0

        return {
            'hits': self._stats.hits,
            'misses': self._stats.misses,
            'similarity_hits': self._stats.similarity_hits,  # NEW
            'content_deduplications': self._stats.content_deduplications,  # NEW
            'evictions': self._stats.evictions,
            'size': self._stats.size,
            'max_size': self._stats.max_size,
            'hit_rate': self._stats.hit_rate,
            'enhanced_hit_rate': self._stats.enhanced_hit_rate,  # NEW: Includes similarity hits
            'memory_efficiency': self._stats.memory_efficiency,
            'ttl': self._stats.ttl,
            'total_size_bytes': self._stats.total_size_bytes,
            'total_size_mb': self._stats.total_size_bytes / (1024 * 1024),
            'average_processing_time': avg_processing_time,
            'ingredient_signatures': len(self._ingredient_index),  # NEW
            'recipe_types': len(self._recipe_type_index),  # NEW
        }

    def optimize(self) -> Dict[str, Any]:
        """Enhanced cache optimization with similarity analysis."""
        # Run standard optimization
        self._cleanup_expired()
        self._enforce_memory_limit()
        
        # NEW: Analyze cache effectiveness
        analysis = {
            'optimization_timestamp': datetime.now().isoformat(),
            'cache_performance': {
                'direct_hit_rate': self._stats.hit_rate,
                'enhanced_hit_rate': self._stats.enhanced_hit_rate,
                'similarity_effectiveness': self._stats.similarity_hits / max(self._stats.hits + self._stats.misses, 1),
                'memory_usage_mb': self._stats.total_size_bytes / (1024 * 1024),
                'entries_count': self._stats.size
            },
            'content_analysis': {
                'unique_ingredient_signatures': len(self._ingredient_index),
                'recipe_types_cached': len(self._recipe_type_index),
                'content_diversity': len(self._content_index)
            },
            'recommendations': self._get_optimization_recommendations()
        }
        
        logger.info(f"🚀 Cache optimization complete: {analysis['cache_performance']['enhanced_hit_rate']:.1%} enhanced hit rate")
        return analysis

    def _get_optimization_recommendations(self) -> List[str]:
        """Get optimization recommendations based on cache performance."""
        recommendations = []
        
        if self._stats.enhanced_hit_rate < 0.5:
            recommendations.append("Consider lowering similarity threshold for more cache hits")
        
        if len(self._ingredient_index) < 10:
            recommendations.append("Cache needs more recipe variety for better ingredient matching")
        
        if self._stats.total_size_bytes > self.max_memory_bytes * 0.9:
            recommendations.append("Consider increasing cache memory limit or cleaning frequency")
        
        if self._stats.similarity_hits > self._stats.hits:
            recommendations.append("Similarity matching is very effective - consider extending TTL")
        
        return recommendations or ["Cache is performing optimally"]

    def clear(self) -> None:
        """Clear all cache data and indexes."""
        self._cache.clear()
        self._content_index.clear()
        self._ingredient_index.clear()  # NEW
        self._recipe_type_index.clear()  # NEW
        self._stats = CacheStats(max_size=self.max_size, ttl=self.ttl)

    def get_popular_entries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most popular cached entries with enhanced metadata."""
        entries_with_popularity = []
        for key, entry in self._cache.items():
            popularity_score = entry.access_count * entry.get_access_frequency()
            entries_with_popularity.append({
                'key': key,
                'access_count': entry.access_count,
                'frequency': entry.get_access_frequency(),
                'popularity_score': popularity_score,
                'age_hours': entry.get_age() / 3600,
                'recipe_type': entry.recipe_type,  # NEW
                'ingredient_signature': entry.ingredient_signature[:100],  # NEW (truncated)
                'processing_time': entry.processing_time
            })
        
        # Sort by popularity score
        entries_with_popularity.sort(key=lambda x: x['popularity_score'], reverse=True)
        return entries_with_popularity[:limit]
