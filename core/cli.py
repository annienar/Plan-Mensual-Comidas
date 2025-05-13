"""
Command-line interface for the Recipe Management System.

Provides a CLI for processing recipes and generating documents.
"""

import argparse
import sys
from pathlib import Path

import pytest

from core.recipe.generators.markdown import generate_all_markdown
from core.recipe.processor import RecipeProcessor
from core.utils.config import (
    JSON_RECIPES_DIR,
    MD_RECIPES_DIR,
    PROJECT_NAME,
    UNPROCESSED_DIR,
    VERSION,
)
from core.utils.logger import get_logger, log_error, log_info

logger = get_logger("cli")


def process_recipes() -> bool:
    """
    Process all unprocessed recipes.

    Returns:
        bool: True if processing was successful
    """
    processor = RecipeProcessor()
    return processor.process_directory(UNPROCESSED_DIR)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog=PROJECT_NAME.lower().replace(" ", "-"),
        description=f"{PROJECT_NAME} v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --process                    # Process all new files
  %(prog)s --generate-md               # Generate Markdown from existing JSONs
  %(prog)s --process --generate-md     # Complete workflow
  %(prog)s --test                      # Run tests
  %(prog)s --version                   # Show version
        """,
    )

    parser.add_argument(
        "--process",
        action="store_true",
        help="Process all files in recipes/unprocessed/",
    )
    parser.add_argument(
        "--generate-md",
        action="store_true",
        help="Generate .md files in recipes/processed/Recetas MD/",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run the test suite with pytest",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
        help="Show program version",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="Increase verbosity of output",
    )

    args = parser.parse_args()

    # Show help if no flags provided
    if not any([args.process, args.generate_md, args.test]):
        parser.print_help()
        sys.exit(0)

    exit_code = 0
    try:
        # Process files
        if args.process and not process_recipes():
            exit_code = 1

        # Generate Markdown
        if args.generate_md and not generate_all_markdown(JSON_RECIPES_DIR, MD_RECIPES_DIR):
            exit_code = 1

        # Run tests
        if args.test:
            test_args = ["-v"] if args.verbose else ["-q"]
            test_args.extend(["--maxfail=1"])
            exit_code = pytest.main(test_args)

    except KeyboardInterrupt:
        log_info("\n⚠️ Operation interrupted by user")
        exit_code = 130
    except Exception as e:
        log_error(f"❌ Unexpected error: {e}")
        exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main() 