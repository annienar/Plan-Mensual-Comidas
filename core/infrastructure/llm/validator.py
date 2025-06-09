from core.utils.logger import get_logger
from datetime import datetime
from typing import Dict, Any, List, Optional, Union, Set
import json
import re

from .models import LLMResponse
from dataclasses import dataclass
from pydantic import BaseModel, Field
logger = get_logger(__name__)

class Ingredient(BaseModel):
    name: str
    quantity: str
    unit: str

class Recipe(BaseModel):
    title: str
    ingredients: List[Ingredient]
    steps: List[str]
    portions: str
    calories: str

def validate_recipe(data: Dict[str, Any]) -> Recipe:
    """Validate that the recipe data matches the expected schema."""
    try:
        return Recipe(**data)
    except Exception as e:
        raise ValueError(f"Invalid recipe data: {str(e)}")

def validate_ingredients(data: List[Dict[str, str]]) -> List[Ingredient]:
    """Validate that the ingredients data matches the expected schema."""
    try:
        return [Ingredient(**ing) for ing in data]
    except Exception as e:
        raise ValueError(f"Invalid ingredients data: {str(e)}")

class ValidationError(Exception):
    """Base exception for validation errors."""
    pass

class SchemaValidationError(ValidationError):
    """Exception raised when response schema is invalid."""
    pass

class ContentValidationError(ValidationError):
    """Exception raised when response content is invalid."""
    pass

class FormatValidationError(ValidationError):
    """Exception raised when response format is invalid."""
    pass

@dataclass

class ValidationResult:
    """Result of validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary.

        Returns:
            Dict[str, Any]: Validation result
        """
        return {
            "is_valid": self.is_valid, 
            "errors": self.errors, 
            "warnings": self.warnings
        }

