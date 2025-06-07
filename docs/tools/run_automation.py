#!/usr / bin / env python3
"""
Documentation Automation Runner

This script runs all documentation automation tools and updates
the documentation files with the generated content.
"""

from datetime import datetime
from glossary_generator import GlossaryGenerator
from pathlib import Path
import os

from api_docs import APIDocGenerator
from diagram_generator import DiagramGenerator
from doc_automation import DocumentationAutomation, DocConfig
from test_docs import TestDocGenerator
import logging
logging.basicConfig(
    level = logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    handlers=[
        logging.FileHandler('documentation_automation.log'), 
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Run all documentation automation tools."""
    # Setup paths
    base_dir = Path(__file__).parent.parent
    code_dir = base_dir / "core"
    docs_dir = base_dir
    output_dir = docs_dir / "generated"

    # Create output directory
    output_dir.mkdir(parents = True, exist_ok = True)

    # Initialize configuration
    config = DocConfig(
        docs_dir = docs_dir, 
        code_dir = code_dir, 
        output_dir = output_dir, 
        notion_api_key = os.getenv("NOTION_TOKEN"), 
        notion_db_ids={
            "recipes": os.getenv("NOTION_RECIPE_DB"), 
            "ingredients": os.getenv("NOTION_INGREDIENT_DB"), 
            "pantry": os.getenv("NOTION_PANTRY_DB")
        }
)

    try:
        # Run main automation
        logger.info("Starting documentation automation...")
        automation = DocumentationAutomation(config)
        automation.run_all()

        # Generate API documentation
        logger.info("Generating API documentation...")
        api_generator = APIDocGenerator(code_dir)
        api_docs = api_generator.generate_api_docs()
        with open(output_dir / "api_docs.md", 'w', encoding='utf - 8') as f:
            f.write(api_docs)

        # Generate test documentation
        logger.info("Generating test documentation...")
        test_generator = TestDocGenerator(code_dir)
        test_docs = test_generator.generate_test_docs()
        test_generator.update_test_docs(output_dir / "test_documentation.md")

        # Generate diagrams
        logger.info("Generating diagrams...")
        diagram_generator = DiagramGenerator(code_dir)
        diagrams = diagram_generator.generate_all_diagrams()
        for i, diagram in enumerate(diagrams):
            with open(output_dir / f"diagram_{i}.mmd", 'w', encoding='utf - 8') as f:
                f.write(diagram)

        # Update glossary
        logger.info("Updating glossary...")
        glossary_generator = GlossaryGenerator(code_dir, docs_dir)
        glossary_generator.update_glossary(output_dir / "glossary.md")

        logger.info("Documentation automation completed successfully!")

    except Exception as e:
        logger.error(f"Error during documentation automation: {str(e)}", exc_info = True)
        raise

if __name__ == "__main__":
    main()
