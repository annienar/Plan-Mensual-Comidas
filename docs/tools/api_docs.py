"""
API Documentation Generator

This module handles the generation of API documentation from code, 
including Notion API integration details and property mappings.
"""

from pathlib import Path
from typing import Dict, List, Optional
import json

import ast
import logging
logger = logging.getLogger(__name__)

class APIDocGenerator:
    """Generates API documentation from code."""

    def __init__(self, code_dir: Path):
        self.code_dir = code_dir
        self.notion_properties = {}
        self.api_endpoints = []

    def extract_notion_properties(self):
        """Extract Notion property mappings from code."""
        for py_file in self.code_dir.rglob("*.py"):
            with open(py_file, 'r', encoding='utf - 8') as f:
                tree = ast.parse(f.read())

            # Find property mappings
            for node in ast.walk(tree):
                if isinstance(node, ast.Dict):
                    # Look for property mapping dictionaries
                    if any(isinstance(k, ast.Constant) and isinstance(k.value, str)
                        and k.value in ["Nombre", "Porciones", "Calorías"]
                        for k in node.keys):
                        self.notion_properties[py_file.name] = self._extract_dict(node)

    def _extract_dict(self, node: ast.Dict) -> Dict:
        """Extract dictionary from AST node."""
        result = {}
        for key, value in zip(node.keys, node.values):
            if isinstance(key, ast.Constant):
                result[key.value] = self._extract_value(value)
        return result

    def _extract_value(self, node: ast.AST) -> any:
        """Extract value from AST node."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Dict):
            return self._extract_dict(node)
        elif isinstance(node, ast.List):
            return [self._extract_value(item) for item in node.elts]
        return None

    def extract_api_endpoints(self):
        """Extract API endpoints from code."""
        for py_file in self.code_dir.rglob("*.py"):
            with open(py_file, 'r', encoding='utf - 8') as f:
                tree = ast.parse(f.read())

            # Find API endpoint definitions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Look for functions that might be API endpoints
                    if any(decorator.id == 'app.route' for decorator in node.decorator_list
                        if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute)):
                        self.api_endpoints.append({
                            'file': py_file.name, 
                            'name': node.name, 
                            'docstring': ast.get_docstring(node)
                        })

    def generate_api_docs(self) -> str:
        """Generate API documentation."""
        self.extract_notion_properties()
        self.extract_api_endpoints()

        docs = []
        docs.append("# API Documentation\n")

        # Add Notion API section
        docs.append("## Notion API Integration\n")

        docs.append("### Property Mappings\n")
        for file_name, props in self.notion_properties.items():
            docs.append(f"#### {file_name}\n")
            docs.append("```json")
            docs.append(json.dumps(props, indent = 2))
            docs.append("```\n")

        # Add API endpoints section
        docs.append("### API Endpoints\n")
        for endpoint in self.api_endpoints:
            docs.append(f"#### {endpoint['name']}\n")
            if endpoint['docstring']:
                docs.append(f"{endpoint['docstring']}\n")
            docs.append(f"File: {endpoint['file']}\n")

        # Add example usage
        docs.append("### Example Usage\n")
        docs.append("```python")
        docs.append("from notion_client import Client")
        docs.append("")
        docs.append("notion = Client(auth = os.environ['NOTION_TOKEN'])")
        docs.append("")
        docs.append("# Create a page")
        docs.append("notion.pages.create(...)")
        docs.append("")
        docs.append("# Update a page")
        docs.append("notion.pages.update(...)")
        docs.append("```\n")

        return '\n'.join(docs)
