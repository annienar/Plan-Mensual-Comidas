#!/usr / bin / env python3
"""
Script management utility for the meal planning project.

This utility helps manage and run various project scripts.
"""

from pathlib import Path
from typing import Dict, List, Optional
import os
import sys

import subprocess

class ScriptManager:
    """Manages project scripts and utilities."""

    def __init__(self):
        """Initialize the script manager."""
        self.scripts_dir = Path(__file__).parent
        self.project_root = self.scripts_dir.parent

        # Define available scripts
        self.scripts = {
            'performance': {
                'path': 'scripts/performance.py',
                'description': 'Monitor recipe processing performance',
                'category': 'monitoring'
            },
            'quality': {
                'path': 'scripts/refactoring/check_code_quality.py',
                'description': 'Check code quality and standards compliance',
                'category': 'quality'
            },
            'format': {
                'path': 'scripts/refactoring/code_formatter.py',
                'description': 'Fix linter issues, whitespace, and flake8 violations',
                'category': 'quality'
            },
            'imports': {
                'path': 'scripts/development/update_imports.py',
                'description': 'Optimize and manage import statements',
                'category': 'development'
            },
            'cleanup': {
                'path': 'scripts/cleanup_logs.sh',
                'description': 'Clean up old log files and test results',
                'category': 'maintenance'
            },
            'test': {
                'path': 'scripts/run_integration_tests.sh',
                'description': 'Run integration tests',
                'category': 'testing'
            },
            'reorganize': {
                'path': 'scripts/development/reorganize.py',
                'description': 'Reorganize project directory structure',
                'category': 'development'
            }
        }

    def list_scripts(self, category: Optional[str] = None) -> None:
        """List available scripts."""
        print("📋 Available Project Scripts")
        print("=" * 50)

        categories = {}
        for name, info in self.scripts.items():
            cat = info['category']
            if category and cat != category:
                continue
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((name, info))

        for cat, scripts in sorted(categories.items()):
            print(f"\n🔧 {cat.title()}:")
            for name, info in scripts:
                status = "✅" if self._script_exists(info['path']) else "❌"
                print(f"   {status} {name:<12} - {info['description']}")

    def run_script(self, script_name: str, args: List[str] = None) -> None:
        """Run a specific script."""
        if script_name not in self.scripts:
            print(f"❌ Error: Script '{script_name}' not found")
            self.list_scripts()
            return

        script_info = self.scripts[script_name]
        script_path = self.project_root / script_info['path']

        if not self._script_exists(script_info['path']):
            print(f"❌ Error: Script file '{script_path}' not found")
            return

        print(f"🚀 Running {script_name}: {script_info['description']}")

        # Prepare command
        if script_path.suffix == '.py':
            cmd = [sys.executable, str(script_path)]
        elif script_path.suffix == '.sh':
            cmd = ['bash', str(script_path)]
        else:
            cmd = [str(script_path)]

        if args:
            cmd.extend(args)

        try:
            result = subprocess.run(cmd, cwd = self.project_root)
            if result.returncode == 0:
                print(f"✅ Script '{script_name}' completed successfully")
            else:
                print(f"❌ Script '{script_name}' failed")
        except Exception as e:
            print(f"❌ Error running script: {e}")

    def _script_exists(self, script_path: str) -> bool:
        """Check if a script file exists."""
        full_path = self.project_root / script_path
        return full_path.exists()

    def check_health(self) -> None:
        """Check the health of all scripts."""
        print("🏥 Script Health Check")
        print("=" * 30)

        total_scripts = len(self.scripts)
        available_scripts = 0

        for name, info in self.scripts.items():
            exists = self._script_exists(info['path'])
            status = "✅ Available" if exists else "❌ Missing"
            print(f"{name:<12} {status}")
            if exists:
                available_scripts += 1

        print(f"\n📊 Summary: {available_scripts}/{total_scripts} scripts available")

def main():
    """Main entry point."""
    if len(sys.argv) == 1:
        manager = ScriptManager()
        manager.list_scripts()
        print("\n💡 Usage:")
        print("  python manage_scripts.py list        # List all scripts")
        print("  python manage_scripts.py health      # Check script health")
        print("  python manage_scripts.py run <name>  # Run a script")
    elif sys.argv[1] == "list":
        manager = ScriptManager()
        category = sys.argv[2] if len(sys.argv) > 2 else None
        manager.list_scripts(category)
    elif sys.argv[1] == "health":
        manager = ScriptManager()
        manager.check_health()
    elif sys.argv[1] == "run" and len(sys.argv) > 2:
        manager = ScriptManager()
        script_name = sys.argv[2]
        args = sys.argv[3:] if len(sys.argv) > 3 else None
        manager.run_script(script_name, args)
    else:
        print("❌ Invalid command. Use 'list', 'health', or 'run <script_name>'")

if __name__ == "__main__":
    main()
