"""
Test Documentation Generator

This module handles the generation of test documentation
from test files and test results.
"""

import pytest
import json
from pathlib import Path
from typing import Dict, List
import logging
import subprocess
import sys

logger = logging.getLogger(__name__)

class TestDocGenerator:
    """Generates test documentation."""

    def __init__(self, code_dir: Path):
        self.code_dir = code_dir
        self.test_files = []
        self.test_results = {}

    def discover_tests(self):
        """Discover test files in the codebase."""
        for py_file in self.code_dir.rglob("test_*.py"):
            self.test_files.append(py_file)
        logger.info(f"Found {len(self.test_files)} test files")

    def run_tests(self):
        """Run tests and collect results."""
        # Run pytest with minimal output and JSON report
        cmd = [
            sys.executable, "-m", "pytest", 
            "--json - report", 
            "--json - report - file = none", 
            "--quiet"
        ]

        try:
            result = subprocess.run(cmd, capture_output = True, text = True)
            if result.returncode == 0:
                logger.info("All tests passed")
            else:
                logger.warning("Some tests failed")

            # Parse test results from output
            self._parse_test_results(result.stdout)
        except Exception as e:
            logger.error(f"Error running tests: {e}")

    def _parse_test_results(self, output: str):
        """Parse test results from pytest output."""
        try:
            # Extract JSON report from output
            json_start = output.find('{')
            json_end = output.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = output[json_start:json_end]
                self.test_results = json.loads(json_str)
        except Exception as e:
            logger.error(f"Error parsing test results: {e}")

    def generate_test_docs(self) -> str:
        """Generate test documentation."""
        self.discover_tests()
        self.run_tests()

        docs = []
        docs.append("# Test Documentation\n")

        # Add test files section
        docs.append("## Test Files\n")
        for test_file in sorted(self.test_files):
            docs.append(f"- {test_file.relative_to(self.code_dir)}\n")

        # Add test results section
        docs.append("\n## Test Results\n")
        if self.test_results:
            total = self.test_results.get('total', 0)
            passed = self.test_results.get('passed', 0)
            failed = self.test_results.get('failed', 0)
            skipped = self.test_results.get('skipped', 0)

            docs.append(f"- Total Tests: {total}\n")
            docs.append(f"- Passed: {passed}\n")
            docs.append(f"- Failed: {failed}\n")
            docs.append(f"- Skipped: {skipped}\n")

            if failed > 0:
                docs.append("\n### Failed Tests\n")
                for test in self.test_results.get('tests', []):
                    if test.get('outcome') == 'failed':
                        docs.append(f"- {test.get('nodeid')}\n")
                        docs.append(f"  Error: {test.get('call', {}).get('longrepr', '')}\n")
        else:
            docs.append("No test results available.\n")

        # Add test coverage section
        docs.append("\n## Test Coverage\n")
        docs.append("Run the following command to generate test coverage report:\n")
        docs.append("```bash\n")
        docs.append("pytest --cov = src tests/\n")
        docs.append("```\n")

        return '\n'.join(docs)

    def update_test_docs(self, output_file: Path):
        """Update the test documentation file."""
        content = self.generate_test_docs()
        with open(output_file, 'w', encoding='utf - 8') as f:
            f.write(content)

        logger.info("Updated test documentation")
