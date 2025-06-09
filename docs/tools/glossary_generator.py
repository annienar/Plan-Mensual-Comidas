"""
Glossary Generator

This module handles the generation and updating of the glossary
from code comments, docstrings, and existing documentation.
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Set
import logging

logger = logging.getLogger(__name__)

class GlossaryGenerator:
    """Generates and updates the glossary."""

    def __init__(self, code_dir: Path, docs_dir: Path):
        self.code_dir = code_dir
        self.docs_dir = docs_dir
        self.terms: Dict[str, str] = {}

    def extract_terms_from_code(self):
        """Extract terms from code comments and docstrings."""
        for py_file in self.code_dir.rglob("*.py"):
            with open(py_file, 'r', encoding='utf - 8') as f:
                tree = ast.parse(f.read())

            # Process docstrings
            for node in ast.walk(tree):
                if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
                    if ast.get_docstring(node):
                        self._process_docstring(ast.get_docstring(node))

    def _process_docstring(self, docstring: str):
        """Process a docstring to extract terms and definitions."""
        # Look for term definitions in docstrings
        # Format: Term: Definition
        matches = re.finditer(r'([A - Z][A - Za - z]+):\s * ([^\n]+)', docstring)
        for match in matches:
            term = match.group(1)
            definition = match.group(2).strip()
            self.terms[term] = definition

    def extract_terms_from_docs(self):
        """Extract terms from documentation files."""
        for md_file in self.docs_dir.glob("*.md"):
            with open(md_file, 'r', encoding='utf - 8') as f:
                content = f.read()

            # Look for term definitions in markdown
            # Format: **Term:** Definition
            matches = re.finditer(r'\*\*([A - Z][A - Za - z]+):\*\*\s * ([^\n]+)', content)
            for match in matches:
                term = match.group(1)
                definition = match.group(2).strip()
                self.terms[term] = definition

            # Also look for terms in code blocks
            code_blocks = re.finditer(r'```(\w+)?\n(.*?)```', content, re.DOTALL)
            for block in code_blocks:
                code = block.group(2)
                # Look for term definitions in code comments
                comment_matches = re.finditer(r'#\s * ([A - Z][A - Za - z]+):\s * ([^\n]+)', code)
                for match in comment_matches:
                    term = match.group(1)
                    definition = match.group(2).strip()
                    self.terms[term] = definition

    def generate_glossary(self) -> str:
        """Generate the complete glossary."""
        self.extract_terms_from_code()
        self.extract_terms_from_docs()

        # Sort terms alphabetically
        sorted_terms = sorted(self.terms.items())

        # Generate markdown
        glossary = ["# Glossary\n"]
        glossary.append("This glossary contains terms used throughout the codebase and documentation.\n")

        for term, definition in sorted_terms:
            glossary.append(f"**{term}:** {definition}\n")

        return '\n'.join(glossary)

    def update_glossary(self, output_file: Path):
        """Update the glossary file."""
        content = self.generate_glossary()
        with open(output_file, 'w', encoding='utf - 8') as f:
            f.write(content)

        logger.info(f"Updated glossary with {len(self.terms)} terms")
