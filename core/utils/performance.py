"""
Performance monitoring utilities for tracking processing times and cache usage.

This module provides tools for monitoring and analyzing the performance of recipe
processing operations, including individual recipe processing and batch operations.
"""

from core.config import config
from core.utils.logger import get_logger, log_performance
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import json
import os

from dataclasses import dataclass, field
import statistics
import time
logger = get_logger(__name__)

@dataclass

class ProcessingMetrics:
    """Metrics for a single processing operation."""
    start_time: float
    end_time: float
    cache_hit: bool
    method: str  # 'llm' or 'rule - based'
    success: bool
    error: Optional[str] = None

    @property
    def duration(self) -> float:
        """Get the duration in seconds."""
        return self.end_time - self.start_time

@dataclass

class BatchMetrics:
    """Metrics for a batch processing operation."""
    start_time: float
    end_time: float
    total_recipes: int
    successful_recipes: int
    failed_recipes: int
    cache_hits: int
    llm_extractions: int
    rule_based_extractions: int
    individual_metrics: List[ProcessingMetrics] = field(default_factory = list)

    @property
    def duration(self) -> float:
        """Get the total duration in seconds."""
        return self.end_time - self.start_time

    @property
    def average_duration(self) -> float:
        """Get the average processing time per recipe."""
        if not self.individual_metrics:
            return 0.0
        return statistics.mean(m.duration for m in self.individual_metrics)

    @property
    def cache_hit_rate(self) -> float:
        """Get the cache hit rate."""
        if not self.total_recipes:
            return 0.0
        return self.cache_hits / self.total_recipes

    @property
    def success_rate(self) -> float:
        """Get the success rate."""
        if not self.total_recipes:
            return 0.0
        return self.successful_recipes / self.total_recipes

