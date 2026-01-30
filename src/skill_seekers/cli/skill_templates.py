#!/usr/bin/env python3
"""
Skill Templates - Domain-Specific Skill Generation

This module provides templates for generating different types of skills based on content type and use case.
Templates define how content should be organized, what sections to include, and how to structure the final skill.

Templates Available:
- API Reference: Function signatures, endpoints, examples
- Tutorial Series: Step-by-step learning paths
- Troubleshooting: Problem-solution mappings
- Best Practices: Guidelines and patterns
- Quick Reference: Cheat sheets and lookup tables
- Comprehensive Guide: Full documentation with all aspects
- FAQ Collection: Question-answer format
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path

from .content_adapters import ContentItem, SkillTemplate


@dataclass
class SkillSection:
    """Represents a section in the generated skill."""
    id: str
    title: str
    content: str
    order: int
    subsections: List['SkillSection'] = None
    
    def __post_init__(self):
        if self.subsections is None:
            self.subsections = []
    
    def to_markdown(self, level: int = 1) -> str:
        """Convert section to markdown format."""
        header = "#" * level
        markdown = f"{header} {self.title}\n\n{self.content}\n\n"
        
        for subsection in sorted(self.subsections, key=lambda x: x.order):
            markdown += subsection.to_markdown(level + 1)
        
        return markdown


class SkillTemplateProcessor(ABC):
    """Abstract base class for skill template processors."""
    
    def __init__(self, template_config: Dict[str, Any]):
        self.config = template_config
    
    @abstractmethod
    def process_content(self, content_items: List[ContentItem]) -> List[SkillSection]:
        """Process content items into structured skill sections.
        
        Args:
            content_items: List of extracted content items
            
        Returns:
            List of skill sections organized according to template
        """
        pass
    
    @abstractmethod
    def generate_skill_md(self, sections: List[SkillSection], metadata: Dict[str, Any]) -> str:
        """Generate the final SKILL.md content.
        
        Args:
            sections: Processed skill sections
            metadata: Skill metadata (name, description, etc.)
            
        Returns:
            Complete SKILL.md content as markdown string
        """
        pass
    
    def get_default_categories(self) -> List[str]:
        """Get default categories for this template type."""
        return ["general"]


class APIReferenceTemplate(SkillTemplateProcessor):
    """Template for API reference documentation skills."""
    
    def process_content(self, content_items: List[ContentItem]) -> List[SkillSection]:
        """Process API content into reference sections."""
        sections = []
        
        # Group content by type
        endpoints = [item for item in content_items if item.content_type == "api_endpoint"]
        overviews = [item for item in content_items if item.content_type == "api_overview"]
        
        # Create overview section
        if overviews:
            overview_content = "\n\n".join([item.content for item in overviews])
            sections.append(SkillSection(
                id="overview",
                title="API Overview",
                content=overview_content,
                order=1
            ))
        
        # Group endpoints by tag/category
        endpoint_groups = {}
        for endpoint in endpoints:
            tags = endpoint.metadata.get('tags', ['general'])
            for tag in tags:
                if tag not in endpoint_groups:
                    endpoint_groups[tag] = []
                endpoint_groups[tag].append(endpoint)
        
        # Create endpoint sections
        order = 2
        for tag, tag_endpoints in endpoint_groups.items():
            subsections = []
            for i, endpoint in enumerate(tag_endpoints):
                subsections.append(SkillSection(
                    id=f"endpoint_{endpoint.id}",
                    title=f"{endpoint.metadata['method'].upper()} {endpoint.metadata['path']}",
                    content=self._format_endpoint_content(endpoint),
                    order=i + 1
                ))
            
            sections.append(SkillSection(
                id=f"endpoints_{tag}",
                title=f"{tag.title()} Endpoints",
                content=f"This section covers all {tag} related API endpoints.",
                order=order,
                subsections=subsections
            ))
            order += 1
        
        return sections
    
    def _format_endpoint_content(self, endpoint: ContentItem) -> str:
        """Format endpoint content for API reference."""
        content = f"{endpoint.content}\n\n"
        
        metadata = endpoint.metadata
        
        # Add method and path
        content += f"**Method:** `{metadata['method'].upper()}`\n"
        content += f"**Path:** `{metadata['path']}`\n\n"
        
        # Add parameters
        if metadata.get('parameters'):
            content += "**Parameters:**\n"
            for param in metadata['parameters']:
                required = " *(required)*" if param.get('required') else ""
                content += f"- `{param['name']}` ({param.get('type', 'string')}){required}: {param.get('description', '')}\n"
            content += "\n"
        
        # Add responses
        if metadata.get('responses'):
            content += "**Responses:**\n"
            for code, response in metadata['responses'].items():
                content += f"- `{code}`: {response.get('description', '')}\n"
            content += "\n"
        
        # Add code examples if available
        if endpoint.code_blocks:
            content += "**Example:**\n\n"
            for code_block in endpoint.code_blocks:
                lang = code_block.get('language', 'http')
                code = code_block.get('content', '')
                content += f"```{lang}\n{code}\n```\n\n"
        
        return content
    
    def generate_skill_md(self, sections: List[SkillSection], metadata: Dict[str, Any]) -> str:
        """Generate API reference SKILL.md."""
        skill_md = f"""# {metadata['name']} API Reference

