# Universal Skills - Create Skills from Any Content Source

**Skill Seekers Universal** extends the core documentation scraping functionality to support any type of content source, making it possible to create Claude AI skills from APIs, videos, forums, databases, and more.

## 🌟 What's New

### Universal Content Sources
- **API Documentation**: REST/GraphQL APIs → API reference skills
- **Video Content**: YouTube tutorials → learning path skills  
- **Community Forums**: Stack Overflow Q&A → troubleshooting skills
- **Books/eBooks**: Technical books → comprehensive guides
- **Database Schemas**: SQL/NoSQL → database reference skills

### Smart Templates
- **API Reference**: Function signatures, endpoints, examples
- **Tutorial Series**: Step-by-step learning progressions
- **Troubleshooting**: Problem-solution mappings
- **Best Practices**: Guidelines and patterns
- **Quick Reference**: Cheat sheets and lookup tables

### AI-Powered Enhancement
- **Auto-categorization**: Intelligently organizes any content type
- **Quality scoring**: Assesses content quality automatically
- **Gap detection**: Identifies missing topics
- **Content synthesis**: Merges overlapping information

## 🚀 Quick Start

### 1. Create Configuration Templates

```bash
# Create an API reference template
skill-seekers create-template api api_reference openai_api.json

# Create a video tutorial template  
skill-seekers create-template video tutorial_series python_tutorials.json

# Create a troubleshooting template
skill-seekers create-template forum troubleshooting stackoverflow_qa.json
```

### 2. Customize Configuration

Edit the generated template with your specific sources:

```json
{
  "name": "openai_api",
  "description": "Complete OpenAI API reference",
  "source_type": "api",
  "template": "api_reference",
  "source_config": {
    "base_url": "https://api.openai.com",
    "openapi_spec_url": "https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml"
  }
}
```

### 3. Generate Skills

```bash
# Create skill from any content source
skill-seekers universal --config openai_api.json

# With AI enhancement
skill-seekers universal --config openai_api.json --enhance

# Test with limited content
skill-seekers universal --config openai_api.json --max-items 50
```

## 📋 Content Source Types

### API Documentation

**Best for**: Creating API reference skills with endpoints, parameters, and examples.

```json
{
  "source_type": "api",
  "template": "api_reference",
  "source_config": {
    "base_url": "https://api.example.com",
    "openapi_spec_url": "https://api.example.com/openapi.json",
    "auth": {
      "type": "bearer",
      "token": "${API_TOKEN}"
    },
    "endpoints": [
      {
        "path": "/v1/users",
        "method": "get",
        "description": "Get list of users"
      }
    ]
  }
}
```

**Generated skill includes**:
- Complete endpoint reference
- Request/response examples
- Authentication details
- Error codes and handling

### Video Content

**Best for**: Creating tutorial series from YouTube playlists or educational videos.

```json
{
  "source_type": "video",
  "template": "tutorial_series",
  "source_config": {
    "video_urls": [
      "https://www.youtube.com/watch?v=VIDEO_ID",
      "https://www.youtube.com/playlist?list=PLAYLIST_ID"
    ],
    "extract_transcripts": true,
    "extract_chapters": true,
    "language": "en"
  }
}
```

**Generated skill includes**:
- Learning progression from beginner to advanced
- Code examples extracted from video content
- Chapter-based organization
- Practice exercises and next steps

### Forum Q&A

**Best for**: Creating troubleshooting guides from community knowledge.

```json
{
  "source_type": "forum",
  "template": "troubleshooting",
  "source_config": {
    "platform": "stackoverflow",
    "search_queries": [
      "python error",
      "pandas troubleshooting"
    ],
    "max_questions": 100,
    "min_score": 5
  }
}
```

**Generated skill includes**:
- Problem-solution mappings
- Community-verified solutions
- Code examples and fixes
- Common error patterns

## 🎨 Skill Templates

### API Reference Template

Optimized for API documentation with clear endpoint organization:

- **Overview Section**: API introduction and authentication
- **Endpoint Groups**: Organized by functionality/tags
- **Request/Response Details**: Parameters, status codes, examples
- **Code Examples**: Multi-language examples for each endpoint

### Tutorial Series Template

Perfect for learning content with progressive difficulty:

