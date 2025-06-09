"""
Metrics module for monitoring.
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
import threading

from collections import defaultdict
from dataclasses import dataclass, field
import time
@dataclass

class MetricValue:
    """A metric value with timestamp."""
    value: float
    timestamp: datetime = field(default_factory = datetime.now)

@dataclass

class Metric:
    """A metric with name and values."""
    name: str
    values: List[MetricValue] = field(default_factory = list)
    description: Optional[str] = None
    unit: Optional[str] = None
    labels: Dict[str, str] = field(default_factory = dict)

class MetricsRegistry:
    """Registry for metrics."""

    def __init__(self):
        """Initialize the registry."""
        self._metrics: Dict[str, Metric] = {}
        self._lock = threading.Lock()

    def register_metric(
        self, 
        name: str, 
        description: Optional[str] = None, 
        unit: Optional[str] = None, 
        labels: Optional[Dict[str, str]] = None
) -> None:
        """Register a new metric.

        Args:
            name: Metric name
            description: Optional description
            unit: Optional unit
            labels: Optional labels
        """
        with self._lock:
            if name in self._metrics:
                raise ValueError(f"Metric {name} already registered")

            self._metrics[name] = Metric(
                name = name, 
                description = description, 
                unit = unit, 
                labels = labels or {}
)

    def record_value(
        self, 
        name: str, 
        value: float, 
        labels: Optional[Dict[str, str]] = None
) -> None:
        """Record a value for a metric.

        Args:
            name: Metric name
            value: Value to record
            labels: Optional labels
        """
        with self._lock:
            if name not in self._metrics:
                raise ValueError(f"Metric {name} not registered")

            metric = self._metrics[name]
            metric.values.append(MetricValue(value = value))

    def get_metric(self, name: str) -> Optional[Metric]:
        """Get a metric by name.

        Args:
            name: Metric name

        Returns:
            Optional[Metric]: Metric if found
        """
        return self._metrics.get(name)

    def get_all_metrics(self) -> Dict[str, Metric]:
        """Get all metrics.

        Returns:
            Dict[str, Metric]: All metrics
        """
        return self._metrics.copy()

    def clear_metrics(self) -> None:
        """Clear all metrics."""
        with self._lock:
            self._metrics.clear()

# Global registry
registry = MetricsRegistry()

# Common metrics
registry.register_metric(
    "recipe_generation_duration_seconds", 
    description="Time taken to generate a recipe", 
    unit="seconds"
)

registry.register_metric(
    "recipe_extraction_duration_seconds", 
    description="Time taken to extract a recipe", 
    unit="seconds"
)

registry.register_metric(
    "recipe_generation_confidence", 
    description="Confidence score for recipe generation", 
    unit="ratio"
)

registry.register_metric(
    "recipe_extraction_confidence", 
    description="Confidence score for recipe extraction", 
    unit="ratio"
)

registry.register_metric(
    "recipe_generation_tokens", 
    description="Number of tokens used for recipe generation", 
    unit="tokens"
)

registry.register_metric(
    "recipe_extraction_tokens", 
    description="Number of tokens used for recipe extraction", 
    unit="tokens"
)

registry.register_metric(
    "recipe_generation_errors", 
    description="Number of errors during recipe generation", 
    unit="count"
)

registry.register_metric(
    "recipe_extraction_errors", 
    description="Number of errors during recipe extraction", 
    unit="count"
)

registry.register_metric(
    "recipe_generation_cache_hits", 
    description="Number of cache hits during recipe generation", 
    unit="count"
)

registry.register_metric(
    "recipe_extraction_cache_hits", 
    description="Number of cache hits during recipe extraction", 
    unit="count"
)

registry.register_metric(
    "recipe_generation_cache_misses", 
    description="Number of cache misses during recipe generation", 
    unit="count"
)

registry.register_metric(
    "recipe_extraction_cache_misses", 
    description="Number of cache misses during recipe extraction", 
    unit="count"
)

registry.register_metric(
    "recipe_generation_circuit_breaker_trips", 
    description="Number of circuit breaker trips during recipe generation", 
    unit="count"
)

registry.register_metric(
    "recipe_extraction_circuit_breaker_trips", 
    description="Number of circuit breaker trips during recipe extraction", 
    unit="count"
)