{metadata['description']}

## When to Use This Skill

Use this skill when you need to:
- Understand API endpoints and their parameters
- Find correct HTTP methods and request formats
- Learn about response formats and status codes
- Get examples of API usage
- Troubleshoot API integration issues

## Quick Reference

This skill contains comprehensive API documentation including:
- Complete endpoint reference with parameters and responses
- Request/response examples in multiple formats
- Authentication and authorization details
- Error handling and status codes

"""
        
        # Add all sections
        for section in sorted(sections, key=lambda x: x.order):
            skill_md += section.to_markdown(2)
        
        skill_md += """
## Best Practices

- Always check authentication requirements before making requests
- Handle error responses gracefully in your applications
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Include proper headers and content types
- Validate request parameters before sending

## Support

For API support and additional examples, refer to the official documentation or contact the API provider.
"""
        
        return skill_md
    
    def get_default_categories(self) -> List[str]:
        return ["endpoints", "authentication", "examples", "responses", "errors"]


class TutorialSeriesTemplate(SkillTemplateProcessor):
    """Template for tutorial/learning series skills."""
    
    def process_content(self, content_items: List[ContentItem]) -> List[SkillSection]:
        """Process tutorial content into learning progression."""
        sections = []
        
        # Sort content by difficulty/progression
        sorted_items = self._sort_by_difficulty(content_items)
        
        # Group into learning modules
        modules = self._group_into_modules(sorted_items)
        
        # Create sections for each module
        for i, (module_name, module_items) in enumerate(modules.items()):
            subsections = []
            for j, item in enumerate(module_items):
                subsections.append(SkillSection(
                    id=f"lesson_{item.id}",
                    title=item.title,
                    content=self._format_tutorial_content(item),
                    order=j + 1
                ))
            
            sections.append(SkillSection(
                id=f"module_{i}",
                title=module_name,
                content=f"This module covers {module_name.lower()} concepts and techniques.",
                order=i + 1,
                subsections=subsections
            ))
        
        return sections
    
    def _sort_by_difficulty(self, content_items: List[ContentItem]) -> List[ContentItem]:
        """Sort content by difficulty level."""
        # Define difficulty keywords
        difficulty_keywords = {
            'beginner': ['beginner', 'intro', 'basic', 'getting started', 'first steps'],
            'intermediate': ['intermediate', 'advanced basics', 'next steps'],
            'advanced': ['advanced', 'expert', 'complex', 'deep dive']
        }
        
        # Score each item by difficulty
        scored_items = []
        for item in content_items:
            score = 0
            content_lower = (item.title + " " + item.content).lower()
            
            for level, keywords in difficulty_keywords.items():
                for keyword in keywords:
                    if keyword in content_lower:
                        if level == 'beginner':
                            score = 1
                        elif level == 'intermediate':
                            score = 2
                        elif level == 'advanced':
                            score = 3
                        break
                if score > 0:
                    break
            
            # Default to intermediate if no keywords found
            if score == 0:
                score = 2
            
            scored_items.append((score, item))
        
        # Sort by score and return items
        scored_items.sort(key=lambda x: x[0])
        return [item for score, item in scored_items]
    
    def _group_into_modules(self, content_items: List[ContentItem]) -> Dict[str, List[ContentItem]]:
        """Group content into learning modules."""
        modules = {}
        current_module = "Getting Started"
        module_items = []
        
        for item in content_items:
            # Check if this item starts a new module (basic heuristic)
            if any(keyword in item.title.lower() for keyword in ['advanced', 'deep dive', 'expert']):
                if module_items:
                    modules[current_module] = module_items
                    module_items = []
                current_module = "Advanced Topics"
            elif any(keyword in item.title.lower() for keyword in ['intermediate', 'next steps']):
                if module_items and current_module == "Getting Started":
                    modules[current_module] = module_items
                    module_items = []
                current_module = "Intermediate Concepts"
            
            module_items.append(item)
        
        # Add final module
        if module_items:
            modules[current_module] = module_items
        
        return modules
    
    def _format_tutorial_content(self, item: ContentItem) -> str:
        """Format content for tutorial presentation."""
        content = f"{item.content}\n\n"
        
        # Add code examples prominently
        if item.code_blocks:
            content += "## Code Example\n\n"
            for code_block in item.code_blocks:
                lang = code_block.get('language', 'python')
                code = code_block.get('content', '')
                content += f"```{lang}\n{code}\n```\n\n"
        
        # Add practice exercises if metadata indicates they exist
        if item.metadata.get('has_exercises'):
            content += "## Practice\n\n"
            content += "Try implementing this concept in your own project.\n\n"
        
        return content
    
    def generate_skill_md(self, sections: List[SkillSection], metadata: Dict[str, Any]) -> str:
        """Generate tutorial series SKILL.md."""
        skill_md = f"""# {metadata['name']} Tutorial Series

