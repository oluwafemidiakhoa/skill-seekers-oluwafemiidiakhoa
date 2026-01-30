#!/usr/bin/env python3
"""
Content Adapters - Universal Content Source Framework

This module provides a unified interface for extracting structured content from any source type,
making Skill Seekers truly universal for creating skills from any domain or content format.

Supported Content Sources:
- Documentation websites (existing)
- GitHub repositories (existing) 
- PDF documents (existing)
- REST/GraphQL APIs (NEW)
- Video content (YouTube, Vimeo) (NEW)
- Forum/Community sites (Stack Overflow, Reddit) (NEW)
- Books/eBooks (EPUB, text) (NEW)
- Database schemas (SQL, NoSQL) (NEW)
- Knowledge bases (Notion, Confluence) (NEW)
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union, Iterator
from dataclasses import dataclass, field
from enum import Enum
import json
import requests
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ContentType(Enum):
    """Supported content types for skill creation."""
    DOCUMENTATION = "documentation"
    GITHUB = "github"
    PDF = "pdf"
    API = "api"
    VIDEO = "video"
    FORUM = "forum"
    BOOK = "book"
    DATABASE = "database"
    KNOWLEDGE_BASE = "knowledge_base"


class SkillTemplate(Enum):
    """Skill templates for different use cases."""
    API_REFERENCE = "api_reference"
    TUTORIAL_SERIES = "tutorial_series"
    TROUBLESHOOTING = "troubleshooting"
    BEST_PRACTICES = "best_practices"
    QUICK_REFERENCE = "quick_reference"
    COMPREHENSIVE_GUIDE = "comprehensive_guide"
    FAQ_COLLECTION = "faq_collection"


@dataclass
class ContentItem:
    """Represents a single piece of extracted content."""
    id: str
    title: str
    content: str
    content_type: str
    url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    code_blocks: List[Dict[str, Any]] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    relationships: List[str] = field(default_factory=list)  # Links to other content items
    quality_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'content_type': self.content_type,
            'url': self.url,
            'metadata': self.metadata,
            'code_blocks': self.code_blocks,
            'categories': self.categories,
            'relationships': self.relationships,
            'quality_score': self.quality_score
        }


@dataclass
class ContentSourceConfig:
    """Configuration for a content source."""
    source_type: ContentType
    name: str
    description: str
    template: SkillTemplate
    source_config: Dict[str, Any]
    processing_options: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContentSourceConfig':
        """Create from dictionary (loaded from JSON)."""
        return cls(
            source_type=ContentType(data['source_type']),
            name=data['name'],
            description=data['description'],
            template=SkillTemplate(data.get('template', 'comprehensive_guide')),
            source_config=data['source_config'],
            processing_options=data.get('processing_options', {})
        )


class ContentAdapter(ABC):
    """Abstract base class for content adapters."""
    
    def __init__(self, config: ContentSourceConfig):
        self.config = config
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
    
    @abstractmethod
    def extract_content(self) -> Iterator[ContentItem]:
        """Extract content from the source.
        
        Yields:
            ContentItem: Individual pieces of structured content
        """
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate the configuration for this adapter.
        
        Returns:
            bool: True if configuration is valid
        """
        pass
    
    def estimate_content_size(self) -> Dict[str, Any]:
        """Estimate the amount of content available.
        
        Returns:
            Dict with estimated counts, processing time, etc.
        """
        return {
            'estimated_items': 0,
            'estimated_time_minutes': 0,
            'confidence': 'low'
        }


