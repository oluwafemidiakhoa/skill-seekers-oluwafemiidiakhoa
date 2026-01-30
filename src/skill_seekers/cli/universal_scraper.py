#!/usr/bin/env python3
"""
Universal Scraper - Create Skills from Any Content Source

This module provides a unified interface for creating skills from any type of content source,
making Skill Seekers truly universal. It integrates content adapters, templates, and AI
enhancement to create high-quality skills from any domain.

Usage:
    python universal_scraper.py --config config.json
    skill-seekers universal --config config.json

Supported Content Sources:
- Documentation websites
- GitHub repositories  
- PDF documents
- REST/GraphQL APIs
- Video content (YouTube, Vimeo)
- Forum/Community sites (Stack Overflow, Reddit)
- Books/eBooks (EPUB, text)
- Database schemas
- Knowledge bases (Notion, Confluence)
"""

import sys
import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import time

from .content_adapters import (
    ContentSourceConfig, ContentItem, ContentType, SkillTemplate,
    get_adapter, create_universal_config_template
)
from .skill_templates import create_skill_from_template, get_template_processor
from .utils import setup_logging, create_directory, save_json


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for universal scraper."""
    parser = argparse.ArgumentParser(
        description="Create Claude AI skills from any content source"
    )
    
    parser.add_argument(
        "--config",
        required=True,
        help="Universal configuration JSON file"
    )
    
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Output directory for generated skills (default: output)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate configuration without extracting content"
    )
    
    parser.add_argument(
        "--template",
        help="Override skill template from config"
    )
    
    parser.add_argument(
        "--max-items",
        type=int,
        help="Maximum content items to extract (for testing)"
    )
    
    parser.add_argument(
        "--enhance",
        action="store_true",
        help="Enable AI enhancement after generation"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    return parser


def load_config(config_path: str) -> ContentSourceConfig:
    """Load and validate universal configuration."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        # Convert to ContentSourceConfig
        return ContentSourceConfig.from_dict(config_data)
    
    except FileNotFoundError:
        raise ValueError(f"Configuration file not found: {config_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in configuration file: {e}")
    except KeyError as e:
        raise ValueError(f"Missing required configuration key: {e}")


def extract_content(config: ContentSourceConfig, max_items: Optional[int] = None) -> List[ContentItem]:
    """Extract content using the appropriate adapter."""
    logger = logging.getLogger("universal_scraper")
    
    # Get the appropriate adapter
    adapter = get_adapter(config)
    
    # Validate configuration
    if not adapter.validate_config():
        raise ValueError(f"Invalid configuration for {config.source_type.value} adapter")
    
    logger.info(f"Extracting content using {adapter.__class__.__name__}")
    
    # Extract content
    content_items = []
    start_time = time.time()
    
    try:
        for i, item in enumerate(adapter.extract_content()):
            if max_items and i >= max_items:
                logger.info(f"Reached maximum items limit: {max_items}")
                break
            
            content_items.append(item)
            
            if i > 0 and i % 10 == 0:
                elapsed = time.time() - start_time
                rate = i / elapsed
                logger.info(f"Extracted {i} items ({rate:.1f} items/sec)")
        
        elapsed = time.time() - start_time
        logger.info(f"Extraction completed: {len(content_items)} items in {elapsed:.1f}s")
        
    except Exception as e:
        logger.error(f"Content extraction failed: {e}")
        raise
    
    return content_items