{metadata['description']}

## Learning Path

This skill provides a structured learning path from beginner to advanced concepts. Each module builds upon the previous one, so it's recommended to follow the order presented.

## How to Use This Skill

1. **Start with the basics** - Begin with the "Getting Started" module
2. **Practice as you go** - Try the code examples in your own environment
3. **Build progressively** - Complete each module before moving to the next
4. **Reference back** - Use this skill as a reference after completing the tutorials

"""
        
        # Add learning objectives
        skill_md += "## Learning Objectives\n\n"
        skill_md += "After completing this tutorial series, you will be able to:\n"
        for i, section in enumerate(sections, 1):
            skill_md += f"{i}. Understand and apply {section.title.lower()} concepts\n"
        skill_md += "\n"
        
        # Add all sections
        for section in sorted(sections, key=lambda x: x.order):
            skill_md += section.to_markdown(2)
        
        skill_md += """
## Next Steps

After completing this tutorial series:
- Practice building real projects using these concepts
- Explore the official documentation for advanced features
- Join the community for support and discussions
- Consider contributing back with your own examples

## Additional Resources

- Official documentation
- Community forums
- Example projects and repositories
"""
        
        return skill_md
    
    def get_default_categories(self) -> List[str]:
        return ["getting_started", "intermediate", "advanced", "examples", "practice"]


class TroubleshootingTemplate(SkillTemplateProcessor):
    """Template for troubleshooting and problem-solving skills."""
    
    def process_content(self, content_items: List[ContentItem]) -> List[SkillSection]:
        """Process content into problem-solution format."""
        sections = []
        
        # Group by problem categories
        problem_groups = {}
        for item in content_items:
            category = self._categorize_problem(item)
            if category not in problem_groups:
                problem_groups[category] = []
            problem_groups[category].append(item)
        
        # Create sections for each problem category
        for i, (category, items) in enumerate(problem_groups.items()):
            subsections = []
            for j, item in enumerate(items):
                subsections.append(SkillSection(
                    id=f"problem_{item.id}",
                    title=self._extract_problem_title(item),
                    content=self._format_troubleshooting_content(item),
                    order=j + 1
                ))
            
            sections.append(SkillSection(
                id=f"category_{category}",
                title=f"{category.title()} Issues",
                content=f"Common problems and solutions related to {category.lower()}.",
                order=i + 1,
                subsections=subsections
            ))
        
        return sections
    
    def _categorize_problem(self, item: ContentItem) -> str:
        """Categorize the type of problem."""
        categories = {
            'installation': ['install', 'setup', 'config', 'environment'],
            'performance': ['slow', 'performance', 'memory', 'speed', 'lag'],
            'errors': ['error', 'exception', 'bug', 'crash', 'fail'],
            'integration': ['integration', 'api', 'connection', 'authentication'],
            'deployment': ['deploy', 'production', 'build', 'release']
        }
        
        content_lower = (item.title + " " + item.content).lower()
        
        for category, keywords in categories.items():
            if any(keyword in content_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def _extract_problem_title(self, item: ContentItem) -> str:
        """Extract a clear problem statement from content."""
        # If it's a Q&A format, use the question
        if item.content_type == "qa_pair":
            return item.title
        
        # Otherwise, try to extract problem from content
        lines = item.content.split('\n')
        for line in lines:
            if any(word in line.lower() for word in ['problem:', 'issue:', 'error:']):
                return line.replace('Problem:', '').replace('Issue:', '').replace('Error:', '').strip()
        
        # Fallback to title
        return item.title
    
    def _format_troubleshooting_content(self, item: ContentItem) -> str:
        """Format content for troubleshooting presentation."""
        content = ""
        
        # Add problem description
        content += "**Problem:**\n"
        content += f"{item.content.split('Answer')[0].strip()}\n\n"
        
        # Add solution
        if 'Answer' in item.content:
            solution = item.content.split('Answer')[1].strip()
            content += "**Solution:**\n"
            content += f"{solution}\n\n"
        
        # Add code examples
        if item.code_blocks:
            content += "**Code Example:**\n\n"
            for code_block in item.code_blocks:
                lang = code_block.get('language', 'bash')
                code = code_block.get('content', '')
                content += f"```{lang}\n{code}\n```\n\n"
        
        # Add additional context from metadata
        if item.metadata.get('score', 0) > 0:
            content += f"*This solution has been verified with a community score of {item.metadata['score']}*\n\n"
        
        return content
    
    def generate_skill_md(self, sections: List[SkillSection], metadata: Dict[str, Any]) -> str:
        """Generate troubleshooting SKILL.md."""
        skill_md = f"""# {metadata['name']} Troubleshooting Guide