- **Learning Path**: Structured progression from basic to advanced
- **Modules**: Grouped by topics and complexity
- **Code Examples**: Prominently featured with syntax highlighting
- **Practice Exercises**: Suggested activities for hands-on learning

### Troubleshooting Template

Ideal for Q&A and problem-solving content:

- **Problem Categories**: Installation, errors, performance, etc.
- **Solution Format**: Clear problem statement + verified solution
- **Community Validation**: Includes scores and verification status
- **Quick Problem Locator**: Index for finding specific issues

## 🔧 Advanced Configuration

### Content Processing Options

```json
{
  "processing_options": {
    "max_content_items": 1000,
    "quality_threshold": 0.3,
    "enable_ai_enhancement": true,
    "auto_categorization": true,
    "extract_code_examples": true,
    "create_practice_exercises": true
  }
}
```

### Quality Filtering

```json
{
  "source_config": {
    "quality_filter": {
      "min_score": 5,
      "min_views": 1000,
      "has_accepted_answer": true
    }
  }
}
```

### Custom Categories

```json
{
  "source_config": {
    "content_categories": {
      "basics": ["introduction", "getting started"],
      "advanced": ["optimization", "performance"],
      "integration": ["api", "webhooks"]
    }
  }
}
```

## 📊 Examples

### Complete API Reference (OpenAI)

```bash
# 1. Create template
skill-seekers create-template api api_reference openai_api.json

# 2. Edit configuration (add API key, endpoints)
# 3. Generate skill
skill-seekers universal --config openai_api.json --enhance

# Result: Complete OpenAI API reference with examples
```

### Python Learning Path (YouTube)

```bash
# 1. Create template
skill-seekers create-template video tutorial_series python_tutorials.json

# 2. Add YouTube playlist URLs
# 3. Generate skill
skill-seekers universal --config python_tutorials.json --max-items 50

# Result: Structured Python learning path with code examples
```

### React Troubleshooting Guide (Stack Overflow)

```bash
# 1. Create template
skill-seekers create-template forum troubleshooting react_troubleshooting.json

# 2. Add React-specific search queries
# 3. Generate skill
skill-seekers universal --config react_troubleshooting.json

# Result: Comprehensive React troubleshooting guide
```

## 🤖 AI Enhancement

Universal skills support the same AI enhancement as traditional skills:

```bash
# During generation
skill-seekers universal --config config.json --enhance

# After generation
skill-seekers enhance output/skill_name/
```

**Enhancement benefits**:
- Improved organization and flow
- Additional context and explanations
- Better code examples
- Cross-references between sections

## 🎯 Use Cases

### For Developers
- **API Integration**: Create reference skills for APIs you work with
- **Learning New Technologies**: Convert video tutorials to structured skills
- **Debugging**: Build troubleshooting guides from community knowledge

### For Teams
- **Internal APIs**: Document internal services and endpoints
- **Onboarding**: Create learning paths for new team members
- **Knowledge Sharing**: Capture team knowledge in searchable skills

### For Educators
- **Course Materials**: Convert video lectures to interactive skills
- **Student Resources**: Create reference materials from multiple sources
- **Assessment**: Build practice problem collections

### For Technical Writers
- **Multi-Source Documentation**: Combine docs, videos, and community content
- **Quality Assurance**: Automatically assess documentation completeness
- **Maintenance**: Keep skills updated with latest information

## 🔮 Roadmap

### Coming Soon
- **Database Schema Support**: SQL/NoSQL → database reference skills
- **Knowledge Base Integration**: Notion, Confluence → organized guides
- **Multi-Modal Content**: Images, diagrams, interactive demos
- **Real-Time Updates**: Auto-refresh skills when source content changes

### Future Possibilities
- **Live Collaboration**: Teams creating skills together
- **Marketplace Integration**: Share and discover universal skill templates
- **AI-Generated Examples**: Automatically create code samples
- **Quality Scoring**: Automated assessment of skill completeness

## 📚 Additional Resources

- **Example Configurations**: See `configs/examples/` directory
- **Template Reference**: Complete list of available templates
- **Content Adapter API**: For creating custom content sources
- **Troubleshooting**: Common issues and solutions

---

**Ready to create universal skills?** Start with a simple template and expand from there. The system is designed to grow with your needs!