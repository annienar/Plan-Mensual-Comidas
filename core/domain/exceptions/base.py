"""
Base domain exceptions.

This module contains the base exception classes for the domain layer.
"""

from typing import Optional

class DomainError(Exception):
    """Base exception for all domain errors."""

    def __init__(self, message: str, *args: object) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            *args: Additional arguments
        """
        self.message = message
        super().__init__(message, *args)

    def __str__(self) -> str:
        """Get string representation of the exception.

        Returns:
            str: String representation
        """
        return self.message
