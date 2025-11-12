#!/usr/bin/env python3
"""
Automated Rebranding Script for Skill Seekers Fork
Rebrand from Yusuf Karaaslan to Oluwafemi Idiakhoa

Usage:
    python rebrand.py --github-username OluwafemiIdiakhoa --email your@email.com
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple


class Rebrander:
    """Rebrand the project automatically."""

    def __init__(
        self,
        github_username: str,
        email: str,
        new_name: str = "Oluwafemi Idiakhoa",
        new_package: str = None
    ):
        self.old_author = "Yusuf Karaaslan"
        self.old_github = "yusufkaraaslan"
        self.old_package = "skill-seekers"

        self.new_author = new_name
        self.new_github = github_username
        self.new_email = email
        self.new_package = new_package or f"{self.old_package}-{github_username.lower()}"

        self.root_dir = Path(__file__).parent
        self.changes_made = []

    def run(self):
        """Execute the rebranding process."""
        print("=== Starting Rebranding Process ===")
        print(f"   From: {self.old_author} (@{self.old_github})")
        print(f"   To:   {self.new_author} (@{self.new_github})")
        print()

        # Ask for confirmation
        response = input("Continue with rebranding? (y/n): ")
        if response.lower() != 'y':
            print("X Rebranding cancelled.")
            return

        print()
        self.update_pyproject_toml()
        self.update_license()
        self.update_readme()
        self.update_markdown_files()
        self.create_attribution()
        self.update_changelog()
        self.show_summary()

    def update_pyproject_toml(self):
        """Update pyproject.toml with new author and package info."""
        print("[*] Updating pyproject.toml...")

        file_path = self.root_dir / "pyproject.toml"
        content = file_path.read_text(encoding='utf-8')

        # Update package name
        content = re.sub(
            r'name = "skill-seekers"',
            f'name = "{self.new_package}"',
            content
        )

        # Update version to 1.0.0 (fork start)
        content = re.sub(
            r'version = "[^"]+"',
            'version = "1.0.0"',
            content,
            count=1  # Only first occurrence
        )

        # Update description
        content = re.sub(
            r'description = "([^"]+)"',
            rf'description = "\1 (Fork by {self.new_author})"',
            content
        )

        # Update author
        content = re.sub(
            r'authors = \[\s*\{name = "[^"]+"\}',
            f'authors = [\n    {{name = "{self.new_author}", email = "{self.new_email}"}}',
            content
        )

        # Add maintainer
        if "maintainers" not in content:
            content = re.sub(
                r'(authors = \[[^\]]+\])',
                rf'\1\nmaintainers = [\n    {{name = "{self.new_author}", email = "{self.new_email}"}}\n]',
                content
            )

        # Update URLs
        content = content.replace(
            f"https://github.com/{self.old_github}/",
            f"https://github.com/{self.new_github}/"
        )

        # Add original project URL
        if "Original Project" not in content:
            content = re.sub(
                r'(\[project\.urls\][^\[]+)',
                rf'\1"Original Project" = "https://github.com/{self.old_github}/Skill_Seekers"\n',
                content
            )

        file_path.write_text(content, encoding='utf-8')
        self.changes_made.append(("pyproject.toml", "Updated author, version, URLs"))
        print("   [OK] pyproject.toml updated")

    def update_license(self):
        """Update LICENSE with proper attribution."""
        print("[*] Updating LICENSE...")

        file_path = self.root_dir / "LICENSE"

        new_license = f"""MIT License

