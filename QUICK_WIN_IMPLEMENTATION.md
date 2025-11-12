# 🎯 Quick Win Implementation Guide

**Goal:** Ship your first "wow" feature in 1 week

This guide provides step-by-step instructions to implement **QW2: Skill Quality Scoring System** - the easiest high-impact feature.

---

## Why Start With Quality Scoring?

✅ **Easy to implement** - Mostly Python, no UI needed
✅ **Immediate value** - Users see benefit instantly
✅ **No dependencies** - Works standalone
✅ **Foundation for later** - Enables marketplace ratings
✅ **Wow factor** - Professional output impresses users

**Time estimate:** 4-6 hours of focused work

---

## Implementation Steps

### Step 1: Create the Scorer Module (1 hour)

Create `src/skill_seekers/cli/skill_scorer.py`:

```python
#!/usr/bin/env python3
"""
Skill Quality Scoring System

Analyzes a generated skill and provides a quality score (0-100)
with detailed feedback and actionable recommendations.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
import re


class SkillScorer:
    """Analyzes skill quality and provides scoring."""

    def __init__(self, skill_directory: str):
        self.skill_dir = Path(skill_directory)
        self.skill_md = self.skill_dir / "SKILL.md"
        self.references_dir = self.skill_dir / "references"

        # Scoring components
        self.completeness_score = 0
        self.code_quality_score = 0
        self.organization_score = 0
        self.enhancement_score = 0

        # Details for report
        self.strengths = []
        self.improvements = []
        self.suggestions = []

    def score(self) -> Tuple[int, Dict]:
        """Calculate overall quality score and generate report."""
        if not self.skill_md.exists():
            return 0, {"error": "SKILL.md not found"}

        # Run scoring components
        self._score_completeness()
        self._score_code_quality()
        self._score_organization()
        self._score_enhancement()

        # Calculate total
        total_score = (
            self.completeness_score +
            self.code_quality_score +
            self.organization_score +
            self.enhancement_score
        )

        # Generate report
        report = self._generate_report(total_score)

        return total_score, report

    def _score_completeness(self):
        """Score: 0-30 points for completeness."""
        score = 0

        # Has code examples (10 points)
        skill_content = self.skill_md.read_text(encoding='utf-8')
        code_blocks = skill_content.count('```')
        if code_blocks >= 10:
            score += 10
            self.strengths.append(f"{code_blocks // 2} code examples found")
        elif code_blocks >= 4:
            score += 5
            self.improvements.append("Add more code examples (currently only {})".format(code_blocks // 2))
        else:
            self.improvements.append("Missing code examples - add at least 5")

        # Has API reference (10 points)
        if self.references_dir.exists():
            ref_files = list(self.references_dir.glob("*.md"))
            if len(ref_files) >= 5:
                score += 10
                self.strengths.append(f"Well-organized into {len(ref_files)} categories")
            elif len(ref_files) >= 2:
                score += 5
            else:
                self.improvements.append("Add more reference categories")

        # Has proper structure (10 points)
        required_sections = ["Quick Reference", "Key Concepts", "Common Patterns"]
        found_sections = sum(1 for section in required_sections if section in skill_content)
        score += found_sections * 3  # 3 points per section

        if found_sections == 3:
            self.strengths.append("All required sections present")
        else:
            missing = [s for s in required_sections if s not in skill_content]
            self.improvements.append(f"Missing sections: {', '.join(missing)}")

        self.completeness_score = min(score, 30)

    def _score_code_quality(self):
        """Score: 0-30 points for code quality."""
        score = 0

        skill_content = self.skill_md.read_text(encoding='utf-8')

        # Language detection (10 points)
        code_blocks = re.findall(r'```(\w+)', skill_content)
        if code_blocks:
            languages = set(code_blocks)
            if len(languages) >= 1:
                score += 10
                self.strengths.append(f"Code blocks with syntax highlighting ({', '.join(languages)})")
        else:
            self.improvements.append("Add language tags to code blocks (```python, ```javascript, etc.)")

        # Real code (not placeholders) (10 points)
        placeholder_patterns = ['...', 'TODO', 'FIXME', 'placeholder', 'Lorem ipsum']
        has_placeholders = any(pattern in skill_content for pattern in placeholder_patterns)

        if not has_placeholders and code_blocks:
            score += 10
            self.strengths.append("Real, production-ready code examples")
        else:
            self.improvements.append("Replace placeholder code with real examples")

        # Valid syntax (10 points) - basic check
        # For now, just check if code blocks are not empty
        empty_blocks = skill_content.count('```\n```')
        if empty_blocks == 0 and code_blocks:
            score += 10
        else:
            self.improvements.append(f"Found {empty_blocks} empty code blocks")

        self.code_quality_score = min(score, 30)

    def _score_organization(self):
        """Score: 0-20 points for organization."""
        score = 0

        # Logical categories (10 points)
        if self.references_dir.exists():
            ref_files = list(self.references_dir.glob("*.md"))
            if len(ref_files) >= 3:
                score += 10
                self.strengths.append("Good category organization")
            elif len(ref_files) >= 1:
                score += 5

        # Working links (10 points) - basic check
        skill_content = self.skill_md.read_text(encoding='utf-8')
        internal_links = re.findall(r'\[.*?\]\((references/.*?\.md)\)', skill_content)

        if internal_links:
            broken_links = []
            for link in internal_links:
                link_path = self.skill_dir / link
                if not link_path.exists():
                    broken_links.append(link)

            if not broken_links:
                score += 10
                self.strengths.append("All internal links working")
            else:
                score += 5
                self.improvements.append(f"{len(broken_links)} broken links detected")
                self.suggestions.append("Run link checker to fix broken references")

        self.organization_score = min(score, 20)

    def _score_enhancement(self):
        """Score: 0-20 points for AI enhancement."""
        score = 0

        skill_content = self.skill_md.read_text(encoding='utf-8')

        # Check if enhanced (backup file exists)
        backup_file = self.skill_dir / "SKILL.md.backup"
        if backup_file.exists():
            score += 20
            self.strengths.append("Enhanced with AI (comprehensive SKILL.md)")
        else:
            # Check content length as proxy
            if len(skill_content) > 3000:  # ~500+ lines
                score += 10
                self.strengths.append("Comprehensive SKILL.md content")
            else:
                score += 5
                self.suggestions.append("Run: skill-seekers enhance {}".format(self.skill_dir))
                self.improvements.append("Consider AI enhancement for better quality")

        self.enhancement_score = min(score, 20)

    def _generate_report(self, total_score: int) -> Dict:
        """Generate detailed scoring report."""

        # Rating
        if total_score >= 90:
            rating = "EXCELLENT ⭐⭐⭐⭐⭐"
        elif total_score >= 75:
            rating = "VERY GOOD ⭐⭐⭐⭐"
        elif total_score >= 60:
            rating = "GOOD ⭐⭐⭐"
        elif total_score >= 40:
            rating = "FAIR ⭐⭐"
        else:
            rating = "NEEDS IMPROVEMENT ⭐"

        return {
            "total_score": total_score,
            "rating": rating,
            "breakdown": {
                "completeness": self.completeness_score,
                "code_quality": self.code_quality_score,
                "organization": self.organization_score,
                "enhancement": self.enhancement_score
            },
            "strengths": self.strengths,
            "improvements": self.improvements,
            "suggestions": self.suggestions
        }


def print_report(score: int, report: Dict):
    """Print beautiful console report."""

    print("\n" + "━" * 60)
    print("SKILL QUALITY REPORT")
    print("━" * 60)
    print(f"\nOverall Score: {score}/100 ({report['rating']})")

    # Breakdown
    print("\n📊 Breakdown:")
    breakdown = report['breakdown']
    print(f"  • Completeness:   {breakdown['completeness']}/30")
    print(f"  • Code Quality:   {breakdown['code_quality']}/30")
    print(f"  • Organization:   {breakdown['organization']}/20")
    print(f"  • Enhancement:    {breakdown['enhancement']}/20")

    # Strengths
    if report['strengths']:
        print("\n✅ Strengths:")
        for strength in report['strengths']:
            print(f"  • {strength}")

    # Improvements
    if report['improvements']:
        print("\n⚠️  Improvements:")
        for improvement in report['improvements']:
            print(f"  • {improvement}")

    # Suggestions
    if report['suggestions']:
        print("\n🎯 Suggestions:")
        for suggestion in report['suggestions']:
            print(f"  • {suggestion}")

    print("\n" + "━" * 60 + "\n")


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Score skill quality (0-100) with detailed feedback"
    )
    parser.add_argument(
        "skill_directory",
        help="Path to skill directory (e.g., output/react/)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of pretty print"
    )

    args = parser.parse_args()

    # Check directory exists
    if not os.path.isdir(args.skill_directory):
        print(f"Error: Directory not found: {args.skill_directory}")
        return 1

    # Score skill
    scorer = SkillScorer(args.skill_directory)
    score, report = scorer.score()

    # Output
    if args.json:
        print(json.dumps({"score": score, "report": report}, indent=2))
    else:
        print_report(score, report)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
```

---

### Step 2: Add CLI Entry Point (10 minutes)

Edit `pyproject.toml` and add the new command:

```toml
[project.scripts]
# ... existing commands ...
skill-seekers-score = "skill_seekers.cli.skill_scorer:main"
```

---

### Step 3: Update Main CLI (10 minutes)

Edit `src/skill_seekers/cli/main.py` and add the score subcommand:

```python
# In create_parser() function, add:

# === score subcommand ===
score_parser = subparsers.add_parser(
    "score",
    help="Analyze skill quality and get score (0-100)",
    description="Score skill quality with detailed feedback"
)
score_parser.add_argument("skill_directory", help="Skill directory path")
score_parser.add_argument("--json", action="store_true", help="Output JSON")

# In main() function, add:

elif args.command == "score":
    from skill_seekers.cli.skill_scorer import main as score_main
    sys.argv = ["skill_scorer.py", args.skill_directory]
    if args.json:
        sys.argv.append("--json")
    return score_main() or 0
```

---

### Step 4: Integrate with Scraper (15 minutes)

Edit `src/skill_seekers/cli/doc_scraper.py` and add auto-scoring after build:

```python
# At the end of main() function, after build_skill():

# Auto-score if requested
if args.score:
    print("\n" + "="*70)
    print("Running quality scoring...")
    print("="*70)

    from skill_seekers.cli.skill_scorer import SkillScorer, print_report

    scorer = SkillScorer(skill_dir)
    score, report = scorer.score()
    print_report(score, report)

# And in the argument parser:
parser.add_argument(
    "--score",
    action="store_true",
    help="Score skill quality after building"
)
```

---

### Step 5: Write Tests (1 hour)

Create `tests/test_skill_scorer.py`:

```python
"""Tests for skill quality scoring."""

import pytest
from pathlib import Path
from skill_seekers.cli.skill_scorer import SkillScorer


def test_scorer_basic(tmp_path):
    """Test basic scorer functionality."""
    # Create minimal skill structure
    skill_dir = tmp_path / "test_skill"
    skill_dir.mkdir()

    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text("""
# Test Skill

## Quick Reference
Some content

## Key Concepts
Some concepts

```python
def hello():
    return "world"
```
""")

    # Create references
    refs_dir = skill_dir / "references"
    refs_dir.mkdir()
    (refs_dir / "api.md").write_text("# API")
    (refs_dir / "guide.md").write_text("# Guide")

    # Score
    scorer = SkillScorer(str(skill_dir))
    score, report = scorer.score()

    # Assertions
    assert score > 0
    assert score <= 100
    assert "total_score" in report
    assert "rating" in report
    assert "breakdown" in report


def test_scorer_completeness():
    """Test completeness scoring."""
    # Test with real skill directory if exists
    skill_dir = Path("output/react")
    if not skill_dir.exists():
        pytest.skip("No test skill available")

    scorer = SkillScorer(str(skill_dir))
    score, report = scorer.score()

    # Should have decent score
    assert score >= 40  # At least fair
    assert report['breakdown']['completeness'] > 0


def test_scorer_json_output(tmp_path, capsys):
    """Test JSON output mode."""
    from skill_seekers.cli.skill_scorer import main
    import sys

    # Create minimal skill
    skill_dir = tmp_path / "test_skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("# Test")

    # Run with JSON flag
    sys.argv = ["skill_scorer.py", str(skill_dir), "--json"]
    main()

    captured = capsys.readouterr()
    import json
    data = json.loads(captured.out)

    assert "score" in data
    assert "report" in data
```

Run tests:
```bash
pytest tests/test_skill_scorer.py -v
```

---

### Step 6: Update Documentation (30 minutes)

Edit `CLAUDE.md` and add the new command:

```markdown
### Skill Quality Scoring

```bash
# Score a skill
skill-seekers score output/react/

# Output JSON for automation
skill-seekers score output/react/ --json

# Auto-score after scraping
skill-seekers scrape --config configs/react.json --score
```
```

Edit `README.md` and add a features section:

```markdown
### ⭐ Skill Quality Scoring (**NEW!**)
Get instant feedback on your skill quality with actionable recommendations.

```bash
skill-seekers score output/react/

# Output:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SKILL QUALITY REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Score: 87/100 (EXCELLENT ⭐⭐⭐⭐⭐)

✅ Strengths:
  • 45 real code examples found
  • Well-organized into 8 categories
  • Enhanced with AI

⚠️  Improvements:
  • 3 broken links detected

🎯 Suggestions:
  • Consider adding Hook examples
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
```

---

### Step 7: Create Demo Video/GIF (30 minutes)

Use a screen recorder to capture:

1. Running `skill-seekers scrape --config configs/react.json --score`
2. Watching the scoring output
3. Following a suggestion (e.g., running enhance)
4. Re-scoring to show improvement

Save as `docs/assets/quality-scoring-demo.gif`

---

### Step 8: Announce & Share (15 minutes)

Create a GitHub Discussion post:

```markdown
# 🎉 New Feature: Skill Quality Scoring!

We just shipped a major quality-of-life improvement: automatic skill quality scoring!

## What is it?
Get instant feedback on your generated skills with a 0-100 score, detailed breakdown, and actionable recommendations.

## How to use
\`\`\`bash
# Score any skill
skill-seekers score output/react/

# Auto-score after scraping
skill-seekers scrape --config configs/react.json --score
\`\`\`

## Why you'll love it
✅ Know quality BEFORE uploading
✅ Actionable feedback, not just numbers
✅ Gamification (aim for 100/100!)
✅ Builds confidence

Try it out and let us know what you think! 🚀

[See demo GIF]
```

Share on:
- Twitter/X
- Reddit (r/Python, r/MachineLearning, r/ClaudeAI)
- Dev.to
- Hacker News (Show HN post)

---

## Testing Your Implementation

### Manual Testing Checklist

```bash
# 1. Test basic scoring
skill-seekers score output/react/
# Should show detailed report

# 2. Test JSON output
skill-seekers score output/react/ --json
# Should output valid JSON

# 3. Test auto-scoring
skill-seekers scrape --config configs/godot.json --score
# Should scrape then score automatically

# 4. Test with missing directory
skill-seekers score nonexistent/
# Should show error message

# 5. Test with minimal skill
mkdir -p /tmp/test_skill
echo "# Test" > /tmp/test_skill/SKILL.md
skill-seekers score /tmp/test_skill/
# Should give low score with suggestions
```

### Automated Testing

```bash
# Run scorer tests
pytest tests/test_skill_scorer.py -v

# Run full test suite
pytest tests/ -v

# Check code coverage
pytest tests/test_skill_scorer.py --cov=src/skill_seekers/cli/skill_scorer --cov-report=html
```

---

## Success Metrics

After shipping, track these metrics:

📊 **Usage Metrics**
- Number of `skill-seekers score` commands run
- Average score of generated skills
- Most common improvement suggestions

💬 **User Feedback**
- GitHub stars increase
- Twitter mentions
- Reddit upvotes
- User testimonials

📈 **Quality Improvement**
- Before/after scoring adoption
- Correlation between score and skill effectiveness
- Reduction in "bad skill" reports

---

## Next Steps

After successfully shipping QW2 (Quality Scoring), move to:

1. **QW5: Smart Config Templates** - Builds on scoring
2. **QW1: Interactive Config Generator** - Needs web UI
3. **QW3: One-Click Updates** - Needs caching system

---

## Troubleshooting

### Common Issues

**Issue:** "Module not found: skill_scorer"
```bash
# Solution: Reinstall in editable mode
pip install -e .
```

**Issue:** "Tests failing"
```bash
# Solution: Update test imports
# Make sure tests use: from skill_seekers.cli.skill_scorer import ...
```

**Issue:** "Entry point not working"
```bash
# Solution: Rebuild package
pip uninstall skill-seekers
pip install -e .
```

---

## Questions?

Open a GitHub issue or discussion. Happy to help! 🚀
