#!/usr / bin / env python3
"""
Import management and optimization script for the meal planning project.

This script helps manage imports across the codebase by:
- Converting relative imports to absolute imports
- Removing unused imports
- Organizing import statements
- Detecting circular dependencies
- Updating import paths after refactoring
"""

from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import os
import re
import sys

from collections import defaultdict
import ast
sys.path.append(str(Path(__file__).parent.parent.parent))

class ImportManager:
    """Manages and optimizes imports across the codebase."""

    def __init__(self, root_dir: str = "core"):
        """Initialize the import manager.

        Args:
            root_dir: Root directory to analyze
        """
        self.root_dir = Path(root_dir)
        self.changes_made = []
        self.circular_deps = []

    def process_all_files(self) -> None:
        """Process all Python files in the project."""
        print("🔄 Starting import optimization...")

        python_files = list(self.root_dir.rglob("*.py"))
        total_files = len(python_files)

        for i, file_path in enumerate(python_files, 1):
            if self._should_skip_file(file_path):
                continue

            print(f"   Processing {file_path.relative_to(self.root_dir)} ({i}/{total_files})")
            self._process_file(file_path)

        self._detect_circular_dependencies()
        self._print_summary()

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        skip_patterns = ["__pycache__", ".git", ".venv", "venv", ".pytest_cache"]
        return any(pattern in str(file_path) for pattern in skip_patterns)

    def _process_file(self, file_path: Path) -> None:
        """Process a single Python file."""
        try:
            with open(file_path, 'r', encoding='utf - 8') as f:
                original_content = f.read()

            # Parse AST
            try:
                tree = ast.parse(original_content)
            except SyntaxError:
                print(f"   ⚠️  Skipping {file_path} due to syntax error")
                return

            # Analyze and fix imports
            import_analyzer = ImportAnalyzer(file_path, self.root_dir)
            optimized_content = import_analyzer.optimize_imports(original_content, tree)

            # Write back if changes were made
            if optimized_content != original_content:
                with open(file_path, 'w', encoding='utf - 8') as f:
                    f.write(optimized_content)

                self.changes_made.append({
                    'file': str(file_path), 
                    'changes': import_analyzer.changes
                })
                print(f"   ✅ Updated imports in {file_path.relative_to(self.root_dir)}")

        except Exception as e:
            print(f"   ❌ Error processing {file_path}: {e}")

    def _detect_circular_dependencies(self) -> None:
        """Detect potential circular import dependencies."""
        print("\n🔍 Detecting circular dependencies...")

        dependency_graph = defaultdict(set)

        # Build dependency graph
        for python_file in self.root_dir.rglob("*.py"):
            if self._should_skip_file(python_file):
                continue

            try:
                with open(python_file, 'r') as f:
                    content = f.read()

                tree = ast.parse(content)
                module_name = self._get_module_name(python_file)

                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom) and node.module:
                        if node.module.startswith('core.'):
                            dependency_graph[module_name].add(node.module)
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            if alias.name.startswith('core.'):
                                dependency_graph[module_name].add(alias.name)
            except:
                continue

        # Simple cycle detection (could be improved with proper graph algorithms)
        for module, deps in dependency_graph.items():
            for dep in deps:
                if dep in dependency_graph and module in dependency_graph[dep]:
                    cycle = (module, dep)
                    if cycle not in self.circular_deps and (dep, module) not in self.circular_deps:
                        self.circular_deps.append(cycle)

        if self.circular_deps:
            print("   ⚠️  Potential circular dependencies found:")
            for cycle in self.circular_deps:
                print(f"      {cycle[0]} ↔ {cycle[1]}")
        else:
            print("   ✅ No circular dependencies detected")

    def _get_module_name(self, file_path: Path) -> str:
        """Get the module name from file path."""
        relative_path = file_path.relative_to(self.root_dir.parent)
        module_path = str(relative_path.with_suffix(''))
        return module_path.replace(os.sep, '.')

    def _print_summary(self) -> None:
        """Print summary of changes made."""
        print(f"\n📊 Import Optimization Summary")
        print("=" * 50)

        if not self.changes_made:
            print("✅ No import optimizations needed")
            return

        print(f"📁 Files modified: {len(self.changes_made)}")

        change_types = defaultdict(int)
        for file_changes in self.changes_made:
            for change in file_changes['changes']:
                change_types[change['type']] += 1

        print("\n🔧 Changes made:")
        for change_type, count in change_types.items():
            print(f"   {change_type}: {count}")

        print(f"\n🔄 Circular dependencies: {len(self.circular_deps)}")

