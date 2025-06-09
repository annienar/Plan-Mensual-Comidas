"""
Event dispatcher module.

This module contains the event dispatcher.
"""

from typing import Dict, List, Type, Any, Callable, Awaitable
from .base import DomainEvent

EventHandler = Callable[[DomainEvent], Awaitable[None]]

class EventDispatcher:
    """Event dispatcher.

    This class handles dispatching events to registered handlers.
    """

    def __init__(self):
        """Initialize the dispatcher."""
        self._handlers: Dict[Type[DomainEvent], List[EventHandler]] = {}

    def register(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """Register an event handler.

        Args:
            event_type: Type of event to handle
            handler: Event handler function
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []

        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)

    def unregister(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """Unregister an event handler.

        Args:
            event_type: Type of event
            handler: Event handler function to unregister
        """
        if event_type in self._handlers:
            self._handlers[event_type] = [
                h for h in self._handlers[event_type]
                if h != handler
            ]

    async def dispatch(self, event: DomainEvent) -> None:
        """Dispatch an event to registered handlers.

        Args:
            event: Event to dispatch
        """
        handlers = self._handlers.get(type(event), [])

        for handler in handlers:
            try:
                await handler(event)
            except Exception as e:
                # Log error but continue with other handlers
                print(f"Error handling event {event}: {e}")

    def clear(self) -> None:
        """Clear all registered handlers."""
        self._handlers.clear()
