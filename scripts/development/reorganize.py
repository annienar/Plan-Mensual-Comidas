#!/usr / bin / env python3
"""
Script to reorganize the project directory structure according to the new architecture.
"""

from pathlib import Path
import os

import shutil

def create_directory(path):
    """Create directory if it doesn't exist."""
    Path(path).mkdir(parents = True, exist_ok = True)

def move_directory(src, dst):
    """Move directory if it exists."""
    if os.path.exists(src):
        shutil.move(src, dst)

def main():
    # Create new directory structure
    directories = [
        "data / recipes", 
        "data / config", 
        "data / templates", 
        "var / logs", 
        "var / cache", 
        "var / test - results", 
    ]

    for directory in directories:
        create_directory(directory)

    # Move directories to their new locations
    moves = [
        ("recetas", "data / recipes"), 
        ("static", "data / static"), 
        ("templates", "data / templates"), 
        (".test_results", "var / test - results"), 
        (".log", "var / logs"), 
    ]

    for src, dst in moves:
        move_directory(src, dst)

    # Move core / cli.py to commands/
    if os.path.exists("core / cli.py"):
        create_directory("commands")
        shutil.move("core / cli.py", "commands / cli.py")

    # Consolidate recipe directories
    if os.path.exists("core / recipe"):
        if not os.path.exists("core / domain / recipe"):
            create_directory("core / domain / recipe")
        # Move contents of core / recipe to core / domain / recipe
        for item in os.listdir("core / recipe"):
            src = os.path.join("core / recipe", item)
            dst = os.path.join("core / domain / recipe", item)
            if os.path.exists(dst):
                shutil.rmtree(dst) if os.path.isdir(dst) else os.remove(dst)
            shutil.move(src, dst)
        # Remove old recipe directory
        shutil.rmtree("core / recipe")

if __name__ == "__main__":
    main()
