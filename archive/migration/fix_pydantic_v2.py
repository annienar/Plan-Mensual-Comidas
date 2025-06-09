#!/usr/bin/env python3
"""
Script to fix Pydantic V1 to V2 migration issues.
Updates @validator to @field_validator and fixes other deprecation warnings.
"""

import os
import re
from pathlib import Path

def fix_validators_in_file(file_path: Path):
    """Fix validators in a single file."""
    print(f"Processing: {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Fix imports - add field_validator if validator is imported
    if 'from pydantic import' in content and 'validator' in content:
        # Replace validator with field_validator in imports
        content = re.sub(
            r'from pydantic import ([^,\n]*)(validator)([^,\n]*)',
            r'from pydantic import \1field_validator\3',
            content
        )
        # Also handle cases where validator is in a list
        content = re.sub(
            r'(from pydantic import[^,\n]*),(\s*)validator(\s*),',
            r'\1,\2field_validator\3,',
            content
        )
        content = re.sub(
            r'(from pydantic import[^,\n]*),(\s*)validator(\s*)$',
            r'\1,\2field_validator\3',
            content, flags=re.MULTILINE
        )
    
    # Fix @validator decorators to @field_validator
    content = re.sub(
        r'@validator\(',
        r'@field_validator(',
        content
    )
    
    # Add @classmethod decorator after @field_validator
    # Pattern: @field_validator(...)\n    def method_name(cls, ...
    content = re.sub(
        r'(@field_validator\([^)]+\))\n(\s+)def (\w+)\(cls,',
        r'\1\n\2@classmethod\n\2def \3(cls,',
        content
    )
    
    # Fix min_items to min_length
    content = re.sub(
        r'min_items\s*=',
        r'min_length=',
        content
    )
    
    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ Updated: {file_path}")
        return True
    else:
        print(f"⚪ No changes needed: {file_path}")
        return False

def main():
    """Main function to fix all Python files."""
    core_dir = Path("core")
    
    if not core_dir.exists():
        print("❌ core/ directory not found")
        return
    
    fixed_files = []
    
    # Find all Python files in core/
    for py_file in core_dir.rglob("*.py"):
        if fix_validators_in_file(py_file):
            fixed_files.append(py_file)
    
    print(f"\n✅ Fixed {len(fixed_files)} files:")
    for file_path in fixed_files:
        print(f"  - {file_path}")
    
    print("\n🧪 Testing imports...")
    try:
        import core.domain.recipe.models.ingredient
        import core.domain.recipe.models.metadata
        print("✅ Imports working!")
    except Exception as e:
        print(f"❌ Import error: {e}")

if __name__ == "__main__":
    main() 