#!/usr / bin / env python3
"""
Performance monitoring script for recipe processing.

This script provides comprehensive performance metrics and analysis
for the recipe processing system, including detailed breakdowns
by processing method, cache performance, and success rates.
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

import click
from datetime import datetime, timedelta
from typing import Dict, Any
from core.utils.performance import performance_monitor
from core.utils.logger import get_logger

logger = get_logger(__name__)

def format_duration(seconds: float) -> str:
    """Format duration in human - readable format.

    Args:
        seconds: Duration in seconds

    Returns:
        str: Formatted duration string
    """
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"

def display_metrics_table(metrics: Dict[str, Any]) -> None:
    """Display metrics in a formatted table.

    Args:
        metrics: Performance metrics dictionary
    """
    click.echo("\n📊 Performance Summary")
    click.echo("=" * 50)

    # Basic metrics
    click.echo(f"{'Total Recipes Processed:':<25} {metrics['total_processed']:>15, }")
    click.echo(f"{'Total Batches:':<25} {metrics['total_batches']:>15, }")
    click.echo(f"{'Success Rate:':<25} {metrics['success_rate']:>14.1%}")

    # Timing metrics
    click.echo("\n⏱️  Timing Metrics")
    click.echo("-" * 30)
    click.echo(f"{'Avg Processing Time:':<25} {format_duration(metrics['average_processing_time']):>15}")
    click.echo(f"{'Avg Batch Time:':<25} {format_duration(metrics['average_batch_time']):>15}")

    # Cache and method metrics
    if metrics['total_processed'] > 0:
        cache_rate = metrics['total_cache_hits'] / metrics['total_processed']
        click.echo(f"{'Cache Hit Rate:':<25} {cache_rate:>14.1%}")
    else:
        click.echo(f"{'Cache Hit Rate:':<25} {'N / A':>15}")

    # Processing method breakdown
    click.echo("\n🔧 Processing Methods")
    click.echo("-" * 30)
    click.echo(f"{'LLM Extractions:':<25} {metrics['total_llm_extractions']:>15, }")
    click.echo(f"{'Rule - based Extractions:':<25} {metrics['total_rule_based_extractions']:>15, }")

    total_extractions = metrics['total_llm_extractions'] + metrics['total_rule_based_extractions']
    if total_extractions > 0:
        llm_percentage = (metrics['total_llm_extractions'] / total_extractions) * 100
        rule_percentage = (metrics['total_rule_based_extractions'] / total_extractions) * 100
        click.echo(f"{'LLM Usage:':<25} {llm_percentage:>14.1f}%")
        click.echo(f"{'Rule - based Usage:':<25} {rule_percentage:>14.1f}%")

def display_detailed_metrics() -> None:
    """Display detailed per - recipe metrics."""
    click.echo("\n📋 Detailed Recipe Metrics")
    click.echo("=" * 60)

    for recipe_id, recipe_metrics in performance_monitor._metrics.items():
        click.echo(f"\n🍳 Recipe: {recipe_id}")
        click.echo("-" * 40)

        for i, metric in enumerate(recipe_metrics, 1):
            click.echo(f"  Processing #{i}:")
            click.echo(f"    Method: {metric.method}")
            click.echo(f"    Duration: {format_duration(metric.duration)}")
            click.echo(f"    Cache Hit: {'✅' if metric.cache_hit else '❌'}")
            click.echo(f"    Success: {'✅' if metric.success else '❌'}")
            if metric.error:
                click.echo(f"    Error: {metric.error}")
            click.echo()

def display_batch_metrics() -> None:
    """Display batch processing metrics."""
    if not performance_monitor._batch_metrics:
        click.echo("\n⚠️  No batch metrics available")
        return

    click.echo("\n📦 Batch Processing Metrics")
    click.echo("=" * 50)

    for batch_id, batches in performance_monitor._batch_metrics.items():
        for i, batch in enumerate(batches, 1):
            click.echo(f"\n📊 Batch {batch_id}-{i}")
            click.echo("-" * 30)
            click.echo(f"Total Recipes: {batch.total_recipes}")
            click.echo(f"Successful: {batch.successful_recipes}")
            click.echo(f"Failed: {batch.failed_recipes}")
            click.echo(f"Duration: {format_duration(batch.duration)}")
            click.echo(f"Avg per Recipe: {format_duration(batch.average_duration)}")
            click.echo(f"Cache Hit Rate: {batch.cache_hit_rate:.1%}")
            click.echo(f"Success Rate: {batch.success_rate:.1%}")

@click.command()
@click.option('--detailed', is_flag = True, help='Show detailed metrics for each recipe')
@click.option('--batch', is_flag = True, help='Show batch processing metrics')
@click.option('--export', type = click.Path(), help='Export metrics to JSON file')
@click.option('--clear', is_flag = True, help='Clear all metrics data')

def performance(detailed: bool, batch: bool, export: str, clear: bool):
    """View and manage performance metrics for recipe processing.

    This command provides comprehensive performance analysis including:
    - Overall processing statistics
    - Cache performance metrics
    - Processing method breakdown (LLM vs rule - based)
    - Detailed per - recipe analysis (with --detailed)
    - Batch processing metrics (with --batch)
    """
    try:
        if clear:
            # Clear metrics
            performance_monitor._metrics.clear()
            performance_monitor._batch_metrics.clear()
            click.echo("✅ Performance metrics cleared")
            return

        metrics = performance_monitor.get_metrics_summary()

        if metrics['total_processed'] == 0:
            click.echo("⚠️  No performance data available")
            click.echo("   Run some recipe processing operations to generate metrics")
            return

        # Display main metrics
        display_metrics_table(metrics)

        # Display detailed metrics if requested
        if detailed:
            display_detailed_metrics()

        # Display batch metrics if requested
        if batch:
            display_batch_metrics()

        # Export metrics if requested
        if export:
            import json
            export_data = {
                "timestamp": datetime.now().isoformat(), 
                "summary": metrics, 
                "detailed_metrics": {
                    recipe_id: [
                        {
                            "method": m.method, 
                            "duration": m.duration, 
                            "cache_hit": m.cache_hit, 
                            "success": m.success, 
                            "error": m.error
                        }
                        for m in recipe_metrics
                    ]
                    for recipe_id, recipe_metrics in performance_monitor._metrics.items()
                }
            }

            with open(export, 'w') as f:
                json.dump(export_data, f, indent = 2)
            click.echo(f"\n💾 Metrics exported to {export}")

        click.echo("\n" + "=" * 50)

    except Exception as e:
        logger.error(f"Error retrieving performance metrics: {e}")
        click.echo(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    performance()