{metadata['description']}

## When to Use This Skill

Use this skill when you encounter:
- Setup and installation problems
- Runtime errors and exceptions
- Performance and optimization issues
- Integration and configuration challenges
- Deployment and production problems

## How to Use This Guide

1. **Identify the problem category** - Browse the sections to find the type of issue you're facing
2. **Find similar symptoms** - Look for problems that match your specific symptoms
3. **Follow the solution steps** - Apply the provided solutions step by step
4. **Verify the fix** - Test to ensure the problem is resolved
5. **Report back** - If the solution doesn't work, note what happened for further troubleshooting

"""
        
        # Add quick problem locator
        skill_md += "## Quick Problem Locator\n\n"
        for section in sections:
            skill_md += f"- **{section.title}**: {len(section.subsections)} common issues\n"
        skill_md += "\n"
        
        # Add all sections
        for section in sorted(sections, key=lambda x: x.order):
            skill_md += section.to_markdown(2)
        
        skill_md += """
## Prevention Tips

To avoid common issues:
- Follow official installation guides
- Keep dependencies up to date
- Use proper error handling
- Test in staging environments
- Monitor performance metrics

## Getting More Help

If you can't find a solution here:
- Check the official documentation
- Search community forums
- Create a detailed issue report
- Consider consulting with experts
"""
        
        return skill_md
    
    def get_default_categories(self) -> List[str]:
        return ["installation", "errors", "performance", "configuration", "deployment"]


def get_template_processor(template: SkillTemplate, config: Dict[str, Any] = None) -> SkillTemplateProcessor:
    """Factory function to get the appropriate template processor."""
    if config is None:
        config = {}
    
    processors = {
        SkillTemplate.API_REFERENCE: APIReferenceTemplate,
        SkillTemplate.TUTORIAL_SERIES: TutorialSeriesTemplate,
        SkillTemplate.TROUBLESHOOTING: TroubleshootingTemplate,
        # Add more processors as they're implemented
    }
    
    processor_class = processors.get(template)
    if not processor_class:
        # Fallback to a generic processor
        processor_class = TutorialSeriesTemplate  # Default template
    
    return processor_class(config)


def create_skill_from_template(
    content_items: List[ContentItem],
    template: SkillTemplate,
    metadata: Dict[str, Any],
    template_config: Dict[str, Any] = None
) -> str:
    """Create a complete SKILL.md from content items using the specified template.
    
    Args:
        content_items: Extracted content items
        template: Skill template to use
        metadata: Skill metadata (name, description, etc.)
        template_config: Optional template-specific configuration
        
    Returns:
        Complete SKILL.md content as markdown string
    """
    if template_config is None:
        template_config = {}
    
    processor = get_template_processor(template, template_config)
    sections = processor.process_content(content_items)
    return processor.generate_skill_md(sections, metadata)