class PerformanceMonitor:
    """Monitor for tracking processing performance."""

    def __init__(self) -> None:
        """Initialize the performance monitor."""
        self._metrics: Dict[str, List[ProcessingMetrics]] = {}
        self._batch_metrics: Dict[str, List[BatchMetrics]] = {}
        self._current_batch: Optional[BatchMetrics] = None
        self._metrics_file = config.PATHS.VAR_DIR / "cache" / "performance_metrics.json"
        self._metrics_file.parent.mkdir(parents = True, exist_ok = True)

    def start_processing(self, recipe_id: str, method: str) -> ProcessingMetrics:
        """Start tracking a processing operation.

        Args:
            recipe_id: Unique identifier for the recipe
            method: Processing method ('llm' or 'rule - based')

        Returns:
            ProcessingMetrics object for tracking
        """
        metrics = ProcessingMetrics(
            start_time = time.time(), 
            end_time = 0.0, 
            cache_hit = False, 
            method = method, 
            success = False
)
        self._metrics.setdefault(recipe_id, []).append(metrics)
        return metrics

    def end_processing(
        self, 
        recipe_id: str, 
        success: bool = True, 
        error: Optional[str] = None
) -> None:
        """End tracking a processing operation.

        Args:
            recipe_id: Unique identifier for the recipe
            success: Whether the processing was successful
            error: Error message if processing failed
        """
        if recipe_id in self._metrics and self._metrics[recipe_id]:
            metrics = self._metrics[recipe_id][-1]
            metrics.end_time = time.time()
            metrics.success = success
            metrics.error = error

            # Update batch metrics if active
            if self._current_batch:
                self._current_batch.individual_metrics.append(metrics)
                if success:
                    self._current_batch.successful_recipes += 1
                else:
                    self._current_batch.failed_recipes += 1
                if metrics.cache_hit:
                    self._current_batch.cache_hits += 1
                if metrics.method == 'llm':
                    self._current_batch.llm_extractions += 1
                else:
                    self._current_batch.rule_based_extractions += 1

    def start_batch(self, total_recipes: int) -> BatchMetrics:
        """Start tracking a batch processing operation.

        Args:
            total_recipes: Total number of recipes in the batch

        Returns:
            BatchMetrics object for tracking
        """
        self._current_batch = BatchMetrics(
            start_time = time.time(), 
            end_time = 0.0, 
            total_recipes = total_recipes, 
            successful_recipes = 0, 
            failed_recipes = 0, 
            cache_hits = 0, 
            llm_extractions = 0, 
            rule_based_extractions = 0
)
        return self._current_batch

    def end_batch(self, batch_id: str) -> None:
        """End tracking a batch processing operation.

        Args:
            batch_id: Unique identifier for the batch
        """
        if self._current_batch:
            self._current_batch.end_time = time.time()
            self._batch_metrics.setdefault(batch_id, []).append(self._current_batch)
            self._log_batch_metrics(self._current_batch)
            self._save_metrics()
            self._current_batch = None

    def _log_batch_metrics(self, metrics: BatchMetrics) -> None:
        """Log batch processing metrics.

        Args:
            metrics: Batch metrics to log
        """
        log_performance(
            "batch_processing", 
            metrics.duration, 
            {
                "total_recipes": metrics.total_recipes, 
                "successful": metrics.successful_recipes, 
                "failed": metrics.failed_recipes, 
                "success_rate": metrics.success_rate, 
                "cache_hit_rate": metrics.cache_hit_rate, 
                "llm_extractions": metrics.llm_extractions, 
                "rule_based_extractions": metrics.rule_based_extractions
            }
)

    def _save_metrics(self) -> None:
        """Save metrics to disk."""
        try:
            metrics_data = {
                "timestamp": datetime.now().isoformat(), 
                "metrics": self.get_metrics_summary()
            }
            with open(self._metrics_file, "w") as f:
                json.dump(metrics_data, f, indent = 2)
        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get a summary of all metrics.

        Returns:
            Dictionary containing metrics summary
        """
        all_metrics = [m for metrics in self._metrics.values() for m in metrics]
        all_batch_metrics = [m for metrics in self._batch_metrics.values() for m in metrics]

        return {
            'total_processed': len(all_metrics), 
            'total_batches': len(all_batch_metrics), 
            'average_processing_time': statistics.mean(m.duration for m in all_metrics) if all_metrics else 0.0, 
            'average_batch_time': statistics.mean(m.duration for m in all_batch_metrics) if all_batch_metrics else 0.0, 
            'total_cache_hits': sum(1 for m in all_metrics if m.cache_hit), 
            'total_llm_extractions': sum(1 for m in all_metrics if m.method == 'llm'), 
            'total_rule_based_extractions': sum(1 for m in all_metrics if m.method == 'rule - based'), 
            'success_rate': sum(1 for m in all_metrics if m.success) / len(all_metrics) if all_metrics else 0.0
        }

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

def print_performance_metrics() -> None:
    """Print a summary of all performance metrics."""
    summary = performance_monitor.get_metrics_summary()

    print("\nPerformance Metrics Summary:")
    print("===========================")
    print(f"Total Processed: {summary['total_processed']}")
    print(f"Total Batches: {summary['total_batches']}")
    print(f"Average Processing Time: {summary['average_processing_time']:.2f}s")
    print(f"Average Batch Time: {summary['average_batch_time']:.2f}s")
    if summary['total_processed'] > 0:
        print(f"Cache Hit Rate: {summary['total_cache_hits'] / summary['total_processed']:.1%}")
    else:
        print("Cache Hit Rate: N / A")
    print(f"LLM Extractions: {summary['total_llm_extractions']}")
    print(f"Rule - based Extractions: {summary['total_rule_based_extractions']}")
    print(f"Overall Success Rate: {summary['success_rate']:.1%}")
    print("===========================\n")

def log_recipe_processing_performance(
    operation: str, 
    duration: float, 
    metadata: Dict[str, Any]
) -> None:
    """Log recipe processing performance metrics.

    Args:
        operation: Name of the operation
        duration: Duration in seconds
        metadata: Additional performance metadata
    """
    log_performance(operation, duration, metadata)
