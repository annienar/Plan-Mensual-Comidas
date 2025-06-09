#!/usr/bin/env python3
"""
Real-time performance monitoring script for Plan Mensual Comidas.

This script continuously monitors system performance, tracks bottlenecks,
and provides actionable optimization recommendations for the recipe processing system.
"""

import asyncio
import json
import sys
import time
import psutil
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import click

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from core.utils.performance import performance_monitor
from core.utils.logger import get_logger
from core.infrastructure.llm.cache import SmartLLMCache

logger = get_logger(__name__)

@dataclass
class SystemMetrics:
    """System performance metrics."""
    timestamp: float
    cpu_usage: float
    memory_usage: float
    memory_available_mb: float
    disk_usage: float
    network_io: Dict[str, int]
    ollama_process_stats: Optional[Dict[str, Any]] = None

@dataclass
class PerformanceReport:
    """Comprehensive performance report."""
    timestamp: str
    system_metrics: SystemMetrics
    llm_performance: Dict[str, Any]
    cache_performance: Dict[str, Any]
    bottlenecks: List[str]
    recommendations: List[str]
    overall_health: str

class PerformanceMonitor:
    """Real-time performance monitoring system."""

    def __init__(self, monitoring_interval: int = 10):
        """Initialize the performance monitor.
        
        Args:
            monitoring_interval: Monitoring interval in seconds
        """
        self.monitoring_interval = monitoring_interval
        self.metrics_history: List[SystemMetrics] = []
        self.max_history = 100  # Keep last 100 metrics
        self.cache = SmartLLMCache()
        
        # Performance thresholds
        self.thresholds = {
            "cpu_usage_critical": 85.0,
            "cpu_usage_warning": 70.0,
            "memory_usage_critical": 85.0,
            "memory_usage_warning": 70.0,
            "disk_usage_critical": 90.0,
            "disk_usage_warning": 80.0,
            "response_time_critical": 45.0,
            "response_time_warning": 30.0,
            "cache_hit_rate_warning": 0.4
        }

    def get_system_metrics(self) -> SystemMetrics:
        """Collect current system metrics."""
        # Basic system stats
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Network I/O
        net_io = psutil.net_io_counters()
        network_io = {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv
        }
        
        # Try to find Ollama process
        ollama_stats = None
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                if 'ollama' in proc.info['name'].lower():
                    ollama_stats = {
                        "pid": proc.info['pid'],
                        "cpu_percent": proc.info['cpu_percent'],
                        "memory_mb": proc.info['memory_info'].rss / 1024 / 1024
                    }
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

        return SystemMetrics(
            timestamp=time.time(),
            cpu_usage=cpu_usage,
            memory_usage=memory.percent,
            memory_available_mb=memory.available / 1024 / 1024,
            disk_usage=disk.percent,
            network_io=network_io,
            ollama_process_stats=ollama_stats
        )

    def analyze_bottlenecks(self, metrics: SystemMetrics) -> List[str]:
        """Analyze system metrics to identify bottlenecks."""
        bottlenecks = []
        
        if metrics.cpu_usage > self.thresholds["cpu_usage_critical"]:
            bottlenecks.append(f"🚨 CRITICAL: CPU usage at {metrics.cpu_usage:.1f}%")
        elif metrics.cpu_usage > self.thresholds["cpu_usage_warning"]:
            bottlenecks.append(f"⚠️ WARNING: High CPU usage at {metrics.cpu_usage:.1f}%")
            
        if metrics.memory_usage > self.thresholds["memory_usage_critical"]:
            bottlenecks.append(f"🚨 CRITICAL: Memory usage at {metrics.memory_usage:.1f}%")
        elif metrics.memory_usage > self.thresholds["memory_usage_warning"]:
            bottlenecks.append(f"⚠️ WARNING: High memory usage at {metrics.memory_usage:.1f}%")
            
        if metrics.disk_usage > self.thresholds["disk_usage_critical"]:
            bottlenecks.append(f"🚨 CRITICAL: Disk usage at {metrics.disk_usage:.1f}%")
        elif metrics.disk_usage > self.thresholds["disk_usage_warning"]:
            bottlenecks.append(f"⚠️ WARNING: High disk usage at {metrics.disk_usage:.1f}%")

        if metrics.ollama_process_stats:
            ollama_memory = metrics.ollama_process_stats.get("memory_mb", 0)
            if ollama_memory > 2000:  # 2GB
                bottlenecks.append(f"🚨 Ollama using {ollama_memory:.0f}MB memory")
        else:
            bottlenecks.append("⚠️ Ollama process not found - check if it's running")

        return bottlenecks

    def generate_recommendations(
        self, 
        bottlenecks: List[str], 
        cache_stats: Dict[str, Any]
    ) -> List[str]:
        """Generate performance optimization recommendations."""
        recommendations = []
        
        # CPU optimization
        if any("CPU" in b for b in bottlenecks):
            recommendations.extend([
                "🔧 Reduce LLM concurrent requests to 2",
                "🔧 Lower Phi model threading to 2",
                "🔧 Enable aggressive caching",
                "🔧 Consider using smaller model context window"
            ])
        
        # Memory optimization
        if any("Memory" in b for b in bottlenecks):
            recommendations.extend([
                "🔧 Reduce cache size to 2000 entries",
                "🔧 Lower cache TTL to 2 hours",
                "🔧 Enable aggressive cache eviction",
                "🔧 Restart Ollama to clear memory leaks"
            ])
        
        # Cache optimization
        cache_hit_rate = cache_stats.get("hit_rate", 0)
        if cache_hit_rate < self.thresholds["cache_hit_rate_warning"]:
            recommendations.extend([
                f"📈 Cache hit rate low ({cache_hit_rate:.1%}) - extend TTL",
                "📈 Implement cache warming for common patterns",
                "📈 Review cache key generation strategy"
            ])
        
        # Ollama optimization
        if any("Ollama" in b for b in bottlenecks):
            recommendations.extend([
                "🦙 Restart Ollama service",
                "🦙 Check Ollama logs for errors",
                "🦙 Verify Phi model is properly loaded",
                "🦙 Consider Ollama memory optimization flags"
            ])
        
        # No issues found
        if not bottlenecks:
            recommendations.append("✅ System performance is optimal")
        
        return recommendations

    def get_overall_health(self, bottlenecks: List[str]) -> str:
        """Determine overall system health."""
        if any("CRITICAL" in b for b in bottlenecks):
            return "🚨 CRITICAL"
        elif any("WARNING" in b for b in bottlenecks):
            return "⚠️ WARNING"
        elif bottlenecks:
            return "📊 MONITORING"
        else:
            return "✅ HEALTHY"

    async def generate_report(self) -> PerformanceReport:
        """Generate comprehensive performance report."""
        # Collect metrics
        system_metrics = self.get_system_metrics()
        
        # Get LLM performance stats
        llm_stats = performance_monitor.get_metrics_summary()
        
        # Get cache performance
        cache_stats = self.cache.get_stats()
        
        # Analyze bottlenecks
        bottlenecks = self.analyze_bottlenecks(system_metrics)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(bottlenecks, cache_stats)
        
        # Determine overall health
        health = self.get_overall_health(bottlenecks)
        
        return PerformanceReport(
            timestamp=datetime.now().isoformat(),
            system_metrics=system_metrics,
            llm_performance=llm_stats,
            cache_performance=cache_stats,
            bottlenecks=bottlenecks,
            recommendations=recommendations,
            overall_health=health
        )

    def print_dashboard(self, report: PerformanceReport):
        """Print performance dashboard to console."""
        click.clear()
        
        # Header
        click.echo("🚀 Plan Mensual Comidas - Performance Monitor")
        click.echo("=" * 60)
        click.echo(f"📅 {report.timestamp}")
        click.echo(f"🏥 Health: {report.overall_health}")
        click.echo()
        
        # System Metrics
        metrics = report.system_metrics
        click.echo("💻 System Resources:")
        click.echo(f"  CPU Usage:    {metrics.cpu_usage:>6.1f}%")
        click.echo(f"  Memory Usage: {metrics.memory_usage:>6.1f}% ({metrics.memory_available_mb:,.0f} MB available)")
        click.echo(f"  Disk Usage:   {metrics.disk_usage:>6.1f}%")
        
        if metrics.ollama_process_stats:
            ollama = metrics.ollama_process_stats
            click.echo(f"  Ollama:       {ollama['memory_mb']:>6.0f} MB (PID: {ollama['pid']})")
        click.echo()
        
        # LLM Performance
        llm = report.llm_performance
        click.echo("🤖 LLM Performance:")
        click.echo(f"  Total Processed:   {llm.get('total_processed', 0):>8,}")
        click.echo(f"  Avg Process Time:  {llm.get('average_processing_time', 0):>8.2f}s")
        click.echo(f"  Success Rate:      {llm.get('success_rate', 0):>8.1%}")
        click.echo(f"  Cache Hits:        {llm.get('total_cache_hits', 0):>8,}")
        click.echo()
        
        # Cache Performance
        cache = report.cache_performance
        click.echo("💾 Cache Performance:")
        click.echo(f"  Hit Rate:      {cache.get('hit_rate', 0):>8.1%}")
        click.echo(f"  Entries:       {cache.get('size', 0):>8,}/{cache.get('max_size', 0):,}")
        click.echo(f"  Memory Usage:  {cache.get('memory_usage_mb', 0):>8.1f} MB")
        click.echo(f"  Evictions:     {cache.get('evictions', 0):>8,}")
        click.echo()
        
        # Bottlenecks
        if report.bottlenecks:
            click.echo("🚨 Issues Detected:")
            for bottleneck in report.bottlenecks:
                click.echo(f"  {bottleneck}")
            click.echo()
        
        # Recommendations
        if report.recommendations:
            click.echo("💡 Recommendations:")
            for rec in report.recommendations[:5]:  # Show top 5
                click.echo(f"  {rec}")
            if len(report.recommendations) > 5:
                click.echo(f"  ... and {len(report.recommendations) - 5} more")
            click.echo()
        
        click.echo("Press Ctrl+C to stop monitoring")

    async def run_continuous_monitoring(self):
        """Run continuous performance monitoring."""
        click.echo("🚀 Starting Performance Monitor...")
        click.echo(f"📊 Monitoring interval: {self.monitoring_interval} seconds")
        click.echo()
        
        try:
            while True:
                report = await self.generate_report()
                self.print_dashboard(report)
                
                # Store metrics for trending
                self.metrics_history.append(report.system_metrics)
                if len(self.metrics_history) > self.max_history:
                    self.metrics_history.pop(0)
                
                await asyncio.sleep(self.monitoring_interval)
                
        except KeyboardInterrupt:
            click.echo("\n👋 Monitoring stopped by user")
        except Exception as e:
            click.echo(f"\n❌ Error during monitoring: {e}")
            logger.error(f"Monitoring error: {e}")

    def export_report(self, report: PerformanceReport, filepath: str):
        """Export performance report to file."""
        report_dict = asdict(report)
        
        with open(filepath, 'w') as f:
            json.dump(report_dict, f, indent=2, default=str)
        
        click.echo(f"📄 Report exported to: {filepath}")

@click.command()
@click.option('--interval', '-i', default=10, help='Monitoring interval in seconds')
@click.option('--export', '-e', help='Export single report to file and exit')
@click.option('--continuous', '-c', is_flag=True, default=True, help='Run continuous monitoring')
@click.option('--dashboard', '-d', is_flag=True, help='Show performance dashboard')
async def main(interval: int, export: str, continuous: bool, dashboard: bool):
    """Performance monitoring tool for Plan Mensual Comidas."""
    
    monitor = PerformanceMonitor(monitoring_interval=interval)
    
    if export:
        # Generate single report and export
        report = await monitor.generate_report()
        monitor.export_report(report, export)
        return
    
    if dashboard or continuous:
        # Run continuous monitoring with dashboard
        await monitor.run_continuous_monitoring()
    else:
        # Generate single report and display
        report = await monitor.generate_report()
        monitor.print_dashboard(report)

if __name__ == "__main__":
    asyncio.run(main()) 