class APIAdapter(ContentAdapter):
    """Adapter for REST/GraphQL APIs to create API reference skills."""
    
    def validate_config(self) -> bool:
        """Validate API configuration."""
        required = ['base_url']
        if self.config.template == SkillTemplate.API_REFERENCE:
            required.extend(['endpoints', 'auth'])
        
        return all(key in self.config.source_config for key in required)
    
    def extract_content(self) -> Iterator[ContentItem]:
        """Extract API documentation and schemas."""
        base_url = self.config.source_config['base_url']
        
        # Extract OpenAPI/Swagger specs
        if 'openapi_spec_url' in self.config.source_config:
            yield from self._extract_openapi_spec()
        
        # Extract from endpoints
        if 'endpoints' in self.config.source_config:
            yield from self._extract_endpoints()
        
        # Extract examples
        if 'examples_config' in self.config.source_config:
            yield from self._extract_examples()
    
    def _extract_openapi_spec(self) -> Iterator[ContentItem]:
        """Extract from OpenAPI/Swagger specification."""
        spec_url = self.config.source_config['openapi_spec_url']
        try:
            response = requests.get(spec_url)
            spec = response.json()
            
            # Extract API info
            yield ContentItem(
                id="api_info",
                title=f"API Overview: {spec.get('info', {}).get('title', 'API')}",
                content=spec.get('info', {}).get('description', ''),
                content_type="api_overview",
                metadata={
                    'version': spec.get('info', {}).get('version'),
                    'servers': spec.get('servers', [])
                }
            )
            
            # Extract endpoints
            for path, methods in spec.get('paths', {}).items():
                for method, endpoint_spec in methods.items():
                    if isinstance(endpoint_spec, dict):
                        yield self._create_endpoint_content_item(path, method, endpoint_spec)
                        
        except Exception as e:
            self.logger.error(f"Failed to extract OpenAPI spec: {e}")
    
    def _extract_endpoints(self) -> Iterator[ContentItem]:
        """Extract individual API endpoints."""
        endpoints = self.config.source_config.get('endpoints', [])
        for endpoint in endpoints:
            try:
                # Create documentation for each endpoint
                yield ContentItem(
                    id=f"endpoint_{endpoint['path']}_{endpoint['method']}",
                    title=f"{endpoint['method'].upper()} {endpoint['path']}",
                    content=endpoint.get('description', ''),
                    content_type="api_endpoint",
                    metadata={
                        'method': endpoint['method'],
                        'path': endpoint['path'],
                        'parameters': endpoint.get('parameters', []),
                        'responses': endpoint.get('responses', {})
                    }
                )
            except Exception as e:
                self.logger.error(f"Failed to extract endpoint {endpoint}: {e}")
    
    def _extract_examples(self) -> Iterator[ContentItem]:
        """Extract code examples and use cases."""
        examples_config = self.config.source_config.get('examples_config', {})
        # Implementation for extracting examples from various sources
        pass
    
    def _create_endpoint_content_item(self, path: str, method: str, spec: Dict) -> ContentItem:
        """Create ContentItem for an API endpoint."""
        return ContentItem(
            id=f"endpoint_{path.replace('/', '_')}_{method}",
            title=f"{method.upper()} {path}",
            content=spec.get('description', ''),
            content_type="api_endpoint",
            metadata={
                'method': method,
                'path': path,
                'summary': spec.get('summary'),
                'parameters': spec.get('parameters', []),
                'responses': spec.get('responses', {}),
                'tags': spec.get('tags', [])
            },
            categories=[f"endpoint_{method}", "api"] + spec.get('tags', [])
        )


class VideoAdapter(ContentAdapter):
    """Adapter for video content (YouTube, Vimeo, etc.) to create learning skills."""
    
    def validate_config(self) -> bool:
        """Validate video configuration."""
        required = ['video_urls']
        return all(key in self.config.source_config for key in required)
    
    def extract_content(self) -> Iterator[ContentItem]:
        """Extract video metadata, transcripts, and chapters."""
        video_urls = self.config.source_config['video_urls']
        
        for url in video_urls:
            try:
                # Extract video metadata
                video_info = self._get_video_info(url)
                
                # Extract transcript if available
                transcript = self._get_transcript(url)
                
                # Extract chapters/timestamps
                chapters = self._extract_chapters(url, transcript)
                
                yield ContentItem(
                    id=f"video_{video_info['id']}",
                    title=video_info['title'],
                    content=transcript,
                    content_type="video_content",
                    url=url,
                    metadata={
                        'duration': video_info.get('duration'),
                        'author': video_info.get('author'),
                        'chapters': chapters,
                        'tags': video_info.get('tags', [])
                    },
                    categories=self._categorize_video_content(video_info, transcript)
                )
                
            except Exception as e:
                self.logger.error(f"Failed to extract video {url}: {e}")
    
    def _get_video_info(self, url: str) -> Dict[str, Any]:
        """Get video metadata (title, description, duration, etc.)."""
        # Implementation would use youtube-dl, yt-dlp, or video platform APIs
        return {
            'id': 'video_id',
            'title': 'Video Title',
            'duration': 600,
            'author': 'Author Name',
            'tags': []
        }
    
    def _get_transcript(self, url: str) -> str:
        """Get video transcript/subtitles."""
        # Implementation would extract captions or use speech-to-text
        return ""
    
    def _extract_chapters(self, url: str, transcript: str) -> List[Dict[str, Any]]:
        """Extract video chapters and key timestamps."""
        # Implementation would parse description or analyze transcript
        return []
    
    def _categorize_video_content(self, video_info: Dict, transcript: str) -> List[str]:
        """Categorize video content based on metadata and transcript."""
        categories = []
        
        # Use video tags
        if video_info.get('tags'):
            categories.extend(video_info['tags'])
        
        # Analyze transcript for topics (could use AI here)
        # Basic keyword detection for now
        keywords = {
            'tutorial': ['tutorial', 'how to', 'step by step'],
            'advanced': ['advanced', 'expert', 'complex'],
            'beginner': ['beginner', 'intro', 'basic', 'getting started']
        }
        
        transcript_lower = transcript.lower()
        for category, words in keywords.items():
            if any(word in transcript_lower for word in words):
                categories.append(category)
        
        return categories