class LLMResponseValidator:
    """Validator for LLM responses."""

    def __init__(self):
        """Initialize the validator."""
        self._required_fields: Set[str] = set()
        self._numeric_fields: Set[str] = set()
        self._array_fields: Set[str] = set()
        self._string_fields: Set[str] = set()
        self._boolean_fields: Set[str] = set()
        self._object_fields: Set[str] = set()
        self._enum_fields: Dict[str, Set[str]] = {}
        self._min_values: Dict[str, Union[int, float]] = {}
        self._max_values: Dict[str, Union[int, float]] = {}
        self._min_lengths: Dict[str, int] = {}
        self._max_lengths: Dict[str, int] = {}
        self._patterns: Dict[str, str] = {}

    def add_required_field(self, field: str) -> None:
        """Add a required field.

        Args:
            field: Field name
        """
        self._required_fields.add(field)

    def add_numeric_field(self, field: str) -> None:
        """Add a numeric field.

        Args:
            field: Field name
        """
        self._numeric_fields.add(field)

    def add_array_field(self, field: str) -> None:
        """Add an array field.

        Args:
            field: Field name
        """
        self._array_fields.add(field)

    def add_string_field(self, field: str) -> None:
        """Add a string field.

        Args:
            field: Field name
        """
        self._string_fields.add(field)

    def add_boolean_field(self, field: str) -> None:
        """Add a boolean field.

        Args:
            field: Field name
        """
        self._boolean_fields.add(field)

    def add_object_field(self, field: str) -> None:
        """Add an object field.

        Args:
            field: Field name
        """
        self._object_fields.add(field)

    def add_enum_field(self, field: str, values: Set[str]) -> None:
        """Add an enum field.

        Args:
            field: Field name
            values: Allowed values
        """
        self._enum_fields[field] = values

    def set_min_value(self, field: str, value: Union[int, float]) -> None:
        """Set minimum value for a field.

        Args:
            field: Field name
            value: Minimum value
        """
        self._min_values[field] = value

    def set_max_value(self, field: str, value: Union[int, float]) -> None:
        """Set maximum value for a field.

        Args:
            field: Field name
            value: Maximum value
        """
        self._max_values[field] = value

    def set_min_length(self, field: str, length: int) -> None:
        """Set minimum length for a field.

        Args:
            field: Field name
            length: Minimum length
        """
        self._min_lengths[field] = length

    def set_max_length(self, field: str, length: int) -> None:
        """Set maximum length for a field.

        Args:
            field: Field name
            length: Maximum length
        """
        self._max_lengths[field] = length

    def set_pattern(self, field: str, pattern: str) -> None:
        """Set regex pattern for a field.

        Args:
            field: Field name
            pattern: Regex pattern
        """
        self._patterns[field] = pattern

    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate response data.

        Args:
            data: Response data to validate

        Returns:
            ValidationResult: Validation result
        """
        errors: List[str] = []
        warnings: List[str] = []

        # Check required fields
        for field in self._required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")

        # Validate fields
        for field, value in data.items():
            # Check numeric fields
            if field in self._numeric_fields:
                if not isinstance(value, (int, float)):
                    errors.append(f"Field {field} must be numeric")
                else:
                    if field in self._min_values and value < self._min_values[field]:
                        errors.append(f"Field {field} must be >= {self._min_values[field]}")
                    if field in self._max_values and value > self._max_values[field]:
                        errors.append(f"Field {field} must be <= {self._max_values[field]}")

            # Check array fields
            if field in self._array_fields:
                if not isinstance(value, list):
                    errors.append(f"Field {field} must be an array")
                else:
                    if field in self._min_lengths and len(value) < self._min_lengths[field]:
                        errors.append(f"Field {field} must have at least {self._min_lengths[field]} items")
                    if field in self._max_lengths and len(value) > self._max_lengths[field]:
                        errors.append(f"Field {field} must have at most {self._max_lengths[field]} items")

            # Check string fields
            if field in self._string_fields:
                if not isinstance(value, str):
                    errors.append(f"Field {field} must be a string")
                else:
                    if field in self._min_lengths and len(value) < self._min_lengths[field]:
                        errors.append(f"Field {field} must have at least {self._min_lengths[field]} characters")
                    if field in self._max_lengths and len(value) > self._max_lengths[field]:
                        errors.append(f"Field {field} must have at most {self._max_lengths[field]} characters")
                    if field in self._patterns and not re.match(self._patterns[field], value):
                        errors.append(f"Field {field} must match pattern: {self._patterns[field]}")

            # Check boolean fields
            if field in self._boolean_fields and not isinstance(value, bool):
                errors.append(f"Field {field} must be a boolean")

            # Check object fields
            if field in self._object_fields and not isinstance(value, dict):
                errors.append(f"Field {field} must be an object")

            # Check enum fields
            if field in self._enum_fields and value not in self._enum_fields[field]:
                errors.append(f"Field {field} must be one of: {', '.join(self._enum_fields[field])}")

        return ValidationResult(
            is_valid = len(errors) == 0, 
            errors = errors, 
            warnings = warnings
)

    def validate_json(self, json_str: str) -> ValidationResult:
        """Validate JSON string.

        Args:
            json_str: JSON string to validate

        Returns:
            ValidationResult: Validation result
        """
        try:
            data = json.loads(json_str)
            return self.validate(data)
        except json.JSONDecodeError as e:
            return ValidationResult(
                is_valid = False, 
                errors=[f"Invalid JSON: {str(e)}"], 
                warnings=[]
)

    def validate_llm_response(self, response: LLMResponse) -> ValidationResult:
        """Validate LLM response.

        Args:
            response: LLM response to validate

        Returns:
            ValidationResult: Validation result
        """
        try:
            data = json.loads(response.text)
            return self.validate(data)
        except json.JSONDecodeError as e:
            return ValidationResult(
                is_valid = False, 
                errors=[f"Invalid JSON in response: {str(e)}"], 
                warnings=[]
)

    def clear_rules(self) -> None:
        """Clear all validation rules."""
        self._required_fields.clear()
        self._numeric_fields.clear()
        self._array_fields.clear()
        self._string_fields.clear()
        self._boolean_fields.clear()
        self._object_fields.clear()
        self._enum_fields.clear()
        self._min_values.clear()
        self._max_values.clear()
        self._min_lengths.clear()
        self._max_lengths.clear()
        self._patterns.clear()
