"""
Diagram Generator

This module handles the generation of diagrams from code, 
including class hierarchies, data flows, and system architecture.
"""

from pathlib import Path
from typing import Dict, List, Set

import ast
import graphviz
import logging
logger = logging.getLogger(__name__)

class DiagramGenerator:
    """Generates diagrams from code."""

    def __init__(self, code_dir: Path):
        self.code_dir = code_dir
        self.classes: Dict[str, Set[str]] = {}
        self.relationships: List[tuple] = []

    def analyze_code(self):
        """Analyze code to extract class relationships."""
        for py_file in self.code_dir.rglob("*.py"):
            with open(py_file, 'r', encoding='utf - 8') as f:
                tree = ast.parse(f.read())

            # Find class definitions
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    self._process_class(node)

    def _process_class(self, node: ast.ClassDef):
        """Process a class definition to extract relationships."""
        class_name = node.name
        self.classes[class_name] = set()

        # Find base classes
        for base in node.bases:
            if isinstance(base, ast.Name):
                self.relationships.append((class_name, base.id, "inherits"))

        # Find class attributes and methods
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                self.classes[class_name].add(f"method: {item.name}")
            elif isinstance(item, ast.ClassDef):
                self.relationships.append((class_name, item.name, "contains"))

    def generate_class_diagram(self) -> str:
        """Generate a class diagram using Graphviz."""
        self.analyze_code()

        dot = graphviz.Digraph(comment='Class Diagram')
        dot.attr(rankdir='BT')

        # Add classes
        for class_name, members in self.classes.items():
            label = f"{class_name}\\n" + "\\n".join(members)
            dot.node(class_name, label)

        # Add relationships
        for source, target, rel_type in self.relationships:
            if rel_type == "inherits":
                dot.edge(source, target, "inherits")
            elif rel_type == "contains":
                dot.edge(source, target, "contains")

        # Save diagram
        diagram_path = Path("Documentation / generated / class_diagram")
        dot.render(diagram_path, format='png', cleanup = True)

        # Return markdown with image
        return f"# Class Diagram\n\n![Class Diagram](class_diagram.png)\n"

    def generate_flow_diagram(self) -> str:
        """Generate a flow diagram using Graphviz."""
        dot = graphviz.Digraph(comment='Flow Diagram')
        dot.attr(rankdir='TB')

        # Add nodes
        nodes = {
            'input': 'User Input', 
            'preprocess': 'Preprocessor', 
            'llm': 'LLM Manager', 
            'validate': 'Response Validator', 
            'model': 'Recipe Model', 
            'sync': 'Notion Sync', 
            'fallback': 'Fallback Manager'
        }

        for node_id, label in nodes.items():
            dot.node(node_id, label)

        # Add edges
        edges = [
            ('input', 'preprocess'), 
            ('preprocess', 'llm'), 
            ('llm', 'validate'), 
            ('validate', 'model'), 
            ('model', 'sync'), 
            ('validate', 'fallback'), 
            ('fallback', 'model')
        ]

        for source, target in edges:
            dot.edge(source, target)

        # Save diagram
        diagram_path = Path("Documentation / generated / flow_diagram")
        dot.render(diagram_path, format='png', cleanup = True)

        # Return markdown with image
        return f"# Flow Diagram\n\n![Flow Diagram](flow_diagram.png)\n"

    def generate_all_diagrams(self) -> List[str]:
        """Generate all diagrams."""
        return [
            self.generate_class_diagram(), 
            self.generate_flow_diagram()
        ]
