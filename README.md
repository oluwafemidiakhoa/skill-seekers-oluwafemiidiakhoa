# 🚀 Skill Seekers (Idiakhoa Edition)

<div align="center">

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/oluwafemidiakhoa/Skill_Seekers/releases/tag/v1.0.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Integration](https://img.shields.io/badge/MCP-Integrated-blue.svg)](https://modelcontextprotocol.io)
[![Tests](https://img.shields.io/badge/Tests-379%20Passing-brightgreen.svg)](tests/)

**Maintained by [Oluwafemi Idiakhoa](https://github.com/oluwafemidiakhoa)**

> 🔱 **Fork Notice:** Enhanced fork of [Skill Seekers by Yusuf Karaaslan](https://github.com/yusufkaraaslan/Skill_Seekers) with advanced features, quality scoring, and comprehensive innovation roadmap.

</div>

---

## 🎯 What is Skill Seekers?

**Skill Seekers** is an enterprise-grade automation tool that transforms documentation websites, GitHub repositories, and PDF files into production-ready [Claude AI skills](https://www.anthropic.com/news/skills). No more manual documentation reading—let AI do the heavy lifting.

### ⚡ The Problem We Solve

- **Manual skill creation takes hours** → We do it in 20-40 minutes
- **Documentation goes stale** → We detect conflicts between docs and code
- **Quality is uncertain** → We score skills 0-100 with actionable feedback
- **Large docs are overwhelming** → We handle 10K-40K+ pages intelligently

### 🎨 What Makes This Fork Unique?

This **Idiakhoa Edition** adds cutting-edge features not found in the original:

| Feature | Original | Idiakhoa Edition |
|---------|----------|------------------|
| **Quality Scoring System** | ❌ | ✅ 0-100 score with AI feedback |
| **Innovation Roadmap** | ❌ | ✅ 15+ planned features |
| **Quick Win Guides** | ❌ | ✅ Ship features in days |
| **Advanced Documentation** | ❌ | ✅ Developer guides & strategies |
| **Rebranding Tools** | ❌ | ✅ Fork & customize easily |

---

## 🌟 Key Features

### 🔥 New in Idiakhoa Edition (v1.0.0)

#### 🎯 **Quality Scoring System**
Get instant AI-powered feedback on skill quality before uploading to Claude.

```bash
skill-seekers score output/react/

# Output:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SKILL QUALITY REPORT: React
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Score: 87/100 (EXCELLENT ⭐⭐⭐⭐⭐)

✅ Strengths:
  • 45 real code examples with syntax highlighting
  • Well-organized into 8 categories
  • Enhanced with AI (comprehensive SKILL.md)

⚠️  Improvements:
  • 3 broken links detected → Auto-fix available
  • Consider adding more API reference content

🎯 Suggestions:
  • Run: skill-seekers enhance output/react/
  • Add: Hook examples (currently missing)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 🗺️ **Innovation Roadmap**
15+ planned features including marketplace, collaboration, self-improving skills, and more. See [INNOVATION_STRATEGY.md](INNOVATION_STRATEGY.md).

#### ⚡ **Quick Win Implementation Guides**
Step-by-step guides to ship major features in 1-2 weeks. See [QUICK_WIN_IMPLEMENTATION.md](QUICK_WIN_IMPLEMENTATION.md).

### 🌐 **Documentation Scraping** (from original)

- ✅ **llms.txt Support** - 10x faster with LLM-ready docs
- ✅ **Universal Scraper** - Works with ANY documentation website
- ✅ **Smart Categorization** - AI-powered content organization
- ✅ **Code Language Detection** - Python, JavaScript, TypeScript, C++, Go, Rust, and more
- ✅ **24 Ready-to-Use Configs** - Godot, React, Vue, Django, FastAPI, Laravel, and more

### 📄 **PDF Support** (v1.2.0)

- ✅ **Text Extraction** - Extract from any PDF
- ✅ **OCR for Scanned PDFs** - Handle scanned documents
- ✅ **Password-Protected PDFs** - Decrypt and extract
- ✅ **Table Extraction** - Complex table parsing
- ✅ **Parallel Processing** - 3x faster with multi-core
- ✅ **Intelligent Caching** - 50% faster on re-runs

### 🐙 **GitHub Repository Scraping** (v2.0.0)

- ✅ **Deep Code Analysis** - AST parsing for 6+ languages
- ✅ **API Extraction** - Functions, classes, methods with types
- ✅ **Repository Metadata** - README, file tree, language stats
- ✅ **Issues & PRs** - Extract with labels and milestones
- ✅ **CHANGELOG & Releases** - Version history extraction
- ✅ **Conflict Detection** - Compare docs vs actual code

### 🔄 **Unified Multi-Source Scraping** (v2.0.0)

**The killer feature:** Combine documentation + GitHub + PDF into ONE skill with automatic conflict detection.

```bash
skill-seekers unified --config configs/react_unified.json
```

**What it does:**
- ✅ **Finds discrepancies** between documentation and actual code
- ✅ **Shows both versions** side-by-side with ⚠️ warnings
- ✅ **Identifies outdated docs** and undocumented features
- ✅ **Creates single source of truth** showing intent (docs) AND reality (code)

**Example conflict report:**
```markdown
#### `useState(initialState)`

⚠️ **Conflict**: Documentation signature differs from implementation

**Documentation says:**
```python
def useState(initialState): [state, setState]
```

**Code implementation:**
```python
def useState(initialState, debugName?: string): [state, setState]
```

💡 **Suggestion**: Update documentation to include optional debugName parameter
```

### 🤖 **AI Enhancement** (FREE)

- ✅ **AI-Powered Enhancement** - Transforms basic templates into comprehensive guides
- ✅ **No API Costs** - FREE local enhancement using Claude Code Max
- ✅ **Quality Boost** - 75-line templates → 500+ line professional guides

### ⚡ **Performance & Scale**

- ✅ **Async Mode** - 2-3x faster scraping (55 pages/sec vs 18)
- ✅ **Large Documentation** - Handle 10K-40K+ pages intelligently
- ✅ **Router/Hub Skills** - Automatic routing to specialized sub-skills
- ✅ **Checkpoint/Resume** - Never lose progress on long scrapes
- ✅ **Intelligent Caching** - Scrape once, rebuild instantly

### ✅ **Quality Assurance**

- ✅ **379 Tests Passing** - Comprehensive test coverage
- ✅ **CI/CD Pipeline** - Automated testing on Ubuntu + macOS
- ✅ **Type Safety** - Full type hints throughout
- ✅ **Production Ready** - Battle-tested in real projects

---

## 📦 Installation

### Option 1: From PyPI (Easiest)

```bash
pip install skill-seekers-oluwafemidiakhoa
```

### Option 2: From Source (Latest)

```bash
git clone https://github.com/oluwafemidiakhoa/Skill_Seekers.git
cd Skill_Seekers
pip install -e .
```

### Option 3: Using uv (Modern & Fast)

```bash
uv tool install skill-seekers-oluwafemidiakhoa
```

**Requirements:**
- Python 3.10 or higher
- pip or uv package manager
- Git (optional, for development)

---

## 🚀 Quick Start

### 1. Scrape Documentation (Fastest)

```bash
# Use a preset configuration
skill-seekers scrape --config configs/react.json

# Or create from scratch
skill-seekers scrape --name myproject --url https://docs.myproject.com/
```

### 2. Score Quality (NEW!)

```bash
# Check quality before upload
skill-seekers score output/react/
```

### 3. Enhance with AI (Recommended)

```bash
# FREE local enhancement (no API key needed)
skill-seekers enhance output/react/
```

### 4. Package & Upload

```bash
# Package into .zip
skill-seekers package output/react/

# Upload to Claude
# 1. Go to https://claude.ai/skills
# 2. Click "Upload Skill"
# 3. Select output/react.zip
# 4. Done! ✅
```

**Total time:** ~25 minutes | **Quality:** Production-ready | **Cost:** Free

---

## 💡 Advanced Usage

### Unified Multi-Source Scraping

Combine multiple sources with conflict detection:

```bash
# Create unified skill (docs + GitHub + code analysis)
skill-seekers unified --config configs/react_unified.json

# Result: One comprehensive skill showing:
# ✅ What's documented
# ✅ What actually exists in code
# ⚠️  Discrepancies between them
```

### Async Mode (3x Faster)

```bash
# Enable async scraping with 8 workers
skill-seekers scrape --config configs/react.json --async --workers 8

# Performance:
# • Sync: ~18 pages/sec
# • Async: ~55 pages/sec (3x faster!)
```

### GitHub Repository Scraping

```bash
# Scrape any GitHub repo
skill-seekers github --repo microsoft/TypeScript --name typescript

# With authentication (higher rate limits)
export GITHUB_TOKEN=ghp_your_token
skill-seekers github --repo django/django
```

### PDF Extraction

```bash
# Basic PDF extraction
skill-seekers pdf --pdf docs/manual.pdf --name myskill

# Advanced: OCR + Tables + Parallel
skill-seekers pdf --pdf docs/manual.pdf --name myskill \
    --ocr \
    --extract-tables \
    --parallel \
    --workers 8
```

### Quality Scoring with Auto-Fix

```bash
# Score and get actionable feedback
skill-seekers score output/react/ --json

# Integrate into CI/CD
if [ $(skill-seekers score output/react/ --json | jq '.score') -lt 80 ]; then
    echo "Quality too low, aborting"
    exit 1
fi
```

---

## 📊 Use Cases

### For Developers
```bash
# Create skill from docs + GitHub with conflict detection
skill-seekers unified --config configs/react_unified.json

# See what's documented vs what's actually in code
# Perfect for finding documentation gaps!
```

### For Teams
```bash
# Combine internal docs + private repo
skill-seekers unified --config configs/internal_api_unified.json

# Result: Single source of truth for your team
```

### For Game Developers
```bash
# Godot Engine skill (docs + examples)
skill-seekers scrape --config configs/godot.json --enhance-local

# Unity with GitHub examples
skill-seekers unified --config configs/unity_unified.json
```

### For Open Source Maintainers
```bash
# Find documentation gaps automatically
skill-seekers unified --config configs/myproject_unified.json

# Output shows:
# • Undocumented features
# • Outdated documentation
# • API mismatches
```

---

## 🎯 Available Configurations

### Single-Source (14 configs)

**Web Frameworks:**
- `react.json` - React (7,102 chars)
- `vue.json` - Vue.js (1,029 chars)
- `django.json` - Django (6,468 chars)
- `fastapi.json` - FastAPI (11,906 chars)
- `laravel.json` - Laravel 9.x (16,131 chars)
- `astro.json` - Astro (145 chars)
- `hono.json` - Hono web framework

**DevOps:**
- `ansible-core.json` - Ansible Core 2.19 (~32K chars)
- `kubernetes.json` - Kubernetes (2,100 chars)

**Game Engines:**
- `godot.json` - Godot Engine (1,688 chars)

**CSS & Tools:**
- `tailwind.json` - Tailwind CSS (195 chars)
- `claude-code.json` - Claude Code docs

**Gaming:**
- `steam-economy-complete.json` - Steam Economy (588 chars)

### Unified Multi-Source (5 configs)

- `react_unified.json` - React (docs + GitHub + analysis)
- `django_unified.json` - Django (docs + GitHub + analysis)
- `fastapi_unified.json` - FastAPI (docs + GitHub + analysis)
- `godot_unified.json` - Godot (docs + GitHub + analysis)
- `fastapi_unified_test.json` - FastAPI test config

---

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/oluwafemidiakhoa/Skill_Seekers.git
cd Skill_Seekers

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .

# Install dev dependencies
pip install -e ".[dev]"
```

### Run Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_scraper_features.py

# Run with coverage
pytest tests/ --cov=src/skill_seekers --cov-report=html

# Run only quality scoring tests
pytest tests/test_skill_scorer.py -v
```

### Build & Publish

```bash
# Build package
uv build  # or: python -m build

# Test locally
pip install dist/skill_seekers_oluwafemidiakhoa-1.0.0-py3-none-any.whl

# Publish to PyPI
uv publish  # or: python -m twine upload dist/*
```

---

## 📚 Documentation

### Getting Started
- **[REBRAND_QUICKSTART.md](REBRAND_QUICKSTART.md)** - Fork & rebrand guide
- **[HOW_TO_WOW.md](HOW_TO_WOW.md)** - Strategic roadmap

### Feature Guides
- **[INNOVATION_STRATEGY.md](INNOVATION_STRATEGY.md)** - 15+ planned features
- **[QUICK_WIN_IMPLEMENTATION.md](QUICK_WIN_IMPLEMENTATION.md)** - Implementation guides
- **[CLAUDE.md](CLAUDE.md)** - Technical architecture
- **[docs/UNIFIED_SCRAPING.md](docs/UNIFIED_SCRAPING.md)** - Multi-source scraping

### References
- **[CHANGELOG.md](CHANGELOG.md)** - Release history
- **[FUTURE_RELEASES.md](FUTURE_RELEASES.md)** - Roadmap
- **[ATTRIBUTION.md](ATTRIBUTION.md)** - Credits & attribution

---

## 🎨 Roadmap (Idiakhoa Edition)

### ✅ Completed (v1.0.0)
- Quality Scoring System
- Enhanced documentation
- Innovation strategy
- Rebranding tools

### 🚧 In Progress (v1.1.0)
- Visual diff viewer for conflicts
- Smart config templates (AI-powered)
- One-click skill updates

### 🔮 Planned (v1.2.0+)
- Skill marketplace
- Live collaboration mode
- Self-improving skills
- Multi-modal skills (voice, video, interactive)

See [INNOVATION_STRATEGY.md](INNOVATION_STRATEGY.md) for complete roadmap.

---

## 🤝 Contributing

Contributions are welcome! This fork focuses on:

1. **Quality & Developer Experience** - Better tools for developers
2. **Innovation** - Features that don't exist elsewhere
3. **Enterprise Features** - Scale, collaboration, analytics

**How to contribute:**

```bash
# 1. Fork the repository
# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Make changes and test
pytest tests/

# 4. Commit with clear message
git commit -m "Add amazing feature"

# 5. Push and create PR
git push origin feature/amazing-feature
```

**Contribution ideas:**
- Implement features from [INNOVATION_STRATEGY.md](INNOVATION_STRATEGY.md)
- Add new documentation configs
- Improve test coverage
- Write tutorials and guides

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

**Copyright (c) 2025 Oluwafemi Idiakhoa**
**Original work Copyright (c) 2025 Yusuf Karaaslan**

This is a fork of [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) with additional features and enhancements.

---

## 🙏 Acknowledgments

- **Yusuf Karaaslan** - Creator of the original Skill Seekers project
- **Anthropic** - Claude AI and skills system
- **Open Source Community** - For amazing tools and libraries

---

## 📧 Contact & Support

- **Maintainer:** Oluwafemi Idiakhoa
- **Email:** oluwafemidiakhoa@gmail.com
- **GitHub:** [@oluwafemidiakhoa](https://github.com/oluwafemidiakhoa)
- **Issues:** [GitHub Issues](https://github.com/oluwafemidiakhoa/Skill_Seekers/issues)

**Original Project:** [yusufkaraaslan/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers)

---

## ⭐ Star This Repo!

If you find this fork useful, please star it on GitHub! It helps others discover the project.

[![GitHub stars](https://img.shields.io/github/stars/oluwafemidiakhoa/Skill_Seekers?style=social)](https://github.com/oluwafemidiakhoa/Skill_Seekers)

---

<div align="center">

**Built with ❤️ by [Oluwafemi Idiakhoa](https://github.com/oluwafemidiakhoa)**

Based on [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) by [Yusuf Karaaslan](https://github.com/yusufkaraaslan)

</div>