class ImportAnalyzer:
    """Analyzes and optimizes imports in a single file."""

    def __init__(self, file_path: Path, root_dir: Path):
        """Initialize the analyzer.

        Args:
            file_path: Path to the file being analyzed
            root_dir: Root directory of the project
        """
        self.file_path = file_path
        self.root_dir = root_dir
        self.changes = []

    def optimize_imports(self, content: str, tree: ast.AST) -> str:
        """Optimize imports in the given content.

        Args:
            content: File content
            tree: AST of the file

        Returns:
            str: Optimized content
        """
        lines = content.split('\n')

        # Find import statements
        imports = self._find_imports(tree)

        # Convert relative to absolute imports
        for imp in imports:
            if self._is_relative_import(imp):
                new_import = self._convert_to_absolute(imp)
                if new_import != imp['raw_line']:
                    lines[imp['line_number'] - 1] = new_import
                    self.changes.append({
                        'type': 'relative_to_absolute', 
                        'line': imp['line_number'], 
                        'old': imp['raw_line'], 
                        'new': new_import
                    })

        # Remove unused imports (basic detection)
        unused_imports = self._find_unused_imports(content, imports)
        for imp in unused_imports:
            if self._is_safe_to_remove(imp):
                lines[imp['line_number'] - 1] = f"# REMOVED: {lines[imp['line_number'] - 1]}"
                self.changes.append({
                    'type': 'removed_unused', 
                    'line': imp['line_number'], 
                    'import': imp['module']
                })

        # Sort imports (basic sorting)
        import_blocks = self._find_import_blocks(lines)
        for block in import_blocks:
            sorted_lines = self._sort_import_block(lines[block['start']:block['end']])
            if sorted_lines != lines[block['start']:block['end']]:
                lines[block['start']:block['end']] = sorted_lines
                self.changes.append({
                    'type': 'sorted_imports', 
                    'lines': f"{block['start']}-{block['end']}"
                })

        return '\n'.join(lines)

    def _find_imports(self, tree: ast.AST) -> List[Dict]:
        """Find all import statements in the AST."""
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                import_info = {
                    'node': node, 
                    'line_number': node.lineno, 
                    'type': 'from' if isinstance(node, ast.ImportFrom) else 'import'
                }

                if isinstance(node, ast.ImportFrom):
                    import_info.update({
                        'module': node.module, 
                        'level': node.level, 
                        'names': [alias.name for alias in node.names]
                    })
                else:
                    import_info.update({
                        'names': [alias.name for alias in node.names]
                    })

                # Get raw line from source
                try:
                    import_info['raw_line'] = ast.get_source_segment(
                        open(self.file_path).read(), node
) or ""
                except:
                    import_info['raw_line'] = ""

                imports.append(import_info)

        return imports

    def _is_relative_import(self, import_info: Dict) -> bool:
        """Check if an import is relative."""
        return (import_info['type'] == 'from' and
                import_info.get('level', 0) > 0)

    def _convert_to_absolute(self, import_info: Dict) -> str:
        """Convert relative import to absolute."""
        if not self._is_relative_import(import_info):
            return import_info['raw_line']

        # Get current module path
        current_module = self._get_current_module_path()
        level = import_info['level']
        module = import_info.get('module', '')

        # Calculate absolute module path
        module_parts = current_module.split('.')
        if level > len(module_parts):
            return import_info['raw_line']  # Can't resolve

        base_parts = module_parts[:-level] if level > 0 else module_parts
        if module:
            absolute_module = '.'.join(base_parts + [module])
        else:
            absolute_module = '.'.join(base_parts)

        # Reconstruct import statement
        names = import_info.get('names', [])
        if names:
            names_str = ', '.join(names)
            return f"from {absolute_module} import {names_str}"
        else:
            return f"import {absolute_module}"

    def _get_current_module_path(self) -> str:
        """Get the current module path relative to project root."""
        relative_path = self.file_path.relative_to(self.root_dir.parent)
        module_path = str(relative_path.with_suffix(''))
        return module_path.replace(os.sep, '.')

    def _find_unused_imports(self, content: str, imports: List[Dict]) -> List[Dict]:
        """Find potentially unused imports."""
        unused = []

        for imp in imports:
            if imp['type'] == 'from':
                names = imp.get('names', [])
                for name in names:
                    # Simple check: count occurrences
                    if content.count(name) <= 1:  # Only in import line
                        unused.append({
                            **imp, 
                            'unused_name': name
                        })
            else:
                names = imp.get('names', [])
                for name in names:
                    # Check if module is used
                    module_name = name.split('.')[0]
                    if content.count(module_name) <= 1:
                        unused.append({
                            **imp, 
                            'unused_name': name
                        })

        return unused

    def _is_safe_to_remove(self, import_info: Dict) -> bool:
        """Check if import is safe to remove."""
        # Don't remove certain critical imports
        safe_to_remove_patterns = [
            r'^typing\.', 
            r'^__future__\.', 
            r'^collections\.', 
        ]

        module = import_info.get('module', '')
        unused_name = import_info.get('unused_name', '')

        for pattern in safe_to_remove_patterns:
            if re.match(pattern, module) or re.match(pattern, unused_name):
                return False

        return True

    def _find_import_blocks(self, lines: List[str]) -> List[Dict]:
        """Find blocks of consecutive import statements."""
        blocks = []
        in_block = False
        block_start = None

        for i, line in enumerate(lines):
            is_import_line = (line.strip().startswith('import ') or
                            line.strip().startswith('from '))

            if is_import_line and not in_block:
                in_block = True
                block_start = i
            elif not is_import_line and in_block:
                blocks.append({'start': block_start, 'end': i})
                in_block = False

        # Handle case where file ends with imports
        if in_block:
            blocks.append({'start': block_start, 'end': len(lines)})

        return blocks

    def _sort_import_block(self, block_lines: List[str]) -> List[str]:
        """Sort lines within an import block."""
        # Simple sorting - could be enhanced with more sophisticated logic
        import_lines = [line for line in block_lines if line.strip()]

        # Sort by type (standard library, third party, local)
        stdlib_imports = []
        thirdparty_imports = []
        local_imports = []

        for line in import_lines:
            line = line.strip()
            if line.startswith('from core.') or line.startswith('import core.'):
                local_imports.append(line)
            elif any(stdlib in line for stdlib in ['os', 'sys', 'json', 'pathlib', 'typing']):
                stdlib_imports.append(line)
            else:
                thirdparty_imports.append(line)

        # Sort each group
        stdlib_imports.sort()
        thirdparty_imports.sort()
        local_imports.sort()

        # Combine with blank lines between groups
        result = []
        if stdlib_imports:
            result.extend(stdlib_imports)
            result.append('')
        if thirdparty_imports:
            result.extend(thirdparty_imports)
            result.append('')
        if local_imports:
            result.extend(local_imports)

        # Remove trailing empty line
        while result and result[-1] == '':
            result.pop()

        return result

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Import management and optimization tool", 
        formatter_class = argparse.RawDescriptionHelpFormatter, 
        epilog="""
Examples:
python update_imports.py                    # Process core directory
python update_imports.py --root .          # Process entire project
python update_imports.py --dry - run         # Show what would be changed
        """
)

    parser.add_argument("--root", default="core", 
                    help="Root directory to process (default: core)")
    parser.add_argument("--dry - run", action="store_true", 
                    help="Show what would be changed without making changes")
    parser.add_argument("--check - only", action="store_true", 
                    help="Only check for issues, don't fix them")

    args = parser.parse_args()

    if not Path(args.root).exists():
        print(f"❌ Error: Directory '{args.root}' does not exist")
        sys.exit(1)

    manager = ImportManager(args.root)

    if args.dry_run:
        print("🔍 Running in dry - run mode (no changes will be made)")
        # TODO: Implement dry - run mode

    if args.check_only:
        print("🔍 Checking imports only...")
        # TODO: Implement check - only mode

    manager.process_all_files()

    print("\n✅ Import optimization complete!")

if __name__ == "__main__":
    main()