def generate_skill(
    content_items: List[ContentItem],
    config: ContentSourceConfig,
    template_override: Optional[str] = None
) -> str:
    """Generate skill using the appropriate template."""
    logger = logging.getLogger("universal_scraper")
    
    # Determine template to use
    template = config.template
    if template_override:
        try:
            template = SkillTemplate(template_override)
        except ValueError:
            logger.warning(f"Invalid template override '{template_override}', using config template")
    
    logger.info(f"Generating skill using {template.value} template")
    
    # Prepare metadata
    metadata = {
        'name': config.name,
        'description': config.description,
        'source_type': config.source_type.value,
        'template': template.value,
        'content_count': len(content_items),
        'generated_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Generate skill using template
    skill_content = create_skill_from_template(
        content_items=content_items,
        template=template,
        metadata=metadata,
        template_config=config.processing_options
    )
    
    return skill_content


def create_references(content_items: List[ContentItem], output_dir: Path) -> Dict[str, Any]:
    """Create reference files organized by categories."""
    logger = logging.getLogger("universal_scraper")
    
    references_dir = output_dir / "references"
    create_directory(references_dir)
    
    # Group content by categories
    category_groups = {}
    for item in content_items:
        for category in item.categories or ['general']:
            if category not in category_groups:
                category_groups[category] = []
            category_groups[category].append(item)
    
    # Create reference files for each category
    reference_files = {}
    for category, items in category_groups.items():
        filename = f"{category}.md"
        filepath = references_dir / filename
        
        # Create category content
        content = f"# {category.title()}\n\n"
        content += f"This section contains {len(items)} items related to {category}.\n\n"
        
        for item in items:
            content += f"## {item.title}\n\n"
            content += f"{item.content}\n\n"
            
            # Add code blocks
            for code_block in item.code_blocks:
                lang = code_block.get('language', 'text')
                code = code_block.get('content', '')
                content += f"```{lang}\n{code}\n```\n\n"
            
            if item.url:
                content += f"*Source: {item.url}*\n\n"
            
            content += "---\n\n"
        
        # Save reference file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        reference_files[category] = {
            'filename': filename,
            'item_count': len(items),
            'filepath': str(filepath)
        }
        
        logger.info(f"Created reference file: {filename} ({len(items)} items)")
    
    # Create index file
    index_content = "# Reference Index\n\n"
    index_content += "This skill contains the following reference sections:\n\n"
    
    for category, info in reference_files.items():
        index_content += f"- **{category.title()}** ({info['item_count']} items) - See [{info['filename']}]({info['filename']})\n"
    
    with open(references_dir / "index.md", 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    return reference_files


def save_extraction_data(content_items: List[ContentItem], output_dir: Path) -> None:
    """Save extracted content data for caching and analysis."""
    data_dir = output_dir.parent / f"{output_dir.name}_data"
    create_directory(data_dir)
    
    # Save individual content items
    pages_dir = data_dir / "pages"
    create_directory(pages_dir)
    
    for item in content_items:
        filename = f"{item.id}.json"
        filepath = pages_dir / filename
        
        save_json(item.to_dict(), filepath)
    
    # Save summary
    summary = {
        'extraction_completed': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_items': len(content_items),
        'content_types': {},
        'categories': {},
        'quality_stats': {
            'avg_quality_score': sum(item.quality_score for item in content_items) / len(content_items) if content_items else 0,
            'high_quality_count': sum(1 for item in content_items if item.quality_score > 0.7),
            'low_quality_count': sum(1 for item in content_items if item.quality_score < 0.3)
        }
    }
    
    # Count content types
    for item in content_items:
        content_type = item.content_type
        summary['content_types'][content_type] = summary['content_types'].get(content_type, 0) + 1
    
    # Count categories
    for item in content_items:
        for category in item.categories or ['general']:
            summary['categories'][category] = summary['categories'].get(category, 0) + 1
    
    save_json(summary, data_dir / "summary.json")


def create_universal_skill(config_path: str, output_dir: str, **options) -> Dict[str, Any]:
    """Create a skill from universal configuration.
    
    Args:
        config_path: Path to configuration file
        output_dir: Output directory for generated skill
        **options: Additional options (dry_run, template, max_items, etc.)
        
    Returns:
        Dictionary with generation results and statistics
    """
    logger = logging.getLogger("universal_scraper")
    
    start_time = time.time()
    
    # Load configuration
    logger.info(f"Loading configuration: {config_path}")
    config = load_config(config_path)
    
    # Create output directory
    skill_dir = Path(output_dir) / config.name
    create_directory(skill_dir)
    
    logger.info(f"Creating {config.template.value} skill: {config.name}")
    logger.info(f"Source type: {config.source_type.value}")
    logger.info(f"Output directory: {skill_dir}")
    
    # Dry run mode - just validate configuration
    if options.get('dry_run'):
        adapter = get_adapter(config)
        if adapter.validate_config():
            logger.info("✅ Configuration validation passed")
            estimate = adapter.estimate_content_size()
            logger.info(f"Estimated content size: {estimate}")
            return {
                'status': 'validated',
                'config': config,
                'estimate': estimate
            }
        else:
            logger.error("❌ Configuration validation failed")
            return {'status': 'validation_failed'}
    
    # Extract content
    logger.info("Starting content extraction...")
    content_items = extract_content(config, options.get('max_items'))
    
    if not content_items:
        logger.warning("No content extracted - skill generation aborted")
        return {
            'status': 'no_content',
            'message': 'No content could be extracted from the source'
        }
    
    # Save extraction data
    save_extraction_data(content_items, skill_dir)
    
    # Generate skill
    logger.info("Generating skill content...")
    skill_content = generate_skill(content_items, config, options.get('template'))
    
    # Save SKILL.md
    skill_file = skill_dir / "SKILL.md"
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(skill_content)
    
    logger.info(f"Generated SKILL.md: {skill_file}")
    
    # Create reference files
    reference_files = create_references(content_items, skill_dir)
    
    # Create empty directories for user assets
    create_directory(skill_dir / "scripts")
    create_directory(skill_dir / "assets")
    
    # Calculate statistics
    total_time = time.time() - start_time
    stats = {
        'status': 'success',
        'skill_name': config.name,
        'source_type': config.source_type.value,
        'template': config.template.value,
        'content_items': len(content_items),
        'reference_files': len(reference_files),
        'generation_time': total_time,
        'skill_directory': str(skill_dir),
        'skill_file': str(skill_file)
    }
    
    logger.info(f"✅ Skill generation completed in {total_time:.1f}s")
    logger.info(f"   Content items: {len(content_items)}")
    logger.info(f"   Reference files: {len(reference_files)}")
    logger.info(f"   Skill directory: {skill_dir}")
    
    # AI enhancement if requested
    if options.get('enhance'):
        logger.info("Starting AI enhancement...")
        try:
            from .enhance_skill_local import enhance_skill_local
            enhanced = enhance_skill_local(str(skill_dir))
            if enhanced:
                stats['enhanced'] = True
                logger.info("✅ AI enhancement completed")
            else:
                logger.warning("⚠️  AI enhancement failed")
        except ImportError:
            logger.warning("AI enhancement not available")
    
    return stats


def main() -> int:
    """Main entry point for universal scraper."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(level=log_level)
    logger = logging.getLogger("universal_scraper")
    
    try:
        # Create skill
        result = create_universal_skill(
            config_path=args.config,
            output_dir=args.output_dir,
            dry_run=args.dry_run,
            template=args.template,
            max_items=args.max_items,
            enhance=args.enhance
        )
        
        if result['status'] == 'success':
            print(f"\n🎉 Successfully created skill: {result['skill_name']}")
            print(f"📁 Location: {result['skill_directory']}")
            print(f"📄 Main file: {result['skill_file']}")
            print(f"⏱️  Generation time: {result['generation_time']:.1f}s")
            print(f"📊 Content items: {result['content_items']}")
            return 0
        
        elif result['status'] == 'validated':
            print("✅ Configuration validation passed")
            return 0
        
        else:
            print(f"❌ Skill generation failed: {result.get('message', 'Unknown error')}")
            return 1
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def create_config_template(content_type: str, template: str, output_path: str) -> None:
    """Create a configuration template file."""
    try:
        content_type_enum = ContentType(content_type)
        template_enum = SkillTemplate(template)
    except ValueError as e:
        raise ValueError(f"Invalid content type or template: {e}")
    
    config_template = create_universal_config_template(content_type_enum, template_enum)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(config_template, f, indent=2)
    
    print(f"Created configuration template: {output_path}")


if __name__ == "__main__":
    # Add support for creating config templates
    if len(sys.argv) > 1 and sys.argv[1] == "create-template":
        if len(sys.argv) != 5:
            print("Usage: python universal_scraper.py create-template <content_type> <template> <output_file>")
            print(f"Content types: {[t.value for t in ContentType]}")
            print(f"Templates: {[t.value for t in SkillTemplate]}")
            sys.exit(1)
        
        try:
            create_config_template(sys.argv[2], sys.argv[3], sys.argv[4])
            sys.exit(0)
        except Exception as e:
            print(f"Error creating template: {e}")
            sys.exit(1)
    
    sys.exit(main())