class ForumAdapter(ContentAdapter):
    """Adapter for forum/community content (Stack Overflow, Reddit, etc.)."""
    
    def validate_config(self) -> bool:
        """Validate forum configuration."""
        required = ['platform', 'search_queries']
        return all(key in self.config.source_config for key in required)
    
    def extract_content(self) -> Iterator[ContentItem]:
        """Extract Q&A pairs, discussions, and solutions."""
        platform = self.config.source_config['platform']
        
        if platform == 'stackoverflow':
            yield from self._extract_stackoverflow_content()
        elif platform == 'reddit':
            yield from self._extract_reddit_content()
        else:
            self.logger.warning(f"Unsupported forum platform: {platform}")
    
    def _extract_stackoverflow_content(self) -> Iterator[ContentItem]:
        """Extract Stack Overflow Q&A content."""
        search_queries = self.config.source_config['search_queries']
        max_questions = self.config.source_config.get('max_questions', 100)
        
        for query in search_queries:
            try:
                # Use Stack Exchange API
                api_url = "https://api.stackexchange.com/2.3/search"
                params = {
                    'order': 'desc',
                    'sort': 'votes',
                    'intitle': query,
                    'site': 'stackoverflow',
                    'pagesize': max_questions,
                    'filter': '!9_bDDxJY5'  # Include body and answers
                }
                
                response = requests.get(api_url, params=params)
                data = response.json()
                
                for question in data.get('items', []):
                    yield self._create_stackoverflow_content_item(question)
                    
            except Exception as e:
                self.logger.error(f"Failed to extract Stack Overflow content for query '{query}': {e}")
    
    def _extract_reddit_content(self) -> Iterator[ContentItem]:
        """Extract Reddit discussion content."""
        # Implementation for Reddit API
        pass
    
    def _create_stackoverflow_content_item(self, question: Dict) -> ContentItem:
        """Create ContentItem from Stack Overflow question."""
        # Combine question and top answers
        content = f"**Question:** {question.get('body', '')}\n\n"
        
        for answer in question.get('answers', []):
            if answer.get('is_accepted') or answer.get('score', 0) > 0:
                content += f"**Answer (Score: {answer.get('score', 0)}):**\n{answer.get('body', '')}\n\n"
        
        return ContentItem(
            id=f"so_question_{question['question_id']}",
            title=question['title'],
            content=content,
            content_type="qa_pair",
            url=question['link'],
            metadata={
                'score': question.get('score', 0),
                'answer_count': question.get('answer_count', 0),
                'view_count': question.get('view_count', 0),
                'tags': question.get('tags', [])
            },
            categories=['troubleshooting', 'qa'] + question.get('tags', [])[:3],  # Limit tags
            quality_score=min(question.get('score', 0) / 10.0, 1.0)  # Normalize score
        )


def get_adapter(config: ContentSourceConfig) -> ContentAdapter:
    """Factory function to get the appropriate adapter for a content source."""
    adapters = {
        ContentType.API: APIAdapter,
        ContentType.VIDEO: VideoAdapter,
        ContentType.FORUM: ForumAdapter,
        # Add more adapters as they're implemented
    }
    
    adapter_class = adapters.get(config.source_type)
    if not adapter_class:
        raise ValueError(f"No adapter available for content type: {config.source_type}")
    
    return adapter_class(config)


def create_universal_config_template(content_type: ContentType, template: SkillTemplate) -> Dict[str, Any]:
    """Create a configuration template for a given content type and skill template."""
    
    base_template = {
        "name": "",
        "description": "",
        "source_type": content_type.value,
        "template": template.value,
        "source_config": {},
        "processing_options": {
            "max_content_items": 1000,
            "quality_threshold": 0.3,
            "enable_ai_enhancement": True,
            "auto_categorization": True
        }
    }
    
    # Add source-specific configuration templates
    if content_type == ContentType.API:
        base_template["source_config"] = {
            "base_url": "https://api.example.com",
            "openapi_spec_url": "https://api.example.com/openapi.json",
            "auth": {
                "type": "bearer",  # bearer, basic, api_key
                "token": "${API_TOKEN}"
            },
            "endpoints": [],
            "examples_config": {
                "example_sources": []
            }
        }
    
    elif content_type == ContentType.VIDEO:
        base_template["source_config"] = {
            "video_urls": [],
            "extract_transcripts": True,
            "extract_chapters": True,
            "language": "en"
        }
    
    elif content_type == ContentType.FORUM:
        base_template["source_config"] = {
            "platform": "stackoverflow",  # stackoverflow, reddit, discourse
            "search_queries": [],
            "max_questions": 100,
            "min_score": 1,
            "include_answers": True
        }
    
    return base_template