Copyright (c) 2025 {self.new_author}
Original work Copyright (c) 2025 {self.old_author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

        file_path.write_text(new_license, encoding='utf-8')
        self.changes_made.append(("LICENSE", "Added dual copyright attribution"))
        print("   [OK] LICENSE updated with proper attribution")

    def update_readme(self):
        """Update README.md header."""
        print("[*] Updating README.md...")

        file_path = self.root_dir / "README.md"
        content = file_path.read_text(encoding='utf-8')

        # Remove original security badge (first line)
        lines = content.split('\n')
        if 'mseep.net' in lines[0]:
            lines = lines[2:]  # Remove badge and empty line

        # Update GitHub URLs
        content = '\n'.join(lines)
        content = content.replace(
            f"https://github.com/{self.old_github}/",
            f"https://github.com/{self.new_github}/"
        )
        content = content.replace(
            f"github.com/users/{self.old_github}/projects/",
            f"github.com/{self.new_github}/Skill_Seekers#readme"
        )

        # Update header
        new_header = f"""# Skill Seeker (Idiakhoa Edition)

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/{self.new_github}/Skill_Seekers/releases/tag/v1.0.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Maintained by {self.new_author}**

> 🔱 **Fork Notice:** This is a fork of [Skill Seekers by {self.old_author}](https://github.com/{self.old_github}/Skill_Seekers) with enhancements and modifications.

"""

        # Replace header (lines 1-14 in original)
        content_lines = content.split('\n')
        content = new_header + '\n'.join(content_lines[14:])

        file_path.write_text(content, encoding='utf-8')
        self.changes_made.append(("README.md", "Updated header and URLs"))
        print("   [OK] README.md updated")

    def update_markdown_files(self):
        """Update all markdown files with new GitHub URLs."""
        print("[*] Updating markdown files...")

        md_files = [
            "CLAUDE.md",
            "INNOVATION_STRATEGY.md",
            "QUICK_WIN_IMPLEMENTATION.md",
            "HOW_TO_WOW.md",
            "FLEXIBLE_ROADMAP.md",
            "FUTURE_RELEASES.md"
        ]

        count = 0
        for filename in md_files:
            file_path = self.root_dir / filename
            if file_path.exists():
                content = file_path.read_text(encoding='utf-8')
                updated = content.replace(
                    f"github.com/{self.old_github}/",
                    f"github.com/{self.new_github}/"
                )
                file_path.write_text(updated, encoding='utf-8')
                count += 1

        self.changes_made.append((f"{count} markdown files", "Updated GitHub URLs"))
        print(f"   [OK] {count} markdown files updated")

    def create_attribution(self):
        """Create ATTRIBUTION.md file."""
        print("[*] Creating ATTRIBUTION.md...")

        file_path = self.root_dir / "ATTRIBUTION.md"

        attribution = f"""# Attribution & Credits

This project is a fork of **Skill Seekers** created by **{self.old_author}**.

## Original Project
- **Author:** {self.old_author}
- **Repository:** https://github.com/{self.old_github}/Skill_Seekers
- **License:** MIT
- **Original Version:** v2.0.0

## This Fork
- **Maintainer:** {self.new_author}
- **Email:** {self.new_email}
- **Repository:** https://github.com/{self.new_github}/Skill_Seekers
- **Fork Version:** v1.0.0
- **Fork Date:** January 2025

## Key Differences from Original
- Added Quality Scoring System
- Enhanced documentation with innovation guides
- Added INNOVATION_STRATEGY.md with 15+ feature ideas
- Added QUICK_WIN_IMPLEMENTATION.md with step-by-step guides
- Added HOW_TO_WOW.md with strategic roadmap
- Enhanced CLAUDE.md with development commands

## License
Both the original and this fork are licensed under the MIT License.
See [LICENSE](LICENSE) for details.

## Contributing
Contributions to this fork are welcome! Please open issues or pull requests
on this fork's repository.

## Acknowledgments
Special thanks to {self.old_author} for creating the original Skill Seekers
project and releasing it under the MIT license, making this fork possible.

All original features and functionality are preserved and credited to the
original author. This fork builds upon that foundation with additional
enhancements and improvements.
"""

        file_path.write_text(attribution, encoding='utf-8')
        self.changes_made.append(("ATTRIBUTION.md", "Created attribution file"))
        print("   [OK] ATTRIBUTION.md created")

    def update_changelog(self):
        """Create fork-specific CHANGELOG."""
        print("[*] Updating CHANGELOG.md...")

        file_path = self.root_dir / "CHANGELOG.md"
        original_changelog = file_path.read_text(encoding='utf-8') if file_path.exists() else ""

        fork_changelog = f"""# Changelog ({self.new_author} Fork)

All notable changes to this fork will be documented in this file.

## [1.0.0] - 2025-01-XX (Fork Release)

### 🎉 Fork Announcement
This is the first release of the {self.new_author} fork of Skill Seekers.

### Added
- **Quality Scoring System** - Automatic skill quality analysis (0-100 score)
- **INNOVATION_STRATEGY.md** - Complete roadmap with 15+ feature ideas
- **QUICK_WIN_IMPLEMENTATION.md** - Step-by-step implementation guides
- **HOW_TO_WOW.md** - Strategic roadmap and action plan
- **Enhanced CLAUDE.md** - Added development commands and workflow
- **ATTRIBUTION.md** - Proper attribution to original author
- **REBRAND_GUIDE.md** - Guide for forking and rebranding

### Changed
- Rebranded to {self.new_author} edition
- Updated all GitHub URLs to new repository
- Updated author information throughout project
- Started fresh version numbering (1.0.0)
- Package renamed to `{self.new_package}`

### Original Project Credit
Based on Skill Seekers v2.0.0 by {self.old_author}:
- Original repository: https://github.com/{self.old_github}/Skill_Seekers
- All original features preserved and fully functional
- Full compatibility maintained with original configs
- MIT License allows forking and modification

---

# Original Changelog (From Upstream)

{original_changelog}
"""

        file_path.write_text(fork_changelog, encoding='utf-8')
        self.changes_made.append(("CHANGELOG.md", "Created fork changelog"))
        print("   [OK] CHANGELOG.md updated")

    def show_summary(self):
        """Show summary of changes made."""
        print()
        print("=" * 60)
        print("SUCCESS! REBRANDING COMPLETE!")
        print("=" * 60)
        print()
        print("Changes Made:")
        for filename, change in self.changes_made:
            print(f"   * {filename}: {change}")
        print()
        print("Next Steps:")
        print("   1. Review changes: git status")
        print("   2. Test package: pip install -e .")
        print("   3. Run tests: pytest tests/")
        print("   4. Commit changes:")
        print("      git add .")
        print(f"      git commit -m 'Rebrand to {self.new_author} edition'")
        print()
        print("   5. Create your GitHub repo:")
        print(f"      https://github.com/new")
        print()
        print("   6. Update remote and push:")
        print("      git remote remove origin")
        print(f"      git remote add origin https://github.com/{self.new_github}/Skill_Seekers.git")
        print("      git push -u origin main")
        print()
        print("   7. Publish to PyPI:")
        print("      uv build")
        print("      uv publish")
        print()
        print("Read REBRAND_GUIDE.md for detailed instructions")
        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Rebrand Skill Seekers fork to your name",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python rebrand.py --github-username OluwafemiIdiakhoa --email oluwafemi@example.com
  python rebrand.py --github-username OluwafemiIdiakhoa --email oluwafemi@example.com --name "Oluwafemi Idiakhoa"
        """
    )

    parser.add_argument(
        "--github-username",
        required=True,
        help="Your GitHub username"
    )
    parser.add_argument(
        "--email",
        required=True,
        help="Your email address"
    )
    parser.add_argument(
        "--name",
        default="Oluwafemi Idiakhoa",
        help="Your full name (default: Oluwafemi Idiakhoa)"
    )
    parser.add_argument(
        "--package-name",
        help="New package name (default: skill-seekers-USERNAME)"
    )

    args = parser.parse_args()

    rebrander = Rebrander(
        github_username=args.github_username,
        email=args.email,
        new_name=args.name,
        new_package=args.package_name
    )

    rebrander.run()

    return 0


if __name__ == "__main__":
    sys.exit(main())
