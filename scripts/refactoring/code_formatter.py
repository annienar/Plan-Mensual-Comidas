#!/usr/bin/env python3
"""
Safe Code Formatter - Basic whitespace cleanup only

This formatter applies only basic, safe whitespace fixes:
- Removes trailing whitespace
- Ensures files end with newline
- Validates syntax before applying changes
"""

import argparse
import ast
import sys
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass, field

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))


@dataclass
class FixResult:
    """Result of a code fix operation."""

    file_path: str
    fixes_applied: List[str] = field(default_factory=list)
    success: bool = True
    error_message: Optional[str] = None


class FixedCodeFormatter:
    """Improved code formatter that properly handles multi-line imports."""

    def __init__(self, root_dir: str = "core"):
        """Initialize the formatter."""
        self.root_dir = Path(root_dir)
        self.total_files = 0
        self.files_modified = 0
        self.total_fixes = 0

    def format_all_files(self, check_only: bool = False) -> None:
        """Format all Python files in the project."""
        print("🔧 Starting SAFE code formatting...")
        if check_only:
            print("   Running in CHECK-ONLY mode")

        python_files = list(self.root_dir.rglob("*.py"))
        self.total_files = len(python_files)

        for i, file_path in enumerate(python_files, 1):
            if self._should_skip_file(file_path):
                continue

            print(
                f"   Processing {file_path.relative_to(self.root_dir)} ({i}/{len(python_files)})"
            )

            result = self._format_file(file_path, check_only)
            if result.fixes_applied:
                self.files_modified += 1
                self.total_fixes += len(result.fixes_applied)

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        skip_patterns = ["__pycache__", ".git", ".venv", "venv"]
        return any(pattern in str(file_path) for pattern in skip_patterns)

    def _format_file(self, file_path: Path, check_only: bool) -> FixResult:
        """Format a single Python file safely."""
        result = FixResult(file_path=str(file_path))

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_content = f.read()

            # Check syntax first
            try:
                ast.parse(original_content)
            except SyntaxError as e:
                result.success = False
                result.error_message = f"Syntax error: {e}"
                print(f"      ❌ Skipping file with syntax error")
                return result

            content = original_content

            # Only apply very safe fixes
            content, fixes = self._fix_safe_whitespace(content)
            result.fixes_applied.extend(fixes)

            if content != original_content and not check_only:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"      ✅ Applied {len(result.fixes_applied)} safe fixes")
            elif content != original_content:
                print(f"      🔍 Would apply {len(result.fixes_applied)} safe fixes")

        except Exception as e:
            result.success = False
            result.error_message = str(e)
            print(f"      ❌ Error: {e}")

        return result

    def _fix_safe_whitespace(self, content: str) -> Tuple[str, List[str]]:
        """Apply only very safe whitespace fixes."""
        fixes = []

        # Remove trailing whitespace
        lines = content.split("\n")
        cleaned_lines = []
        for line in lines:
            cleaned = line.rstrip()
            if cleaned != line:
                fixes.append("Removed trailing whitespace")
            cleaned_lines.append(cleaned)

        content = "\n".join(cleaned_lines)

        # Ensure file ends with newline
        if content and not content.endswith("\n"):
            content += "\n"
            fixes.append("Added newline at end")

        return content, fixes


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Safe code formatter")
    parser.add_argument("--root", default="core", help="Root directory")
    parser.add_argument("--check-only", action="store_true", help="Check only")

    args = parser.parse_args()

    formatter = FixedCodeFormatter(args.root)
    formatter.format_all_files(args.check_only)

    print(
        f"\n✅ Safe formatting complete! Processed {
            formatter.total_files} files"
    )
    print(
        f"   Modified {
            formatter.files_modified} files with {
            formatter.total_fixes} fixes"
    )


if __name__ == "__main__":
    main()
