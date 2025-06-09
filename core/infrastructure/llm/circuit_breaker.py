"""
Circuit breaker implementation for LLM client.
"""

from core.utils.logger import get_logger, log_performance
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from collections import deque
from dataclasses import dataclass, field
from enum import Enum
import time
logger = get_logger(__name__)

class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "CLOSED"  # Normal operation
    OPEN = "OPEN"      # Failing, rejecting requests
    HALF_OPEN = "HALF_OPEN"  # Testing if service is back

@dataclass

class CircuitBreakerMetrics:
    """Metrics for circuit breaker state changes and performance."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    state_changes: Dict[CircuitState, int] = field(default_factory = lambda: {s: 0 for s in CircuitState})
    last_state_change: Optional[datetime] = None
    failure_timestamps: deque = field(default_factory = lambda: deque(maxlen = 100))
    success_timestamps: deque = field(default_factory = lambda: deque(maxlen = 100))
    total_time_open: timedelta = timedelta()
    total_time_half_open: timedelta = timedelta()
    last_open_time: Optional[datetime] = None
    last_half_open_time: Optional[datetime] = None

    def record_state_change(self, new_state: CircuitState) -> None:
        """Record a state change and update metrics."""
        now = datetime.now()
        self.state_changes[new_state] = self.state_changes.get(new_state, 0) + 1
        self.last_state_change = now

        if new_state == CircuitState.OPEN:
            self.last_open_time = now
        elif new_state == CircuitState.HALF_OPEN:
            self.last_half_open_time = now
        elif new_state == CircuitState.CLOSED:
            if self.last_open_time:
                self.total_time_open += now - self.last_open_time
            if self.last_half_open_time:
                self.total_time_half_open += now - self.last_half_open_time

    def get_stats(self) -> Dict[str, Any]:
        """Get a summary of the circuit breaker metrics."""
        return {
            "total_requests": self.total_requests, 
            "success_rate": self.successful_requests / self.total_requests if self.total_requests > 0 else 0, 
            "failure_rate": self.failed_requests / self.total_requests if self.total_requests > 0 else 0, 
            "state_changes": {state.value: count for state, count in self.state_changes.items()}, 
            "total_time_open_seconds": self.total_time_open.total_seconds(), 
            "total_time_half_open_seconds": self.total_time_half_open.total_seconds(), 
            "last_state_change": self.last_state_change.isoformat() if self.last_state_change else None, 
            "recent_failures": len(self.failure_timestamps), 
            "recent_successes": len(self.success_timestamps)
        }

class CircuitBreaker:
    """Circuit breaker for protecting LLM service from cascading failures."""

    def __init__(
        self, 
        failure_threshold: int = 5, 
        recovery_timeout: int = 60, 
        half_open_max_requests: int = 3
):
        """Initialize the circuit breaker.

        Args:
            failure_threshold: Number of consecutive failures before opening circuit
            recovery_timeout: Time in seconds to wait before attempting recovery
            half_open_max_requests: Maximum number of requests to allow in half - open state
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_requests = half_open_max_requests

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.half_open_requests = 0
        self.metrics = CircuitBreakerMetrics()

    def can_execute(self) -> bool:
        """Check if a request can be executed.

        Returns:
            bool: True if request can be executed, False otherwise
        """
        now = time.time()

        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            if self.last_failure_time and now - self.last_failure_time >= self.recovery_timeout:
                self._transition_to_half_open()
                return True
            return False

        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_requests < self.half_open_max_requests:
                self.half_open_requests += 1
                return True
            return False

        return False

    def on_success(self) -> None:
        """Record a successful request."""
        self.metrics.total_requests += 1
        self.metrics.successful_requests += 1
        self.metrics.success_timestamps.append(datetime.now())

        if self.state == CircuitState.HALF_OPEN:
            self._transition_to_closed()
        else:
            self.failure_count = 0

    def on_failure(self) -> None:
        """Record a failed request."""
        self.metrics.total_requests += 1
        self.metrics.failed_requests += 1
        self.metrics.failure_timestamps.append(datetime.now())

        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
            self._transition_to_open()
        elif self.state == CircuitState.HALF_OPEN:
            self._transition_to_open()

    def _transition_to_open(self) -> None:
        """Transition to open state."""
        if self.state != CircuitState.OPEN:
            self.state = CircuitState.OPEN
            self.half_open_requests = 0
            self.metrics.record_state_change(CircuitState.OPEN)

    def _transition_to_half_open(self) -> None:
        """Transition to half - open state."""
        if self.state != CircuitState.HALF_OPEN:
            self.state = CircuitState.HALF_OPEN
            self.half_open_requests = 0
            self.metrics.record_state_change(CircuitState.HALF_OPEN)

    def _transition_to_closed(self) -> None:
        """Transition to closed state."""
        if self.state != CircuitState.CLOSED:
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            self.half_open_requests = 0
            self.metrics.record_state_change(CircuitState.CLOSED)

    def get_stats(self) -> Dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dict[str, Any]: Circuit breaker statistics
        """
        stats = self.metrics.get_stats()
        stats.update({
            "current_state": self.state.value, 
            "failure_count": self.failure_count, 
            "half_open_requests": self.half_open_requests, 
            "last_failure_time": datetime.fromtimestamp(self.last_failure_time).isoformat() if self.last_failure_time else None
        })
        return stats

    def reset(self) -> None:
        """Reset the circuit breaker to initial state."""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.half_open_requests = 0
        self.metrics = CircuitBreakerMetrics()

    def get_metrics(self) -> dict:
        """Get current circuit breaker metrics.

        Returns:
            dict: Current metrics summary
        """
        return self.metrics.get_stats()
